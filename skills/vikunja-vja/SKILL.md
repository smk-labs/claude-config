---
name: vikunja-vja
description: Manage Vikunja tasks, projects, and labels via the vja CLI. Use whenever the user mentions tasks, todos, Vikunja, due dates, priorities, or wants to create, list, edit, complete, or delete anything in their task manager.
---

# Vikunja Tasks (vja CLI)

Interact with a Vikunja instance using the `vja` command-line tool.

**Two rules that always apply:**
- Always pass `--json` for machine-readable output
- Task titles are **positional** arguments — not `--title`

---

## Tasks

### Create
```bash
vja add "Task title"
vja add "Task title" -n "Description" -d "tomorrow" -p 3 -l urgent -A alice
vja add "Task title" -d "next monday at 9:00" -r "1h before due_date" -o "My Project"
```

| Flag | Meaning |
|------|---------|
| `-n` / `--note` | Description/body |
| `-d` / `--due` | Due date (natural language or ISO) |
| `--start` / `--end` | Start/end dates |
| `-p` / `--prio` | Priority: 1=low, 2=medium, 3=high, 4=urgent |
| `-l` / `--label` | Label (repeat for multiple: `-l bug -l backend`) |
| `-A` / `--assignee` | Username to assign |
| `-r` / `--reminder` | Reminder time (`"in 3 days at 18:00"`, `"1h before due_date"`) |
| `-o` / `--project` | Project name or ID |
| `-f` / `--star` | Mark as favorite |
| `--force-create` | Create the label if it doesn't exist |

### List & Filter
```bash
# Basic list
vja ls --json | jq '.tasks[] | {id, title, due_date, priority}'

# Common filters
vja ls --filter "done eq false" --json | jq '.tasks[] | {id, title}'
vja ls --filter "priority ge 3" --json | jq '.tasks[] | {id, title, priority}'
vja ls --filter "due_date before today" --json | jq '.tasks[] | {id, title, due_date}'
vja ls -l urgent --json | jq '.tasks[] | {id, title}'
vja ls -o "My Project" --json | jq '.tasks[] | {id, title}'
vja ls -u 3 --json | jq '.tasks[] | {id, title, urgency}'  # urgency score >= 3
vja ls --all --json | jq '.tasks[] | {id, title, done}'    # include completed
vja ls --sort "-priority,due_date" --json | jq '.tasks[] | {id, title}'
```

Filter operators: `eq`, `ne`, `gt`, `lt`, `ge`, `le`, `before`, `after`, `contains`
Multiple `--filter` flags are ANDed together.

### Show
```bash
vja show <task_id> --json | jq '{id, title, description, due_date, priority, assignees, labels}'
```

### Edit
```bash
vja edit <task_id> -i "New title"
vja edit <task_id> -n "Updated description"
vja edit <task_id> -a "Appended note"         # append to existing description
vja edit <task_id> -d "next friday" -p 4
vja edit <task_id> -l bug -l backend          # replace labels
vja edit <task_id> -A alice                   # toggle assignee (adds if absent, removes if present)
vja edit <task_id> -c true                    # mark completed
vja edit <task_id> -f                         # star; use --no-star to unstar
vja edit <task_id> -o "Other Project"         # move to a different project
```

### Other task commands
```bash
vja toggle <task_id>               # toggle done/undone
vja delete <task_id> -q            # delete quietly
vja defer <task_id> 2d             # push due date forward (also shifts reminders)
vja defer <task_id> 1h30m
vja clone <task_id> "New title"    # duplicate a task
vja open <task_id>                 # open in browser
```

---

## Projects

```bash
vja project ls --json | jq '.[] | {id, title, parent_project_id}'
vja project show <project_id> --json | jq .
vja project add "Project name"
vja project add "Sub-project" -o "Parent Project"
```

## Labels

```bash
vja label ls --json | jq '.[] | {id, title}'
vja label add "new-label"
```

## User

```bash
vja user show --json | jq '{id, username, email}'
```

---

## Workflow Examples

### Daily review
```bash
# Overdue open tasks
vja ls --filter "due_date before today" --filter "done eq false" --json \
  | jq '.tasks[] | {id, title, due_date}'

# High-priority open tasks, sorted by urgency
vja ls --filter "priority ge 3" --filter "done eq false" --sort "-urgency" --json \
  | jq '.tasks[] | {id, title, priority, urgency, due_date}'
```

### Create with full context in one shot
```bash
vja add "Review PR #42" -p 3 -d "today" -A alice -l review --force-create
```

### Bulk-defer all overdue tasks by one day
```bash
vja ls --filter "due_date before today" --filter "done eq false" --json \
  | jq '.tasks[].id' \
  | xargs -I{} vja defer {} 1d -q
```

### Mark complete and confirm
```bash
vja toggle <task_id> -v --json | jq '{id, title, done}'
```

---

## Notes
- Dates accept natural language via parsedatetime: `"tomorrow"`, `"next monday"`, `"in 3 days at 9:00"`, `"2025-12-31"`
- `--json` returns Vikunja API format; `--jsonvja` returns vja's internal format
- Config lives at `~/.config/vja/config.rc` (legacy: `~/.vjacli/vja.rc`)
