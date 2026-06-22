---
name: inchikey-extraction-from-spectral-library
description: Use when you have a GNPS DBResult file from spectral library matching that lacks ClassyFire superclass, class, and subclass columns, and you need to restore chemical ontology annotations by submitting compound identifiers to external batch classification services for re-annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0622
  tools:
  - GNPS
  - ClassyFire Batch
  - pandas
  - ConCISE
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- Currently GNPS has stopped supplying classyfire ontology information for spectral library matches
- Currently GNPS has stopped supplying classyfire ontology information for spectral library matches.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_concise_cq
    doi: 10.3390/metabo12121275
    title: ConCISE
  dedup_kept_from: coll_concise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12121275
  all_source_dois:
  - 10.3390/metabo12121275
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# inchikey-extraction-from-spectral-library

## Summary

Extract InChIKey identifiers from GNPS DBResult spectral library match files to enable batch chemical classification lookup via external services like ClassyFire when GNPS no longer supplies ontology annotations automatically. This skill bridges the gap between spectral matching and structural taxonomy assignment.

## When to use

You have a GNPS DBResult file from spectral library matching that lacks ClassyFire superclass, class, and subclass columns, and you need to restore chemical ontology annotations by submitting compound identifiers to external batch classification services for re-annotation.

## When NOT to use

- GNPS DBResult file already contains superclass, class, and subclass columns — re-annotation is redundant.
- Your compounds lack valid InChIKeys (e.g., from very novel or unstructured metabolites not in any chemical database).
- You require real-time, per-query classification rather than batch processing — ClassyFire Batch is optimized for bulk submissions and may incur delays.

## Inputs

- GNPS DBResult file (TSV/CSV with InChIKey column)
- List of InChIKeys (extracted from DBResult file)

## Outputs

- Extracted InChIKey list (text, CSV, or TSV format)
- ClassyFire batch results table (CSV/TSV indexed by InChIKey with superclass, class, subclass columns)
- Augmented GNPS DBResult file with merged ClassyFire ontology columns

## How to apply

Load the GNPS DBResult file using pandas and extract the InChIKey column, which serves as the stable compound identifier. Export or copy the InChIKey list to a format compatible with batch submission (typically comma- or newline-separated text, or direct copy-paste into a web form). Submit the InChIKeys to the Fiehn Labs ClassyFire Batch identifier service at cfb.fiehnlab.ucdavis.edu. Parse the returned CSV/TSV results, which will include superclass, class, and subclass ontology assignments indexed by InChIKey. Merge these columns back into your original DBResult file using InChIKey as the join key, ensuring column names match the expected format (superclass, class, subclass) for downstream use in ConCISE or similar consensus tools.

## Related tools

- **GNPS** (source of spectral library match results and DBResult files containing InChIKey identifiers) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ClassyFire Batch** (batch chemical classification service that accepts InChIKeys and returns superclass, class, and subclass ontology assignments) — https://cfb.fiehnlab.ucdavis.edu/
- **pandas** (Python library for loading, extracting, and merging DBResult dataframes)
- **ConCISE** (downstream consensus classification tool that uses the re-annotated DBResult file with ClassyFire ontologies) — https://github.com/Zquinlan/conCISE

## Evaluation signals

- InChIKey column successfully extracted from GNPS DBResult file with no null values in the output list.
- ClassyFire Batch submission completes without HTTP errors; returned results table contains one row per unique InChIKey with non-null superclass, class, and subclass values.
- Merge operation joins all InChIKeys from the original DBResult with ClassyFire results; row count post-merge equals row count pre-merge (no loss due to join).
- Column names in augmented DBResult exactly match expected schema (superclass, class, subclass) for downstream ConCISE or consensus workflow ingestion.
- Spot-check 5–10 randomly selected compounds: verify that returned ClassyFire ontology assignments are semantically reasonable for known metabolite structures.

## Limitations

- InChIKey extraction depends on GNPS DBResult file containing a valid, populated InChIKey column; files from older GNPS workflows or custom formats may not have this field.
- ClassyFire Batch service availability and response time are external dependencies; batch submissions may be rate-limited or temporarily unavailable.
- InChIKeys that do not exist in the ClassyFire database will return no classification; such rows must be manually handled or filtered post-merge.
- Merging by InChIKey assumes InChIKeys are globally unique and stable across GNPS and ClassyFire services; mismatches or whitespace differences can cause join failures.

## Evidence

- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches"
- [readme] You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier: "You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier"
- [readme] Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file in place of the libraryID.: "Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file"
- [other] Load the GNPS DBResult file and extract the InChIKey column using pandas. Copy or export the InChIKey list to a format suitable for batch submission to Fiehn Lab ClassyFire Batch identifier service. Submit the InChIKeys to the Fiehn Lab ClassyFire Batch database and retrieve the superclass, class, and subclass taxonomy for each InChIKey. Parse the ClassyFire batch results into a structured table (CSV or TSV) indexed by InChIKey. Merge the superclass, class, and subclass columns from the ClassyFire results back into the original DBResult file using InChIKey as the join key.: "Load the GNPS DBResult file and extract the InChIKey column using pandas. Copy or export the InChIKey list to a format suitable for batch submission to Fiehn Lab ClassyFire Batch identifier service."
