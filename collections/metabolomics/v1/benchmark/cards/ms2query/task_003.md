# SciTask Card: Reconstruct the Scoring Module computing average InChIKey and neighbourhood scores

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T21:30:15.767044+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_ms2query/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- GitHub: `iomega/ms2query`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 5 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `analog-search`, `cosine-similarity-scoring`, `database-annotation`, `metabolite-identification`, `spectral-library-matching`, `tandem-ms`
- Keywords: `ms/ms spectral matching` · `analogue search` · `tandem mass spectrometry` · `spectral library search` · `metabolomics`

## Research Question
How does the scoring module compute average InChIKey score and neighbourhood score for candidate matches in MS2Query?

## Connected Finding
The provided document is a README file containing installation and usage instructions, workflow steps, and repository links, but does not include technical descriptions of the scoring module implementation, score computation methods, or output record structures.

## Task Description
Implement the Scoring Module that computes average InChIKey score and neighbourhood score for candidate matches returned by the library-matching step, and output the scored candidate records.

## Inputs
- task_001.expected_outputs[0]: Control-flow specification or architectural diagram documenting the two-branch orchestration logic (library-match vs. analogue-search), decision criteria, and routing for MS2Query workflow as introduced in PR #72
- Candidate match records from library-matching step

## Expected Outputs
- Scored candidate matches with average InChIKey score and neighbourhood score fields
- Test results verifying score computation correctness

## Expected Output File

- `scored_candidates.csv`

## Landmark Outputs

- `candidate_matches_loaded.json`
- `inchikey_scores_intermediate.csv`
- `neighbourhood_scores_intermediate.csv`
- `scoring_tests_passed.log`

## Tools
- MS2Query
- Python
- GitHub

## Skills
- spectral-library-candidate-ranking
- inchikey-structural-similarity-scoring
- neighbourhood-density-computation
- scoring-module-unit-testing
- candidate-metadata-record-serialization

## Workflow Description
1. Load candidate matches produced by the library-matching step (including match identifiers and InChIKey annotations). 2. Compute average InChIKey score for each candidate by aggregating structural similarity metrics across matched InChIKey layers. 3. Compute neighbourhood score for each candidate by evaluating the density and proximity of similar candidates in the spectral feature space. 4. Combine both scores into a single candidate record with standardized fields (candidate ID, InChIKey score, neighbourhood score). 5. Validate output record structure and score ranges using unit tests via Python pytest or setuptools. 6. Write scored candidates to output file with complete metadata.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/features_used.png` | figure | False |
| `figures/ms2query_logo.png` | figure | False |
| `figures/ms2query_logo.svg` | figure | False |
| `figures/worflow_average_ms2deepscore.png` | figure | False |
| `figures/workflow_ms2query.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- The specific mathematical definition, aggregation method (e.g., mean, median, weighted average), and input data sources for computing the 'average InChIKey score' are not provided in the changelog entry.
- The specific mathematical definition, distance/similarity metric, and neighbourhood selection criteria for computing the 'neighbourhood score' are not provided in the changelog entry.
- The structure and field names of the output record produced by the scoring module (e.g., JSON keys, column names if tabular) are not documented in the changelog.
- The relationship between the scoring module (PR #78) and the library-matching refactoring (PR #65) — specifically how scores are passed between these workflow steps — is not documented in the changelog.

## Domain Knowledge
- InChIKey is a standardized chemical structure identifier; average InChIKey score measures structural similarity between a query spectrum and candidate library entries across multiple InChIKey layers.
- Neighbourhood score quantifies the clustering or density of similar candidate matches in spectral feature space; higher neighbourhood scores indicate robust consensus among spectrally-similar library entries.
- Scoring modules in spectral matching pipelines must balance multiple dimensions (structure, spectral similarity, local density) to rank candidates for downstream annotation confidence.
- Python setuptools test runner (python setup.py test) is the standard validation method for MS2Query module implementations; tests must verify score ranges and record structure completeness.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Scored candidate matches with average InChIKey score and neighbourhood score fields, Test results verifying score computation correctness.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] How does the scoring module compute average InChIKey score and neighbourhood score for candidate matches in MS2Query?: 'No verbatim evidence available in provided text'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The provided document is a README file containing installation and usage instructions, workflow steps, and repository links, but does not include technical descriptions of the scoring module implementation, score computation methods, or output record structures.: 'MS2Query - Reliable and fast MS/MS spectral-based analogue search'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Candidate match records from library-matching step: 'You want to make some kind of change to the code base (e.g. to fix a bug, to add a new feature, to update documentation)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Scored candidate matches with average InChIKey score and neighbourhood score fields: 'add your own tests (if necessary)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Test results verifying score computation correctness: 'make sure the existing tests still work by running ``python setup.py test``'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] MS2Query: 'MS2Query - Reliable and fast MS/MS spectral-based analogue search'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Python: 'make sure the existing tests still work by running ``python setup.py test``'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] GitHub: 'fork the repository to your own Github profile and create your own feature branch off of the latest master commit'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] The specific mathematical definition, aggregation method (e.g., mean, median, weighted average), and input data sources for computing the 'average InChIKey score' are not provided in the changelog entry.: 'Average inchikey score and neighbourhood score [#78]'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] The specific mathematical definition, distance/similarity metric, and neighbourhood selection criteria for computing the 'neighbourhood score' are not provided in the changelog entry.: 'Average inchikey score and neighbourhood score [#78]'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] The structure and field names of the output record produced by the scoring module (e.g., JSON keys, column names if tabular) are not documented in the changelog.: 'Average inchikey score and neighbourhood score [#78]'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] The relationship between the scoring module (PR #78) and the library-matching refactoring (PR #65) — specifically how scores are passed between these workflow steps — is not documented in the changelog.: 'Refactored library matching [#65]'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that PR #78 branch or merged code in iomega/ms2query contains a module or function implementing average InChIKey score computation
- file_exists: verify that PR #78 branch or merged code in iomega/ms2query contains a module or function implementing neighbourhood score computation
- script_runs: execute the scoring module with a synthetic candidate match record (from library-matching step) and verify output_matches_reference by comparing returned score fields against manually computed ground-truth values for both metrics — robust to parameter choices in candidate inputs
- field_present: verify that the output record structure includes a named field or key for 'average inchikey score' (or exact variant used in codebase)
- field_present: verify that the output record structure includes a named field or key for 'neighbourhood score' (or exact variant used in codebase)
- file_format_is: verify that scoring module outputs are serialized in a format compatible with downstream matching workflow (e.g. JSON, CSV, or Python dict) — no canonical answer as multiple formats are defensible

### Expert Review
- Validate that the mathematical definition and aggregation logic for 'average InChIKey score' aligns with the intended semantics (e.g., is it mean, median, or weighted average across candidates; does it handle missing or null scores)
- Validate that the mathematical definition and computation of 'neighbourhood score' aligns with domain expectations (e.g., what constitutes a 'neighbour' in chemical or spectral space, how is proximity measured, what weighting scheme is used)
- Validate that both scores produce outputs within defensible numerical ranges (e.g., 0–1 for similarity scores) and that score scaling/normalization is consistent with library-matching step conventions

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load candidate match records from upstream library-matching module, retaining match IDs and InChIKey annotations.
2. Compute average InChIKey score per candidate by aggregating structural similarity across InChIKey layers.
3. Compute neighbourhood score per candidate by evaluating spectral feature-space density and proximity of similar matches.
4. Merge both scores into a single standardized candidate record structure with ID, InChIKey score, and neighbourhood score fields.
5. Validate: Unit tests confirm score ranges are within expected bounds (e.g. 0–1 or 0–100), record structure matches specification, and output file is machine-readable CSV or JSON.

## Workflow Ports

**Inputs:**

- `candidate_matches` — Candidate match records from library-matching

**Outputs:**

- `scored_candidates` — Scored candidate matches with InChIKey and neighbourhood scores
- `test_results` — Unit test results for scoring module

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:iomega__ms2query`
- **Synthesized at:** 2026-06-15T21:36:15+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (5):
  - research_question: evidence_span not found in section 'methods' (value='How does the scoring module compute average InChIKey score a', span='No verbatim evidence available in provided text')
  - research_question and finding are semantically misaligned: RQ asks 'how does the scoring module compute scores' but finding states 'the document does not include technical descriptions of scoring module implementation'
  - inputs[0]: evidence_span 'You want to make some kind of change to the code base...' is generic placeholder text unrelated to candidate match records
  - expected_outputs[0]: evidence_span 'add your own tests (if necessary)' does not support claim about 'scored candidate matches with average InChIKey score and neighbourhood score fields'
  - expected_outputs[1]: evidence_span 'make sure the existing tests still work...' is generic instruction, not evidence of specific test validation for scoring module
- Notes: This card exhibits a fundamental logical contradiction: it correctly identifies (in task_objective and finding) that the source material is insufficient, yet simultaneously specifies a detailed implementation workflow, skill requirements, evaluation strategy, and landmark outputs as though the source were complete. The research_question presupposes technical documentation that the finding denies exists. The input and output evidence_spans are either placeholder text (generic GitHub instructions) or generic methodology language ('add your own tests') rather than article-specific references. The groundedness_failures should be escalated: this is not a card ready for task execution—it is a specification that exceeds the constraints of the available source material. Recommend either: (A) revising the RQ to ask 'what information is missing from the MS2Query documentation regarding scoring module implementation?' (matching the finding), or (B) sourcing technical documentation (code repository, API docs, or peer-reviewed methods paper) that contains the algorithmic specifications implied by the workflow.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
