# Changelog

## [0.4.0] - 2024-12-29
### Added
- **Tasks Split View**: Overhauled Tasks screen to use a Bagel-style split layout (List + Detail Card).
- **Versioning**: Updated app version to 0.4.0.
### Changed
- **Login Visibility**: Improved Login button styling for better contrast and visibility in TopNav.
- **TopNav**: Updated version label.
### Fixed
- **Navigation Crash**: Refactored TasksView integration to prevent crashes on tab switching.

## [0.3.3] - 2024-12-29
### Changed
- Replaced separate Login Screen with a "Login" button in the Top Navigation bar.
- Refactored Dashboard Layout to 6 containers:
    - Split Center Column into Calendar (Top) and Hosting/System (Bottom).
- Fixed Calendar Widget to not encroach on full height.

## [0.3.2] - 2024-12-29
### Added
- "Bagel" UI Aesthetics (Grid Layout, Neon Colors).
- Custom `CalendarWidget` with Rich Text rendering.
- 6-column CSS Grid Layout.
