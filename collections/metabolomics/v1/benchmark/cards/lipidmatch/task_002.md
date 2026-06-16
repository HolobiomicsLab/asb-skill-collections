# SciTask Card: Reconstruct the fragment m/z matching engine that maps experimental to library values

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-16T06:03:34.399740+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_lipidmatch/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `information-extraction`
- GitHub: `GarrettLab-UF/LipidMatch`
- Input from: `task_001`
- Quality: Score 3/5 — placeholder

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `lipidomics`
- Subdomains: `lipidomics`
- Techniques: `database-annotation`, `high-resolution-ms`, `lc-ms`, `metabolite-identification`, `spectral-library-matching`, `tandem-ms`

## Research Question
How does LipidMatch match experimental fragment m/z values to in-silico library m/z values to identify lipids?

## Connected Finding
LipidMatch performs lipid identification by matching experimental fragment m/z values against simulated m/z values from in-silico fragmentation libraries containing over 500,000 lipid species across over 60 lipid types.

## Task Description
Given experimental fragment m/z values from a Q-Exactive or Q-TOF peaklist file and LipidMatch in-silico library CSV files, apply LipidMatch matching logic to produce a table of matched lipid identifications with m/z tolerance filtering.

## Inputs
- task_001.expected_outputs[0]: Summary report documenting distinct lipid species count, distinct lipid-type category count, and threshold validation (≥500,000 species, ≥60 types)
- Experimental fragment m/z peaklist file (from Q-Exactive orbitrap or Q-TOF UHPLC-HRMS/MS, e.g., CSV table with m/z and intensity columns)
- LipidMatch in-silico fragmentation library CSV files (covering 500,000+ lipid species across 60+ lipid types)

## Expected Outputs
- Matched lipid identifications table (CSV or TSV) with columns: lipid name/class, experimental m/z, library m/z, mass error, match score, and confidence metrics

## Expected Output File

- `matched_lipids.csv`

## Landmark Outputs

- `experimental_peaklist_loaded.csv`
- `library_fragments_indexed.csv`
- `matched_lipids.csv`

## Tools
- LipidMatch
- Q-Exactive orbitrap
- Agilent Q-TOF UHPLC-HRMS/MS
- Bruker Q-TOF UHPLC-HRMS/MS
- SCIEX Q-TOF UHPLC-HRMS/MS

## Skills
- mass-spectrometry-fragment-matching
- lipid-library-annotation-from-mz
- mass-accuracy-tolerance-calibration
- hrms-data-format-parsing
- lipid-identification-scoring

## Workflow Description
1. Load experimental fragment m/z values from a peaklist file (Q-Exactive or Q-TOF format, e.g., CSV or mzML-derived table). 2. Load LipidMatch in-silico fragmentation library CSV files covering the 500,000+ lipid species across 60+ lipid types. 3. Apply LipidMatch m/z matching algorithm: compare each experimental m/z against library fragments using mass tolerance thresholds to identify candidate lipid matches. 4. Output matched lipid identifications as a structured table with lipid name, class, m/z, and match quality metrics.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/LipidMatch_Icon2.png` | figure | False |
| `figures/LipidMatch_Icon3.png` | figure | False |
| `figures/LipidMatch_Icon4.png` | figure | False |
| `figures/LipidPioneer_Icon.png` | figure | False |
| `figures/LipidPioneer_Icon2.png` | figure | False |
| `figures/adwaita.png` | figure | False |
| `figures/ambiance.png` | figure | False |
| `figures/aqua.png` | figure | False |
| `figures/arrowStyles.png` | figure | False |
| `figures/baghira.png` | figure | False |
| `figures/browse.png` | figure | False |
| `figures/browseTree.png` | figure | False |
| `figures/bwidget.png` | figure | False |
| `figures/config.png` | figure | False |
| `figures/dirViewer.png` | figure | False |
| `figures/dust.png` | figure | False |
| `figures/dustSand.png` | figure | False |
| `figures/embeddedWindows.png` | figure | False |
| `figures/embeddedWindows_tile.png` | figure | False |
| `figures/scatterplot3d.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history is provided

## Domain Knowledge
- LipidMatch relies on matching experimental fragment m/z values against pre-computed in-silico fragmentation patterns; accuracy depends critically on instrument mass calibration and the ppm tolerance setting used during matching.
- The library covers over 500,000 lipid species across 60+ classes; matching quality varies by lipid class and ionization mode (positive/negative).
- Q-Exactive orbitrap and Q-TOF instruments produce different mass accuracy profiles; Q-Exactive typically achieves <5 ppm error while Q-TOF instruments may have wider tolerance windows.
- LipidMatch is format-agnostic for peakfiles but does not currently support Waters instrument output; input peaklists must be from MZmine, XCMS, MS-DIAL, or Compound Discoverer preprocessing.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Bruker Q-TOF UHPLC-HRMS/MS, SCIEX Q-TOF UHPLC-HRMS/MS.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does LipidMatch match experimental fragment m/z values to in-silico library m/z values to identify lipids?: 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch performs lipid identification by matching experimental fragment m/z values against simulated m/z values from in-silico fragmentation libraries containing over 500,000 lipid species across over 60 lipid types.: 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] Experimental fragment m/z peaklist file (from Q-Exactive orbitrap or Q-TOF UHPLC-HRMS/MS, e.g., CSV table with m/z and intensity columns): 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch in-silico fragmentation library CSV files (covering 500,000+ lipid species across 60+ lipid types): 'in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Matched lipid identifications table (CSV or TSV) with columns: lipid name/class, experimental m/z, library m/z, mass error, match score, and confidence metrics: 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch: 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Q-Exactive orbitrap: 'tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Agilent Q-TOF UHPLC-HRMS/MS: 'Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] Bruker Q-TOF UHPLC-HRMS/MS: 'Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] SCIEX Q-TOF UHPLC-HRMS/MS: 'Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history is provided: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify that inputs include a peaklist file in a supported format (mzML, mzXML, or CSV with m/z and intensity columns) from Q-Exactive or Q-TOF instrument
- verify that inputs include at least one in-silico library .csv file from the LipidMatch repository or a user-generated library with required columns (lipid name, adduct, theoretical m/z)
- verify that the matching output table file exists and is in CSV or tabular format
- verify that output table contains at least the following named columns: matched lipid identifier, experimental m/z, theoretical m/z, m/z error (ppm or Da), matched fragment count, confidence score or ranking
- verify that all rows in output table have non-null values in the m/z error field and that error values are numeric and within a biologically plausible range (typically ≤ 5–10 ppm for high-resolution instruments)
- verify that the LipidMatch matching script runs without fatal errors when executed with the provided peaklist and library files
- verify that row count of output table is greater than zero (at least one lipid matched)
- byte-for-byte match of output against a reference result file (if a reference matched-identifications table from a published validation is deposited) or expert review of match quality

### Expert Review
- assess whether matched lipid identifications are chemically and biochemically plausible given the sample type and ionization mode
- assess whether m/z error distribution across all matched fragments is reasonable and consistent with instrument calibration and resolution
- assess whether the number of matched lipids and their relative abundances are consistent with expected lipidome composition for the sample type
- verify that the matching logic correctly applies mass tolerance thresholds and fragment matching rules as documented in the LipidMatch method
- assess whether any false-positive or false-negative matches are evident by comparing against independent lipid annotations (if available from the same sample)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** light
- **Commercial software:** Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF
- **Open-source alternatives:**
  - MZmine → XCMS
  - Compound Discoverer → MS-DIAL

## Methodology Summary
1. Load experimental fragment m/z peaklist from Q-Exactive or Q-TOF instrument output
2. Load LipidMatch pre-computed in-silico fragmentation library (500,000+ species, 60+ lipid classes)
3. Apply m/z matching algorithm with mass tolerance threshold to compare experimental fragments against library entries
4. Score and rank candidate lipid matches by similarity and confidence metrics
5. Validation: output table contains matched lipid identifications with m/z error within instrument tolerance specification and match scores above confidence threshold

## Workflow Ports

**Inputs:**

- `experimental_mz_peaklist` — Experimental fragment m/z peaklist file (Q-Exactive or Q-TOF)
- `lipidmatch_library` — LipidMatch in-silico fragmentation library CSV files

**Outputs:**

- `matched_lipids` — Matched lipid identifications table with m/z and quality metrics

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:GarrettLab-UF__LipidMatch`
- **Synthesized at:** 2026-06-16T06:08:18+00:00

## Extraction Quality
- Score: 3/5
- Coherent: true
- Placeholder detected: true
- Notes: The card is semantically coherent: research_question and finding align on the core concept (m/z matching for lipid identification). However, the research_question asks 'how' (implying algorithmic mechanism), while the finding and evidence provide only functional description ('by matching'). The expected_outputs and parameters fields lack specificity—no concrete column names beyond placeholders, and critical tunable parameters (ppm tolerance, minimum fragment count, score threshold) are absent. The evaluation_strategy is well-structured but relies on generic MS best-practices (5–10 ppm) rather than LipidMatch-specific thresholds. Domain knowledge mentions Waters instrument exclusion, but this is not reflected in task constraints or input validation rules. The card would benefit from: (1) explicit parameter documentation with default values, (2) LipidMatch-specific m/z tolerance ranges per instrument type, (3) concrete output column specifications with metric definitions, and (4) clarification of ranking/scoring algorithm. Overall functional quality is adequate for task scoping, but implementation readiness is moderate.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
