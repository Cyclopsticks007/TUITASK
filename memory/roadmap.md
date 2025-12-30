# Roadmap

# Roadmap

## Phase 2: Core Functionality (Current)
- [x] **UI Overhaul** (Bagel Aesthetics v0.4.0)
- [x] **Architecture Refactor** (MVVM v0.5.0)
- [ ] **Tasks Implementation**
    - [/] Task List & Details View (Split Layout)
    - [ ] Create/Edit Task Logic (CRUD)
    - [ ] Filtering & Sorting
- [ ] **Storage Layer (v0.6.0)**
    - [ ] **Async SQLite**: Implement `aiosqlite` for non-blocking local storage.
    - [ ] **ORM**: Integrate `SQLModel` or `Tortoise ORM`.
    - [ ] **Schema**: Define `Task`, `User`, `Project` tables.

## Phase 3: Connected Future (Planned)
- [ ] **Real-time Sync**
    - [ ] Host Mode: Shared Postgres/Redis backend.
    - [ ] Sync Engine: Sync local SQLite diffs to Host (e.g., using CRDTs or Litestream).
    - [ ] Offline-first capability.
- [ ] **Gamification**
    - [ ] XP and Velocity tracking logic.
    - [ ] Leaderboards and Badges.
- [ ] **Audit Logging**
    - [ ] Track all changes for accountability.
