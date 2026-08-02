# Changelog

All notable changes to this project will be documented in this file.

## [1.4.0] - 2026-08-03
### Added
- Factory Demo selector for the scene IDs used by firmware 1.6.6 and newer.
- State Word diagnostic sensor with decoded flags and live notifications.

### Fixed
- Correct scene commands 30/31 to Stop Scenes and Start Scenes.
- Encode basic commands using the official app's four-byte header.

## [1.3.0] - 2026-08-02
### Added
- Home Assistant controls for permanent mute and permanent DND.
- Recurring DND and silent schedule controls, including start/end hours.
- User activity timeout control.
- Safe buttons and services to stop timers/alarms and navigate scenes.
- Complete sound and animation choices in the Send Notice action UI.

### Fixed
- Preserve nested and previously written settings when updating a single value.
- Refresh the shared device settings cache after successful writes.

## [1.2.0] - 2025-11-14
### Added
- Support for icons in notification text using `[icon:CODE]` syntax. See `ICONS.md` for available codes.
- New timer service: send timer scenes with intervals and final text, including icon support.
- Major code cleanup and refactor:
	- Moved service handlers to dedicated files under `services/`.
	- Moved color utilities to `utils/color_utils.py`.
	- Improved Bluetooth connection management and modularized code.
	- Updated and clarified documentation and service descriptions.

## [1.1.0] - 2025-11-11
### Added
- Calibration flow added to the integration.
- Placeholder for "Scene clear" added to integration

## [1.0.2]
### Added
- Updated readme to include Bluetooth CTS addon

## [1.0.1]
### Added
- Cleanup and HAC submission prep

## [1.0.0]
### Added
- Initial release.
