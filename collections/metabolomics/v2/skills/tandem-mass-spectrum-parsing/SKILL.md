---
name: tandem-mass-spectrum-parsing
description: Use when when you have raw or instrument-native tandem mass spectrometry data (MS/MS) in formats such as mzML, mzXML, or proprietary binary formats, and you need to align, match, or compare spectra using methods like SIMILE that require structured access to precursor m/z, fragment m/z values, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SIMILE
  - Python
derived_from:
- doi: 10.1038/s41467-022-30118-9
  title: SIMILE
evidence_spans:
- SIMILE (Significant Interrelation of MS/MS Ions via Laplacian Embedding) is a Python library
- is a Python library for interrelating fragmentation spectra with significance estimation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_simile_cq
    doi: 10.1038/s41467-022-30118-9
    title: SIMILE
  dedup_kept_from: coll_simile_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-022-30118-9
  all_source_dois:
  - 10.1038/s41467-022-30118-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-mass-spectrum-parsing

## Summary

Parse and extract structural information from tandem mass spectra (MS/MS data) to recover precursor mass, fragment ion m/z values, and intensity values in a format compatible with spectrum alignment and matching workflows. This is a prerequisite step for similarity computation and statistical significance testing in fragmentation spectrum analysis.

## When to use

When you have raw or instrument-native tandem mass spectrometry data (MS/MS) in formats such as mzML, mzXML, or proprietary binary formats, and you need to align, match, or compare spectra using methods like SIMILE that require structured access to precursor m/z, fragment m/z values, and peak intensities for each spectrum.

## When NOT to use

- Input is already parsed and available as a pre-formatted feature matrix or similarity matrix (e.g., cosine similarity scores between spectra).
- You have only aggregate or metadata about spectra without access to raw m/z and intensity values.
- The analysis focuses on protein sequence alignment or genomic data rather than mass spectrometry fragmentation patterns.

## Inputs

- Tandem mass spectra in mzML or compatible format
- Spectrum objects with precursor m/z and fragment ion peaks
- Raw MS/MS data files from mass spectrometry instruments

## Outputs

- Parsed spectrum objects indexed by spectrum identifier
- Structured table or array of precursor m/z values
- Structured table or array of fragment ion m/z and intensity pairs
- Spectrum metadata (instrument source, acquisition parameters)

## How to apply

Load the input MS/MS data into a spectrum object or data structure compatible with SIMILE (e.g., mzML format or SIMILE's internal spectrum representation). Extract the precursor mass (m/z and optional charge state) and the list of fragment ion m/z and intensity pairs for each spectrum. Validate that all required fields are present and numeric. The parsed spectra are then indexed by spectrum identifier and stored in a format that supports efficient random access and bulk operations (e.g., NumPy arrays, pandas DataFrames, or SIMILE's native structures). This structured representation enables downstream mass difference counting, fragment ion matching, and significance testing.

## Related tools

- **SIMILE** (Loads and processes parsed spectrum objects; computes mass difference counts and fragment ion matching on structured spectrum data) — https://github.com/biorack/simile
- **Python** (Programming language and ecosystem for implementing parsing workflows and interfacing with SIMILE)

## Examples

```
import simile as sml; S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=tolerance)
```

## Evaluation signals

- All spectrum objects contain non-null precursor m/z values and at least one fragment ion m/z-intensity pair.
- Fragment ion m/z values are numeric, positive, and typically range from ~50 to the precursor m/z.
- Spectrum identifiers are unique and enable consistent indexing across downstream matching and scoring steps.
- Downstream mass difference counting and fragment ion matching produce consistent results across multiple runs (reproducibility).
- Parsed spectra can be used to generate a similarity matrix via SIMILE without errors or missing data exceptions.

## Limitations

- Parser must handle multiple MS/MS file formats (mzML, mzXML, vendor-specific binary); format-specific quirks may require conditional logic.
- Parsing speed and memory usage scale with the number and size of spectra; very large spectral libraries may require streaming or chunked processing.
- Spectrum quality depends on instrument calibration and settings; uncalibrated m/z values or noisy baseline can degrade downstream alignment accuracy.
- Some instrument formats do not consistently report intensity or charge state; missing or default values may reduce the robustness of subsequent matching.

## Evidence

- [other] Load input tandem mass spectra (MS/MS data) in a format compatible with SIMILE (e.g., mzML or internal spectrum objects).: "Load input tandem mass spectra (MS/MS data) in a format compatible with SIMILE (e.g., mzML or internal spectrum objects)."
- [other] Extract precursor mass and fragment ion m/z values from each spectrum.: "Extract precursor mass and fragment ion m/z values from each spectrum."
- [other] Load two tandem mass spectra (query and reference) with precursor m/z and fragment ion peaks.: "Load two tandem mass spectra (query and reference) with precursor m/z and fragment ion peaks."
- [readme] SIMILE (Significant Interrelation of MS/MS Ions via Laplacian Embedding) is a Python library for interrelating fragmentation spectra: "SIMILE (Significant Interrelation of MS/MS Ions via Laplacian Embedding) is a Python library for interrelating fragmentation spectra"
