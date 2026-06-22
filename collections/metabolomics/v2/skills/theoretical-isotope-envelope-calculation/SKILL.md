---
name: theoretical-isotope-envelope-calculation
description: Use when when processing mass spectrometry data from stable isotope probing (SIP) experiments where peptides contain known levels of heavy isotope incorporation (13C, 15N, 2H, 18O), and you need to annotate observed MS2 peaks by matching them to theoretical B and Y ion fragments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Aerith
  - Raxport
  - R
  - ThermoRawFileParser
  - mzR
  - MSnbase
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum scans
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03207
  all_source_dois:
  - 10.1021/acs.analchem.5c03207
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# theoretical-isotope-envelope-calculation

## Summary

Compute theoretical isotopic peak envelopes for peptide precursors and their B/Y fragment ions under specified stable isotope labeling conditions. This skill enables prediction of expected m/z and intensity patterns for heavily labeled peptides (e.g., 52% 13C incorporation), which are then matched against observed MS2 peaks to validate and annotate peptide-spectrum matches.

## When to use

When processing mass spectrometry data from stable isotope probing (SIP) experiments where peptides contain known levels of heavy isotope incorporation (13C, 15N, 2H, 18O), and you need to annotate observed MS2 peaks by matching them to theoretical B and Y ion fragments. This skill is essential when peak matching cannot rely on nominal mass alone and isotopic fine structure must be explicitly modeled—for example, when a 52% 13C-labeled peptide (HYAHVDCPGHADYVK) produces complex multiplet envelopes that require sequential convolution to predict accurately.

## When NOT to use

- Input peptides are unlabeled or naturally abundant isotope composition is sufficient—use standard (unlabeled) peptide mass prediction instead.
- Observed peaks have already been manually validated and annotated by expert inspection; recalculating envelopes is redundant.
- Incorporation probability is unknown or highly heterogeneous across the sample; this skill assumes a fixed, homogeneous labeling level per peptide.

## Inputs

- Peptide sequence (character string, e.g., 'HYAHVDCPGHADYVK')
- Stable isotope label specification: isotope type (C13, N15, H2, O18) and incorporation probability (0–1, e.g., 0.52)
- Precursor charge state (integer, typically +1 or +2)
- Observed MS2 peak data: m/z (numeric vector), intensity (numeric vector), charge state per peak
- Precursor m/z (numeric)
- Isolation window width (numeric, e.g., 5.0 Da for mass range of precursor extraction)

## Outputs

- ExpectedBYions table: theoretical m/z and intensity for each B and Y ion, including isotopic envelope
- matchedIndices vector: positions in the observed peak list that matched each theoretical fragment (non-negative values indicate successful match)
- PSM annotation result: validated fragment assignments with residue-position counts reflecting heavy isotope labels per position

## How to apply

Define the peptide sequence, charge state(s), isotope type (e.g., C13), and incorporation probability (e.g., 0.52 for 52% labeling). Use Aerith's sequential convolution algorithm to calculate theoretical isotopic peak envelopes for the intact precursor and for all theoretical B and Y ion fragments. For each fragment, convolve the elemental composition (C, H, N, O, S) with the specified isotope probability distribution to generate the expected multiplet envelope at each fragment's theoretical m/z. Pass these envelopes, together with observed m/z, intensity, and charge information, to the annotatePSM scoring function, which matches observed peaks to theoretical envelopes and returns matchedIndices indicating successful annotations. Filter results to non-negative matchedIndices to extract validated fragment matches. The accuracy of this step depends on correct specification of incorporation probability and proper handling of charge states (both precursor and fragment).

## Related tools

- **Aerith** (Primary R package implementing sequential convolution for peptide fragments and Monte Carlo simulation for fine isotopic structures; provides annotatePSM function to score and match observed peaks to theoretical B/Y ion envelopes) — https://github.com/xyz1396/Aerith
- **Raxport** (Extracts visualization information from .FT2 files (Thermo RAW format), enabling input of observed MS2 peak data into Aerith) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Converts Thermo RAW files to mzML, MGF, and other open formats; provides alternative input pathway for observed MS2 spectra) — https://github.com/CompOmics/ThermoRawFileParser
- **mzR** (Bioconductor package integrated with Aerith for parsing mzML and MGF files containing observed spectra)
- **MSnbase** (Bioconductor package integrated with Aerith for parsing pepXML and related metadata files)

## Examples

```
# In R using Aerith:
library(Aerith)
# Define observed MS2 peaks from scan 2596 (m/z, intensity, charge)
observed_peaks <- data.frame(mz = c(175.1, 188.2, 205.3), intensity = c(1000, 800, 600), charge = c(1, 1, 1))
# Calculate theoretical envelopes for HYAHVDCPGHADYVK with 52% C13 labeling
result <- annotatePSM(observed_mz = observed_peaks$mz, observed_intensity = observed_peaks$intensity, observed_charge = observed_peaks$charge, peptide_seq = 'HYAHVDCPGHADYVK', precursor_mz = 945.5, precursor_charge = 2, isotope = 'C13', incorporation_prob = 0.52, isolation_window = 5.0)
# Extract matched fragments (non-negative matchedIndices)
matched <- result$expected_by_ions[result$expected_by_ions$matchedIndices >= 0, ]
```

## Evaluation signals

- All theoretical B and Y ion m/z values fall within the observed m/z range of the MS2 spectrum (after accounting for instrument resolution and isolation window).
- matchedIndices are non-negative integers corresponding to valid observed peak indices; negative values indicate unmatched theoretical fragments.
- Matched observed peaks have intensity and charge consistent with expectations for fragments derived from the specified precursor charge and labeling level.
- Residue-position counts (heavy isotope labels per position in the peptide backbone) are monotonically increasing from N-terminus to C-terminus or follow the expected distribution under the specified 52% incorporation probability.
- Comparison of matched fragment ions to the original peptide sequence confirms that matched B and Y ions span non-overlapping, complementary portions of the sequence.

## Limitations

- Sequential convolution algorithm assumes constant, homogeneous incorporation probability across all positions in the peptide; heterogeneous labeling patterns (e.g., selective labeling of specific residues) are not modeled.
- Monte Carlo and FFT-based methods for fine isotopic structure are computationally efficient but introduce approximation error; exact closed-form calculations become intractable for very long peptides or high incorporation probabilities.
- Charge state determination from observed peaks is instrument-dependent; Raxport-processed .FT2 files include charge information only from Orbitrap instruments, not IonTrap. If charge is missing or incorrect, peak-to-fragment matching will fail.
- Peak matching sensitivity depends on correct specification of precursor m/z and isolation window width; misspecification can exclude valid observed peaks or include spurious noise peaks.
- Heavy isotope incorporation may produce complex multiplet envelopes that overlap with natural-abundance isotope peaks of non-labeled peptides or contaminants; resolution and mass accuracy of the instrument determine whether such overlaps can be resolved.

## Evidence

- [abstract] sequential convolution for peptide fragments to accurately generate isotopic distributions: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [other] annotatePSM accepts observed peak data and isotope label parameters to return matched fragments: "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence (HYAHVDCPGHADYVK), charge states (1:2), isotope atom (C13), incorporation probability (0.52), precursor m/z, and"
- [intro] Calculate theoretical isotopic peak envelope of peptide precursors and their B Y ions: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [intro] Aerith supports flexible specification of isotopic abundances for SIP experiments: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment"
- [readme] Raxport extracts scans from .FT2 files generated by ThermoFisher instruments: "Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans. However, the generated `.FT1` or `.FT2`"
