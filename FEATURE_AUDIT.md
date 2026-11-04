# Initial source-level feature audit

Baseline: M-VAVE FM1 Open V14 commit `4c7496daac04a95ff10d1afdcc8f9ead2dbabc41`, imported under `firmware/`. Comparison target: the user-supplied manual, inventoried in [CAPABILITIES.md](CAPABILITIES.md).

This is an initial code audit, not certification of every inventory row. “Present” below means visible in the source/API; only items explicitly described as tested were exercised. The Linux web engine and the separately supplied native device engine are distinct implementations. A passing simulator test does not establish native behavior.

| Manual capability | Finding in the imported base | Evidence / remaining work |
| --- | --- | --- |
| Six operators, 32 algorithms, per-operator tuning/envelopes/scaling, pitch envelope, FM LFO | Operator and common parameter pages are present | `app/screen.c` `fm_pages`, `fm_parameter`; all six operators and all six per-operator pages tested for reachability in Simple view. Audio/range parity for every parameter is untested. |
| Additional ADSR envelope, enable/bypass | Present; both views use the same values and edit handlers | `groove_adsr_edit`, `groove_adsr_enable`; simulated edits, view switching, panel save, and reboot tested. Exact stock envelope timing still needs hardware comparison. |
| 128 voices and four DX7 banks | Present in the independent library; source supports bank and single-voice transfer | `app/fm_library.c`, `app/fm_factory.c`, `app/transfer.c`; MIDI SysEx framing, compatibility, and all preset sounds need explicit tests. Main HOME preset browsing also involves project/demo presets; it is not simply the manual's 128-voice browser. |
| Mono/poly, glide and original 12-voice capacity | FM controls expose mono/poly, but device allocation and all stock ranges are not verified | `app/instrument.h`, `app/screen.c`; native SDK audio behavior needs Windows build and hardware tests. Do not infer polyphony from web audio success. |
| Seven ARP modes | **Gap:** APP offers UP, DOWN, UP-DN, RANDOM only | `app/screen.c` `edit_page_draw`; `web/engine/sound.c` `groove_arp_edit` limits mode to 0–3. Inclusive/exclusive endpoints, Order, Repeat and repeat behavior need implementation/specification. Native equivalents require investigation. |
| ARP gate/swing/rate and ARP/SEQ exclusion | **Different:** APP gate is 25/50/75/100%; four rate divisions; swing stored 0–50; per-track ARP architecture differs | `web/engine/sound.c`; original gate minimum is 20%, manual swing is 50–75%. Conversion and transport interactions need explicit design and tests. |
| Six reorderable effects, filter/reverb types, independent on/off and original ranges | **Gap:** APP FX pages expose track sends/cutoff/drive and shared reverb/delay, not the manual's six-slot chain | `app/screen.c` `effects_draw`, `web/engine/effects.c`, `web/engine/sound.c`; no original chorus/phaser/reordering UI is established. Audit native SDK capabilities before choosing an implementation. |
| Octave −3…+3, performance transpose and combined reset | **Gap:** APP octave clamp is −2…+2; original gesture/reset parity not established | `app/screen.c` `apply_controls`; performance transpose must remain distinct from FM patch transpose and sequence transpose. |
| 16-step patterns, per-step rate, chain, long notes/rest/replacement | **Different:** eight tracks with 16/32/48/64-step loops and project/arrangement storage | `app/instrument.h`, `web/engine/sequencer.c`; an extension is not automatic compatibility. Original chain/rate/recording semantics and migration need mapping. |
| SAVE, automatic pattern storage, bank reset and voice management | **Different storage model:** project slots, staging, independent voice library, copy/paste and undo | `app/project.c`, `app/fm_library.c`; simulated project save/reboot passed for edited ADSR. Original autosave/reset/copy/name behavior and power-loss atomicity are not certified. |
| USB/BLE/DIN MIDI, PC, CC, velocity-zero Note On, pitch bend, clock | Native interfaces and routing code present | `app/midi_router.c`, `app/board`, SDK headers; simultaneous physical ports, original CC map and bend/channel ranges remain untested. |
| TFT, LEDs, speaker/headphones, volume, battery warnings and HOME oscilloscope | Panel/board code present; HOME is an eight-track overview rather than the manual's oscilloscope | `app/board`, `app/screen.c`, `app/audio_output.c`; inspect physical warning priorities, jack detection, LEDs and UI behavior on hardware. Simulator battery/radio/flash are platform substitutes. |
| Firmware update and rollback | Vendor update resources retained unchanged; no device test | SDK manifest verified. Native toolchain, update/recovery and interrupted-write behavior remain outstanding. |

## Changes in this milestone

Only `firmware/app/screen.c` differs from the imported upstream tree. It adds a session-only Simple/Advanced setting, a help page, alternate labels for the FM envelope and first LFO page, and a bypass hint. Existing sound handlers, other editors, SDK files, storage structures and updater resources are unchanged.

Two independent builds use the same WASI SDK 27 and upstream compiler flags. Eight executed integration tests verify audible baseline output, equivalent initial parameter values, panel navigation, view-switch state preservation, edited-value persistence across a simulated reboot, both LFO pages, all operator pages, and byte-identical rendered audio for the tested note sequence. These results apply to the simulator only.

The immediate engineering priority after a native build is to resolve the confirmed stock-feature gaps. This base is suitable for prototyping the interface; it is not yet a complete replacement preserving every capability in the manual.
