---
name: peak-labeling-and-annotation
description: Use when immediately after automatic peak detection on a raw or processed MS spectrum when you have a list of candidate peaks with m/z and intensity values but lack systematic identifiers, confidence estimates, or ranked ordering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
  techniques:
  - direct-infusion-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-labeling-and-annotation

## Summary

Assign systematic labels and confidence-ranked annotations to mass spectrometry peaks detected in high-resolution spectra, organizing them by intensity ranking and m/z values to enable downstream sample matching and database scoring. This skill transforms raw peak lists into structured, annotated tables suitable for species authentication and comparative analysis.

## When to use

Apply this skill immediately after automatic peak detection on a raw or processed MS spectrum when you have a list of candidate peaks with m/z and intensity values but lack systematic identifiers, confidence estimates, or ranked ordering. Use it when preparing peaks for database search algorithms or when you need to disambiguate peaks for visual inspection and validation by domain experts.

## When NOT to use

- Input is already a manually curated or database-matched peak list with established identities—re-annotation risks losing validated assignments.
- Spectrum is too noisy or poorly resolved to distinguish true peaks from baseline noise; detection must succeed before annotation can be reliable.
- Analysis does not require downstream database matching or comparative species discrimination; simple intensity thresholding may suffice.

## Inputs

- raw or processed MS spectrum data (mz/intensity pairs)
- detected peak list with m/z and intensity values
- peak detection results from RapidMass automatic peak detection algorithm

## Outputs

- structured peak annotation table with peak identifiers, m/z values, intensity values, and confidence scores
- labeled and ranked peak list suitable for database search

## How to apply

After RapidMass identifies peaks of interest from the spectrum using its automatic detection algorithm, assign unique peak identifiers and annotations based on intensity ranking (highest to lowest) and m/z ordering. Compute confidence scores for each peak—the article workflow does not specify the scoring method, but confidence should reflect detection quality relative to noise and instrument baseline. Aggregate all labeled peaks, their m/z values, intensities, and confidence scores into a structured output table. This annotation step bridges raw peak detection and database matching, enabling the downstream database search algorithms to perform unknown sample scoring with properly ranked and justified peak lists.

## Related tools

- **RapidMass** (Performs automatic peak detection and applies peak labeling and annotation as integrated steps in its data processing workflow; provides the peak detection input and execution environment for annotation.) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (Direct infusion mass spectrometry instrument supported by RapidMass; produces raw spectra that are inputs to peak detection and annotation.)
- **ASAP-MS** (Ambient ionization mass spectrometry instrument supported by RapidMass; produces raw spectra that are inputs to peak detection and annotation.)

## Evaluation signals

- All detected peaks are assigned unique, sequential identifiers with no duplicates or gaps.
- Peaks in the output table are ranked by intensity in descending order and secondarily ordered by increasing m/z within tied intensity bins.
- Confidence scores for all peaks fall within a defined valid range (e.g., 0–1 or 0–100) with no null or invalid values.
- The structured output table is complete: every peak has all required fields (identifier, m/z, intensity, confidence score) with correct data types and no missing values.
- Annotated peak list produces meaningful database match results when passed to RapidMass database search algorithms; poor annotation should correlate with low or ambiguous sample scoring.

## Limitations

- Peak annotation relies on the accuracy of prior automatic peak detection; false positives or missed peaks in detection propagate as incorrect or missing annotations.
- Confidence score methodology is not explicitly detailed in the article; users may need to validate confidence estimates against manual expert curation on a subset of spectra.
- Annotation quality may degrade on spectra from poorly resolved or contaminated samples, or on data from non-standard instrument configurations not covered in RapidMass validation.
- The article does not report sensitivity to instrumental parameters (e.g., mass resolution, signal-to-noise ratio thresholds); annotation robustness across diverse MS instruments remains unquantified.

## Evidence

- [other] The workflow assigns labels and annotations to detected peaks based on intensity ranking and m/z values, then aggregates results into a structured output table with peak identifiers, m/z, intensity, and confidence scores.: "Assign labels and annotations to detected peaks based on intensity ranking and m/z values. 4. Aggregate results into a structured output table with peak identifiers, m/z, intensity, and confidence"
- [intro] RapidMass integrates automatic peak identification as part of its data processing workflow.: "software provides automatic identification of interested MS peaks"
- [readme] RapidMass uses database search algorithms to score unknown samples, for which annotated peaks are essential inputs.: "RapidMass offers several database search algorithms to achieve unknown sample scoring."
- [other] Peak annotation and detection are consecutive workflow steps that feed downstream analysis.: "Load raw or processed MS spectrum data (mz/intensity pairs) from input file. 2. Apply RapidMass automatic peak detection algorithm to identify peaks of interest from the spectrum. 3. Assign labels"
