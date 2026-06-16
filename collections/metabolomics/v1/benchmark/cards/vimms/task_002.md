# SciTask Card: Reproduce Simulated vs Real Beer mzML Comparison via Top-N DDA

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T12:40:40.120497+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_vimms/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `simulation`, `benchmark-evaluation`
- DOI: `10.1021/acs.analchem.0c03895`
- GitHub: `glasgowcompbio/vimms`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `data-independent-acquisition`, `feature-detection`, `machine-learning`, `metabolite-identification`, `spectral-library-matching`
- Keywords: `liquid chromatography` · `tandem mass spectrometry` · `ms/ms fragmentation` · `untargeted metabolomics` · `fragmentation strategy optimization` · `small molecule identification`

## Research Question
Can ViMMS simulate Top-N MS/MS acquisition on real beer samples and reproduce the fragmentation coverage observed in the original experimental data?

## Connected Finding
The Beer Top-N demo notebook demonstrates simulation of Top-N fragmentation strategy on Beer1pos mzML data by extracting chemicals from the real acquisition and running them through ViMMS with TopNController to compare simulated versus original fragmentation results.

## Task Description
Load the Beer1pos real mzML dataset, simulate it using ViMMS with TopNController, and compare the simulated output against the real acquisition to reproduce the reported Top-N fragmentation comparison.

## Inputs
- Beer1pos real mzML file from vimms-data repository (https://github.com/glasgowcompbio/vimms-data/raw/main/example_data.zip)

## Expected Outputs
- Simulated mzML file generated from Beer1pos chemicals using TopNController
- Comparison report with fragmentation coverage and intensity metrics between real and simulated Beer1pos acquisition

## Expected Output File

- `beer_topn_comparison_report.txt`

## Landmark Outputs

- `beer_chemicals_extracted.p`
- `beer_simulated.mzML`
- `beer_real_peaks.csv`
- `beer_simulated_peaks.csv`

## Tools
- VIMMS
- Python
- OpenMS

## Skills
- mzml-file-parsing-and-loading
- unknown-chemical-extraction-from-spectra
- mass-spectrometer-simulation-parameter-tuning
- retention-time-and-intensity-chromatogram-modeling
- fragmentation-strategy-comparison-across-datasets
- peak-detection-and-alignment-in-metabolomics

## Workflow Description
1. Download the Beer1pos mzML file from the vimms-data repository. 2. Extract unknown chemicals from the Beer1pos mzML using ChemicalMixtureFromMZML class to create a chemical list with known retention times and m/z values. 3. Set up an IndependentMassSpectrometer with the extracted chemicals in positive polarity mode. 4. Configure a TopNController with N=5, isolation_width=1, and appropriate intensity thresholds matching the real acquisition parameters. 5. Create an Environment with the mass spectrometer and controller, setting min_time=0 and max_time to match the real data acquisition window. 6. Run the simulation and write the simulated mzML output using Environment.write_mzML(). 7. Extract peaks from both real and simulated mzML files using OpenMS-based peak detection with consistent parameters. 8. Compare fragmentation coverage and intensity metrics between real and simulated datasets and generate a summary report.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/architecture_diagram.jpg` | figure | False |
| `figures/bipartite_matching.svg` | figure | False |
| `figures/logo.png` | figure | False |
| `figures/matching_workflow.svg` | figure | False |
| `figures/old_schematic.png` | figure | False |
| `figures/schematic.png` | figure | False |
| `figures/spectra.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting version history, bug fixes, or API changes for the ViMMS repository
- Specific TopNController parameter values (N, isolation_width, other tuning parameters) used in the Beer Top-N demo reported result
- Exact numerical reference values (fragmentation coverage %, number of matched compounds, retention time range) for the Beer Top-N demo comparison result to be reproduced
- Link or accession number for Beer1pos raw mzML dataset location within vimms-data or external repository

## Domain Knowledge
- Unknown chemicals extracted from mzML files represent detected peaks with elution time and intensity profiles; their chemical identities need not be known for fragmentation simulation, only their m/z and RT values.
- TopNController N parameter sets the number of most intense precursor ions selected for MS/MS fragmentation in each survey scan; N=5 is a standard Data-Dependent Acquisition (DDA) setting.
- Isolation width (typically 1 Da or m/z unit) defines the mass range around each precursor ion that is transmitted into the collision cell for fragmentation.
- Real versus simulated comparison requires consistent peak-picking thresholds and m/z tolerance (typically 1 ppm for MS1, 0.05 ppm for MS2) to fairly evaluate fragmentation coverage.
- Fragmentation metrics such as cumulative coverage (percentage of chemicals fragmented) and intensity preservation (ratio of simulated to real peak intensities) are standard measures of acquisition strategy fidelity.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Simulated mzML file generated from Beer1pos chemicals using TopNController, Comparison report with fragmentation coverage and intensity metrics between real and simulated Beer1pos acquisition.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Can ViMMS simulate Top-N MS/MS acquisition on real beer samples and reproduce the fragmentation coverage observed in the original experimental data?: 'loads an existing beer ('Beer1pos') data, runs it through the simulator and compares the simulated results to the original input data'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] The Beer Top-N demo notebook demonstrates simulation of Top-N fragmentation strategy on Beer1pos mzML data by extracting chemicals from the real acquisition and running them through ViMMS with TopNController to compare simulated versus original fragmentation results.: 'Extract chemicals from the previously downloaded beer mzML files using `ChemicalMixtureFromMZML` class. The results are a list of `UnknownChemical` objects for each input mzML file.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [results] Beer1pos real mzML file from vimms-data repository (https://github.com/glasgowcompbio/vimms-data/raw/main/example_data.zip): 'Download beer and urine .mzML files used as examples in the paper'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Simulated mzML file generated from Beer1pos chemicals using TopNController: 'The `Environment` class provides `write_mzML` to export the generated scans'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Comparison report with fragmentation coverage and intensity metrics between real and simulated Beer1pos acquisition: 'The report dictionary contains metrics such as the number of times each chemical was fragmented, cumulative coverage and intensity information'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] VIMMS: 'a flexible and modular framework designed to simulate fragmentation strategies'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Python: 'ViMMS is compatible with Python 3+'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] OpenMS: 'Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, bug fixes, or API changes for the ViMMS repository: '_No changelog found._'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] Specific TopNController parameter values (N, isolation_width, other tuning parameters) used in the Beer Top-N demo reported result: 'Source: github:glasgowcompbio__vimms'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] Exact numerical reference values (fragmentation coverage %, number of matched compounds, retention time range) for the Beer Top-N demo comparison result to be reproduced: 'Source: github:glasgowcompbio__vimms'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] Link or accession number for Beer1pos raw mzML dataset location within vimms-data or external repository: 'Source: github:glasgowcompbio__vimms'

## Evaluation Strategy
### Direct Checks
- verify file exists at github:glasgowcompbio__vimms (repository accessible)
- verify Beer1pos mzML dataset is retrievable from glasgowcompbio/vimms-data repository
- verify ViMMS package can be imported and TopNController class is accessible
- verify simulated mzML output file is generated with valid mzML format
- verify simulated mzML contains MS1 and MS2 scans in byte-for-byte valid XML structure
- verify comparison metrics (fragmentation coverage, peak matching) can be computed from both real and simulated mzML files using reported parameters (MS1 tolerance 1 ppm, MS2 tolerance 0.05 ppm, minimum 3 matching peaks)
- verify output comparison table or figure matches structure and numerical range of reported Beer Top-N demo result

### Expert Review
- assess whether simulated acquisition strategy (TopNController with N parameter) faithfully reproduces the selectivity and timing patterns of real Beer1pos instrument run
- assess whether comparison metrics (fragmentation coverage percentage, number of matched compounds) are consistent with metabolomics best practices and the paper's reported values
- assess biological plausibility: verify that matched metabolites and fragmentation patterns are chemically and biologically consistent with beer composition

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Download and load the Beer1pos real mzML file from the vimms-data repository.
2. Extract unknown chemical objects (m/z, retention time, intensity profiles) from the real mzML using ChemicalMixtureFromMZML.
3. Instantiate an IndependentMassSpectrometer with the extracted chemicals and positive polarity mode.
4. Configure a TopNController with N=5, isolation_width=1, and match the real acquisition intensity thresholds.
5. Run the simulation via Environment.run() and export the simulated mzML.
6. Apply consistent peak detection (OpenMS parameters) to both real and simulated mzML files.
7. Compute fragmentation coverage and intensity metrics and compare across datasets.
8. Validation: reproduce the reported Top-N fragmentation coverage and intensity comparison for Beer1pos from the demo notebook, confirming consistency of simulated versus real acquisition metrics.
9. References: source article (DOI: 10.1021/acs.analchem.0c03895)

## Workflow Ports

**Inputs:**

- `beer_real_mzml` — Beer1pos real mzML file ← `task_001/fullscan_mzml`

**Outputs:**

- `simulated_mzml` — Simulated mzML output from ViMMS
- `comparison_report` — Real vs. simulated fragmentation coverage and intensity metrics

**Used:** `urn:asb:port:task_001/fullscan_mzml`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:glasgowcompbio__vimms`
- **Synthesized at:** 2026-06-15T12:49:32+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
