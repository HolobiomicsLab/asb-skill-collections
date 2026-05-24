---
name: Submit agent or RAG system result
about: Add a result to the benchmark leaderboard
title: "[LEADERBOARD] <system-name> on <collection>/<version>"
labels: ["leaderboard-submission", "needs-validation"]
assignees: "lfnothias"
---

## Leaderboard submission

> **Next step after this issue:** Open a PR adding your result to
> `collections/<slug>/v<N>/benchmark/leaderboard.jsonld`.
> The `leaderboard-validate.yml` CI action will validate your entry.

## System information

**System name:** <!-- e.g., Claude-Opus-4-RAG, GPT-4o-Agent -->
**System type:** <!-- agent | rag_system | hybrid -->
**Collection + version:** <!-- e.g., metabolomics/v1 -->
**Submission date:** YYYY-MM-DD

## Reproducibility

**Agent container image (if agent):**
<!-- Docker image hash or `ghcr.io/...@sha256:...` -->

**Commit SHA:**
<!-- SHA of the code used to run the evaluation -->

**Cost and latency stats:**
- Total API cost (USD):
- Average latency per task (seconds):
- Median latency per task (seconds):

## Results (summary)

**For agent tasks (benchmark/tasks/):**
- Tasks attempted:
- Tasks solved (tier: full):
- Tasks partially solved (tier: structural_only):
- Overall score (eval.json pass rate):

**For RAG/claim retrieval (benchmark/claims/):**
- MRR (per-paper):
- Recall@5 (per-paper):
- MRR (cross-paper):
- Claim conformance (%):

## Reproducibility declaration

- [ ] My results are reproducible from the container image + commit SHA above
- [ ] I did not have access to the held-out test set (if any)
- [ ] I am not a maintainer of this collection (or I declare the conflict)
- [ ] I accept that my results may be re-scored by maintainers using the held-out set
