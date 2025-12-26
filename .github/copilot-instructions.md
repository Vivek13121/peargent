# Peargent – PR Review Rules

## Goal

Provide **concise, high-signal PR reviews** for the Peargent Python Agent Framework.  
Favor **clarity over completeness** and **summary over inline comments**.

One PR = **one review comment**, unless there is a real bug.

---

## Review Style (STRICT)

- Prefer **one high-level summary comment**
- Inline comments are **allowed ONLY** for:
  - Bugs
  - Security issues
  - Broken imports
  - Public API breakage
- If the PR is acceptable, say **“Looks good”** and stop.

Do not behave like a linter.

---

## Comment Size Rules

- Maximum **5 bullet points** in a review
- Any explanation longer than **3 lines** must be collapsible

```md
<details>
<summary>Details</summary>

Additional context here.
</details>
````

---

## Do NOT Comment On

* Formatting or style (Black handles this)
* Naming preferences
* Minor refactors
* “Consider adding comments”
* Suggestions already enforced by CI
* Hypothetical improvements

---

## Blocking Rules

Only block a PR if one of these is true:

* Tests fail (`python -m pytest`)
* Public API is broken
* Internal modules are imported (`peargent._core.*`)
* Missing type hints on **public** APIs
* CI fails on supported Python versions

Everything else is **non-blocking**.

---

## CI Awareness

* Assume CI is authoritative
* Do not restate CI errors unless necessary
* Do not explain test failures unless subtle

---

## Import Rule (CRITICAL)

✅ Allowed:

```python
from peargent import create_agent, create_tool, create_pool
from peargent.models import groq, anthropic, openai
```

❌ Forbidden:

```python
from peargent._core.agent import Agent
from peargent._core.tool import Tool
```

Importing internal modules is always **blocking**.

---

## Review Checklist (Mental)

* Imports work
* Tests pass
* Public API unchanged or intentionally updated
* Types present
* CI green

If all pass → approve.

---

## Final Instruction

If no blocking issues exist:

* Write **one short summary**
* Do NOT leave inline comments
* Do NOT suggest optional improvements

Minimal is correct.

