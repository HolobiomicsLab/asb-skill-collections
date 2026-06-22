---
name: spectral-database-integration-and-sampling
description: Use when you need to generate synthetic LC/GC-MS feature tables or raw mzML files with realistic peak complexity, ion multiplicities, and natural spectral variation—not just theoretical m/z values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3812
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3172
  tools:
  - R
  - mzrtsim
  - enviGCMS
  - xml2
  - simmzml
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager") BiocManager::install("mzrtsim")
- github.com__yufree__mzrtsim
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrtsim_cq
    doi: 10.1021/acs.analchem.5c01213
    title: mzrtsim
  dedup_kept_from: coll_mzrtsim_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01213
  all_source_dois:
  - 10.1021/acs.analchem.5c01213
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-database-integration-and-sampling

## Summary

Load experimental mass spectrometry spectral databases (MoNA, HMDB) and probabilistically sample compounds and their fragmentation patterns to seed realistic LC/GC-MS data simulation. This skill bridges real spectral repositories to synthetic peak generation, ensuring simulated data retains structural and chemical complexity of observed MS1 spectra.

## When to use

You need to generate synthetic LC/GC-MS feature tables or raw mzML files with realistic peak complexity, ion multiplicities, and natural spectral variation—not just theoretical m/z values. Trigger: you have access to MoNA (MassBank of North America) or HMDB (Human Metabolome Database) spectral export files and want simulated data to reflect observed fragmentation patterns, isotope clusters, and adduct diversity rather than simple formula-predicted peaks.

## When NOT to use

- You already have a validated, custom spectral library in native mzML/mzXML format and do not need to integrate public databases.
- Your simulation goal is to test only theoretical isotope patterns or formula-based fragmentation; you do not need empirical spectral complexity.
- You are working with targeted assays where peaks are pre-identified and you only need to simulate intensity variation, not spectral multiplicity.

## Inputs

- MoNA msp export file (LC-MS Spectra format)
- HMDB GC-MS XML export (Experimental spectra)
- Parsed spectral database R list (msp or custom.RDS)
- Compound selection criteria: name, inchikey, or random index

## Outputs

- Filtered spectral database (R list, MS1 only, instrument-specific subset)
- Sampled compound records with m/z–intensity spectra
- Ready-to-use database object for simmzml() or mzrtsim() (e.g. monams1, monahrms1, hmdbcms)

## How to apply

Load a spectral database (MoNA in msp format or HMDB GC-MS XML export) into R using `getMSP()` from enviGCMS or custom XML parsing. Filter the database to retain MS1 entries only and subset by instrument type (e.g., HRMS instruments containing 'FT' or 'TOF' in instrument name). For each compound selected (by random sampling, name lookup, or inchikey match), extract the stored m/z–intensity pairs from the `spectra` field of the database record. These real spectral signatures replace theoretical predictions and are passed to `simmzml()` or `mzrtsim()` to generate synthetic chromatograms and feature tables. The resulting simulated data inherits the complexity of soft ionization (fragment ions, adducts, redundant peaks) and baseline matrix effects observed in the original spectral database, providing a more realistic benchmark for method development and validation.

## Related tools

- **enviGCMS** (Parse MoNA msp spectral exports into R list structures; filter MS1 records and subset by instrument type)
- **xml2** (Parse HMDB GC-MS experimental spectra XML files; extract m/z, intensity, retention index, precursor mass, and metadata fields)
- **simmzml** (Accept sampled spectral database records and generate realistic mzML files with chromatographic peak shapes, noise, and matrix background) — https://github.com/yufree/mzrtsim
- **mzrtsim** (Accept filtered database as db parameter to generate feature tables with controlled condition and batch effects from sampled spectral signatures) — https://github.com/yufree/mzrtsim

## Examples

```
msp <- enviGCMS::getMSP('MoNA-export-LC-MS_Spectra.msp'); idx <- sapply(msp, function(x) grepl('MS1', x$msm)); monams1 <- msp[sapply(idx, length) > 0]; simmzml(db=monams1, name='test')
```

## Evaluation signals

- Spectral database list contains all required fields: name, ionmode, prec (precursor m/z), formula, inchikey, np (number of peaks), spectra (m/z–intensity pairs), and instrument metadata.
- Filtered database retains only MS1 records (msm field == 'MS1'); non-MS1 entries are removed.
- Instrument-specific subset (e.g. monahrms1) contains only records with 'FT' or 'TOF' in instr field and median peak count ≥ threshold (article reports median ~77 peaks for MoNA HRMS).
- Compound lookup by name or inchikey returns correct record(s) with matching metadata and non-zero spectra intensities.
- Generated mzML files contain m/z, retention time, and simulated intensity values that match sampled spectral signatures (verifiable via accompanying CSV ground-truth files).

## Limitations

- MoNA msp files require manual download from https://mona.fiehnlab.ucdavis.edu/downloads and local parsing; no direct API integration.
- HMDB GC-MS XML requires download of full 'Experimental' spectra subset; parsing is compute-intensive for large libraries (multicore processing recommended).
- Database filtering (MS1 only, instrument type) can drastically reduce library size; users must verify post-filter record counts to ensure sufficient sampling diversity.
- Sampled compounds retain only the spectral signatures stored in the database; absent or rare adducts/fragments will not be generated.
- No automatic validation that selected spectral database is compatible with intended ionization mode (ESI, EI, APCI, etc.) or instrument class (HRMS vs low-resolution).

## Evidence

- [readme] MS1 full scan data has been proved more complex than theoretical prediction. Recently study showed that soft ionization will also contain fragment ions for structure identification and contain lots of redundant peaks.: "MS1 full scan data has been proved more complex than theoretical prediction. Recently study showed that soft ionization will also contain fragment ions for structure identification and contain lots"
- [intro] produces `.mzML` files from real spectral databases (MoNA, HMDB), with realistic chromatographic peak shapes, tailing, noise, and matrix background: "produces `.mzML` files from real spectral databases (MoNA, HMDB), with realistic chromatographic peak shapes, tailing, noise, and matrix background"
- [readme] idx2 <- sapply(monams1, function(x) grepl('MS1',x$msm)) / monams1 <- monams1[idx2]: "idx2 <- sapply(monams1, function(x) grepl('MS1',x$msm)) and monams1 <- monams1[idx2] filters to MS1 only"
- [readme] monams13 <- monams12[grepl('FT|TOF',idx5)] subsets database to HRMS instruments: "monams13 <- monams12[grepl('FT|TOF',idx5)] subsets database to HRMS instruments"
- [readme] To select certain compound for review/simulation, you could use name or inchikey.: "To select certain compound for review/simulation, you could use name or inchikey."
