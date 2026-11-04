# FM1 accessible custom firmware

## Goal

Make the user's Mwave FM1 approachable for someone with little music knowledge while retaining every capability of the original device. The supplied *Detailed User Manual — FM-1 Synthesizer* establishes the documented controls and functions; manufacturer identity and the owner's hardware/firmware revision still need confirmation. See [CAPABILITIES.md](CAPABILITIES.md) for the documented baseline and unresolved details.

## Proposed experience

- Start in a simple view focused on choosing a sound, playing, and saving a variation.
- Describe controls by audible results, using plain language such as “brighter” where appropriate. Pair these labels with exact technical parameter names in the advanced view.
- Offer an advanced view with direct access to every supported parameter and original function. Switching views must preserve the current sound and settings.
- Make editing reversible: compare against the saved sound, undo edits, and confirm before overwriting saved work.
- Provide short, contextual explanations that fit the actual display and controls. Do not assume a touchscreen, additional buttons, or a companion application.
- Keep assistance optional. If the hardware supports scales or chord tools, allow them to be disabled so unrestricted playing remains available.
- Preserve expressiveness and avoid adding audible latency or interruptions during navigation and editing.

These are design proposals, not claims about existing FM1 features or validated hardware feasibility.

## Preserve the original capabilities

The initial manual-based inventory is in [CAPABILITIES.md](CAPABILITIES.md). Its entries are documented requirements, not hardware test results. Supplement it with stock behavior and source inspection before implementation. Do not claim feature parity until every inventory item is verified.

## Simple view on the documented controls

These mappings are proposals to prototype, not installed behavior. Use the existing 1.54-inch TFT, SELECT/PRESETS/ALGORITHM encoders, four parameter encoders, physical mode buttons, and 27 illuminated keys. Keep the MASTER volume control dedicated to volume. Do not require extra controls or assume encoder push actions beyond those confirmed for the target unit.

| Task | Proposed simple experience | Full controls retained |
| --- | --- | --- |
| Choose a sound | PRESETS browses existing named sounds; display the name and an unsaved-change indicator | All 128 voices; preserve SEQ's documented pattern-voice selection rule |
| Shape a sound | ENV: Fade in (Attack), Settle (Decay), Hold level (Sustain), Fade out (Release), with the same parameter values | ENV enable/bypass and all four parameters; separate per-operator envelopes remain in EDIT |
| Add space or texture | FX: SELECT chooses an effect; show readable parameter names and current values | Every effect parameter, subtype, bypass, and SEL-based ordering |
| Add movement | LFO: Shape, Speed, Pitch wobble (PMD), Volume wobble (AMD); show the technical name on the detail page | Both LFO pages, depth sensitivity, delay, and both sync settings |
| Play a repeating pattern | ARP: explain Mode as Note order, Octave as Octave span, Rate as Note division, Tempo as BPM | All seven modes, gate, swing, latch, external clock, and octave span |
| Record a phrase | SEQ: show Record / Playing / Stopped and current step; provide a short recording hint | All patterns, chain/length, pattern voice, per-step rate, long notes, rests, replacement, and timing controls |
| Edit synthesis deeply | EDIT opens the full operator editor with plain-language explanations alongside technical labels | All six operators, pitch envelope, synthesis globals, mono/poly, init, rename, copy, and mute |
| Return to playing | HOME keeps its documented short-press behavior | Long HOME continues to toggle Bluetooth |

Use SELECT to navigate short pages, with four consistently positioned knob labels and a value focus when a knob turns. Keep prompts readable on the small screen; do not rely on long paragraphs or color alone. Keep critical battery warnings visible.

Put the Simple / Advanced preference on an explicit system-settings page, with a visible route back. Do not assign it to a stock long-press shortcut. Both views share a single parameter state; switching changes presentation only. Existing scale/chord assistance is not documented and is outside the initial parity scope.

Avoid a universal “Brightness” macro initially: filter cutoff is an exact, explainable control, while changing FM operator levels has algorithm-dependent consequences. Sound categories also need a verified preset list before assigning names such as Bass or Keys.

## Proposed improvements requiring implementation validation

- Add an edit buffer, compare/revert, and an explicit destination/confirmation when overwriting a voice. Do not claim the stock firmware already supports undo or backup export.
- Explain ARP/SEQ mutual exclusion with a prompt offering to stop the active mode and switch; do not silently run them together or discard a recording.
- When SEQ owns voice selection, explain why PRESETS is inactive and show the pattern's voice control.
- Distinguish returning HOME from stopping playback, saving edits, or disabling a sound-processing function.
- Keep imported voice-bank replacement, initialization, pattern clearing, copying, and reset behind clear prompts showing what will change. Preserve original ranges and storage contents; storage format and write timing need investigation.

## Implementation prerequisites

1. Identify the exact product and hardware revision from its label and official manual.
2. Establish whether firmware source, an SDK, or a documented custom-firmware mechanism exists, and check its license.
3. Identify the processor, memory, display, controls, audio hardware, bootloader, and update format from authoritative evidence. Do not choose a toolchain by guessing.
4. Establish a supported recovery procedure and obtain a verified stock firmware image before any device flashing. Keep the owner's saved sounds backed up using supported methods.
5. Verify the original workflow, then build one small vertical slice: choose a sound, edit one supported parameter through both views, and save/reload without losing settings.

If custom firmware cannot be installed through an established mechanism, investigate a companion editor only if the device exposes a documented control protocol. A companion editor would require agreement on the changed project scope and is not equivalent to device firmware.

## Acceptance criteria

- A beginner can choose a sound, make a predictable change, undo it, and save a variation without needing synthesis terminology.
- Simple and advanced views operate on the same parameter state and do not reset it when switching.
- Every original capability has a verified entry in the inventory and remains accessible.
- Saved sounds and supported external protocols remain compatible where required by the verified inventory.
- Builds are reproducible with the identified toolchain, and device tests meet the hardware's audio and timing requirements.
- Update and recovery procedures are validated before recommending installation to another owner.

## Current status

The official APP and binary SDK are imported under `firmware/`, with provenance and licenses retained. Both unchanged and modified C sources build as Linux WebAssembly simulators. The first Simple/Advanced prototype covers envelope/LFO labels and a session-only help/settings page; eight integration tests pass. See [README.md](README.md) for reproduction and [FEATURE_AUDIT.md](FEATURE_AUDIT.md) for confirmed differences from the manual. Native Windows firmware compilation, physical-device validation, recovery, and full original-feature parity remain outstanding. No custom device firmware has been built or flashed.
