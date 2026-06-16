# SciTask Card: Reconstruct the MassGrid alignment step and verify its conditional pairwise vs. landmark-based routing

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:33:42.864961+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_asari/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- DOI: `10.1038/s41467-023-39889-1`
- GitHub: `shuzhao-li-lab/asari_pcpfm_tutorials`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `lc-ms`, `feature-detection`, `chromatogram-alignment`, `quality-control`, `database-annotation`
- Keywords: `high-resolution metabolomics` · `lc-ms` · `gc-ms` · `peak detection` · `mass alignment` · `extracted ion chromatogram` · `untargeted metabolomics` · `composite map processing` · `peak quality tracking`

## Research Question
How does asari determine which mass alignment algorithm to apply based on study size?

## Connected Finding
Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional algorithm selection.

## Task Description
Implement the m/z alignment module that constructs a MassGrid by dispatching between pairwise alignment (≤10 samples) and nearest-neighbor clustering (>10 samples), producing a _mass_grid_mapping.csv file from aligned mass tracks across all samples.

## Inputs
- Mass track data from all samples, each containing m/z and full-RT-range intensity arrays
- Anchor mass track pairs (isotopic or adduct differences) per sample for confidence-based alignment
- Sample count and user-specified reference sample identifier (if provided)

## Expected Outputs
- _mass_grid_mapping.csv file documenting aligned m/z values, sample-track associations, and consensus m/z per grid position
- MassGrid object linking aligned mass tracks across all samples with consensus m/z identifiers

## Expected Output File

- `_mass_grid_mapping.csv`

## Landmark Outputs

- `anchor_mass_track_registry.json`
- `reference_sample_designation.txt`
- `aligned_pairwise_sample_tracks.json`
- `_mass_grid_mapping.csv`

## Tools
- Python
- asari mass_functions module (nn_cluster_by_mz_seeds)
- asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)

## Skills
- m/z-alignment-across-samples
- mass-track-consensus-computation
- pairwise-alignment-with-anchor-prioritization
- nearest-neighbor-clustering-by-mass-difference
- sample-study-size-stratified-algorithm-selection
- mass-grid-construction-and-mapping

## Workflow Description
1. Determine study size (sample count) to select alignment strategy: if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method. 2. Identify reference sample as the one with highest number of anchor mass tracks (13C/12C isotopes or Na/H adducts) unless user-specified. 3. For small studies, perform pairwise sample-wise alignment: align anchor mass tracks first between each sample and reference list, recalibrate all sample m/z values if systematic difference exceeds 1 ppm, then align remaining mass tracks. 4. For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance. 5. Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity. 6. Generate _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership across the MassGrid.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/conda_asari_screenshot.png` | figure | False |
| `figures/viz_screen_shot20220518.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog provided

## Domain Knowledge
- Anchor mass tracks (isotope/adduct markers) are prioritized in alignment because they have higher confidence and less stable m/z from centroiding artifacts; aligning them first prevents the remaining tracks from competing and causing spurious matches.
- ppm tolerance is the default precision threshold (5 ppm); the method detects systematic m/z shifts >1 ppm between sample and reference and recalibrates all sample m/z values accordingly to ensure alignment fidelity.
- The sample with the highest number of anchor mass tracks is designated as reference unless user-overridden, because abundance of confident isotopic/adduct patterns indicates a high-quality, representative profile.
- For studies with ≤10 samples (small studies), pairwise anchor-first alignment prevents statistical undersampling errors; for >10 samples (large studies), nearest-neighbor clustering is computationally efficient and statistically robust.
- Consensus m/z per grid position is computed as the mean of the median m/z and the m/z at maximum intensity to avoid instability from centroiding outliers and multiple data points in the same scan.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: asari mass_functions module (nn_cluster_by_mz_seeds), asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs), _mass_grid_mapping.csv file documenting aligned m/z values, sample-track associations, and consensus m/z per grid position.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does asari determine which mass alignment algorithm to apply based on study size?: 'Taking advantage of high mass resolution to prioritize mass separation and alignment'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional algorithm selection.: 'Scalable, performance conscious, disciplined use of memory and CPU'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Mass track data from all samples, each containing m/z and full-RT-range intensity arrays: 'Build mass tracks per data bin. If the m/z range in a data bin is within 2 x tolerance ppm, the bin leads to a single mass track.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Anchor mass track pairs (isotopic or adduct differences) per sample for confidence-based alignment: 'Establish anchor mass tracks by finding m/z differences that match to either 13C/12C isotopes or Na/H adducts.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Sample count and user-specified reference sample identifier (if provided): 'The sample with the highest number of anchor mass tracks is designated as the reference sample, unless a user specifies a reference sample via input parameters.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] _mass_grid_mapping.csv file documenting aligned m/z values, sample-track associations, and consensus m/z per grid position: 'MassGrid is exported as a csv file.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] MassGrid object linking aligned mass tracks across all samples with consensus m/z identifiers: 'Aignment of mass tracks across samples, resulting in the MassGrid'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Python: 'Requires Python 3.8+.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] asari mass_functions module (nn_cluster_by_mz_seeds): 'a nearest neighbor (NN) clustering is performed to establish the number of mass tracks. See [mass_functions.nn_cluster_by_mz_seeds](mass_functions.nn_cluster_by_mz_seeds).'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs): 'See [MassGrid.build_grid_sample_wise](MassGrid.build_grid_sample_wise), [MassGrid.add_sample](MassGrid.add_sample). See [MassGrid.build_grid_by_centroiding](MassGrid.build_grid_by_centroiding),'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No changelog provided: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that _mass_grid_mapping.csv file exists in expected output location
- verify file format is CSV with expected columns for m/z alignment mappings
- verify script runs without errors when processing mzML inputs through COMP_MASSGRID dispatcher
- verify that studies with ≤10 samples invoke ALG_PAIRWISE_ALIGN by checking function call logs or code execution trace
- verify that studies with >10 samples invoke ALG_LANDMARK_PEAKS and/or ALG_NN_CLUSTERING by checking function call logs or code execution trace
- verify output _mass_grid_mapping.csv row count is greater than zero and contains valid m/z alignment records
- verify that all input mzML files are successfully parsed by pymzml without parse errors

### Expert Review
- expert review of alignment quality: assess whether m/z alignment in _mass_grid_mapping.csv achieves expected mass separation and alignment precision given high mass resolution settings
- expert review of algorithm selection logic: confirm that the conditional dispatch (sample count threshold ≤10 vs >10) is correctly implemented and produces scientifically defensible alignments for both small and large studies
- expert review of mass track consistency: verify that aligned mass tracks in the output grid are reproducible and trackable back to original EICs per the asari design principle

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Determine alignment strategy by evaluating sample count: if ≤10, use pairwise anchor-prioritized alignment; else use nearest-neighbor clustering.
2. Identify reference sample as the sample with the highest count of anchor mass tracks (isotopic/adduct pairs).
3. For small studies, align anchor mass tracks first between each sample and the reference, then recalibrate all m/z values if systematic shift exceeds 1 ppm, then align remaining tracks.
4. For large studies, apply nearest-neighbor clustering to bin mass tracks by m/z difference, using histogram-based m/z seed detection with peaks separated by at least mz_tolerance.
5. Compute consensus m/z for each aligned bin as the mean of median m/z and m/z at highest intensity.
6. Validation: _mass_grid_mapping.csv is produced with all samples represented, consensus m/z values are numeric and within instrument ppm tolerance, and pairwise/clustering dispatching is correctly applied based on sample count threshold (≤10 vs >10).
7. References: source article (DOI: 10.1038/s41467-023-39889-1)

## Workflow Ports

**Inputs:**

- `mass_tracks_all_samples` — Mass track data from all samples ← `task_001/preferred_feature_table`
- `anchor_pairs_registry` — Anchor mass track pairs (isotopic/adduct) per sample
- `sample_count` — Total number of samples and reference sample ID

**Outputs:**

- `mass_grid_mapping` — _mass_grid_mapping.csv file with aligned m/z grid
- `massgrid_object` — MassGrid data structure with consensus m/z and sample track linkages

**Used:** `urn:asb:port:task_001/preferred_feature_table`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:shuzhao-li-lab__asari`
- **Synthesized at:** 2026-06-16T05:44:32+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
