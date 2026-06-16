# SciTask Card: Reconstruct the per-sample molecular transformation network generation step of the MetaboDirect pipeline

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:03:26.683093+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_metabodirect`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`, `visualization`
- GitHub: `Coayala/MetaboDirect`
- Input from: `task_002`
- Quality: Score 3/5 — placeholder

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `microbiome-metabolomics`, `environmental-metabolomics`, `untargeted-metabolomics`
- Techniques: `direct-infusion-ms`, `high-resolution-ms`, `feature-detection`, `metabolite-identification`, `multivariate-statistics`, `molecular-networking`

## Research Question
How does MetaboDirect construct biochemical transformation networks from FT-ICR MS peak data, and what are the input requirements and output formats for this mass-difference network generation step?

## Connected Finding
MetaboDirect generates transformation networks ab initio from high-resolution mass spectrometry data by identifying chemically transformed species using clearly defined mass differences, with the networks designed to quantify differences in microbial metabolic pathways and identify hub metabolites involved in many reactions.

## Task Description
Implement a standalone mass-difference network construction module that accepts a filtered peak list with assigned molecular formulas and reference biochemical transformation keys, computes pairwise mass differences with 1 ppm error tolerance, matches them to known transformations, and outputs Cytoscape-compatible node and edge CSV files.

## Inputs
- Filtered peak list CSV containing peak identifiers, m/z values, assigned molecular formulas, compound class, and normalized intensities from preprocessing step
- Reference biochemical transformation key containing predefined masses of common metabolic reactions, optionally user-specific for analyzed system

## Expected Outputs
- Edge CSV file(s) per sample containing source peak m/z, target peak m/z, mass difference, transformation type (biotic/abiotic), and ppm error
- Node CSV file containing all detected peaks with m/z, molecular formula, compound class, and sample presence
- Transformation statistics CSV reporting number of transformations occurring per sample and transformation frequency
- Network visualization files and statistics tables exported as CSV and bar plots

## Expected Output File

- `transformation_networks_edges.csv`

## Landmark Outputs

- `pairwise_mass_differences.csv`
- `matched_transformations_raw.csv`
- `transformation_classifications_filtered.csv`
- `cytoscape_nodes.csv`
- `transformation_frequency_per_sample.csv`
- `network_statistics.csv`

## Tools
- MetaboDirect
- Cytoscape

## Skills
- mass-difference-network-construction
- biochemical-transformation-matching
- ppm-error-tolerance-filtering
- peak-pairwise-comparison
- transformation-classification-biotic-abiotic
- cytoscape-edge-node-file-formatting
- mass-spectrometry-molecular-formula-handling

## Workflow Description
1. Load filtered peak list (CSV with m/z values and molecular formulas) and reference biochemical transformation key containing predefined masses of common metabolic reactions. 2. Calculate all pairwise mass differences between detected peaks in each sample. 3. Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error ≤1 ppm against reference values. 4. Classify matched transformations as biotic or abiotic based on prior categorization. 5. Generate edge CSV files containing putative transformations (source peak m/z, target peak m/z, transformation type, error) for each sample. 6. Generate node CSV file with all detected peaks, their m/z values, molecular formulas, and compound class assignments. 7. Output transformation statistics (count per sample, transformation frequency distribution) as summary CSV and bar plots. 8. Prepare node and edge files formatted for Cytoscape import.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `metabodirect.pdf` | main_article | True |

## Missing Information
- No explicit specification of which reference transformation table (e.g., KEGG database, custom in-house library, or published biochemical transformation catalog) should be used for mass-difference matching in the standalone module
- No documented mass tolerance (ppm or Da) for matching observed mass differences to reference transformation masses
- No description of how the script handles or filters transformations with multiple equally plausible biochemical identities at the same observed mass difference
- No specification of input file format requirements (column headers, delimiter, data type for m/z and formula columns, row order)
- No documented output schema or example node/edge list file showing expected column names, data types, and edge weight definitions for Cytoscape import

## Domain Knowledge
- Mass-difference networks represent chemical transformations as edges connecting detected peaks (nodes) via their m/z differences; a 1 ppm mass tolerance threshold filters out spurious matches unlikely to occur by chance.
- Biochemical transformation keys are curated reference lists of common metabolic reaction masses (e.g., +16 for oxidation, −2 for dehydration); transformations can be classified as biotic (enzyme-catalyzed) or abiotic (spontaneous/photochemical) based on biochemical context.
- FT-ICR MS produces exact m/z measurements with sub-ppm resolution; the 1 ppm error cutoff exploits this high mass accuracy to confidently assign chemical transformations to mass differences.
- Cytoscape edge and node CSV files follow a standard format (edge lists with source, target, and attributes; node lists with identifiers and properties); proper formatting enables automated network visualization and topological analysis.
- Peak intensity normalization in the preprocessing step must be applied consistently before mass-difference calculations to ensure reproducible transformation detection across samples with different ionization efficiencies.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How does MetaboDirect construct biochemical transformation networks from FT-ICR MS peak data, and what are the input requirements and output formats for this mass-difference network generation step?: 'The last step of MetaboDirect produces molecular transformation networks for each of the samples. These networks are generated ab initio from the masses that are determined through high-resolution'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] MetaboDirect generates transformation networks ab initio from high-resolution mass spectrometry data by identifying chemically transformed species using clearly defined mass differences, with the networks designed to quantify differences in microbial metabolic pathways and identify hub metabolites involved in many reactions.: 'These networks are generated ab initio from the masses that are determined through high-resolution mass spectrometry and are based on the fact that the ultra-high mass accuracy of the method allows'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Filtered peak list CSV containing peak identifiers, m/z values, assigned molecular formulas, compound class, and normalized intensities from preprocessing step: 'This pre-processing step generates several .csv files containing the list of filtered peaks with their respective thermodynamic and molecular indices and the normalized and unnormalized intensities'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Reference biochemical transformation key containing predefined masses of common metabolic reactions, optionally user-specific for analyzed system: 'comparing them to the list of pre-defined masses of common metabolic reactions (biochemical transformations key)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Edge CSV file(s) per sample containing source peak m/z, target peak m/z, mass difference, transformation type (biotic/abiotic), and ppm error: 'The results are exported as .csv "edge" files containing the potential transformations occurring between the masses in each sample.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Node CSV file containing all detected peaks with m/z, molecular formula, compound class, and sample presence: 'nodes represent peaks detected in the different samples and edges represent the putative chemical transformations happening between the nodes'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Transformation statistics CSV reporting number of transformations occurring per sample and transformation frequency: 'Additional files with the number of transformations occurring per sample are also generated.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Network visualization files and statistics tables exported as CSV and bar plots: 'network statistics will be calculated and reported as .csv tables and bar plots'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] MetaboDirect: 'Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Cytoscape: 'Networks are then constructed using Cytoscape [79] and colored based on their molecular class.'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] No explicit specification of which reference transformation table (e.g., KEGG database, custom in-house library, or published biochemical transformation catalog) should be used for mass-difference matching in the standalone module: 'calculation of mass-based chemical transformations'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] No documented mass tolerance (ppm or Da) for matching observed mass differences to reference transformation masses: 'mass-based chemical transformations'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] No description of how the script handles or filters transformations with multiple equally plausible biochemical identities at the same observed mass difference: 'transformation networks'
- `ev_014` from `agent2_synthesis` (agent2_traced): [intro] No specification of input file format requirements (column headers, delimiter, data type for m/z and formula columns, row order): 'The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] No documented output schema or example node/edge list file showing expected column names, data types, and edge weight definitions for Cytoscape import: 'transformation networks'

## Evaluation Strategy
### Direct Checks
- verify that input file contains at least 2 columns: m/z and assigned molecular formula (field_present)
- verify that the standalone script accepts a peak list file as command-line argument or config parameter (script_runs)
- verify that the script computes pairwise mass differences and outputs a numeric matrix or edge list (output_matches_reference: check against Example transformation network data in bacterium-phage dataset OSF deposit https://doi.org/10.17605/OSF.IO/XFHZ9)
- verify that output node/edge list file is in Cytoscape-compatible format (.sif, .gml, or edge-attribute table; format_is)
- verify that file_exists for output node list and edge list artifacts
- verify that transformation matching correctly retrieves entries from reference transformation table (no canonical answer—multiple valid transformation databases may apply; expert_review required for chemistry accuracy)
- verify that script completes without error on bacterium-phage dataset (40 samples, average 495 peaks with assigned formula per sample) in parameter-sensitive runtime (expected sub-minute based on reported ~36 s for main pipeline steps without KEGG mapping)
- verify that rows in output edge list contain at minimum: source_mass, target_mass, mass_difference, transformation_name fields (row_count_equals and field_present)

### Expert Review
- Assess whether mass-difference matching algorithm correctly resolves ambiguous transformations (multiple biochemically valid transformations at same Δm/z)
- Evaluate whether the standalone implementation preserves the transformation network generation logic reported for bacterium-phage results (Fig. 3B shows lignin–protein interaction clusters; expert should verify those patterns reproduce from script output)
- Review whether edge weights (if present) accurately reflect transformation abundance or frequency across samples, consistent with Fig. 3A heatmap methodology
- Confirm that script output is suitable for direct import into Cytoscape without manual curation or format conversion

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load filtered peak list and reference biochemical transformation key into memory
2. Calculate all pairwise mass differences between detected peaks within each sample
3. Match mass differences to reference transformation key, retaining matches with ≤1 ppm error tolerance
4. Classify matched transformations as biotic or abiotic based on prior biochemical categorization
5. Generate node CSV (peaks with m/z, formula, compound class) and edge CSV files (transformations with source, target, type, error) formatted for Cytoscape
6. Compute and export transformation summary statistics (count per sample, frequency distribution) as CSV tables and bar plots
7. Validation: verify edge files contain no transformations with mass error >1 ppm, confirm all nodes reference detected peaks in input list, and confirm all transformations are classified (biotic or abiotic)

## Workflow Ports

**Inputs:**

- `filtered_peak_list` — Filtered peak list with m/z, molecular formula, and compound class ← `task_002/phage_runtime`
- `transformation_key` — Reference biochemical transformation key with predefined metabolic reaction masses

**Outputs:**

- `edge_files` — Edge CSV files per sample with transformation details
- `node_file` — Node CSV file with peak metadata
- `transformation_stats` — Transformation statistics and summary plots

## Extraction Quality
- Score: 3/5
- Coherent: true
- Placeholder detected: true
- Notes: The card is well-structured and comprehensive in scope, but suffers from three key quality issues: (1) both research_question and finding evidence_spans are syntactically incomplete (mid-sentence truncations), preventing full groundedness validation; (2) the research_question asks about input requirements but the finding omits this entirely, creating a coherence gap; (3) the card conflates abstract methodology with concrete implementation requirements—no actual transformation reference table, input schema, or output example is provided, leaving the task implementation ambiguous. The expected_artifact_name (singular 'edges.csv') contradicts the multi-file output structure (nodes, edges, stats). The 1 ppm tolerance is embedded in workflow but not highlighted in research_question/finding. Recommend: (a) complete the evidence_span sentences in source section; (b) revise research_question to focus on network generation logic rather than broad input/output coverage, or expand finding to address input requirements; (c) provide concrete example files, reference table URI, or schema specification; (d) update expected_artifact_name to reflect multi-file outputs.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
