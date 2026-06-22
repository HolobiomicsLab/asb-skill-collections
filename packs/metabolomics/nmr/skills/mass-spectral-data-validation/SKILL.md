---
name: mass-spectral-data-validation
description: Use when you have raw LC-MS/MS spectral data in vendor formats or unvalidated .mgf files before feeding them into the specXplore importing pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MZmine3
  - matchms.Spectrum
  - text editor
  techniques:
  - LC-MS
  - GC-MS
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.3c04444
  title: specxplore
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_specxplore
    doi: 10.1021/acs.analchem.3c04444
    title: specxplore
  dedup_kept_from: coll_specxplore
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04444
  all_source_dois:
  - 10.1021/acs.analchem.3c04444
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-data-validation

## Summary

Validate LC-MS/MS spectral data integrity and metadata correctness before importing into the specXplore pipeline. This skill ensures raw spectral data conform to required formats (.mgf) and contain essential feature identifiers needed for downstream processing and visualization.

## When to use

Apply this skill when you have raw LC-MS/MS spectral data in vendor formats or unvalidated .mgf files before feeding them into the specXplore importing pipeline. Validation is mandatory if feature identifiers are missing, malformed, or use non-standard key names (anything other than 'feature_id'), or if the file format is uncertain.

## When NOT to use

- Input data is already a processed specXplore session data object (.pkl or serialized file) — skip to dashboard loading
- Raw vendor files are already confirmed to be in valid .mgf format with correct 'feature_id' keys — proceed directly to importing pipeline
- Working with spectral data from non-LC-MS/MS sources (e.g. GC-MS, IR, NMR) — specXplore is designed for LC-MS/MS only

## Inputs

- Raw LC-MS/MS spectral data in vendor formats (e.g. .raw, .d, .ms)
- .mgf file (Mascot Generic Format) with MS/MS spectral data
- Feature list with feature identifiers (in any initial key format)

## Outputs

- Validated .mgf file with consistently named 'feature_id' metadata fields
- Confirmation report of metadata field presence and naming compliance

## How to apply

First, confirm input spectral data is in .mgf (Mascot Generic Format) with MS/MS spectral records. Second, verify that each spectrum contains a feature identifier metadata field; specXplore expects this key to be named exactly 'feature_id'. If the feature identifier exists but uses a different key name (e.g. 'wrong_key='), use either matchms.Spectrum module in Python to programmatically rename it, or use a text editor to find-and-replace all instances of the incorrect key with 'feature_id='. Third, if raw vendor data requires conversion to .mgf, use vendor-specific software or MZmine3 with GNPS-FBMN export options. Validate the resulting .mgf file by spot-checking several spectra to confirm feature_id fields are present and consistently formatted before passing to the importing pipeline.

## Related tools

- **MZmine3** (Convert raw vendor spectral data to .mgf format with GNPS-FBMN export options) — https://mzmine.github.io/mzmine_documentation/getting_started.html
- **matchms.Spectrum** (Programmatically add or rename metadata keys (e.g. feature_id) in .mgf spectra using Python) — https://matchms.readthedocs.io/en/latest/api/matchms.html#matchms.Spectrum
- **text editor** (Quick bulk replacement of incorrect feature identifier key names in .mgf files)

## Examples

```
# Using matchms to rename feature_id key in Python:
from matchms import Spectrum
import pickle
spectra = pickle.load(open('raw_spectra.pkl', 'rb'))
for spec in spectra:
    if 'wrong_key' in spec.metadata:
        spec.metadata['feature_id'] = spec.metadata.pop('wrong_key')
pickle.dump(spectra, open('validated_spectra.pkl', 'wb'))

# Or quick fix with text editor: sed -i 's/wrong_key=/feature_id=/g' data.mgf
```

## Evaluation signals

- Every spectrum in the .mgf file contains a 'feature_id=' metadata line with a non-empty value
- No validation warnings or errors are raised when the .mgf file is loaded into specXplore's importing pipeline
- Spot-check of 5–10 random spectra confirms consistent presence and formatting of feature_id metadata across the file
- The specXplore session data object is successfully created and serialized without metadata-related errors
- Feature identifier counts match between the original feature list and the validated .mgf file (no records dropped during validation)

## Limitations

- specXplore currently requires .mgf format and does not accept other common formats (e.g. mzML, mzXML) — conversion is mandatory
- Feature identifiers must be present and correctly named; spectral records lacking 'feature_id' will not be properly indexed in downstream exploration
- Validation does not check chemical correctness or mass accuracy of spectral peaks — only metadata structure and naming
- Windows installation of specXplore has known incompatibilities; validation and importing pipeline may fail on Windows systems
- macOS arm64 systems with ms2deepscore may produce unreliable similarity scores that propagate through the pipeline despite validation passing

## Evidence

- [readme] specXplore currently requires a .mgf formatted file with MS/MS spectral data: "Note that specXplore currently requires a .mgf formatted file with MS/MS spectral data."
- [readme] Feature lists should contain 'feature_id' as the feature identifier key: "Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to be "feature_id"."
- [readme] Feature identifier keys can be renamed using matchms or text editor: "Renaming the feature identifying key in a .MGF file is possible using matchms, specifically the matchms.Spectrum module which provides a means of adding metadata keys to existing spectra in Python."
- [readme] MZmine3 provides export options for .mgf format from raw vendor data: "To generate a .MGF file from your raw data please refer to processing options in your vendor specific software or the workflows described in MZmine. MZmine3 provides exporting options for the .MGF"
