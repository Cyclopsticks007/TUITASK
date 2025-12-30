# Agent Instructions

## Memory System
This `memory/` folder is the brain of the project. Always check these files when starting a session to understand context.

### Files Definition
1.  **memory_bank.md**: A persistent summary of what has been accomplished. Update this after every major task completion. Append ~100 lines of history max (summarize older stuff).
2.  **roadmap.md**: The "ToDo" list. Move items from here to `task.md` (active artifact) when working. Update status here.
3.  **errors.md**: A log of significant technical hurdles. Format: `[Date] Error -> Cause -> Solution`.
4.  **style_guide.md**: The source of truth for visual design.

## Operational Rules
- **Check Memory**: Read `memory_bank.md` and `roadmap.md` first.
- **Update Memory**: Before finishing a task, update `memory_bank.md` with what you did.
- **Log Errors**: If you hit a tricky bug, log it in `errors.md`.
- **Styling**: Always consult `style_guide.md` before creating new UI components.
