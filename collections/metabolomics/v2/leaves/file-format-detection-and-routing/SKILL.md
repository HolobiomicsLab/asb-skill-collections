---
name: file-format-detection-and-routing
description: Use when when you receive a mass spectrometry imaging dataset in unknown
  or mixed vendor formats and need to apply format-specific preprocessing before generating
  ion images.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSIGen
  - Python
  - pyBaf2Sql
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- MSIGen provides tools for processing mass spectrometry imaging data acquired in
  line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
- If you are planning on using Bruker .d data in the .baf format, you will also need
  to install pyBaf2Sql from GitHub
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msigen_cq
    doi: 10.1021/jasms.4c00178
    title: MSIGen
  dedup_kept_from: coll_msigen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00178
  all_source_dois:
  - 10.1021/jasms.4c00178
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-format-detection-and-routing

## Summary

Automatically detect mass spectrometry imaging (MSI) input file format by extension and route to the appropriate MSIGen processing module. This skill enables unified handling of vendor-specific (.raw, .d, .baf, .tsf, .tdf) and open-source (.mzML) formats within a single data processing pipeline.

## When to use

When you receive a mass spectrometry imaging dataset in unknown or mixed vendor formats and need to apply format-specific preprocessing before generating ion images. Specifically, use this skill at pipeline entry when the input file path is provided but the processing module has not yet been determined.

## When NOT to use

- Input file is already converted to a standardized intermediate format (e.g., NumPy array or .mzML) that does not require vendor-specific parsing.
- File extension is missing or ambiguous (e.g., generic .dat or .bin without vendor metadata).
- Processing pipeline is designed for a single known vendor format; format detection adds unnecessary latency.

## Inputs

- file path string (e.g., '/data/sample.raw', '/data/sample.d', '/data/sample.mzML')
- file extension (extracted from path)

## Outputs

- MSIGen module object or handler (e.g., MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tsf, MSIGen.tdf, MSIGen.mzml)
- confirmation of format support

## How to apply

Extract the file extension from the input file path string. Implement conditional dispatch logic that maps each supported extension to its corresponding MSIGen module: MSIGen.raw for Thermo .raw files, MSIGen.D for Agilent .d directories, MSIGen.tsf for Bruker .tsf, MSIGen.baf for Bruker .baf (which requires pyBaf2Sql), MSIGen.tdf for Bruker .tdf, and MSIGen.mzml for open-source .mzML files. Return the selected module object or callable handler. If the file extension is unsupported, raise a clear exception listing the recognized formats. This routing ensures that format-specific metadata extraction, spectral parsing, and mobility filtering (where applicable) are delegated to the correct module.

## Related tools

- **MSIGen** (provides modular handlers (MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tsf, MSIGen.tdf, MSIGen.mzml) for format-specific data import and preprocessing) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (required dependency for parsing Bruker .baf format files via BafData class and SQL queries) — https://github.com/gtluu/pyBaf2Sql

## Examples

```
# Python snippet
from pathlib import Path
import msigen

file_path = '/data/sample.raw'
extension = Path(file_path).suffix.lower()

if extension == '.raw':
    module = msigen.raw
elif extension == '.d':
    module = msigen.D
elif extension == '.baf':
    module = msigen.baf
elif extension == '.tsf':
    module = msigen.tsf
elif extension == '.tdf':
    module = msigen.tdf
elif extension == '.mzml':
    module = msigen.mzml
else:
    raise ValueError(f'Unsupported format: {extension}')

MSIGen_generator = module(example_file=file_path, mass_list_dir='mass_list.xlsx', ...)
```

## Evaluation signals

- Verify that the returned module object matches the expected handler for the input file extension (e.g., MSIGen.raw for .raw files).
- Confirm that the module object is callable or has the required methods (e.g., get_image_data()) for downstream processing.
- Test with all supported format strings (.raw, .d, .baf, .tsf, .tdf, .mzML) and verify no incorrect mappings occur.
- Verify that unsupported extensions (e.g., .csv, .xyz) raise an exception with a clear error message listing recognized formats.
- For .baf files, confirm that pyBaf2Sql is installed and that the BafData class can be instantiated with the routed module.

## Limitations

- Agilent .d format is a directory, not a single file; path extraction must handle directory paths correctly.
- Bruker .baf format requires optional pyBaf2Sql dependency; if not installed, routing succeeds but downstream instantiation will fail; consider pre-flight dependency check.
- Extension-based detection does not validate actual file content; a .raw file with corrupted or mismatched headers will be routed correctly but fail during module initialization.
- Some vendors may use case-sensitive extensions (.RAW vs .raw); normalization to lowercase is recommended but not enforced in the article.

## Evidence

- [other] Accept a file path string as input and extract the file extension (e.g., .raw, .d, .baf, .tsf, .tdf, .mzML). Implement conditional dispatch logic that maps each supported extension to its corresponding MSIGen module: MSIGen.raw for Thermo .raw files, MSIGen.D for Agilent .d, MSIGen.tsf for Bruker .tsf, MSIGen.baf for Bruker .baf (requiring pyBaf2Sql), MSIGen.tdf for Bruker .tdf, and MSIGen.mzml for open-source .mzML files.: "Accept a file path string as input and extract the file extension (e.g., .raw, .d, .baf, .tsf, .tdf, .mzML). Implement conditional dispatch logic that maps each supported extension to its"
- [other] Return the selected module object or callable handler. Raise a clear exception if the file extension is unsupported or unrecognized.: "Return the selected module object or callable handler. Raise a clear exception if the file extension is unsupported or unrecognized."
- [intro] MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types.: "MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types."
- [readme] If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
