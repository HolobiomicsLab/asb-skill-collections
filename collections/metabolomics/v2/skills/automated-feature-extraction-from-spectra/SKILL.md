---
name: automated-feature-extraction-from-spectra
description: Use when when you have raw or processed direct-infusion MS (DI-MS) or
  ASAP-MS spectra as mz/intensity pairs and need to rapidly identify salient peaks
  for species authentication, sample scoring, or comparative profiling without manual
  inspection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
  techniques:
  - LC-MS
  - direct-infusion-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
- supports data from multiple instruments, including DI-MS and ASAP-MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# automated-feature-extraction-from-spectra

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automatic identification and annotation of peaks of interest from raw or processed mass spectrometry spectra using algorithmic detection. This skill extracts m/z and intensity features with confidence scoring, enabling downstream species discrimination and sample characterization without manual peak curation.

## When to use

When you have raw or processed direct-infusion MS (DI-MS) or ASAP-MS spectra as mz/intensity pairs and need to rapidly identify salient peaks for species authentication, sample scoring, or comparative profiling without manual inspection. Particularly useful in high-throughput contexts where sample volume precludes manual curation and intuitive visual outputs are required for validation.

## When NOT to use

- Input data are already curated peak tables or feature matrices — the skill duplicates work already performed.
- Manual peak assignment is a regulatory or method validation requirement — automatic identification may not satisfy audit trails or reproducibility mandates.
- Spectrum data are from chromatographic methods (LC-MS) where retention time and peak shape are critical discriminators not captured by mz/intensity pairs alone.

## Inputs

- raw mass spectrometry spectrum data (mz/intensity pairs)
- processed MS spectrum data (mz/intensity pairs)
- input file in format supported by DI-MS or ASAP-MS instruments

## Outputs

- structured peak table with peak identifiers, m/z values, intensity values, and confidence scores
- annotated peak list with labels assigned by intensity ranking
- visual peak representations for intuitive validation

## How to apply

Load raw or processed MS spectrum data as mz/intensity pairs from the input file into RapidMass. Apply the platform's automatic peak detection algorithm to identify peaks of interest based on intensity ranking and m/z value clustering. The algorithm assigns labels and annotations to each detected peak, generating confidence scores that reflect detection reliability. Aggregate results into a structured output table containing peak identifiers, m/z values, intensity measurements, and confidence scores. Validate results by examining the visual outputs and comparing detected peaks against known reference patterns or database entries to confirm biological relevance and absence of noise artifacts.

## Related tools

- **RapidMass** (executes automatic peak detection algorithm and generates confidence-scored peak annotations from mz/intensity data) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (source instrument format supported for raw or processed spectrum input)
- **ASAP-MS** (source instrument format supported for raw or processed spectrum input)

## Evaluation signals

- Detected peaks are ranked consistently by intensity; no negative or NaN values in confidence scores.
- Peak m/z values fall within expected mass range for the analyte and ion mode (positive/negative); isotope peaks are correctly clustered.
- Visual output shows clear separation between high-confidence peaks and noise baseline; intensity distribution matches known reference spectra for the sample species.
- Annotated peak table has no duplicate m/z entries (within instrument resolution tolerance) and confidence scores correlate with intensity magnitude.
- Downstream database matching (if performed) retrieves the expected sample species with high cosine similarity or scoring metric, validating that extracted peaks are biologically relevant.

## Limitations

- Algorithm performance depends on spectrum quality and signal-to-noise ratio; low-intensity or noisy spectra may generate false-positive or false-negative peaks.
- Automatic detection does not distinguish chemical isomers or adducts differing only in neutral loss; manual interpretation may be required for complex spectra.
- Confidence scoring methodology is not explicitly detailed in the article; users should validate performance on their own instrument type and sample matrix before deployment in regulatory contexts.
- The skill is validated on 'easily confused plant materials'; generalization to other biological matrices (e.g., microorganisms, metabolites) is not explicitly claimed.

## Evidence

- [other] Load raw or processed MS spectrum data (mz/intensity pairs) from input file. 2. Apply RapidMass automatic peak detection algorithm to identify peaks of interest from the spectrum. 3. Assign labels and annotations to detected peaks based on intensity ranking and m/z values. 4. Aggregate results into a structured output table with peak identifiers, m/z, intensity, and confidence scores.: "Load raw or processed MS spectrum data (mz/intensity pairs) from input file. 2. Apply RapidMass automatic peak detection algorithm to identify peaks of interest from the spectrum. 3. Assign labels"
- [other] RapidMass provides automatic identification of interested MS peaks as part of its integrated data processing workflow.: "RapidMass provides automatic identification of interested MS peaks as part of its integrated data processing workflow."
- [readme] the software provides automatic identification of interested MS peaks and supports data from multiple instruments, including DI-MS and ASAP-MS: "the software provides automatic identification of interested MS peaks and supports data from multiple instruments, including DI-MS and ASAP-MS"
- [readme] RapidMass features a user-friendly, visual interface, making it accessible to users without programming expertise: "RapidMass features a user-friendly, visual interface, making it accessible to users without programming expertise"
- [readme] The performance of RapidMass was validated using easily confused plant materials, with satisfactory results.: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results."
