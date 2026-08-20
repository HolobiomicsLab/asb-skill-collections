---
name: feature-quality-assessment-metrics
description: Use when after nontargeted peak detection and segmentation has generated a feature table from raw LC-MS data (mzML or vendor format), apply quality assessment when you need to rank or filter features by confidence before annotation, adduct grouping, or MS/MS matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
  - direct-infusion-MS
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing
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

# feature-quality-assessment-metrics

## Summary

Comprehensive evaluation of LC-MS detected features using quality metrics to filter and rank chromatographic peaks by reliability. This skill assesses feature integrity, noise characteristics, and signal consistency to support confident downstream annotation and metabolite identification.

## When to use

After nontargeted peak detection and segmentation has generated a feature table from raw LC-MS data (mzML or vendor format), apply quality assessment when you need to rank or filter features by confidence before annotation, adduct grouping, or MS/MS matching. Use this skill when the feature table includes retention time, m/z, intensity, and peak width metadata and you aim to reduce false positives or prioritize high-confidence features for downstream analysis.

## When NOT to use

- Input is already a manually validated or curated feature set and quality re-assessment is not needed.
- Analysis requires only presence/absence of features and does not benefit from confidence ranking or intensity-based filtering.
- Raw LC-MS data is from non-chromatographic or non-mass-spectrometry modalities (e.g., direct infusion, imaging MS without retention time dimension).

## Inputs

- raw LC-MS data (mzML or vendor format)
- feature table (detected peaks with m/z, retention time, intensity, peak width)

## Outputs

- feature table with quality metrics (CSV or feather format)
- quality-filtered feature table (high-confidence peaks)

## How to apply

MassCube applies comprehensive feature quality evaluation by computing multiple metrics on detected peaks, including signal-to-noise ratios, peak shape characteristics, intensity consistency across scans, and retention time precision. The package generates quality scores that can be used to filter features (e.g., retaining only high-confidence peaks) or to rank features for priority in annotation workflows. Quality metrics are embedded in the output feature table alongside m/z, retention time, intensity, and peak width, allowing downstream tools to prioritize features or apply thresholds. The rationale is that peaks with poor shape, low signal-to-noise, or unstable intensity are more likely to be artifacts or contaminants, so filtering on quality metrics reduces false annotations and improves annotation confidence.

## Related tools

- **masscube** (Integrated Python package that performs nontargeted peak detection, segmentation, and comprehensive feature quality evaluation on LC-MS data) — https://github.com/huaxuyu/masscube/
- **Python** (Programming environment for scripting MassCube workflows and custom quality metric calculations)

## Examples

```
from masscube import MassCube; mc = MassCube(); features = mc.load_raw('sample.mzML'); detected = mc.peak_detection_and_segmentation(features); quality_features = mc.feature_quality_evaluation(detected); quality_features.export('features_with_quality.csv')
```

## Evaluation signals

- Output feature table includes a quality metric column (or multiple columns for different quality dimensions) with numeric values that correlate with peak reliability.
- Quality scores enable reproducible filtering: applying a quality threshold consistently ranks/removes the same features across replicate runs.
- High-quality features (retained after filtering) show lower false annotation rates in downstream MS/MS matching or adduct grouping compared to unfiltered features.
- Quality metric distributions are visually distinct between noise and signal peaks (e.g., signal peaks cluster toward high scores while noise/artifact peaks show low scores).
- Feature table schema is preserved in output (m/z, retention time, intensity, peak width, plus new quality columns); all detected peaks remain in the table with their quality scores for downstream filtering.

## Limitations

- Quality metrics are computed only on features already detected; poor peak detection upstream will not be corrected by quality assessment.
- Quality thresholds may be data-dependent (e.g., different LC-MS instrument types, ionization modes, or matrix effects may require re-tuning of cutoff values).
- No changelog was found in the repository, limiting traceability of changes to quality metric definitions across versions.

## Evidence

- [readme] Comprehensive feature quality evaluation: "Comprehensive feature quality evaluation."
- [other] Quality metrics extracted alongside peak characteristics: "Generate and export feature table in tabular format (CSV or feather) containing detected peaks with their metadata and quality metrics."
- [readme] Core MassCube capability for LC-MS data processing: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
