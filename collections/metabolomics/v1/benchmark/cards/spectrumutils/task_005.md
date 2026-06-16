# SciTask Card: Reproduce publication-quality spectrum plot using spectrum_utils.plot and Matplotlib

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:16:56.758905+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_spectrumutils/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `visualization`, `information-extraction`
- DOI: `10.1021/acs.analchem.9b04884`
- GitHub: `bittremieuxlab/spectrum_utils`
- Input from: `task_002`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Techniques: `feature-detection`, `spectral-library-matching`, `quality-control`, `tandem-ms`

## Research Question
Can spectrum_utils load a publicly deposited mass spectrometry spectrum via Universal Spectrum Identifier (USI) and annotate it with fragment ion types for visualization?

## Connected Finding
spectrum_utils provides capabilities for spectrum loading from online resources via USI and annotating observed spectrum fragments using the ProForma 2.0 specification, supporting both data retrieval and fragment annotation workflows.

## Task Description
Load a publicly deposited tandem mass spectrum via Universal Spectrum Identifier (USI), annotate fragment ions using ProForma 2.0 specification for b and y peptide ions, and render a publication-quality spectrum visualization as a PNG file.

## Inputs
- Universal Spectrum Identifier (USI) string for a public tandem MS spectrum (e.g., mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555)
- ProForma 2.0 peptide sequence string with optional modifications (e.g., VLHPLEGAVVIIFK or EM[Oxidation]EVEES[Phospho]PEK)
- Fragment ion mass tolerance value and mode (e.g., 10 ppm or 0.05 Da)

## Expected Outputs
- PNG image file containing the annotated mass spectrum with b and y ions highlighted and labeled

## Expected Output File

- `annotated_spectrum.png`

## Landmark Outputs

- `spectrum_object.pkl`
- `annotated_spectrum.png`

## Tools
- spectrum_utils
- Python
- matplotlib
- ProForma 2.0

## Skills
- spectral-peak-annotation-using-proforma
- fragment-ion-mass-matching
- peptidoform-representation-and-interpretation
- spectrum-visualization-and-figure-rendering
- usi-spectrum-retrieval-and-loading

## Workflow Description
1. Retrieve the spectrum from an online proteomics data resource using MsmsSpectrum.from_usi() with the provided USI accession. 2. Annotate the spectrum with a ProForma peptide string using annotate_proforma() method, specifying ion_types='by' to label b and y fragment ions and a fragment tolerance (e.g., 10 ppm). 3. Create a matplotlib figure and use spectrum_utils.plot.spectrum() to render the annotated spectrum with grid disabled and spine visibility adjusted. 4. Save the resulting figure as a PNG file with 300 dpi resolution and tight bounding box.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/annot_fmt.png` | figure | False |
| `figures/facet.png` | figure | False |
| `figures/ion_types.png` | figure | False |
| `figures/mass_errors.png` | figure | False |
| `figures/mirror.png` | figure | False |
| `figures/neutral_losses_1.png` | figure | False |
| `figures/neutral_losses_2.png` | figure | False |
| `figures/proforma_ast.png` | figure | False |
| `figures/proforma_ex1.png` | figure | False |
| `figures/proforma_ex2.png` | figure | False |
| `figures/proforma_ex3.png` | figure | False |
| `figures/quickstart.png` | figure | False |
| `figures/runtime.png` | figure | False |
| `figures/spectrum_utils.png` | figure | False |
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| massive | `MSV000082283` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283 | # Retrieve the spectrum by its USI.     usi = "mzspec:MSV000082283:f07074:scan:5475"     spectrum = sus.MsmsSpectrum.from_usi( |
| massive | `MSV000079960` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960 | as sus   peptide = "DLTDYLM[Oxidation]K" usi_top = "mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372" spectrum_top = sus.MsmsSpectrum. |
| massive | `MSV000080679` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679 | a(peptide, 0.5, "Da", ion_types="aby") usi_bottom = "mzspec:MSV000080679:j11962_C1orf144:scan:10671" spectrum_bottom = sus.MsmsSpect |
| pride | `PXD000561` | https://www.ebi.ac.uk/pride/archive/projects/PXD000561 | s sup import spectrum_utils.spectrum as sus   usi = "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555" peptide = |
| pride | `PXD014834` | https://www.ebi.ac.uk/pride/archive/projects/PXD014834 | s sup import spectrum_utils.spectrum as sus   usi = "mzspec:PXD014834:TCGA-AA-3518-01A-11_W_VU_20120915_A0218_3F_R_FR01:scan:8370 |
| pride | `PXD022531` | https://www.ebi.ac.uk/pride/archive/projects/PXD022531 | as sup import spectrum_utils.spectrum as sus  usi = "mzspec:PXD022531:j12541_C5orf38:scan:12368" peptide = "VAATLEILTLK/2" spectr |
| pride | `PXD004732` | https://www.ebi.ac.uk/pride/archive/projects/PXD004732 | s sup import spectrum_utils.spectrum as sus   usi = "mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840" |

## Missing Information
- No version or changelog information is available to confirm which version of spectrum_utils was used or what changes may have been made to the plotting and annotation API.

## Domain Knowledge
- ProForma 2.0 is a standardized notation for representing peptide sequences and peptidoforms (modified peptides) using controlled vocabularies such as Unimod and PSI-MOD; modifications can be specified by name, CV accession, or delta mass.
- Fragment ion types include primary peptide fragments (a, b, c, x, y, z ions) and internal fragments (m ions); by default spectrum_utils annotates b and y ions, which are the most commonly observed in tandem MS of peptides.
- USI (Universal Spectrum Identifier) is a standardized mechanism for retrieving spectra from public proteomics and metabolomics repositories (PXD, MSV, and GNPS datasets); the USI format includes dataset identifier, file name, and scan number.
- Fragment mass tolerance is typically specified in parts per million (ppm) for high-resolution mass spectrometers or in Daltons (Da) for lower-resolution instruments; common thresholds are 5–20 ppm for Orbitrap instruments.
- Spectrum visualization in publication-quality form requires normalization of intensities, removal of precursor and noise peaks, and application of intensity scaling (e.g., square-root scaling) to de-emphasize overly intense peaks.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Can spectrum_utils load a publicly deposited mass spectrometry spectrum via Universal Spectrum Identifier (USI) and annotate it with fragment ion types for visualization?: 'Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] spectrum_utils provides capabilities for spectrum loading from online resources via USI and annotating observed spectrum fragments using the ProForma 2.0 specification, supporting both data retrieval and fragment annotation workflows.: 'Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism. ... Annotating observed spectrum fragments using the ProForma 2.0'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Universal Spectrum Identifier (USI) string for a public tandem MS spectrum (e.g., mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555): 'usi = "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555"'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] ProForma 2.0 peptide sequence string with optional modifications (e.g., VLHPLEGAVVIIFK or EM[Oxidation]EVEES[Phospho]PEK): 'peptide = "VLHPLEGAVVIIFK"'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Fragment ion mass tolerance value and mode (e.g., 10 ppm or 0.05 Da): 'spectrum.annotate_proforma(peptide, 10, "ppm", ion_types="abyIm")'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] PNG image file containing the annotated mass spectrum with b and y ions highlighted and labeled: 'plt.savefig("proforma_ex1.png", bbox_inches="tight", dpi=300, transparent=True)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] spectrum_utils: 'spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Python: 'spectrum_utils is a Python package'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] matplotlib: 'fig, ax = plt.subplots(figsize=(12, 6))'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] ProForma 2.0: 'fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No version or changelog information is available to confirm which version of spectrum_utils was used or what changes may have been made to the plotting and annotation API.: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists: output PNG or SVG artifact from spectrum_utils.plot
- file_format_is: output artifact is valid PNG or SVG (byte-for-byte magic number check)
- script_runs: Python script successfully loads USI mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:1 using spectrum_utils
- script_runs: annotate_proforma method executes without exception when called with ion_types parameter including b and y ions
- output_matches_reference: rendered figure contains annotated b and y ion labels in the output artifact (robust to rendering engine variation in exact pixel placement)

### Expert Review
- visual inspection of rendered spectrum confirms b/y ion annotations are chemically plausible and positioned at correct m/z values
- expert assessment that annotated fragment ions follow ProForma 2.0 specification as claimed in package documentation

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Retrieve the spectrum from a public proteomics data repository using the USI accession.
2. Parse the ProForma peptide string and match fragment ion masses against observed m/z peaks within the specified tolerance.
3. Generate and label annotated peaks for b and y ion types.
4. Render a publication-quality spectrum plot with annotated fragments, appropriate axis labels, and styling (grid, spines).
5. Validation: Output PNG file exists, contains rendered spectrum with visible annotated peaks, and pixel dimensions are consistent with specified figure size.
6. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732)

## Workflow Ports

**Inputs:**

- `usi_identifier` — Universal Spectrum Identifier (USI) string ← `task_002/annotation_report`
- `peptide_proforma` — ProForma peptide sequence string
- `fragment_tolerance_config` — Fragment ion mass tolerance (value and mode)

**Outputs:**

- `annotated_spectrum_png` — PNG image of annotated spectrum

**Used:** `urn:asb:port:task_002/annotation_report`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bittremieux-lab__spectrum_utils`
- **Synthesized at:** 2026-06-16T07:23:50+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
