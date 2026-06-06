# Meshmorize 🧠

Multi-layer memory system for OpenClaw agents. Fresh layer, mesh indexing, auto-logging, and compliance checks.

## Layers

| Layer | File | Purpose |
|-------|------|---------|
| **Fresh** | `memory/fresh/today.md` | Daily notes, 5-day rotation |
| **Mesh** | `memory/mesh.json` | Graph nodes + search index |
| **Log** | `scripts/auto_log` | Auto-log every interaction |
| **Search** | `scripts/memory_search` | Cross-layer search |
| **Check** | `scripts/memory_check` | Full compliance check |

## Quick start

```bash
mem-bridge init                # Rotate fresh layer
auto_log "msg" "reply"         # Log an interaction
memory_search "query"          # Search all layers
memcheck                       # Full compliance check
```

## Commands

- `memcheck` — Run all 10 compliance checks
- `memory?` — Trigger full check from agent
- `bridge.py init` — Initialize daily rotation
