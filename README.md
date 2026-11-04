# Beginner-friendly M-VAVE FM-1 firmware

An initial Simple/Advanced interface prototype built on M-VAVE's official FM1 Open V14 APP and SDK. The goal is an approachable instrument that preserves the original FM-1 capabilities. **That goal is not complete: the official open base differs from the stock firmware described in the manual.** See [FEATURE_AUDIT.md](FEATURE_AUDIT.md) for known gaps.

## What works now

- The actual application C code builds into a WebAssembly simulator on Linux.
- Simple view starts by default: ENV uses **Fade in / Settle / Hold level / Fade out**; the first FM LFO page uses **Shape / Speed / Pitch / Volume**.
- Advanced view restores the original technical labels. Both views edit the same values; full operator editing remains accessible in either view.
- View switching does not change project contents, edit history, flash, or the dirty flag. The preference lasts for the session and resets to Simple after reboot; no upstream storage layout was changed.
- The native SDK, licenses, integrity manifest, updater, and packaging scripts are retained unchanged under `firmware/`.

This is a tested simulator prototype, not a device-validated firmware release. No custom `.fwsc` has been built or flashed.

## Try Simple / Advanced

In the simulator's virtual panel:

1. Hold **SEQ**, then press **EDIT** to open the existing actions menu. Alternatively hold SEQ for at least 600 ms while its step page is open.
2. Turn **SELECT** to the last action, **INTERFACE / HELP**, and press **SAVE** to open it. This selects a menu command; it does not write the view preference to flash.
3. Turn **KNOB 1** left for Simple, right for Advanced.
4. Press **ENV** to try the labels, or **HOME** to return. Turn **PRESETS** right on the FM ENV page to enable its envelope; it is bypassed initially.

Use EDIT for quick FM controls and hold EDIT for the full operator editor. The preference changes envelope/LFO presentation only in this milestone, not every screen. Other instrument engines keep their genuine engine-specific controls.

## Reproduce the Linux preview and tests

Requires Linux x86_64, Python 3.12+, Node.js 24, Git, curl, and tar support. Run from this repository root:

```bash
python3 tools/setup_wasi.py
python3 tools/check.py --wasi-sdk build/tools/wasi-sdk-27.0-x86_64-linux
```

The setup helper downloads WASI SDK 27 (about 119 MiB), verifies its published SHA-256, and extracts it under ignored `build/tools/`. TLS verification remains enabled. It can be rerun to restore the compiler from the verified archive.

`check.py` fetches the exact upstream commit from [UPSTREAM.json](UPSTREAM.json) into `build/upstream/`, rejects a dirty or different baseline, builds both unchanged and modified application sources, and executes eight simulator integration tests. It verifies 65 SDK files against the retained upstream manifest before each build. It does not run a device flasher.

To use an existing clean upstream checkout or SDK:

```bash
python3 tools/check.py --baseline-source /path/to/fm1_open --wasi-sdk /path/to/wasi-sdk-27.0-x86_64-linux
```

To rebuild only the modified preview:

```bash
python3 tools/build_preview.py --wasi-sdk build/tools/wasi-sdk-27.0-x86_64-linux
```

Outputs are `build/preview/index.html`, `simulator.wasm`, and `build.json`. The HTML embeds the compiled simulator and license notices. It is a local development workbench with no custom firmware payload. Serve the static preview directory with a local HTTP server if the browser requires it for audio features. All generated files and compiler downloads remain ignored by Git.

The [GitHub workflow](.github/workflows/simulator.yml) runs the same checks on Linux and uploads the preview as an artifact. Local execution has passed; a hosted workflow run is a separate check.

## Native device build: still outstanding

The vendor's documented native build requires **Windows x64**, PowerShell, and **JieLi Windows toolchain 2.5.3**, including PI32v2 clang 4.0.1 targeting `r3`. The Linux WASI compiler is solely for simulation and cannot produce FM-1 device firmware.

Follow [firmware/README.md](firmware/README.md) to install the official compiler. From a Windows PowerShell session:

```powershell
cd firmware
./sdk/Build.ps1 -FirmwareOnly -Toolchain 'C:\JL\pi32'
```

The vendor script verifies the SDK and all 22 toolchain files and checks the linked firmware. Keep these checks enabled. The documented device output is `firmware/build/dx7/generated/FM1_OFFICIAL_OPEN.fwsc`. This native command has not been executed in the current Linux environment.

Before distribution, the vendor packaging flow also requires an HTTPS URL for an archive of the exact corresponding modified source. Preserve the licenses and build/install scripts. Before device installation, establish compatibility, backups, and a tested update/recovery route for the target unit; the project has not demonstrated recovery from a failed write.

## Next development work

1. Reproduce and validate the unchanged Windows device build, then build this UI change with the same toolchain.
2. Resolve the original-feature gaps in [FEATURE_AUDIT.md](FEATURE_AUDIT.md), especially the six-effect chain and seven ARP modes. Do not replace these with a reduced feature set.
3. Expand Simple view into guided sound selection and recording, keeping technical controls available and edits reversible.
4. Test on the owner's matching hardware, including audio timing, simultaneous MIDI, power-cycle persistence, update entry, and recovery.

## Project records

- [Design](DESIGN.md)
- [Original manual capability inventory](CAPABILITIES.md)
- [Source-level feature audit](FEATURE_AUDIT.md)
- [Upstream research](UPSTREAM_REVIEW.md)
- [Licensing](LICENSE.md)

Each cloud task is already isolated; use the existing checkout rather than creating a worktree unless explicitly requested. Setup and development do not require flashing a physical device.
