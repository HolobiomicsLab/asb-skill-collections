---
name: high-resolution-mass-accuracy-analysis
description: "High-resolution mass accuracy analysis applies sub-ppm mass tolerance thresholds and mass defect filtering to prioritize metabolite features from LC–HRMS data and constrain molecular formula assignments in xenobiotic screening. This skill combines instrumental mass accuracy monitoring, mass defect shift filtering, and formula validation to distinguish true metabolites from background noise and matrix artifacts."
when_to_use_negative: |
  - "Input data already contains curated, reference-matched metabolite identifications from a spectral library (skill would be redundant)"
  - "Mass accuracy of the instrument is unknown or unstable (>5 ppm drift observed); recalibrate before applying ±8 ppm tolerance thresholds"
  - "Parent compound structure or elemental composition is unknown or ambiguous (GenForm formula constraints cannot be properly defined)"
edam_operation: "http://edamontology.org/operation_3632"
edam_topics: |
  - "http://edamontology.org/topic_0218"
  - "http://edamontology.org/topic_3520"
tools: |
  - name: "XCMS"
  role: "Feature detection, alignment, and retention time correction prior to mass accuracy filtering"
  - name: "CAMERA"
  role: "Isotope, adduct, and neutral-loss annotation; componentization of features before mass defect filtering"
  - name: "mzR"
  role: "Extraction of MS2 spectra corresponding to prioritized metabolite features from data-dependent MS2 acquisition"
  - name: "GenForm"
  role: "Command-line molecular formula assignment from MS1 m/z and MS2 spectra, with elemental composition constraints derived from parent formula"
  - name: "OrgMassSpecR"
  role: "Calculation of dot-product similarity scores (SpectrumSimilarity function) to assess MS2 spectral quality and confidence in formula assignment"
  - name: "Sirius"
  role: "In silico fragmentation and molecular fingerprint prediction for structure elucidation when fragmentation patterns are complex or ambiguous"
  - name: "ProteoWizard"
  role: "Conversion of raw vendor mass spectra to mzML format and centroiding before feature detection"
  - name: "incubatoR"
  role: "R workflow wrapper implementing automated LC–HRMS data processing including mass defect filtering, feature prioritization, and GenForm integration"
  repo: "https://github.com/chufz/incubatoR"
provenance: |
  source_task_ids:
  - task_004
  source_papers:
  - doi: "10.1021/acs.analchem.1c00972"
  title: "Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing"
schema_version: "0.2.0"
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/high-resolution-mass-accuracy-analysis@sha256:fc610fed99c9b7d4dc5e0d14760ec32926d5fd3336a3ba0893b86bdcb0c11fce
---

# high-resolution-mass-accuracy-analysis

## Summary

High-resolution mass accuracy analysis applies sub-ppm mass tolerance thresholds and mass defect filtering to prioritize metabolite features from LC–HRMS data and constrain molecular formula assignments in xenobiotic screening. This skill combines instrumental mass accuracy monitoring, mass defect shift filtering, and formula validation to distinguish true metabolites from background noise and matrix artifacts.

## When to use

Apply this skill when analyzing LC–HRMS data for unknown metabolite features and you need to reduce false positives by enforcing mass accuracy constraints before molecular formula assignment. Specifically: (1) after feature detection and statistical filtering, when thousands of candidate peaks remain; (2) when instrumental mass accuracy is characterized and stable (e.g., <2 ppm observed); (3) when the parent xenobiotic structure and elemental composition are known; (4) to filter features whose mass shift relative to the parent compound exceeds biochemically plausible bounds (e.g., mass defect ±100 to +50 mmu).

## When NOT to use

- Input data already contains curated, reference-matched metabolite identifications from a spectral library (skill would be redundant)
- Mass accuracy of the instrument is unknown or unstable (>5 ppm drift observed); recalibrate before applying ±8 ppm tolerance thresholds
- Parent compound structure or elemental composition is unknown or ambiguous (GenForm formula constraints cannot be properly defined)

## Inputs

- LC–HRMS feature table (XCMS + CAMERA output: peaklist.tsv with m/z, retention time, and intensity across samples)
- Statistical test results (fold-change and p-value for incubated vs. control/blank groups)
- Parent pesticide exact mass and molecular formula
- Data-dependent MS2 spectra (mzML format, extracted via mzR)
- Internal standard mass accuracy measurements (mass error in ppm for spiked standards across sequence)

## Outputs

- Mass-defect-filtered feature list (subset of input peaklist passing −100 to +50 mmu and +50 u thresholds)
- Molecular formula assignments from GenForm (one formula per feature, or flagged as ambiguous)
- Cleaned MS2 spectra (fragments explicable by assigned formula only)
- Spectral quality report (dot-product similarity scores between experimental and reference spectra via OrgMassSpecR)

## How to apply

First, establish a mass accuracy baseline by monitoring internal standards across the analysis sequence to verify instrumental stability (target: <2 ppm, as reported in QA/QC). Second, apply mass defect filtering by calculating the shift between each feature's exact mass and the parent compound mass, then remove features with defect shifts <−100 mmu (lower cutoff) or >+50 mmu (upper cutoff), retaining only features within the biochemically plausible range for Phase I/II transformations. Third, remove features with m/z >+50 u above the parent compound, as these are unlikely single-step metabolites and more consistent with conjugation artifacts. Fourth, pass the filtered feature list to GenForm with constrained elemental composition rules derived from the parent pesticide formula (e.g., C 0−X_C, H 0−∞, N 0−X_N, O 0−(X_O +3), etc.), using MS1 mass at ±8 ppm tolerance and MS2 fragments at ±8 ppm acceptance and ±15 ppm rejection thresholds. Finally, validate assigned formulas by checking that all major MS2 fragment peaks can be explained by the proposed molecular structure; remove features for which the MS2 fragmentation pattern is inconsistent with the formula.

## Related tools

- **XCMS** (Feature detection, alignment, and retention time correction prior to mass accuracy filtering)
- **CAMERA** (Isotope, adduct, and neutral-loss annotation; componentization of features before mass defect filtering)
- **mzR** (Extraction of MS2 spectra corresponding to prioritized metabolite features from data-dependent MS2 acquisition)
- **GenForm** (Command-line molecular formula assignment from MS1 m/z and MS2 spectra, with elemental composition constraints derived from parent formula)
- **OrgMassSpecR** (Calculation of dot-product similarity scores (SpectrumSimilarity function) to assess MS2 spectral quality and confidence in formula assignment)
- **Sirius** (In silico fragmentation and molecular fingerprint prediction for structure elucidation when fragmentation patterns are complex or ambiguous)
- **ProteoWizard** (Conversion of raw vendor mass spectra to mzML format and centroiding before feature detection)
- **incubatoR** (R workflow wrapper implementing automated LC–HRMS data processing including mass defect filtering, feature prioritization, and GenForm integration) — https://github.com/chufz/incubatoR

## Evaluation signals

- Mass accuracy of internal standards remains <2 ppm across the entire analysis sequence (confirms stable instrument calibration); median retention time shift <0.3 sec (negative mode) and <0.7 sec (positive mode)
- Mass defect filtering reduces feature count by 60–70% (consistent with reported reduction after blank subtraction and isotope/adduct removal); remaining features cluster within −100 to +50 mmu band relative to parent mass
- GenForm successfully assigns unambiguous molecular formulas to ≥80% of filtered features (reported: 91 unambiguous formulas across 121 total prioritized features for 22 pesticides)
- MS2 spectra cleaned by GenForm show ≥60% of major peaks explicable by assigned formula; dot-product similarity scores between experimental and reference spectra indicate high spectral quality (threshold: >0.7 recommended, per OrgMassSpecR implementation)
- Identified metabolites match known Phase I/II biotransformation pathways (oxidation, reduction, hydroxylation, conjugation) for the parent compound; detected metabolites consistent with literature or in silico prediction tools (e.g., BioTransformer) for ≥60% of studied compounds

## Limitations

- Mass defect filtering thresholds (−100 to +50 mmu) are optimized for Phase I/II single-step transformations and may not detect rare multi-step or rearrangement metabolites; some predicted metabolites may not be detected due to low ionization efficiency or loss during sample extraction/cleanup
- GenForm formula assignment depends critically on MS2 spectral quality and signal-to-noise ratio; ambiguous or weak fragmentation patterns (e.g., for fipronil with only one major metabolite detected vs. six reported in literature) limit unambiguous formula assignment
- The workflow assumes parent pesticide structure and elemental composition are known; applicability to novel or un-registered xenobiotics is limited without prior characterization
- Relative standard deviation in metabolite signal intensity across replicates (21–23%) is partly attributable to matrix effects from human liver extract in the incubation assay, which can inflate fold-change thresholds and potentially mask weak metabolites
- S9 liver incubation does not cover all potential metabolic routes (e.g., reduction, consecutive hydroxylations, or breaking of weak bonds in molecules); comparison with literature and prediction tools showed only partial overlap, indicating the skill captures only a subset of in vivo metabolites

## Evidence

- [methods] Mass defect filtering to constrain metabolite detection: "For mass defect filtering, features with a mass defect shift of <−100 and >+50 mmu were removed."
- [supplementary] Mass accuracy monitoring and tolerance specification: "Mass accuracy was measured to be within < 2 ppm, while the retention time shift for the internal standards was observed with a median standard deviation of 0.3 sec for negative (maximum deviation of"
- [supplementary] GenForm formula assignment with MS accuracy thresholds: "GenForm intensity weighting wi sqrt MS1 accuracy ppm 8 acceptance of MS2 peak acc 8 rejection of MS2 peak rej 15"
- [methods] Molecular formula calculation workflow applied to filtered features: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides."
- [methods] MS2 spectrum extraction and validation for filtered features: "all spectra corresponding to the metabolite features were extracted from the data-dependent MS2 acquisition using mzR.32"
- [methods] Mass difference filtering to remove unlikely transformations: "Features with an m/z value >+50 mu to the parent pesticide were removed since they are more likely to occur from conjugation"
- [methods] Elemental composition constraints for GenForm molecular formula assignment: "constraining elemental compositions based on parent pesticide formula (C 0−X C H 0−∞ N 0−X N O 0−(X O +3) P 0−X P S 0−X S F 0−X F Cl 0−X Cl Br 0−X Br)"
- [methods] Spectral quality assessment via dot-product similarity: "Dot-product scores were calculated using the function SpectrumSimilarity in OrgMassSpecR.34"
- [methods] Workflow validation against literature and predicted metabolites: "About two-thirds of the in vitro-metabolites were reported in the literature or predicted"
- [readme] incubatoR automated workflow implementation: "Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering and"
