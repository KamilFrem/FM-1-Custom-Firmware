// SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';

const compiled = new WebAssembly.Module(readFileSync('build/preview/simulator.wasm'));
const baseline = new WebAssembly.Module(readFileSync('build/baseline/simulator.wasm'));
const PAGE = { home: 0, env: 3, lfo: 4, actions: 12, settings: 19 };
const BUTTON = { env: 4, home: 8, save: 9, seq: 11 };

function core(module = compiled) {
  const c = new WebAssembly.Instance(module, {}).exports;
  c._initialize(); c.sim_boot(1);
  assert.equal(c.sim_select(0, 0), 0);
  return c;
}
function tick(c, n = 16) { for (let i = 0; i < n; i++) c.sim_render(); }
function open(c, page) { assert.equal(c.sim_open(page), 0); tick(c); }
function tap(c, button) { c.sim_control(0, button, 1); c.sim_control(0, button, 0); tick(c); }
function knob(c, index, delta) { c.sim_control(2, index, delta); tick(c); }
function labels(c) {
  return Array.from({ length: 4 }, (_, i) => Array.from({ length: 2 }, (_, j) =>
    Buffer.from(c.memory.buffer, c.sim_knobs() + i * 32 + j * 16, 16)
      .toString('ascii').split('\0')[0]));
}
function bytes(c, address, size) { return Buffer.from(new Uint8Array(c.memory.buffer, address, size)); }
function project(c) { assert.equal(c.sim_export(), 0); return bytes(c, c.sim_file(), 4264); }
function timbre(c) { assert.equal(c.sim_timbre_export(), 0); return bytes(c, c.sim_file(), 223); }
function state(c) { return bytes(c, c.sim_state(), 225); }

test('unchanged upstream simulator produces finite, audible stereo samples', () => {
  const c = core(baseline);
  c.sim_control(1, 7, 1);
  let energy = 0;
  for (let i = 0; i < 100; i++) {
    const pointer = c.sim_render();
    const audio = new Float32Array(c.memory.buffer, pointer, c.sim_block_frames() * 2);
    for (const sample of audio) { assert.ok(Number.isFinite(sample)); energy += sample * sample; }
  }
  assert.ok(energy > 0.001, `No audible signal: ${energy}`);
  c.sim_release();
});

test('default simple envelope uses the stock parameter values', () => {
  const a = core(), b = core(baseline);
  open(a, PAGE.env); open(b, PAGE.env);
  assert.deepEqual(labels(a).map(x => x[0]), ['FADE IN', 'SETTLE', 'HOLD LVL', 'FADE OUT']);
  assert.deepEqual(labels(a).map(x => x[1]), labels(b).map(x => x[1]));
  assert.deepEqual(project(a), project(b));
});

test('the panel action menu opens settings and HOME exits', () => {
  const c = core();
  // SEQ + EDIT is the existing upstream menu gesture; no new shortcut is consumed.
  c.sim_control(0, BUTTON.seq, 1); c.sim_control(0, 6, 1); c.sim_release(); tick(c);
  assert.equal(state(c)[1], PAGE.actions);
  knob(c, 0, 20); tap(c, BUTTON.save);
  assert.equal(state(c)[1], PAGE.settings);
  assert.deepEqual(labels(c)[0], ['VIEW', 'SIMPLE']);
  tap(c, BUTTON.home);
  assert.equal(state(c)[1], PAGE.home);
});

test('view switching preserves edits, project contents, edit history and flash', () => {
  const c = core(); open(c, PAGE.env);
  // One exact detent through the same browser-to-panel handler.
  assert.equal(c.sim_lcd(c.sim_lcd_context(), 0, 0, 0, 7), 0); tick(c);
  assert.equal(labels(c)[0][1], '7%');
  const savedProject = project(c), savedTimbre = timbre(c);
  const revision = c.sim_edit_revision(), flash = c.sim_flash_revision();
  const dirty = c.sim_project_dirty();
  open(c, PAGE.settings);
  assert.equal(c.sim_lcd_mask(), 1);
  assert.equal(c.sim_lcd(c.sim_lcd_context(), 0, 0, 0, 1), 0); tick(c);
  assert.deepEqual(labels(c)[0], ['VIEW', 'ADVANCED']);
  open(c, PAGE.env);
  assert.deepEqual(labels(c)[0], ['ATTACK', '7%']);
  assert.deepEqual(project(c), savedProject); assert.deepEqual(timbre(c), savedTimbre);
  assert.equal(c.sim_edit_revision(), revision); assert.equal(c.sim_flash_revision(), flash);
  assert.equal(c.sim_project_dirty(), dirty);
  open(c, PAGE.settings); knob(c, 2, -1); open(c, PAGE.env);
  assert.deepEqual(labels(c)[0], ['FADE IN', '7%']);
  assert.deepEqual(project(c), savedProject);
});

test('edits made in either view survive panel save and simulated reboot', () => {
  const c = core(); open(c, PAGE.env);
  c.sim_lcd(c.sim_lcd_context(), 0, 0, 0, 9); tick(c);
  open(c, PAGE.settings); knob(c, 2, 1); open(c, PAGE.env);
  c.sim_lcd(c.sim_lcd_context(), 0, 1, 0, 13); tick(c);
  const saved = timbre(c);
  tap(c, BUTTON.save); tap(c, BUTTON.save); tick(c, 100);
  assert.equal(c.sim_project_dirty(), 0);
  c.sim_boot(0); tick(c); open(c, PAGE.env);
  assert.deepEqual(timbre(c), saved);
  assert.deepEqual(labels(c).slice(0, 2), [['FADE IN', '9%'], ['SETTLE', '13%']]);
});

test('simple LFO labels retain both pages and the exact FM patch', () => {
  const c = core(); open(c, PAGE.lfo);
  assert.deepEqual(labels(c).map(x => x[0]), ['SHAPE', 'SPEED', 'PITCH', 'VOLUME']);
  const original = timbre(c);
  knob(c, 0, 1);
  assert.deepEqual(labels(c).map(x => x[0]), ['DELAY', 'P SENS', 'LFO SYNC', 'OSC SYNC']);
  open(c, PAGE.settings); knob(c, 2, 1); open(c, PAGE.lfo); knob(c, 0, -1);
  assert.deepEqual(labels(c).map(x => x[0]), ['WAVE', 'SPEED', 'PMD', 'AMD']);
  assert.deepEqual(timbre(c), original);
});

test('all six operator editors and their six pages remain reachable in simple view', () => {
  const c = core();
  open(c, 2);
  const keys = [1, 3, 5, 8, 10, 13];
  for (let operator = 0; operator < 6; operator++) {
    c.sim_control(1, keys[operator], 1); c.sim_control(1, keys[operator], 0); tick(c);
    assert.equal(state(c)[5], operator);
    for (let page = 1; page <= 5; page++) {
      knob(c, 0, 1);
      assert.equal(state(c)[6], page);
    }
  }
  open(c, PAGE.settings);
  assert.deepEqual(labels(c)[0], ['VIEW', 'SIMPLE']);
});

test('presentation changes leave rendered audio identical to upstream', () => {
  const a = core(), b = core(baseline);
  for (const c of [a, b]) { open(c, PAGE.env); c.sim_control(1, 7, 1); }
  let energy = 0;
  for (let i = 0; i < 100; i++) {
    const pa = a.sim_render(), pb = b.sim_render();
    const audio = new Float32Array(a.memory.buffer, pa, a.sim_block_frames() * 2);
    assert.deepEqual(bytes(a, pa, audio.byteLength), bytes(b, pb, audio.byteLength));
    for (const sample of audio) energy += sample * sample;
  }
  assert.ok(energy > 0.001);
});
