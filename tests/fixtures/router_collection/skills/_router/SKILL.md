---
name: fixture-router
description: Search the compact fixture collection, then apply and ground one skill.
---

# Fixture router

Entry point for **10 evidence-grounded skills**, each derived from a method paper.

## 1. Search

```bash
python "<collection root>/bin/search_skills.py" --collection "<collection root>" --query "<the user's task>" -k 10
python "<collection root>/bin/search_skills.py" --collection "<collection root>" --query "<the user's task>" --target workflows -k 10
```

Read the selected `leaves/<slug>/SKILL.md` and follow its procedure.

## 2. Ground

```bash
python "<collection root>/bin/perspicacite_kb_bind.py" query --collection "<collection root>" --skill <slug> --question "<what you need to verify>"
```

## Licence tiers

Read `license_tier`: open, noncommercial, or restricted. Noncommercial skills
require an acknowledgment of the intended non-commercial purpose before use.
