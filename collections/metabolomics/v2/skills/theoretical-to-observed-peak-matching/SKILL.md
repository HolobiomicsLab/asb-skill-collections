---
name: theoretical-to-observed-peak-matching
description: Use when you have a mass spectrum scan containing observed precursor ions (m/z, intensity pairs) in a narrow isolation window, a known peptide sequence with specified charge state and stable isotope labeling parameters (atom type, incorporation probability), and you need to determine which observed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - mzR
  - Raxport
  - R
  - ThermoRawFileParser
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum scans
- Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files
- Extract visualization information from `.FT2` files
- Aerith is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aerith_cq
    doi: 10.1021/acs.analchem.5c03207
    title: Aerith
  dedup_kept_from: coll_aerith_cq
schema_version: 0.2.0
---

# theoretical-to-observed-peak-matching

## Summary

Match observed precursor isotope peaks from mass spectrometry data to theoretical isotopic patterns computed for a peptide sequence at a specified charge state and isotopic labeling condition. This enables validation and quantification of stable isotope probing (SIP) enrichment in proteomics by aligning measured m/z and intensity to predicted isotopic envelopes.

## When to use

Apply this skill when you have a mass spectrum scan containing observed precursor ions (m/z, intensity pairs) in a narrow isolation window, a known peptide sequence with specified charge state and stable isotope labeling parameters (atom type, incorporation probability), and you need to determine which observed peaks correspond to the predicted isotopic distribution and quantify their SIP abundances. Typical scenarios: validating peptide identifications in labeled proteomics experiments, extracting accurate isotope ratio measurements from Orbitrap or IonTrap data, or assessing labeling completeness across a cohort of samples.

## When NOT to use

- Input is unlabeled (natural-abundance only) and you require only nominal mass matching—use simpler isotope pattern libraries instead of this inference-heavy matching.
- Isolation window is very wide (>>10 m/z) or contains overlapping precursor ions from multiple peptides—matching becomes ambiguous and the single-peptide assumption fails.
- The observed spectrum is heavily noisy or has severe baseline distortion; preprocessing (smoothing, baseline correction) must be applied before peak matching.

## Inputs

- Mass spectrum scan (FT1/FT2 file, mzML, or MGF format)
- Observed precursor m/z array and corresponding intensity array
- Peptide sequence (string, amino acid codes)
- Charge state (positive integer, e.g., +3)
- Isotope labeling specification: atom type (string, e.g., 'C13'), incorporation probability (0.0–1.0)
- Isolation window parameters: center m/z (float), width (float, typically ±2.0 Da)

## Outputs

- ExpectedPrecursorIons table with columns: m/z (float), intensity (float), charge (int), matchedIndices (vector of matched peak indices), SIPabundances (float, fractional isotope ratio)

## How to apply

Load the mass spectrum scan (e.g., FT1/FT2 files via Raxport or mzML via mzR) and extract the observed m/z range within the isolation window (center ± width, e.g., 880–890 m/z for isoCenter 886.65 and isoWidth 4.0). Call annotatePrecursor with the peptide sequence, charge state (+3 in the example), isotope atom type (e.g., C13), incorporation probability (e.g., 0.0107 for ~1% natural abundance), and isolation window coordinates. The function computes the theoretical isotopic peak envelope using sequential convolution, matching observed ions to predicted peaks by m/z proximity within the window. Calculate stable isotope probing (SIP) abundances for each matched peak based on the isotopic enrichment model. Validate that matched peak intensities and m/z differences are consistent with theoretical isotopic spacing (typically ~1 Da for +3 charge = ~0.33 m/z) and that the sum of matched peak intensities is physically plausible (e.g., not exceeding scan saturation limits). Return an ExpectedPrecursorIons table with m/z, intensity, charge, matchedIndices, and SIPabundances columns for downstream reporting or visualization.

## Related tools

- **Aerith** (R package hosting the annotatePrecursor function; reads spectrum files, computes theoretical isotopic envelopes via sequential convolution, and performs PSM scoring and visualization for SIP experiments) — https://github.com/xyz1396/Aerith
- **mzR** (Parses mzML and MGF spectrum files and extracts scan data (m/z, intensity arrays) for annotatePrecursor input) — https://bioconductor.org/packages/mzR
- **Raxport** (Converts Thermo RAW mass spectrometer files to FT1/FT2 format; enables extraction of precursor scans with charge information (for Orbitrap data)) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Alternative cross-platform tool to convert RAW files to mzML or MGF for input to mzR and Aerith) — https://github.com/CompOmics/ThermoRawFileParser

## Examples

```
annotatePrecursor(observedMz = c(886.65, 887.32, 887.99), observedIntensity = c(100, 80, 40), peptideSeq = 'HSQVFSTAEDNQSAVTIHVLQGER', charge = 3, isotopeAtom = 'C13', incorporationProb = 0.0107, isoCenter = 886.65, isoWidth = 4.0)
```

## Evaluation signals

- Matched peak m/z differences from median are ≤0.01 m/z (consistent with instrument mass accuracy at observed charge), suggesting correct isotopic spacing resolution.
- SIPabundances are bounded in [0, 1] and sum across matched peaks to approximately the expected total isotope ratio for the labeling model (e.g., ~0.01 for 1% C13 natural abundance); outliers indicate model-fit failure.
- MatchedIndices are monotonically increasing and reference valid positions within the observed spectrum; no duplicate or out-of-bounds indices.
- ExpectedPrecursorIons table is non-empty (at least the monoisotopic peak is matched) and contains no NaN or Inf values in numeric columns.
- Visual inspection: overlay of matched observed peaks against theoretical isotopic envelope shows good peak-by-peak alignment; large unexplained observed peaks suggest contamination or isotope pattern misspecification.

## Limitations

- Assumes a single peptide precursor per isolation window; co-isolated peptides will cause incorrect or ambiguous matches.
- Isotope incorporation probability is assumed uniform across all atoms of the specified type; heterogeneous labeling is not modeled.
- Depends critically on accurate charge state input; incorrect charge will shift predicted m/z by orders of magnitude relative to observed data.
- Monte Carlo fine-structure simulation (for high-resolution isotope patterns) has inherent stochasticity; reproducibility may vary with random seed.
- Performance degrades with very low precursor signal-to-noise ratio (SNR << 3) where peak detection is unreliable.

## Evidence

- [other] annotatePrecursor accepts observed precursor mass, probability, and charge along with peptide sequence, charge state, isotope atom type, incorporation probability, isolation window center and width to produce a table of ExpectedPrecursorIons: "annotatePrecursor accepts observed precursor mass, probability, and charge along with peptide sequence, charge state, isotope atom type, incorporation probability, isolation window center and width"
- [other] Call annotatePrecursor with the peptide sequence HSQVFSTAEDNQSAVTIHVLQGER, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak envelope using sequential convolution: "Call annotatePrecursor with the peptide sequence HSQVFSTAEDNQSAVTIHVLQGER, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak"
- [abstract] sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites to accurately generate isotopic distributions: "sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [intro] Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic"
- [other] Calculate SIP (stable isotope probing) abundances for each matched peak based on the isotopic enrichment model: "Calculate SIP (stable isotope probing) abundances for each matched peak based on the isotopic enrichment model"
- [intro] Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files: "Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files"
