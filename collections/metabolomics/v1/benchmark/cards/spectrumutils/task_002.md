# SciTask Card: Reproduce fragment annotation of a spectrum using ProForma 2.0 peptidoform notation

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:16:56.758905+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_spectrumutils/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- DOI: `10.1021/acs.analchem.9b04884`
- GitHub: `bittremieuxlab/spectrum_utils`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Techniques: `feature-detection`, `spectral-library-matching`, `quality-control`, `tandem-ms`

## Research Question
Does spectrum_utils.fragment_annotation correctly annotate b and y ions for a given ProForma 2.0 peptidoform string when applied to a publicly deposited spectrum?

## Connected Finding
spectrum_utils provides functionality to annotate observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms, enabling ion type annotation.

## Task Description
Annotate b and y fragment ions in a publicly deposited tandem mass spectrum using spectrum_utils' ProForma 2.0 parser, then verify that annotated peak m/z values and ion types match expected fragment assignments.

## Inputs
- A ProForma 2.0 peptidoform string specifying sequence and modifications (e.g., 'DLTDYLM[Oxidation]K' or 'EM[Oxidation]EVEES[Phospho]PEK')
- A tandem mass spectrum as a public USI accession or mzspec resource (e.g., mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372)
- Fragment ion mass tolerance and tolerance mode (e.g., 10 ppm or 0.5 Da)

## Expected Outputs
- A structured annotation report listing all matched b and y ion peaks with their assigned ion type, charge state, theoretical m/z, observed m/z, and mass error
- A validation table or JSON structure confirming that each annotated peak's m/z and ion type match expected values within the tolerance window

## Expected Output File

- `fragment_annotation_report.json`

## Landmark Outputs

- `spectrum_metadata.json`
- `theoretical_fragments.csv`
- `annotated_peaks.json`

## Tools
- spectrum_utils
- Python
- ProForma 2.0
- Unimod

## Skills
- proforma-2-0-peptidoform-parsing
- fragment-ion-annotation-matching
- mass-error-calculation-and-validation
- ion-type-assignment-verification
- spectrum-peak-to-fragment-mapping
- modification-notation-interpretation

## Workflow Description
1. Retrieve the mass spectrum from a public proteomics data repository using its Universal Spectrum Identifier (USI), e.g. mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372. 2. Parse the ProForma 2.0 peptidoform string (e.g. DLTDYLM[Oxidation]K) using spectrum_utils.proforma to extract the peptide sequence and modification positions. 3. Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks within the specified tolerance. 4. Iterate through annotated peaks and validate that each peak's assigned ion_type ('b' or 'y'), charge state, and m/z deviation from theoretical mass are correct and consistent with the input parameters.

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
- No changelog found.

## Domain Knowledge
- ProForma 2.0 is a standardized notation for representing peptide sequences and modifications using controlled vocabularies (Unimod, PSI-MOD) and allows modifications to be specified by name, CV accession, or delta mass.
- b and y ions are the primary peptide fragments routinely observed in tandem mass spectra; b ions contain the N-terminus while y ions contain the C-terminus.
- Fragment ion mass tolerance (typically 5–20 ppm for high-resolution or 0.02–0.1 Da for low-resolution instruments) determines the matching window within which an observed peak is considered evidence for a theoretical fragment.
- The Universal Spectrum Identifier (USI) mechanism allows computational retrieval of public spectra from distributed proteomics repositories without manual download.
- Internal spectrum_utils representation uses an abstract syntax tree derived from a formal grammar to robustly parse ProForma strings and handle all optional extensions including cross-linking, glycans, and chemical formulas.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does spectrum_utils.fragment_annotation correctly annotate b and y ions for a given ProForma 2.0 peptidoform string when applied to a publicly deposited spectrum?: 'Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] spectrum_utils provides functionality to annotate observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms, enabling ion type annotation.: 'Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] A ProForma 2.0 peptidoform string specifying sequence and modifications (e.g., 'DLTDYLM[Oxidation]K' or 'EM[Oxidation]EVEES[Phospho]PEK'): 'fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] A tandem mass spectrum as a public USI accession or mzspec resource (e.g., mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372): 'usi = "mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372"'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Fragment ion mass tolerance and tolerance mode (e.g., 10 ppm or 0.5 Da): 'fragment_tol_mass, fragment_tol_mode = 10, "ppm"'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] A structured annotation report listing all matched b and y ion peaks with their assigned ion type, charge state, theoretical m/z, observed m/z, and mass error: 'Fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] A validation table or JSON structure confirming that each annotated peak's m/z and ion type match expected values within the tolerance window: 'spectrum_utils uniquely supports the _full_ ProForma 2.0 specification'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] spectrum_utils: 'fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Python: 'spectrum = sus.MsmsSpectrum.from_usi(usi)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] ProForma 2.0: 'Modifications are defined by controlled vocabularies (CVs), including [Unimod](https://www.unimod.org/)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] Unimod: 'Specify modifications by their name: `EM[Oxidation]EVEES[Phospho]PEK`'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found.: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists at public accession mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372
- script_runs: Python script that imports spectrum_utils.fragment_annotation, loads the spectrum via USI, calls annotate_proforma() with a valid ProForma 2.0 peptidoform string (default ion_types='by'), and returns annotated peaks
- output_matches_reference: annotated peak m/z values and ion type assignments (b or y) are consistent with theoretical fragment masses calculated from the ProForma peptidoform string, within specified fragment tolerance (no canonical answer — tolerance depends on instrument calibration and user specification)
- field_present: each annotated peak record contains at least 'mz', 'intensity', and 'ion_type' fields
- value_in_range: all annotated peak m/z values fall within the valid mass range for the given precursor and peptide sequence

### Expert Review
- verify that ProForma 2.0 specification parsing correctly handles any post-translational modifications (PTMs) present in the input peptidoform string, including Unimod references
- verify that b and y ion peak assignments are chemically plausible given the peptide sequence and spectrum properties (e.g., no spurious assignments at impossible neutral losses)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load the target spectrum from a public USI-indexed repository using MsmsSpectrum.from_usi().
2. Parse the ProForma 2.0 string to extract sequence, modification sites, and modification types using the internal formal grammar and abstract syntax tree.
3. Compute theoretical m/z values for all b and y ions from the annotated peptide.
4. Match observed spectrum peaks to theoretical fragments within the specified mass tolerance (default: 10 ppm or 0.5 Da).
5. Assign ion type ('b' or 'y'), charge state, and mass error to each matched peak.
6. Validation: confirm that all returned annotations have m/z values within the input tolerance and ion types are correctly labeled as 'b' or 'y'.
7. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732)

## Workflow Ports

**Inputs:**

- `proforma_string` — ProForma 2.0 peptidoform string ← `task_001/filtered_spectrum`
- `spectrum_usi` — Mass spectrum USI accession
- `fragment_tolerance` — Fragment ion mass tolerance (mass + mode)

**Outputs:**

- `annotation_report` — Structured fragment ion annotation report with ion types and mass errors
- `validation_result` — Validation table confirming peak m/z and ion type correctness

**Used:** `urn:asb:port:task_001/filtered_spectrum`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bittremieux-lab__spectrum_utils`
- **Synthesized at:** 2026-06-16T07:23:50+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
