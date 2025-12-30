# Memory Bank

## Project Overview
TUITASK is a Terminal User Interface task management system built with Python and Textual. The goal is to create a "State of the Art" application with a premium "Bagels" aesthetic (Neon/Dark/Cyberpunk).

## Architecture Spec — v0.5.0 (MVVM)
> Updated: 2024-12-29

### Design Pattern
The application follows a **Model-View-ViewModel (MVVM)** architecture to separate concerns and improve modularity.

- **Models** (`tuitask/models/`):
    - `Task`: Data structure for tasks.
    - `User`: User storage and authentication logic.
- **Components** (`tuitask/components/`):
    - Reusable UI widgets (`TopNav`, `CalendarWidget`, `AccountsPanel`, etc.).
- **ViewModels** (`tuitask/viewmodels/`):
    - `TasksViewModel`: Manages task data and business logic for the Tasks view.
- **Views** (`tuitask/views/`):
    - `MainScreen`: Main application shell managing navigation.
    - `DashboardView`: Home dashboard with grid layout.
    - `TasksView`: Split-view interface for task management.

### Entry Point
- `app.py`: Minimal entry point that initializes the App and pushes `MainScreen`.

## TUI Layout Spec — Bagels Style 0.4.0 (Textual)
> Updated: 2024-12-29

### Grid Layout
The application uses a 6-column Grid layout (`12fr 11fr 23fr 18fr 18fr 18fr`).

- **Column A (12fr)**: Part of Left Region.
- **Column B (11fr)**: Part of Left Region.
- **Column C (23fr)**: **Center Region**. Split into Calendar (Top) and Hosting (Bottom).
- **Column D (18fr)**: Part of Right Region.
- **Column E (18fr)**: Part of Right Region.
- **Column F (18fr)**: Part of Right Region.

### Regions & Spacing
- **Left Region (A+B)**: Vertical stack of `AccountsPanel` (Top) and `InsightsPanel` (Bottom).
- **Center Region (C)**:
    - `CalendarPanel`: Top (~60%).
    - `HostingPanel`: Bottom (Remaining), displaying system/server status.
- **Right Region (D+E+F)**: Vertical stack of `TemplatesPanel` (Top) and `RecordsPanel` (Bottom).

### Tasks View Layout (Horizontal Split)
- **Left (40%)**: `TaskListPanel` (DataTable).
- **Right (60%)**: `TaskCardPanel` (Detailed Card View).
- **Styling**: Consistent with Dashboard panels (Rounded borders, Bagel colors).

**Spacing Constants**:
- Outer Frame Padding: `1 3`
- Grid Gutter: `0 2`
- Panel Padding: `1 2`
- Header Height: `3`

### Widget Tree
```
App
└─ Container#outer_frame
   ├─ TopNav#header_nav (Includes Login Button)
   ├─ Grid#main_grid
   │  ├─ Container#left_region
   │  │  ├─ AccountsPanel#accounts_panel
   │  │  └─ InsightsPanel#insights_panel
   │  ├─ Container#center_region (was calendar_region)
   │  │  ├─ CalendarPanel#calendar_panel
   │  │  │  └─ CalendarWidget#calendar_grid
   │  │  └─ HostingPanel#hosting_panel
   │  └─ Container#right_region
   │     ├─ TemplatesPanel#templates_panel
   │     └─ RecordsPanel#records_panel
```

### CalendarWidget Implementation
- **Type**: Custom `Widget` (not Container).
- **Rendering**: Rich `Text` object via `render()`.
- **Logic**:
    - 7 Columns (S M T W T F S).
    - 3 chars per day cell (right aligned).
    - **Highlight Band**: Days 17-23 are highlighted with `reverse` style to create a continuous band effect.

## Recent History
### Layout Rework (Bagels 0.3.2)
- **Objective**: Refactor existing layout to matches specific user wireframes/screenshots.
- **Top Navigation**: Fixed height (3 lines), solid background, "Slick" styling with Breadcrumbs (`-> Bagels 0.3.2`) and solid tabs.
- **Grid Architecture**:
    - **MainArea**: Split into Layout Left (40%) and Right (60%).
    - **Left Group**:
        - `AccountsPanel`: Top-Left.
        - `ViewAddWrapper`: Top-Mid. Includes `ViewAddControls` (Flat, simplified) and `CalendarPanel`.
        - `InsightsPanel`: Bottom-Left (Spanning).
    - **Right Group**:
        - `TemplatesPanel`: Top-Right (Cyan Outline).
        - `RecordsPanel`: Bottom-Right (Orange Outline).
- **Calendar Fixes**:
    - Implemented CSS Grid (7 columns) for perfect day alignment.
    - Compacted vertical spacing (single line rows).
    - Separated from controls to fix rendering constraints.
- **Visual Polish**:
    - Removed borders from Period controls (Direct plain text/arrow integration).
    - Applied color-coded outlines (Orange/Cyan).
    - Ensured "Round" borders everywhere.

## Current State
- **Files**:
    - `tuitask/app.py`: Main application logic, layout composition.
    - `tuitask/styles.tcss`: Global stylesheet.
- **Status**: Dashboard layout is complete with new Grid system and custom CalendarWidget. Navigation crash fixed. Next focus is Task Management features.
