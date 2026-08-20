---
name: compound-identifier-mapping
description: Use when after filtering a peak table to remove mispicked ions, group
  contaminants, and low-replicability features, you have a curated feature list with
  m/z, retention time, and MS/MS spectra ready for annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS-DIAL
  - mpactr
  - MPACT
  - Progenesis
  techniques:
  - LC-MS
  - NMR
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  dedup_kept_from: coll_mpactr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-identifier-mapping

## Summary

Map filtered MS/MS features to external chemical databases (e.g., GNPS, spectral libraries) to assign putative compound identities and retrieve structural, spectroscopic, and chemical annotation data. This skill bridges the gap between feature-level filtering and biological interpretation by connecting m/z and MS/MS fragmentation patterns to known metabolites.

## When to use

After filtering a peak table to remove mispicked ions, group contaminants, and low-replicability features, you have a curated feature list with m/z, retention time, and MS/MS spectra ready for annotation. Apply this skill when you need to convert abstract features (identified only by mass and retention time) into named compounds with structural and chemical context for downstream metabolite profiling, comparative genomics, or biological hypothesis generation.

## When NOT to use

- Input peak table has not been filtered for mispicked ions, group contaminants, or low-replicability features; unfiltered features will inflate false-positive identifications and downstream noise.
- MS/MS spectra are unavailable or of poor quality (low signal-to-noise ratio, fragmentation patterns inconsistent with precursor mass); spectral matching will be unreliable.
- No reference database or spectral library is available that matches your sample type or biological matrix; identifications cannot be made.

## Inputs

- Filtered mpactr object (data.table with compound IDs, m/z, retention time, MS/MS spectra, and abundance across samples)
- Peak table in GNPS, Progenesis, or MS-DIAL format
- MS/MS fragmentation patterns (m/z-intensity pairs)
- Sample metadata (group assignments, sample type)

## Outputs

- Annotated feature table with compound names, database identifiers, and spectral match scores
- CSV or TSV file with columns: feature ID, m/z, retention time, putative compound name, database source, cosine similarity or match score, SMILES, molecular weight
- Filtered database hit table stratified by kingdom and genus (optional)

## How to apply

Load the filtered mpactr object (output from chained filter operations: mispicked, group, cv, insource) and export the feature table in a format compatible with external databases (e.g., GNPS peak table format for MS-DIAL or Progenesis input). Use the mpactr or MPACT interface to submit MS/MS spectra (m/z, intensity pairs) and metadata (sample group, abundance patterns) to spectral matching services; alternatively, filter database hits by taxonomic or chemical domain criteria (kingdom, genus) to prioritize relevant annotations. Evaluate matches based on cosine similarity or spectral match score thresholds; only accept high-confidence hits (e.g., cosine > 0.7 or vendor-specific score cutoffs) to minimize false-positive identifications. Integrate matched compound metadata (SMILES, molecular weight, InChI, known biological roles) back into the feature table for statistical and pathway analysis.

## Related tools

- **GNPS (Global Natural Products Social Molecular Networking)** (Cloud-based spectral matching and networking service for MS/MS data; enables database hit filtering by taxonomy and retrieval of compound annotations and mass spectral similarity networks)
- **MS-DIAL** (Peak detection and deconvolution software that supports MSP file export and spectral matching; produces GNPS-compatible peak tables)
- **mpactr** (R package for quality filtering of MS1 features before annotation; exports filtered feature tables in formats compatible with GNPS and database services) — https://github.com/mums2/mpactr
- **MPACT** (Python/Spyder GUI for peak table preprocessing, filtering, and annotation; supports database hit filtering by kingdom and genus, and MSP file writer for in-source fragmentation patterns) — https://github.com/BalunasLab/mpact
- **Progenesis** (Commercial metabolomics software; produces peak tables importable into mpactr and exportable to spectral databases for compound annotation)

## Examples

```
# After filtering, export annotated table: data_filtered |> qc_summary() -> summary_table; write.csv(summary_table, 'filtered_compounds.csv'); # Submit peak table to GNPS for database matching via mpactr export or directly via GNPS web interface with FBMN workflow
```

## Evaluation signals

- Annotated feature table contains no null or missing values in compound name, database ID, and match score columns for accepted hits.
- Spectral match scores (cosine similarity or vendor metric) exceed a predefined threshold (e.g., cosine > 0.7) for all retained identifications; visual inspection of a subset of matched spectra confirms fragment pattern alignment with expected MS/MS behavior.
- Assigned compound names are chemically and biologically consistent with sample context (e.g., secondary metabolites expected from Streptomyces cultures, not human metabolites).
- Molecular weight of identified compounds aligns with observed m/z and adduct assignment (e.g., [M+H]+ for positive mode); mass discrepancy < 5 ppm or vendor tolerance.
- Kingdom and genus filtering (if applied) removes implausible matches; remaining annotations cluster by expected taxonomic origin or biosynthetic pathway.

## Limitations

- Spectral database coverage is incomplete; rare or novel metabolites may not match any entry, leaving features unannotated despite high quality.
- High-scoring false positives can occur when multiple chemically distinct compounds produce similar MS/MS fragmentation or when database entries are contaminated or mislabeled; cosine similarity alone is insufficient for confident annotation without orthogonal validation (e.g., NMR, chemical standards).
- Retention time prediction and matching are often unreliable across instruments and chromatographic methods; m/z and MS/MS matching dominate; retention time serves primarily as a disambiguation aid, not a primary matching criterion.
- In-source fragmentation and thermal degradation products may dominate MS/MS spectra, obscuring true molecular ion fragments and degrading match quality; pre-filtering with filter_insource_ions() is recommended but does not eliminate all artifacts.
- Adduct complexity (e.g., [M+Na]+, [M+K]+, [2M+H]+) in positive or negative mode can confound mass matching; manual curation of adduct assignment may be necessary for reliable annotation.

## Evidence

- [readme] The goal of mpactr is to correct for errors that occur during the pre-processing of raw tandem MS/MS data.: "The goal of mpactr is to correct for errors that occur during the pre-processing of raw tandem MS/MS data."
- [readme] Added GNPS peak table filtering functionality (experimental, only tested with FBMN export in MS-DIAL); Added filtering of database hits by kingdom and genus: "Added GNPS peak table filtering functionality (experimental, only tested with FBMN export in MS-DIAL); Added filtering of database hits by kingdom and genus"
- [methods] Visualizing each compound by m/z and retention time, and their fate during filtering may be useful to see if filters are removing features at certain retention time or m/z ranges.: "Visualizing each compound by m/z and retention time, and their fate during filtering may be useful to see if filters are removing features at certain retention time or m/z ranges."
- [methods] We will check our feature table for mispicked ions, remove solvent blank and media blanks features with a relative ion abundance > 0.01, relative to other groups, and check ions for replicability.: "We will check our feature table for mispicked ions, remove solvent blank and media blanks features with a relative ion abundance > 0.01, relative to other groups, and check ions for replicability."
- [readme] Added support for Bruker Metaboscape peak lists; Added support for MS-DIAL MSP files; Added MSP file writer to export in-source fragmentation patterns: "Added support for Bruker Metaboscape peak lists; Added support for MS-DIAL MSP files; Added MSP file writer to export in-source fragmentation patterns"
