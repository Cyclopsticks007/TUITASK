# Error Log

## [2025-12-29] CSS Variable Startup Crash
- **Error**: `Error in stylesheet: ... reference to undefined variable '$text-blue'`
- **Cause**: In `styles.tcss`, referenced `$text-blue` for the Templates Panel border, but only `$accent-blue` was defined in the variable block.
- **Solution**: Changed reference to `$accent-blue`.

## [2025-12-29] Calendar Constraint Issue
- **Error**: Period container "Cutting into" the calendar top.
- **Cause**: Negative margin or lack of spacing between the "View and Add" controls and the Calendar container.
- **Solution**:
    - Separated Controls and Calendar into distinct containers (`#panel-controls`, `#panel-calendar`).
    - Removed `min-height` constraints that forced overlapping.
    - Simplified the Period controls to reduce height pressure.

## [2025-12-29] CSS Update Failure
- **Error**: Tool call failure led to missing styles (Calendar invisible, outlines gone).
- **Cause**: `replace_file_content` failed or was interrupted, leaving CSS in an inconsistent state.
- **Solution**: Performed a full manual restore of the CSS file with the intended styles.
