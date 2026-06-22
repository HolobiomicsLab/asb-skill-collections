---
name: fragmentation-pattern-annotation
description: Use when when you have an experimental MS/MS spectrum (query spectrum as m/z–intensity pairs) and need to identify the compound by comparing its fragmentation pattern to a spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MASSBANK
  - DrugBANK
  - meRgeION2
  - MergeION2
  - GNPS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c04343
  title: MeRgeION
evidence_spans:
- search and annotate an unknown spectrum in their local database or public databases (i.e. drug structures in GNPS, MASSBANK and DrugBANK)
- github.com__daniellyz__meRgeION2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  dedup_kept_from: coll_mergeion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04343
  all_source_dois:
  - 10.1021/acs.analchem.2c04343
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragmentation-pattern-annotation

## Summary

Annotate unknown MS/MS spectra by matching their fragmentation patterns (m/z and intensity pairs) against spectral libraries using similarity scoring algorithms. This enables compound identification in metabolomics and pharmaceutical screening when spectra are matched to reference libraries with known metadata.

## When to use

When you have an experimental MS/MS spectrum (query spectrum as m/z–intensity pairs) and need to identify the compound by comparing its fragmentation pattern to a spectral library. Triggered by: precursor m/z is known, MS/MS fragmentation data is available in mzML/mzXML format or as extracted m/z–intensity matrix, and a reference library (local or public: GNPS, MASSBANK, DrugBANK) is accessible. Essential when confidentiality or data governance prevents use of public-only databases.

## When NOT to use

- Query spectrum is from negative-ion or mixed-polarity mode and library is positive-ion only (e.g., pre-compiled GNPS_MASSBANK_PROCESSED_POS_CONSENSUS contains 'all in positive ion mode').
- Raw data is in vendor-proprietary format (Thermo, Waters, Bruker) without prior conversion to mzML/mzXML format.
- No suitable reference library is available or library contains insufficient spectral diversity for the compound class of interest.

## Inputs

- Query MS/MS spectrum as two-column matrix (m/z, intensity pairs)
- Precursor m/z value (float, monoisotopic mass)
- Reference spectral library in GNPS format or mzML/mzXML raw chromatogram files
- Library search parameters: polarity, similarity method, min_frag_match, min_score threshold

## Outputs

- Ranked list of candidate library matches with similarity scores (Cosine or dot-product)
- Annotated spectrum metadata: compound name, molecular formula, INCHI, INCHIKEY, library accession
- Mirror plot visualization of query spectrum vs. best-matching library spectrum
- Match confidence score and number of matching fragments

## How to apply

Load or download a reference spectral library (e.g., GNPS-style local library or pre-compiled GNPS_MASSBANK_PROCESSED_POS_CONSENSUS database). Read the experimental query spectrum as a two-column matrix (m/z, intensity). Collect query parameters including precursor m/z (prec_mz), polarity, similarity method (typically Cosine), minimum fragment matches (min_frag_match, often ≥6), and minimum similarity score threshold (min_score, typically ≥0.6–0.7 for Cosine). Execute library search using cosine similarity or spectral dot-product to compute match scores between query and all candidate library spectra. Rank candidates by similarity score, filter by threshold and precursor m/z match (use_prec=TRUE for classical approach), and retrieve top-ranked hits with associated compound metadata (name, molecular formula, INCHI, accession). Validate results by visual inspection (mirror plot) and INCHIKEY confirmation against expected compound.

## Related tools

- **MergeION2** (R package that implements library search algorithms (Cosine similarity, spectral dot-product) and provides library_query() function for spectrum matching, visualization (library_visualizer), and compound annotation) — https://github.com/daniellyz/MergeION2
- **GNPS** (Public spectral library source; MergeION merges data into GNPS-style format and queries GNPS database for annotation)
- **MASSBANK** (Public spectral database source for library search; merged into pre-compiled reference libraries)
- **DrugBANK** (Public pharmaceutical structure database queried for drug compound annotation)

## Examples

```
query.sp = read.csv('example_cinnarizine.txt', header = F, sep = '\t'); params.query.sp = list(prec_mz = 369.232, use_prec = T, polarity = 'Positive', method = 'Cosine', min_frag_match = 6, min_score = 0); search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp)
```

## Evaluation signals

- Cosine similarity score is ≥0.7 (or user-defined min_score threshold) for top-ranked match, indicating high spectral concordance.
- Precursor m/z of matched library spectrum matches query precursor m/z within instrument tolerance (typically <5 ppm).
- INCHIKEY and molecular formula of top match correspond to known compound structure or expected metabolite/drug.
- Mirror plot visualization shows significant peak overlap and fragment ion matching between query and library spectra.
- Number of matching fragments (min_frag_match) exceeds threshold, typically ≥6 major peaks aligned between spectra.

## Limitations

- Annotation accuracy depends on spectral library quality, coverage, and metadata completeness; confidential in-house databases may lack sufficient reference spectra.
- Fragmentation patterns vary with ionization mode, collision energy, and instrument type; library must be acquired under comparable conditions to query spectrum.
- Isomeric compounds often produce similar fragmentation patterns, leading to ambiguous or incorrect matches; visual inspection and retention time or additional orthogonal data needed for confirmation.
- Pre-compiled spectral databases are currently restricted to positive-ion mode ESI-MS/MS; negative-ion queries require local library building from appropriate reference standards.

## Evidence

- [intro] Several library search algorithms are available, allowing users to search and annotate an unknown spectrum in their local database or public databases: "Several library search algorithms are available, allowing users to search and annotate an unknown spectrum in their local database or public databases (i.e. drug structures in GNPS, MASSBANK and"
- [other] Library search algorithm computes similarity scores using cosine similarity or spectral dot-product between query and candidate spectra: "Apply library search algorithm to compute similarity scores (e.g., cosine similarity or spectral dot-product) between query spectrum and candidate library spectra"
- [other] Matched spectra are ranked by similarity threshold and annotated with metadata: "Rank and filter matched spectra by similarity threshold to identify best-matching library entries. 5. Retrieve and annotate matched spectra with metadata (compound name, molecular formula, INCHI,"
- [readme] Pre-compiled database contains 11,642 metabolites and is positive-ion mode only: "We have pre-compiled a small molecule spectral database containing MS/MS spectra of 11,642 metabolites, natural products and drugs. The database combines public repositories such as GNPS, MassBank"
- [readme] Precursor m/z and use_prec parameter control matching strategy: "Only important parameters to check are the _prec_mz_, which indicates the precursor mass, and _use_prec_, which forces precursor mass match in the search output by setting to TRUE (the classical"
- [readme] Query spectrum should be read as a two-column matrix: "The MS/MS spectrum should be read as well into the R environment as a two-column matrix"
