---
description: Ground the ASB skill in play against its source paper/repo (Perspicacité KB, with a serverless local-clone fallback).
argument-hint: "[skill-slug-or-doi] [question]"
---
You are grounding an ASB skill against the evidence it was distilled from.

Steps:
1. Identify the target skill: use the argument if given, else the skill most recently applied in this conversation. Read its record in this plugin's `kb_bundle.json` (`dois`, `kb_slugs`, `repo_urls`).
2. If a Perspicacité server is reachable at $PERSPICACITE_BASE (default http://127.0.0.1:8000), ground via its KB (auto-creates + ingests on first use):
   `python "<plugin>/bin/perspicacite_kb_bind.py" query --collection "<plugin>" --skill <slug> --question "<question>"`
3. Otherwise fall back to serverless local grounding (clones the source repo, best-effort fetches the OA paper), then read the fetched files:
   `python "<plugin>/bin/perspicacite_kb_bind.py" local --collection "<plugin>" --skill <slug> --paper`
4. Answer the user's question grounded in what you retrieved; cite the KB/repo/paper. If neither backend yields a source, say so and proceed ungrounded.

Arguments: $ARGUMENTS
