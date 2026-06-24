---
name: nontargeted-metabolomics-data-processing
description: Use when you have raw LC-MS data in vendor or mzML format and need to
  systematically discover and extract all detectable metabolite features across the
  full retention time range, without predefined target lists.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
  - direct-infusion-MS
  - MS-imaging
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: huaxuyu/masscube
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nontargeted-metabolomics-data-processing

## Summary

Nontargeted metabolomics data processing is a workflow for extracting chromatographic features from raw LC-MS data without prior knowledge of target analytes. It combines peak detection, segmentation, feature quality evaluation, and annotation to generate a comprehensive feature table suitable for discovery and comparative metabolomics studies.

## When to use

Apply this skill when you have raw LC-MS data in vendor or mzML format and need to systematically discover and extract all detectable metabolite features across the full retention time range, without predefined target lists. This is the entry point for nontargeted metabolomics discovery experiments where you seek to identify novel or unexpected signals.

## When NOT to use

- Input is already a preprocessed feature table or peak list — use this skill only on raw LC-MS data files.
- Analysis requires targeted detection of a predefined set of analytes with known m/z and retention times — use targeted peak extraction instead.
- Data is from non-chromatographic mass spectrometry (e.g., direct infusion MS or MALDI imaging) — this skill is specific to LC-MS.

## Inputs

- Raw LC-MS data in mzML format
- Raw LC-MS data in vendor format
- Mass spectrometry run files

## Outputs

- Feature table in tabular format (CSV or feather)
- Detected peaks with m/z, retention time, intensity, and peak width
- Peak metadata and quality metrics
- Annotated feature groups (isotopes, adducts, in-source fragments)

## How to apply

Load raw LC-MS data (mzML or vendor format) into MassCube and apply the nontargeted peak detection algorithm to identify chromatographic peaks across the full retention time range. Perform peak segmentation to define precise peak boundaries and extract peak characteristics (m/z, retention time, intensity, peak width). Apply comprehensive feature quality evaluation to filter low-confidence features. Annotate feature groups to identify isotopes, adducts, and in-source fragments. Finally, generate and export the feature table in tabular format (CSV or feather) containing detected peaks with their metadata and quality metrics.

## Related tools

- **masscube** (Integrated Python package performing nontargeted peak detection, segmentation, feature quality evaluation, and annotation of LC-MS data) — https://github.com/huaxuyu/masscube/
- **Python** (Programming language for executing MassCube workflows and data processing pipeline)

## Examples

```
pip install masscube; python -c "from masscube import MSData; data = MSData('raw_sample.mzML'); peaks = data.detect_peaks(); features = peaks.segment_and_quality_filter(); features.export('features.csv')"
```

## Evaluation signals

- Feature table is generated with expected schema: columns for m/z, retention time, intensity, peak width, and quality metrics.
- Peak boundaries are consistent and non-overlapping; retention time ordering matches chromatographic elution order.
- Detected peaks show expected intensity distributions and signal-to-noise characteristics across the sample.
- Feature group annotations correctly identify isotopic patterns (e.g., M and M+1 with expected 13C ratio and intensity), common adducts ([M+H]+, [M+Na]+, [M-H]−), and in-source fragments.
- Feature table is exportable in CSV or feather format and contains metadata suitable for downstream statistical analysis and metabolite identification.

## Limitations

- Peak detection accuracy depends on signal-to-noise ratio and chromatographic resolution; low-intensity features near baseline may be missed or incorrectly segmented.
- No changelog found — version-to-version changes and algorithmic improvements are not publicly documented.
- Annotation of feature groups relies on known patterns for isotopes and common adducts; novel or unconventional adducts may not be captured.

## Evidence

- [readme] Highly accurate nontargeted peak detection and segmentation.: "Highly accurate nontargeted peak detection and segmentation."
- [other] Load raw LC-MS data (mzML or vendor format) into MassCube. Apply nontargeted peak detection algorithm to identify chromatographic peaks across the full retention time range. Perform peak segmentation to define precise peak boundaries and extract peak characteristics (m/z, retention time, intensity, peak width). Generate and export feature table in tabular format (CSV or feather) containing detected peaks with their metadata and quality metrics.: "Load raw LC-MS data (mzML or vendor format) into MassCube. 2. Apply nontargeted peak detection algorithm to identify chromatographic peaks across the full retention time range. 3. Perform peak"
- [readme] Comprehensive feature quality evaluation and Confident annotation of feature groups including isotopes, adducts and in-source fragments.: "Comprehensive feature quality evaluation. Confident annotation of feature groups including isotopes, adducts and in-source fragments."
- [readme] masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
