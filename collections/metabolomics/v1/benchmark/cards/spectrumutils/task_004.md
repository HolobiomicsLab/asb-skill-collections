# SciTask Card: Reconstruct neutral-loss annotation to verify that neutral losses increase the fraction of interpreted peaks

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:16:56.758905+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_spectrumutils/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `information-extraction`, `benchmark-evaluation`
- DOI: `10.1021/acs.analchem.9b04884`
- GitHub: `bittremieuxlab/spectrum_utils`
- Input from: `task_002`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Techniques: `feature-detection`, `spectral-library-matching`, `quality-control`, `tandem-ms`

## Research Question
How does enabling neutral loss annotation in spectrum_utils.fragment_annotation affect the fraction of observed peaks that receive an interpretation?

## Connected Finding
spectrum_utils provides fragment annotation functionality using the ProForma 2.0 specification to interpret observed spectrum peaks, with the capability to enable or disable neutral loss annotation to modulate peak interpretation coverage.

## Task Description
Load a publicly deposited MS/MS spectrum via USI, annotate fragment ions using spectrum_utils with neutral loss disabled and enabled, compute the fraction of observed peaks receiving interpretation in each condition, and verify the increase matches reported results.

## Inputs
- Public MS/MS spectrum deposited in PRIDE/MassIVE repository (e.g., mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840)
- ProForma 2.0 peptide sequence string (e.g., 'WNQLQAFWGTGK' or with modifications)

## Expected Outputs
- Fraction of observed peaks annotated without neutral loss (numeric value between 0 and 1)
- Fraction of observed peaks annotated with neutral loss enabled (numeric value between 0 and 1)
- Comparison report showing increase in peak interpretation fraction when neutral losses are enabled

## Expected Output File

- `peak_annotation_comparison.csv`

## Landmark Outputs

- `spectrum_processed.pkl`
- `annotations_without_nl.json`
- `annotations_with_nl.json`
- `peak_counts.csv`

## Tools
- spectrum_utils
- Python

## Skills
- spectral-fragment-ion-annotation-with-proforma
- neutral-loss-peak-interpretation
- peptide-spectrum-matching-evaluation
- fragment-mass-tolerance-calibration
- peak-annotation-quantification-and-comparison

## Workflow Description
1. Retrieve spectrum from public repository using Universal Spectrum Identifier (USI) with spectrum_utils.MsmsSpectrum.from_usi(). 2. Set m/z range to 100–1400 using set_mz_range(). 3. Remove precursor peak using remove_precursor_peak() with 10 ppm fragment tolerance. 4. Filter low-intensity noise peaks using filter_intensity() with minimum intensity 0.05 and maximum 50 peaks. 5. Scale peak intensities by square root using scale_intensity('root'). 6. Annotate fragment ions using annotate_proforma() with ProForma peptide string, ion_types='aby', and neutral_losses disabled (default). 7. Count annotated peaks and calculate fraction of observed peaks with interpretation. 8. Repeat annotation step 6 with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} enabled. 9. Count annotated peaks in neutral-loss condition and recalculate fraction. 10. Compare fractions and verify increase against reported benchmark.

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
- No changelog found

## Domain Knowledge
- Neutral losses (NH₃ = −17.026549 Da, H₂O = −18.010565 Da) represent common post-translational modifications and peptide fragmentation artifacts that, when included in annotation workflows, increase the number of interpretable peaks in tandem mass spectra.
- Fragment ion annotation relies on matching observed m/z values against theoretical fragment masses within a specified tolerance window (typically 10 ppm or 0.05 Da); the fraction of peaks receiving interpretation is a key quality metric for peptide-spectrum match confidence.
- ProForma 2.0 is a machine-readable, standardized specification for peptidoform notation that integrates modification names (Unimod, PSI-MOD), controlled vocabularies, and delta masses, enabling unambiguous representation of modified peptides across tandem MS experiments.
- Ion types (a, b, c, x, y, z, internal m, immonium I) differ in fragmentation chemistry and frequency; the default annotation focuses on singly-charged b and y ions to reduce label clutter while maximizing peak coverage.
- USI (Universal Spectrum Identifier) is a standardized format for unambiguously retrieving individual tandem MS spectra from public proteomics repositories (PRIDE, MassIVE) without requiring local file downloads or format conversion.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does enabling neutral loss annotation in spectrum_utils.fragment_annotation affect the fraction of observed peaks that receive an interpretation?: 'Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] spectrum_utils provides fragment annotation functionality using the ProForma 2.0 specification to interpret observed spectrum peaks, with the capability to enable or disable neutral loss annotation to modulate peak interpretation coverage.: 'Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Public MS/MS spectrum deposited in PRIDE/MassIVE repository (e.g., mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840): 'Retrieve the spectrum by its USI.
usi = "mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840"'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] ProForma 2.0 peptide sequence string (e.g., 'WNQLQAFWGTGK' or with modifications): 'Annotate the spectrum with its ProForma string.
peptide = "EM[Oxidation]EVEES[Phospho]PEK"'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Fraction of observed peaks annotated without neutral loss (numeric value between 0 and 1): 'peaks that correspond to peptide fragments with a neutral loss are highlighted in the matching color'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Fraction of observed peaks annotated with neutral loss enabled (numeric value between 0 and 1): 'Neutral losses need to be specified by a concise label (preferably their molecular formula) and mass difference'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Comparison report showing increase in peak interpretation fraction when neutral losses are enabled: 'the same peptide--spectrum match without considering neutral losses is able to explain far fewer peaks'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] spectrum_utils: 'spectrum_utils supports several other ion types'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Python: 'import matplotlib.pyplot as plt
import spectrum_utils.plot as sup
import spectrum_utils.spectrum as sus'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists: mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840 is retrievable via USI mechanism
- script_runs: Python script instantiates spectrum_utils.fragment_annotation with neutral_loss parameter set to False
- script_runs: Python script instantiates spectrum_utils.fragment_annotation with neutral_loss parameter set to True
- output_matches_reference: fraction of peaks receiving interpretation (neutral_loss=False) computed and recorded as a single numeric value
- output_matches_reference: fraction of peaks receiving interpretation (neutral_loss=True) computed and recorded as a single numeric value
- value_in_range: difference between fractions (neutral_loss=True minus neutral_loss=False) is a non-negative number, robust to minor numerical precision differences

### Expert Review
- reported result for neutral loss annotation effect on peak interpretation fraction matches the article text or supplementary materials — requires domain knowledge to locate the specific claimed improvement and verify computation matches article methodology

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Retrieve public MS/MS spectrum via USI and load into spectrum_utils MsmsSpectrum object.
2. Apply standard spectrum preprocessing: m/z range filtering (100–1400), precursor peak removal (10 ppm tolerance), noise filtering (0.05 min intensity, max 50 peaks), and square-root intensity scaling.
3. Annotate fragment ions using ProForma peptide string with default ion types (a, b, y) and neutral losses disabled; count peaks receiving interpretation.
4. Re-annotate the same spectrum with common neutral losses (NH₃, H₂O) enabled; count peaks receiving interpretation.
5. Calculate peak annotation fractions for both conditions and compute the relative increase.
6. Validation: verify that peak interpretation fraction increase when neutral losses are enabled matches the order-of-magnitude improvement shown in the reported neutral loss example spectra.
7. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732)

## Workflow Ports

**Inputs:**

- `spectrum_usi` — Public MS/MS spectrum Universal Spectrum Identifier ← `task_002/annotation_report`
- `peptide_sequence` — ProForma 2.0 peptide sequence with optional modifications

**Outputs:**

- `fraction_without_nl` — Fraction of observed peaks annotated without neutral loss
- `fraction_with_nl` — Fraction of observed peaks annotated with neutral loss enabled
- `comparison_report` — Comparison report with increase in peak interpretation fraction

**Used:** `urn:asb:port:task_002/annotation_report`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bittremieux-lab__spectrum_utils`
- **Synthesized at:** 2026-06-16T07:23:50+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
