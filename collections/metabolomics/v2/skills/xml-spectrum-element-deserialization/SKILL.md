---
name: xml-spectrum-element-deserialization
description: Use when when you have retrieved a decompressed XML data block from an indexed gzip file (via GSGR bracket notation) and need to convert that raw XML string into a usable Python spectrum or chromatogram object for downstream analysis, filtering, or comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0943
  tools:
  - ElementTree
  - pymzML
  - ElementTree (xml.etree.ElementTree)
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

# xml-spectrum-element-deserialization

## Summary

Deserialize XML spectrum and chromatogram elements from indexed gzip files into Python objects (Spectrum or Chromatogram instances) by parsing extracted data blocks with ElementTree. This skill enables rapid random-access retrieval and instantiation of mass spectrometry data structures from compressed mzML files.

## When to use

When you have retrieved a decompressed XML data block from an indexed gzip file (via GSGR bracket notation) and need to convert that raw XML string into a usable Python spectrum or chromatogram object for downstream analysis, filtering, or comparison.

## When NOT to use

- Input data is already a Spectrum or Chromatogram object — deserialization is unnecessary.
- XML data has not yet been retrieved or decompressed from the indexed gzip file; use GSGR reader first.
- Raw mzML file is uncompressed or not indexed; use standard sequential mzML parsers instead of GSGR-based workflow.

## Inputs

- XML string (decompressed data block from indexed gzip file)
- ElementTree root element (parsed from XML string)
- Element tag name ('spectrum' or 'chromatogram')

## Outputs

- Spectrum object (pymzML.spec.Spectrum instance)
- Chromatogram object (pymzML.spec.Chromatogram instance)

## How to apply

After retrieving a data block (XML string) from an indexed gzip reader using bracket notation (e.g., `reader[index]`), parse the XML string using ElementTree's `fromstring()` or `parse()` to obtain the root element. Inspect the element tag to determine the data type: 'spectrum' elements become Spectrum objects, 'chromatogram' elements become Chromatogram objects. Instantiate the appropriate object class (from pymzML.spec) by passing the parsed XML element, which triggers internal attribute extraction and normalization. The resulting object is then ready for spectral comparison, filtering, or visualization without further deserialization steps.

## Related tools

- **pymzML** (Provides Spectrum and Chromatogram classes for object instantiation from parsed XML elements; handles mzML parsing and random access to indexed gzip data) — https://github.com/pymzml/pymzML
- **ElementTree (xml.etree.ElementTree)** (Parses XML data blocks into element trees; enables tag-based routing to determine spectrum vs. chromatogram type)

## Examples

```
from pymzml import spec; import xml.etree.ElementTree as et; root = et.fromstring(decompressed_xml_string); spectrum = spec.Spectrum(root) if root.tag == 'spectrum' else spec.Chromatogram(root)
```

## Evaluation signals

- Returned object is an instance of Spectrum or Chromatogram, not a raw string or dict.
- Object attributes (m/z values, intensities, scan metadata) are accessible and correctly populated from the XML element.
- Element tag matches the returned object type ('spectrum' → Spectrum, 'chromatogram' → Chromatogram).
- Object can be serialized back to XML or compared with other spectrum objects without ValueError or AttributeError.
- Sequential access (iteration over many indexed entries) produces consistent object instantiation with no parse failures.

## Limitations

- Deserialization performance depends on XML complexity; large spectra with many peaks will incur parsing overhead at each index access.
- Only supports mzML XML schemas compatible with pymzML's Spectrum and Chromatogram class definitions; non-standard or malformed XML will raise parsing exceptions.
- No built-in validation of element completeness; missing mandatory mzML attributes will result in incomplete or None-valued object fields.
- Index-based access (GSGR) requires that the gzip file was previously indexed and written with GSGW; pre-existing non-indexed gzip files cannot be used.

## Evidence

- [other] Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object based on the element tag.: "Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object based on the element tag."
- [other] Implement the __getitem__ method to accept an integer index and retrieve the corresponding chapter/spectrum from the indexed gzip file.: "Implement the __getitem__ method to accept an integer index and retrieve the corresponding chapter/spectrum from the indexed gzip file."
- [intro] access the chapters conveniently by the python bracket notation ([]): "access the chapters conveniently by the python bracket notation ([])"
- [other] import xml.etree.ElementTree as et: "import xml.etree.ElementTree as et"
- [readme] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data: "pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data"
