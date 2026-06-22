---
name: mzml-spectrum-chromatogram-object-construction
description: Use when you have an indexed gzip–compressed mzML file (mzML.gz with internal index structure) and need to retrieve and work with individual spectra or chromatograms by integer index without decompressing the entire file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ElementTree
  - pymzML
  - Python
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import xml.etree.ElementTree as et
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pymzml_cq
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty046
  all_source_dois:
  - 10.1093/bioinformatics/bty046
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzml-spectrum-chromatogram-object-construction

## Summary

Construct Python Spectrum or Chromatogram objects from indexed gzip–compressed mzML data by parsing decompressed XML blocks and instantiating the appropriate object type based on the element tag. This enables random-access retrieval and in-memory representation of individual mass spectra or chromatograms from large compressed mzML files.

## When to use

Use this skill when you have an indexed gzip–compressed mzML file (mzML.gz with internal index structure) and need to retrieve and work with individual spectra or chromatograms by integer index without decompressing the entire file. Applicable when memory efficiency is critical and selective access to specific scans is required.

## When NOT to use

- Input is an uncompressed or non-indexed mzML file; use standard sequential parsing instead.
- Input is a different compressed format (e.g., standard gzip without internal index) or a non-mzML data type.
- Workflow requires sequential iteration over all spectra; use the read() method for line-by-line parsing instead of random access.

## Inputs

- indexed gzip file path (mzML.gz with internal byte-offset index)
- integer index (chapter/spectrum identifier)

## Outputs

- Spectrum object or Chromatogram object (pymzML spectrum/chromatogram instance)
- parsed XML element tree fragment

## How to apply

Instantiate a GSGR (Generalized Seekable Gzip Reader) class with the path to an indexed gzip mzML file. Load the internal index mapping to translate integer keys to byte offsets within the gzip stream. When accessing a chapter by integer index via bracket notation (e.g., reader[42]), seek to the corresponding byte offset, extract and decompress the data block, and parse the XML fragment using ElementTree. Inspect the root element tag to determine whether to instantiate a Spectrum or Chromatogram object. Populate the object with parsed attributes and child elements, then return it to the caller. The correctness of byte offset lookup is crucial; verify that the index was created with a compatible GSGW (Generalized Seekable Gzip Writer) class during file preparation.

## Related tools

- **pymzML** (Core library providing Spectrum/Chromatogram classes and GSGR/GSGW classes for indexed gzip access; parses mzML XML into objects) — https://github.com/pymzml/pymzML
- **ElementTree** (XML parser used to deserialize decompressed data blocks into element trees before object instantiation)
- **Python** (Language runtime providing file I/O, bracket notation (__getitem__), and module organization)

## Examples

```
from pymzML import GSGR; reader = GSGR('data.mzML.gz'); spectrum = reader[42]; print(spectrum.mz, spectrum.intensity)
```

## Evaluation signals

- Returned object is an instance of Spectrum or Chromatogram class (type check).
- Object attributes (m/z array, intensity array, retention time, scan metadata) are correctly populated from parsed XML.
- Bracket notation access (reader[i]) returns consistent objects across repeated calls to the same index.
- Byte offset lookup does not raise IndexError or seek exceptions; offsets are valid within the gzip stream.
- Decompressed XML block can be re-serialized to valid XML and matches the canonical mzML schema for spectrum/chromatogram elements.

## Limitations

- Index structure must be created during file writing using compatible GSGW class; pre-existing standard gzip files cannot be retrofitted with this index.
- Random access performance depends on index quality and gzip block alignment; fragmented indices may cause suboptimal seek times.
- Large XML elements that span multiple gzip blocks may require special handling; implementation details depend on pymzML version.
- Element tag determination (Spectrum vs. Chromatogram) assumes well-formed mzML; malformed or non-standard XML may instantiate incorrect object type or raise parsing errors.

## Evidence

- [intro] The GSGR class accepts an indexed gzip file path and implements bracket notation for retrieval: "The GSGR class accepts an indexed gzip file path during initialization and implements bracket notation access to retrieve data blocks."
- [intro] Implement __getitem__ to map integer index to byte offset and extract data block: "Implement the __getitem__ method to accept an integer index and retrieve the corresponding chapter/spectrum from the indexed gzip file."
- [intro] Parse extracted XML and instantiate Spectrum or Chromatogram based on element tag: "Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object based on the element tag."
- [other] pymzML supports indexed gzip files with random access capability: "pymzML is an extension to Python that offers... a) easy access to mass spectrometry (MS) data that allows the rapid development of tools... d) random access in compressed files"
- [other] Access indexed gzip data using bracket notation: "access the chapters conveniently by the python bracket notation ([])"
- [intro] Indexed gzip files allow mzML file sizes to reach levels comparable to the original RAW format: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
