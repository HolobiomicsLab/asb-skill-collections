---
name: mzml-mzxml-file-parsing
description: Use when parsing open-format mass spectrometry data files (mzML, mzXML, MGF) in the domain of metabolomics to convert them into memory-resident data structures (pandas DataFrames) for downstream spectral filtering and pattern queries, specifically for accessing MS1 and MS2 spectra programmatically.
when_to_use_negative:
- Input is already a pre-processed feature table or consensus spectrum library (e.g., GNPS spectral library or MGF from molecular networking); re-parsing adds computational overhead without new information.
- You require vendor-specific raw file formats (.raw from Thermo, .d from Agilent) without prior conversion to open formats; pyteomics cannot directly read proprietary binaries.
- Analysis requires ion mobility separation metadata not embedded in the mzML/mzXML file structure; additional parsing or vendor libraries may be needed.
edam_operation: http://edamontology.org/operation_3763
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: pyteomics
  role: Reads mzML, mzXML, and MGF files into Python data structures; handles mass spectrometry file I/O
- name: pandas
  role: Stores parsed spectra as DataFrames; enables efficient filtering and slicing by m/z, retention time, scan number, and other metadata
- name: Apache Feather
  role: Caches parsed spectra to disk in columnar format for fast reloading during repeated queries without re-parsing raw files
- name: MZmine
  role: Open-source MS data analysis platform; natively supports mzML/mzXML import and spectral browsing
  repo: https://github.com/mzmine/mzmine
- name: lark
  role: Parser library used to transform MassQL query strings into parse trees for execution against parsed spectral DataFrames
  repo: https://github.com/lark-parser/lark
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_s41592_full/skills/mzml-mzxml-file-parsing/SKILL.md
    - outputs/audit_s41592_full/skills/mzml-mzxml-file-parsing/skill.md
    merged_at: '2026-05-25T06:57:01.570487+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/mzml-mzxml-file-parsing@sha256:a95235cf9686fe6c8bd0f41f394b2dc9dd496fe245f493bcb7856066c44637e6
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# mzml-mzxml-file-parsing

## Summary

Parse open-format mass spectrometry data files (mzML, mzXML, MGF) into memory-resident data structures (pandas DataFrames) to enable downstream spectral filtering and pattern queries. This is foundational for accessing MS1 and MS2 spectra programmatically.

## When to use

You have raw or processed MS data in open-format files (mzML, mzXML, or MGF) and need to extract MS1 or MS2 spectral metadata (m/z, intensity, retention time, scan number, precursor charge) for filtering, querying, or molecular networking. Use this skill before any pattern-matching or spectral comparison workflow.

## When NOT to use

- Input is already a pre-processed feature table or consensus spectrum library (e.g., GNPS spectral library or MGF from molecular networking); re-parsing adds computational overhead without new information.
- You require vendor-specific raw file formats (.raw from Thermo, .d from Agilent) without prior conversion to open formats; pyteomics cannot directly read proprietary binaries.
- Analysis requires ion mobility separation metadata not embedded in the mzML/mzXML file structure; additional parsing or vendor libraries may be needed.

## Inputs

- mzML file (open standardized format)
- mzXML file (open standardized format)
- MGF file (Mascot generic format)
- File path or directory containing multiple MS data files

## Outputs

- pandas DataFrame with columns: scan_number, precursor_mz, charge_state, retention_time, ms_level, intensity_array, mz_array
- Apache Feather file (cached parsed spectra for repeated queries)
- JSON or CSV export of matched spectral records

## How to apply

Use the pyteomics library to read mzML/mzXML/MGF files and convert them into pandas DataFrames, preserving scan metadata (precursor m/z, charge state, retention time, scan number, intensity arrays). Cache the resulting DataFrames as Apache Feather files for repeated queries to avoid re-parsing large files. For large repositories (>100 million spectra), consider streaming or batching to manage memory. The parsed structure must retain both MS1 isotope pattern information and MS2 product ion m/z values so that subsequent filtering operations (e.g., by MS1MZ, MS2PREC, POLARITY, retention time windows) can operate efficiently.

## Related tools

- **pyteomics** (Reads mzML, mzXML, and MGF files into Python data structures; handles mass spectrometry file I/O)
- **pandas** (Stores parsed spectra as DataFrames; enables efficient filtering and slicing by m/z, retention time, scan number, and other metadata)
- **Apache Feather** (Caches parsed spectra to disk in columnar format for fast reloading during repeated queries without re-parsing raw files)
- **MZmine** (Open-source MS data analysis platform; natively supports mzML/mzXML import and spectral browsing) — https://github.com/mzmine/mzmine
- **lark** (Parser library used to transform MassQL query strings into parse trees for execution against parsed spectral DataFrames) — https://github.com/lark-parser/lark

## Examples

```
from pyteomics import mzml
import pandas as pd
spectra_list = []
for spectrum in mzml.read('sample.mzML'):
    spectra_list.append({'scan_number': spectrum['ID'], 'precursor_mz': spectrum.get('precursorList', [{}])[0].get('mz'), 'retention_time': spectrum['scanList']['scan'][0]['scan start time']})
df = pd.DataFrame(spectra_list)
df.to_feather('sample_spectra.feather')
```

## Evaluation signals

- All MS1 and MS2 spectra from the input file(s) are present in the output DataFrame with no missing or truncated records.
- Metadata columns (precursor m/z, charge, retention time, scan number) match the values reported in the original file headers or vendor software.
- Retention time, m/z, and intensity values fall within physically plausible ranges (e.g., m/z > 50, intensity ≥ 0, retention time ≥ 0).
- Cached Feather files can be reloaded and produce identical DataFrames to the original parse, confirming lossless serialization.
- Downstream MassQL filters (e.g., MS1MZ=163.1, RTMIN=5) successfully retrieve expected subsets of spectra without errors.

## Limitations

- pyteomics does not natively read vendor-specific raw formats (.raw, .d); pre-conversion to mzML/mzXML or use of vendor SDKs is required.
- Very large files (>10 GB) may exhaust memory if loaded entirely into a single DataFrame; streaming or chunked parsing is necessary.
- Ion mobility spectrometry data embedded in mzML may not be fully parsed by default; additional schema interpretation may be needed.
- MassQL has limited capability to leverage consecutive MS spectra from a single chromatographic feature; the skill does not guarantee coherent peak shape representation across retention time.
- Parsing performance depends on file size and disk I/O speed; initial parse can be slow for multi-gigabyte repositories.

## Evidence

- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations: "The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations"
- [full_text] spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying: "spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying"
- [other] Retrieve and read the Eutypa lata E. lata post-liquid chromatography iron-addition mzML/mzXML data files from MassIVE using pyteomics library into pandas data frames.: "Retrieve and read the Eutypa lata E. lata post-liquid chromatography iron-addition mzML/mzXML data files from MassIVE using pyteomics library into pandas data frames"
- [full_text] MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source: "MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source"
