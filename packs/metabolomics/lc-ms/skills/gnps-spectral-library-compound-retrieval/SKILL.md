---
name: gnps-spectral-library-compound-retrieval
description: Use when you have GNPS library accession IDs (e.g. CCMSLIB00011906190) for a reference compound and a chemically or biologically modified analog, and need to load their full MS/MS spectra and structural annotations to set up a modification-finding analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ModiFinder
  - BasicEvaluationEngine
  - Python
  - RDKit
  - GNPS Library
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.4c00061
  title: ModiFinder
evidence_spans:
- mf = ModiFinder(known_compound, modified_compound, mz_tolerance=0.01, ppm_tolerance=40)
- mf = ModiFinder(known_compound, modified_compound, helpers=helpers_array, **args)
- eval_engine = BasicEvaluationEngine(default_method="is_max")
- eval_engine = BasicEvaluationEngine(default_method="average_distance")
- ModiFinder requires Python 3.9 or above.
- ModiFinder requires Python 3.9 or above
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_modifinder_cq
    doi: 10.1021/jasms.4c00061
    title: ModiFinder
  dedup_kept_from: coll_modifinder_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00061
  all_source_dois:
  - 10.1021/jasms.4c00061
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# GNPS Spectral Library Compound Retrieval

## Summary

Fetches MS/MS spectra and structural metadata (SMILES, precursor m/z, charge, adduct) for known and modified compounds from the GNPS spectral library by accession identifier. This retrieval is the essential first step for comparative tandem mass spectral alignment workflows where ground-truth structures must be loaded before modification site analysis can begin.

## When to use

You have GNPS library accession IDs (e.g. CCMSLIB00011906190) for a reference compound and a chemically or biologically modified analog, and need to load their full MS/MS spectra and structural annotations to set up a modification-finding analysis. Use this skill when you must establish baseline spectra with known, curated metadata rather than importing raw experimental data.

## When NOT to use

- Input is already a local, parsed spectrum object (e.g., .mzML or .mgf file loaded in memory) — use spectrum import instead.
- You need to search GNPS by molecular formula, mass, or structure similarity rather than by known accession ID — use GNPS network search or molecular networking tools instead.
- The compound is proprietary, unpublished, or not yet deposited in GNPS — use manual spectral entry or in-house database instead.

## Inputs

- GNPS accession ID(s) (string, format: CCMSLIB* or mzspec:GNPS:GNPS-LIBRARY:accession:*)
- Spectral filtering parameters (mz_tolerance, ppm_tolerance, ratio_to_base_peak thresholds)

## Outputs

- Compound object(s) with fields: spectrum (list of [m/z, intensity] pairs), precursor_mz (float), precursor_charge (int), adduct (string), smiles (string)
- Normalized peak list (intensity-scaled, filtered by abundance threshold)
- Structured metadata record (accession, source, collection date if available)

## How to apply

Query the GNPS library API or web interface using a compound accession ID to retrieve the spectrum (formatted as m/z–intensity peak pairs), precursor m/z, precursor charge, ionization adduct, and SMILES string. Apply spectral filtering parameters (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01) and peak normalization (normalize_peaks=True) to standardize the retrieved spectrum for downstream alignment. Instantiate a Compound object with these fields to create a queryable, structured representation suitable for ModiFinder analysis. Repeat for both the known and modified compound to establish a paired comparison set.

## Related tools

- **ModiFinder** (Consumes retrieved Compound objects as known and modified reference structures for site localization via tandem mass spectral alignment) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **GNPS Library** (Authoritative source database for MS/MS spectral and structural metadata retrieval by accession) — https://gnps.ucsd.edu/
- **RDKit** (Parses SMILES strings and enables molecular structure visualization and comparison after retrieval) — http://www.rdkit.org/
- **Python** (Programming environment for scripting accession lookups, spectrum normalization, and Compound object instantiation)

## Examples

```
# Load known and modified compounds from GNPS library
known = Compound(spectrum=s1_peaks, precursor_mz=506.2651, precursor_charge=1, adduct='[M+H]+', smiles=known_smiles)  # CCMSLIB00011906190
modified = Compound(spectrum=s2_peaks, precursor_mz=507.2730, precursor_charge=1, adduct='[M+H]+', smiles=None)  # CCMSLIB00011906105
```

## Evaluation signals

- Retrieved spectrum contains ≥1 peak and precursor_mz is non-null and positive (validates non-empty, valid spectrum record).
- Precursor charge is a positive integer (int ≥ 1) and adduct string matches common ion formats (e.g. '[M+H]+', '[M-H]-').
- SMILES string parses without error in RDKit and produces a valid molecular graph (validates structural integrity).
- Retrieved spectrum, when normalized with normalize_peaks=True and filtered by ratio_to_base_peak=0.01, contains peak intensities in [0, 1] range (validates normalization was applied).
- For paired comparisons (known + modified), both Compound objects have matching precursor_charge and compatible adduct classes (e.g. both positive or both negative), indicating compatible ionization contexts.

## Limitations

- GNPS accession IDs may become obsolete or records may be merged; no versioning guarantee is provided by the library.
- Retrieved SMILES may be missing or incorrect if the record was deposited without structural validation; external chemical database cross-referencing may be needed.
- Spectral filtering parameters (mz_tolerance, ppm_tolerance, ratio_to_base_peak) must be chosen a priori; no automated recommendation is provided for dataset-specific optimization.
- GNPS library records reflect the ionization and instrumental conditions of the original deposition; retrieved spectra may not match user's instrument settings or desired energy regime.

## Evidence

- [other] Workflow step of loading compounds from GNPS library before analysis: "Get compound from GNPS; Draw the molecule"
- [other] Specific accession IDs used in the paper's evaluation task: "Load known compound (CCMSLIB00011906190) and modified compound (CCMSLIB00011906105) from GNPS"
- [other] Spectral filtering parameters applied during retrieval: "with mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True"
- [readme] Core API for constructing Compound objects from retrieved data: "main_compound = Compound(
    spectrum=s1_peaks,                       # Formatted as [[mz, int], ...]
    precursor_mz=s1_prec_mz,                 # Float
    precursor_charge=s1_charge,"
- [intro] Purpose of spectral retrieval in modification site analysis: "ModiFinder is a tool for site localization of structural modifications using MS/MS data"
