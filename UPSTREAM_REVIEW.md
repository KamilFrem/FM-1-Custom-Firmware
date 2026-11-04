# Firmware foundation review

Reviewed 2026-11-04 for the proposed beginner-friendly FM-1 firmware.

## Resource hub supplied by the user

[aroum/fm1-custom-fw](https://github.com/aroum/fm1-custom-fw), inspected at commit `2ddf341675cc1503365b5056e8ffe292d209d46c`.

This is a directory of firmware projects, technical references, and Python MIDI utilities. Its tracked files contain no synthesizer C/C++ implementation or native firmware build system. It is useful for discovery, not a firmware codebase to fork for the proposed interface.

The repository's `fm1_flasher.py` explicitly describes its flash streaming as experimental/non-functional because its host-push framing differs from the device-pull protocol. Do not use this script as the installation path. Its scanner also sends messages to a device; the “read-only” label alone does not verify their behavior across firmware versions.

The hub claims hardware details for the JieLi AC791N/WL82 family and lists the official source, community instruments, and stock binary modifications. Treat these as leads to primary sources. Its detailed recovery claims are not established by this review.

## Official source: strongest candidate to evaluate first

[m-vave/fm1_open](https://github.com/m-vave/fm1_open), README, `app/instrument.h`, `LICENSE.md`, and `THIRD_PARTY.md` inspected at commit `4c7496daac04a95ff10d1afdcc8f9ead2dbabc41`.

- The current README identifies this as **FM1 Open V14**. This version name must not be confused with the original stock V14/V15 firmware or the hub's claims about stock V16.
- The application has editable sources and a separately licensed binary device SDK. It is not a fully source-available device engine.
- The README documents eight tracks, eight sample slots, a DX7 library of 128 voices in four banks, single-voice/bank SysEx import/export, step and live recording, internal/external timing, MIDI routing, and a browser preview.
- `app/instrument.h` exposes shared parameter descriptors, FM editing state, arpeggiator controls, sequencer controls, project snapshots, and device/session preferences. These are promising interfaces for building simple and advanced views over the same state.
- The public API describes 16/32/48/64-step track lengths, additional instrument sources, and project formats. This is a different architecture from the supplied single-part, 16-step manual. Feature parity requires mapping and testing; it cannot be assumed from the manufacturer name.
- APP sources use GPLv3-only with an explicit SDK linking exception. The SDK has separate terms allowing development and distribution for M-VAVE FM1 devices, with required notices. Distributed changes need corresponding APP source and build/install scripts. Preserve `LICENSE.md` and `THIRD_PARTY.md`.
- The documented native build requires **Windows x64**, PowerShell, and **JieLi toolchain 2.5.3 / PI32v2 clang 4.0.1**, targeting `r3`. The build verifies 22 toolchain files against its manifest; those checks must remain enabled.
- Web builds use WASI SDK 27, also through the documented Windows build flow. A browser simulator is available, but no build or simulator was run during this review.
- The README describes a local firmware build using `sdk/Build.ps1 -FirmwareOnly`, a packaged `.fwsc` output, and a workbench route back to original V15. It explicitly limits third-party migration compatibility. This is documentation, not a recovery test on the owner's device.

Recommendation: evaluate this pinned official APP/SDK first, reproduce its unchanged build and preview, and add beginner presentation without replacing the FM engine. Audit every item in CAPABILITIES.md before selecting it as the final base. A Linux-hosted native build is not yet established; do not substitute an arbitrary Linux toolchain for the pinned Windows release.

## Reverse-engineering reference

[AL-255/FM-1-RE](https://github.com/AL-255/FM-1-RE), README inspected at commit `ec832f281ca165a7d5e0722985f3acb1465046d5`.

The current main branch expressly contains no replacement firmware/builders; its old experimental implementation is on `with-custom-firmware`. It provides architecture research, OTA analysis, a Linux protocol client, and offline protocol tests.

Its README says ROM recovery, rollback, and safe interrupted writes have **not** been established. This conflicts with the resource hub's stronger recovery language. Keep recovery unverified rather than promising that a failed flash is always reversible.

## Other leads

The hub lists Felucca and many derivatives. It also lists Gnomad as an existing Easy/Advanced interface with picture-based sound selection. These may be useful design references, but their sources and claimed feature sets were not inspected here. An alternative instrument may change polyphony, effects, storage, or MIDI behavior, so an appealing beginner interface is not evidence of original-feature parity.

## What this review establishes

An editable manufacturer application and documented SDK/build path exist. This removes the earlier uncertainty about whether there is any source-based development route. It does not establish that the owner's board revision is compatible, that the cloud environment can execute the required Windows build, or that this base retains every original function.

No dependencies were installed, no firmware was built, and no MIDI scan, update, reset, or device write was performed. The hub was cloned into a separate temporary review directory; the user's project and repository configuration were not replaced.

Next implementation steps: inspect the full official checkout and its agent/build instructions; establish a supported build environment; validate the unchanged native/web outputs; map all manual capabilities against actual APP controls; then prototype one reversible edit through both interface views. Preserve the device update handler throughout development.
