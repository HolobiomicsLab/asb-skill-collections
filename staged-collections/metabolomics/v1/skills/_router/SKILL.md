---
name: metabolomics-router
description: Use when seeking information in the domain of metabolomics, specifically utilizing LC-MS or GC-MS techniques for untargeted lipidomics analysis.
allowed-tools:
- mcp__perspicacite__search_skill_kb
- mcp__perspicacite__search_knowledge_base
- Read
license: Apache-2.0
metadata:
  iri: w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1/router
  routes_to_collection: w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
---

# Metabolomics Router

## When to use this skill
Whenever the user mentions metabolomics, LC-MS, GC-MS, untargeted, lipidomics or asks about Metabolomics-related tasks.
This router covers 105 specialized skills derived from 5 papers.

## How to route
1. Call `mcp__perspicacite__search_skill_kb(query=<user-question>, edam_topics=['http://edamontology.org/topic_3172', 'http://edamontology.org/topic_3520'])`.
2. Read the top-3 returned skill IRIs' SKILL.md files via Read tool.
3. Synthesize an answer from the most-relevant skill(s).
4. If Perspicacité MCP is unavailable, fall back to `_index.md`.

## Fallback (no Perspicacité)
The collection ships `_index.md` listing every skill with its description.
Read it, pick the best match, load that skill's SKILL.md.
