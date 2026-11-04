# FM-1 documented capability baseline

Source: user-supplied `FM-1-manual.pdf`, titled *Detailed User Manual — FM-1 Synthesizer*. References below use the English section's printed page numbers, not PDF viewer page numbers. The Chinese specification section carries a revision date of 2026-08-10; this is not evidence of the owner's hardware or firmware version.

All rows below are **documented, not device-verified**. Tests describe future acceptance work. The manual is reference material, not authorization to reset, overwrite, or flash the owner's device.

## Controls and performance

| Capability to preserve | Documented behavior | Source | Future verification |
| --- | --- | --- | --- |
| Master volume | Dedicated 300-degree potentiometer | pp. 1, 14 | Output level responds independently of menus |
| Navigation | SELECT pages through modes and selects FX slots; PRESETS, ALGORITHM, and four parameter encoders; seven 360-degree controls total | pp. 1–5, 14 | Every mode/page and parameter reachable |
| Display | 1.54-inch TFT; preset header, mode/page footer, parameter values, battery indicator, transient popups | pp. 2–3 | Readability on actual display; correct status after edits |
| Presets | 001–128, immediate load, wraparound, temporary list popup | p. 1 | Load all slots, wrap both directions, preserve names |
| Algorithm | 32 routings for six operators; routing/feedback diagram | p. 1 | Every routing selectable; compare stock audio |
| Keyboard | 27 LED-equipped silicone keys; MIDI note = key position + 53 + octave × 12 + transpose | pp. 12, 14 | Note and LED behavior, including range boundaries |
| Octave | −3 to +3; directional LEDs slow/fast/solid for magnitude 1/2/3 | p. 2 | Boundaries and LED states |
| Performance transpose | Hold OCT− or OCT+ and turn ALGORITHM; −12 to +12 semitones; automatically saved globally | pp. 1–2 | Distinguish from synthesis and sequencer transpose |
| Pitch reset | OCT− and OCT+ together reset octave and performance transpose to zero | p. 2 | Both reset without unintended note events |
| Voice allocation | Mono with last-note priority; poly up to 12 simultaneous voices | pp. 7, 12 | Repeated/overlapping notes; allocation at and beyond 12 |
| Glide | Mono-only; Full Time / Fingered; amount 0–100 corresponding to 0–1 second | p. 8 | Legato versus detached notes and endpoints |
| Home and Bluetooth | HOME opens output oscilloscope; long HOME toggles BT; LED distinguishes off, waiting, connected | p. 8 | Navigation and connection state; no stuck notes |

## Synthesis and effects

| Capability to preserve | Documented parameters/ranges | Source | Future verification |
| --- | --- | --- | --- |
| Six operator editors, page 1 | Detune −7…+7; coarse 0–31; fine 0–99; output level 0–99 | p. 4 | Each operator independently retains exact values |
| Operator pages 2–3 | Four envelope rates and four levels, each 0–99 | p. 4 | All envelope stages, save/reload, stock sound comparison |
| Operator page 4 | Amplitude modulation sensitivity 0–3; velocity sensitivity 0–7; Ratio/Fixed oscillator mode | p. 4 | Both modes and sensitivity behavior |
| Operator pages 5–6 | Left/right depth 0–99; breakpoint A−1…C7; left/right curves −LN/−EX/+LN/+EX; rate scaling 0–7 | p. 4 | Both sides of breakpoint and every curve |
| Operator selection/mute | OP1–6 keys select; last page remembered per operator; long press mutes until voice switch | pp. 7, 12 | Mute restoration, selection LEDs and page memory |
| Pitch envelope | Four rates and four levels, each 0–99, across two PIT pages | p. 5 | Stages and persistence |
| Synthesis globals | Algorithm 1–32; feedback 0–7; oscillator sync; transpose 0–48 | p. 5 | Endpoints and stock transpose interpretation |
| Voice management | Initialize, rename, copy with source selection/target overwrite confirmation | p. 7 | Names, cancel paths, correct copy direction; no accidental writes |
| Additional ENV | Initially disabled; enable/bypass; Attack/Decay/Sustain/Release each 0–100% | pp. 4, 6 | Enabled versus bypassed behavior; interaction with operator envelopes |
| LFO page 1 | Triangle, Saw Down, Saw Up, Square, Sine, Sample & Hold; speed, PMD, AMD each 0–99 | pp. 4, 7 | All waveforms and modulation depths |
| LFO page 2 | Delay 0–99; pitch sensitivity 0–7; LFO reset sync and oscillator reset sync | pp. 4, 7 | Reset/free-run distinction and shared oscillator-sync state |
| FX chain | Six effects, individual on/off via knob 4; SELECT selects; SEL grabs/releases to reorder adjacent slots | pp. 3, 6 | Chain order, bypass, parameters retained after moving |
| Filter | Low Pass / Band Pass / High Pass; cutoff 100–20,000 Hz in 100 logarithmic steps; Q 0–100 | p. 4 | Subtypes, cutoff scale, resonance endpoints |
| Reverb | Room / Hall / Plate; decay and mix 0–100% | p. 4 | All subtypes and dry/wet endpoints |
| Delay | Decay, rate, mix 0–100% | p. 4 | Range mapping and repeat timing against stock |
| Distortion | Gain, tone, level 0–100% | p. 4 | Audio response and output level |
| Chorus and Phaser | Each has frequency, depth, mix 0–100% | p. 4 | Both independently tested across range |

## Arpeggiator and sequencer

| Capability to preserve | Documented parameters/behavior | Source | Future verification |
| --- | --- | --- | --- |
| ARP modes | Up, Down, Inclusive, Exclusive, Random, Order, Repeat | p. 9 | Endpoint handling, played order, repeat behavior |
| ARP timing | Octave span 1–4; rate; tempo 30–300 BPM; gate 20–100%; swing 50–75% | p. 5 | Timing at endpoints; rate choices need identification |
| ARP latch/sync | Hold notes after release; new keys replace pattern; latch off stops; sync to external MIDI clock | p. 9 | Key release/replacement, stop, external clock |
| ARP/SEQ exclusion | Either mode blocks enabling the other until deactivated | pp. 9, 11 | No overlapping transports or lost recording |
| SEQ structure | 16 patterns, up to 16 steps, chain 1–16, selected playback length 1–16 | pp. 5, 10–11 | Pattern selection, chain boundaries/wrap, shortened loops |
| SEQ recording | REC toggles recording; notes advance steps; rate adjustable per step; hold note and turn SELECT for long notes | p. 10 | Rates and ties/long notes without overwriting existing notes |
| SEQ rest/replacement | Hold REC and rotate SELECT to navigate, add/replace notes or insert rests | p. 10 | Correct step affected; rest representation |
| SEQ voice/timing | Voice 1–128 per pattern; rate; tempo 30–300; gate 20–100%; swing 50–75%; external clock sync; transpose −24…+24 | pp. 5, 10–11 | Independent pattern voices, timing and transpose boundaries |
| SEQ preset ownership | Panel PRESETS inactive while SEQ enabled; pattern Voice chooses sound | p. 11 | UI explanation and MIDI Program Change interaction |
| Transport and LEDs | PLAY/STOP and REC require SEQ; play green, stop orange, record red; step LEDs show occupied/empty/current | pp. 10–11 | State transitions, including stop during recording |
| SEQ clear/deactivation | Clear control on page 1; SEQ press in its mode stops/deactivates and returns Home | pp. 5, 11 | Determine exact clear scope; stop all scheduled notes |

## MIDI, storage, and device functions

| Capability to preserve | Documented behavior | Source | Future verification |
| --- | --- | --- | --- |
| Concurrent MIDI | USB MIDI, BLE MIDI, and 3.5 mm MIDI IN active simultaneously; wired MIDI 31,250 baud | p. 13 | Concurrent input, disconnect/reconnect, no stuck notes |
| MIDI receive | Note On/Off with velocity; zero-velocity Note On means Note Off; Pitch Bend; CC; PC 0–127 | p. 13 | Message parsing, channels, program numbering |
| MIDI transmit | Note On/Off with velocity from keyboard, ARP, and SEQ | p. 13 | Confirm routing separately for each supported output interface |
| MIDI settings | Receive ALL or 1–16; effect-control channel 1–16; upward/downward bend each 1–24 semitones; global velocity 1–127 | pp. 5, 8 | Channel filtering, asymmetric bend, velocity interpretation |
| DX7 bank import | Standard Yamaha DX7 banks, 32 voices each; select destination A/B/C/D | pp. 9, 13 | Exact SysEx framing/checksum and bank mapping need separate specification |
| SAVE | Hold to persist pending voice, FX, SEQ, and global changes; save LED and completion popup | pp. 8–9 | Power-cycle persistence and correct write scope |
| Pattern persistence | Patterns and assigned voices also described as automatically saved | p. 11 | Identify automatic-write timing versus SAVE; power-loss behavior |
| Reset Patches | Select A/B/C/D; confirm/cancel; restores selected bank to previously imported voices | p. 8 | Baseline source and affected data; do not equate with firmware recovery |
| Battery/power | Battery or USB; 3.7 V 2,000 mAh battery; level icon; persistent priority LOW BATTERY warning | pp. 13–14 | Battery sensing, warning thresholds, charging-related behavior on hardware |
| Audio output | Built-in speaker; 3.5 mm TRS headphones automatically mute speaker | pp. 13–14 | Jack detection and output switching |

## Unknowns and manual ambiguities

- No processor, RAM/flash capacity, board revision, display controller/resolution, audio codec, pinout, source license, SDK, build instructions, firmware image, update entry point, or bootloader/recovery procedure is provided. USB MIDI and DX7 bank import do not establish firmware-update support.
- The complete CC mapping is explicitly deferred to an “Official MIDI Response Table,” which was not supplied. Do not invent CC numbers or assume all deep editing parameters are remotely accessible.
- The two LFO/synthesis oscillator-sync entries may share one parameter; confirm in source or on stock hardware.
- Performance transpose (−12…+12), synthesis transpose (0…48), and sequence transpose (−24…+24) are distinct documented controls. Their combined behavior and neutral synthesis-transpose value need verification.
- The manual does not list ARP/SEQ rate choices, Repeat mode repeat count, delay-rate time units, exact swing timing, sequencer polyphony, or external-clock start/stop/loss behavior.
- REC exit is described both as switching to playback mode (p. 10) and leaving STOP lit (p. 11). Observe actual transport behavior before encoding it.
- Clear scope, chain wrap behavior, preset-change handling of unsaved edits, save atomicity, SysEx export, and full-device backup are unspecified. Documented bank import must not be presented as backup export.
- Keyboard “velocity” language does not establish physical velocity-sensitive keys; the global velocity control could provide a fixed value. Check the unit.
- No stock scale lock, chord assistance, undo, or beginner mode is documented. These would be new features, and resource feasibility is unknown.

## First implementation milestone

Once a supported firmware/source path and recovery method are established, compile the original firmware first. Then implement one shared-state edit through both presentations (for example ENV Attack / Fade in), verify switching views preserves its value, and test save/reload on the actual device. Expand only after that path is validated. A UI simulation alone cannot demonstrate firmware compatibility or feature parity.
