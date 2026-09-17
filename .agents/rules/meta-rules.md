---
trigger: always_on
description: Use for rule priority, navigation, and skill invocation (planning, review, commit, rule governance).
---

# Meta rules

## Priority (highest -> lowest)
1. AGENTS.md - persona and behavioral constraints
2. project-rules - tech stack, venv, and repository layout
3. agents-feature-checklist - quality gate and post-change verification
4. project-architecture - MVC layer boundaries and invariants
5. project-tests - test suite structure and execution
6. docs/llm/software-engineering-rules.md - Python coding standards

## Skill Invocation (single registry)
| Trigger / Intent | Action |
| --- | --- |
| Commit, branch, or any git write | @commit |
| Create, edit, or self-heal agent rules / conventions | @project-rules-writing |
| Ambiguous or relevant behavior change, before planning | @interview-plan |
| Any diff before delivery or git write | @adversarial-review |

## Navigation - when to read what
| Question | Read |
| --- | --- |
| Persona, communication style | AGENTS.md |
| Tech stack, venv, project facts | project-rules |
| Quality gate and post-change verification | agents-feature-checklist 
| MVC layout, routers, controllers, models | project-architecture |
| Test suite layout, running pytest | project-tests |
| Python patterns, error handling, imports | docs/llm/software-engineering-rules.md |