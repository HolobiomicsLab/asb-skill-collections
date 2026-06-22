---
name: vendor-raw-file-format-recognition
description: Use when you have a directory containing mass spectrometry data files from multiple instrument vendors (Thermo, AB Sciex, Agilent, Bruker, etc.) and need to convert them to a common format (Aird or mzML).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - AirdPro V6
  - pwiz_bindings_cli.dll
  - ProteoWizard
  - AirdPro
  - ProteoWizard MSConvert
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V6 is now available at 2024.4
- based on pwiz_bindings_cli.dll from the ProteoWizard project
- pwiz_bindings_cli.dll from the ProteoWizard project
- based on pwiz_bindings_cli.dll from the ProteoWizard project.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aird_cq
    doi: 10.1186/s12859-021-04490-0
    title: aird
  dedup_kept_from: coll_aird_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04490-0
  all_source_dois:
  - 10.1186/s12859-021-04490-0
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# vendor-raw-file-format-recognition

## Summary

Identify and classify vendor-specific mass spectrometry raw file formats (e.g., .raw, .wiff2, .d) to select the appropriate conversion pathway and acquisition method handler in AirdPro. This skill is essential for batch or automated conversion pipelines where file origins are heterogeneous.

## When to use

You have a directory containing mass spectrometry data files from multiple instrument vendors (Thermo, AB Sciex, Agilent, Bruker, etc.) and need to convert them to a common format (Aird or mzML). You must distinguish vendor formats to route each file to the correct ProteoWizard conversion handler and to infer or validate the acquisition method (DDA, DIA_SWATH, PRM, MRM).

## When NOT to use

- Input files are already in open formats (mzML, mzXML, Aird). Skip format recognition and proceed directly to downstream analysis.
- You have pre-curated metadata that definitively specifies vendor origin and acquisition method for all files. Use that metadata instead of re-detecting.
- Working with a single known vendor format in a controlled environment where format homogeneity is guaranteed.

## Inputs

- vendor raw file (e.g., Thermo .raw, Agilent .d folder, AB Sciex .wiff2)
- file path or directory path containing heterogeneous vendor files
- optional: instrument metadata or sample information embedded in vendor file headers

## Outputs

- vendor format classification string (e.g., 'Thermo RAW', 'Agilent .d', 'AB Sciex WIFF2')
- acquisition method label (DDA, DIA_SWATH, PRM, MRM, or COMMON)
- ConvertJob object with sourcePath, targetPath, type, and mzPrecision fields populated

## How to apply

Inspect the file extension and folder structure of the raw input. AirdPro supports all vendor formats that ProteoWizard MSConvert handles; common formats include Thermo .raw, Agilent folder-format .d directories, and AB Sciex .wiff2. Use AirdPro's automatic acquisition method detection feature to infer whether the file is DDA, DIA_SWATH, PRM, MRM, or COMMON type. If automatic detection fails or is ambiguous, consult instrument metadata (e.g., sample info XML within Agilent .d folders) or manually specify the acquisition type in the ConvertJob JSON object. This classification step must occur before invoking the pwiz_bindings_cli.dll conversion mechanism, because the correct handler depends on both vendor format and acquisition method.

## Related tools

- **AirdPro** (GUI and CLI client that wraps format detection and delegates conversion to ProteoWizard; includes automatic acquisition method identification) — https://github.com/CSi-Studio/AirdPro
- **pwiz_bindings_cli.dll** (Underlying ProteoWizard DLL that performs vendor-specific format parsing and routing; invoked by AirdPro after format is recognized)
- **ProteoWizard MSConvert** (Foundation library exposing vendor format handlers for all major MS instrument vendors; AirdPro depends on its format support)

## Examples

```
java -c "StringRedisTemplate st = new StringRedisTemplate(); ConvertJob job = new ConvertJob(); job.sourcePath = 'C:\vendor\test.raw'; job.targetPath = 'D:\output'; job.type = 'DDA'; job.mzPrecision = 0.0001; st.opsForSet().add('ConvertTask', JSON.toJSONString(job));"
```

## Evaluation signals

- Returned format classification matches the actual file extension and internal file structure (e.g., .raw → Thermo, .d → Agilent, .wiff2 → AB Sciex).
- Acquisition method label is consistent with instrument acquisition mode (DDA files contain variable scan windows; SWATH files contain fixed overlapping windows; PRM files contain targeted transition lists).
- ConvertJob JSON object is valid and contains non-empty, non-null sourcePath, targetPath, type, and mzPrecision fields.
- Downstream conversion using the identified format and method completes without vendor-specific parsing errors.
- Output file (Aird or mzML) contains expected spectral data and metadata corresponding to the input vendor file.

## Limitations

- Automatic acquisition method detection may fail or be ambiguous for non-standard or hybrid acquisition modes; manual specification may be required.
- AirdPro supports only vendors and formats that ProteoWizard MSConvert explicitly handles; proprietary or newly released formats may not be recognized.
- Folder-format vendor files (e.g., Agilent .d) require correct path specification; passing the folder path rather than individual files inside is critical.
- Format recognition relies on file extension and internal headers; corrupted or renamed files may be misclassified.
- MRM and WIFF2 format support was added in V5.1.0; older AirdPro versions may not recognize these formats.

## Evidence

- [readme] By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format.: "By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format."
- [readme] AirdPro is based on pwiz_bindings_cli.dll from the ProteoWizard project: "AirdPro is based on pwiz_bindings_cli.dll from the ProteoWizard project"
- [readme] [New Feature] Automatic identification for Acquisition methods: "[New Feature] Automatic identification for Acquisition methods"
- [readme] The detail of the ConvertJob object is described here: String sourcePath, String targetPath, Double mzPrecision, String type=DDA: "The detail of the ConvertJob object is described here: String sourcePath, String targetPath, Double mzPrecision, String type="DIA_SWATH", "DDA", "PRM", "COMMON""
- [readme] [New Feature] Supporting Wiff2 format: "[New Feature] Supporting Wiff2 format"
- [readme] Batch Conversion: Scan the directory structure and convert automatically: "Batch Conversion: Scan the directory structure and convert automatically"
