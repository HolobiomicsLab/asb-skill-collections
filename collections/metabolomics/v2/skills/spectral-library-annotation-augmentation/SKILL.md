---
name: spectral-library-annotation-augmentation
description: Use when you have a GNPS DBResult file containing spectral library matches with InChIKey identifiers but lacking ClassyFire ontology columns (superclass, class, subclass), and you need to restore this taxonomic context for consensus classification or chemical ontology annotation workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3174
  tools:
  - GNPS
  - ClassyFire
  - ConCISE
  - pandas
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

# spectral-library-annotation-augmentation

## Summary

Manually restore taxonomic ontology annotations (superclass, class, subclass) to GNPS spectral library matches by batch-retrieving ClassyFire classifications for InChIKeys and merging the results back into the original DBResult file. This skill addresses the loss of automatic ClassyFire annotation supply from GNPS.

## When to use

You have a GNPS DBResult file containing spectral library matches with InChIKey identifiers but lacking ClassyFire ontology columns (superclass, class, subclass), and you need to restore this taxonomic context for consensus classification or chemical ontology annotation workflows.

## When NOT to use

- GNPS DBResult file already contains superclass, class, and subclass columns populated from automatic GNPS supply.
- Spectral library matches lack InChIKey identifiers (no stable join key available).
- You prefer to use NPClassifier ontologies instead of ClassyFire (use NPClassifier option in ConCISE GUI or set NPC argument to True).

## Inputs

- GNPS DBResult file (TSV/CSV with InChIKey column)
- InChIKey list extracted from DBResult

## Outputs

- Augmented GNPS DBResult file with superclass, class, and subclass columns
- Structured ClassyFire batch results table (indexed by InChIKey)

## How to apply

Extract the InChIKey column from the GNPS DBResult file using pandas. Submit the InChIKey list to the Fiehn Labs ClassyFire Batch identifier service (https://cfb.fiehnlab.ucdavis.edu/), which will return superclass, class, and subclass annotations indexed by InChIKey. Parse the batch results into a structured table (CSV or TSV). Merge the superclass, class, and subclass columns from the ClassyFire results back into the original DBResult file using InChIKey as the join key, ensuring the new columns are named correctly (superclass, class, subclass) to substitute for libraryID. Save the augmented DBResult file. The InChIKey serves as the stable join key across the GNPS and ClassyFire datasets.

## Related tools

- **ClassyFire** (Batch web service that retrieves superclass, class, and subclass taxonomic annotations for InChIKeys) — https://cfb.fiehnlab.ucdavis.edu/
- **GNPS** (Source spectral library database providing DBResult files with InChIKey identifiers; previously supplied ClassyFire annotations automatically) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ConCISE** (Consensus classification tool that consumes augmented DBResult files with ClassyFire ontologies to find consensus annotations) — https://github.com/Zquinlan/conCISE
- **pandas** (Python library for loading, extracting, and merging columns in DBResult files)

## Evaluation signals

- The augmented DBResult file contains three new columns (superclass, class, subclass) with no null values for rows with valid InChIKeys.
- Row count in the augmented file matches the original DBResult file (no rows dropped during merge).
- All InChIKeys in the original DBResult are present as join keys in the merged output; verify no unmatched rows remain.
- Column names in the merged file are exactly 'superclass', 'class', 'subclass' to match expected ConCISE input schema.
- Sample spot-check: pick 2–3 InChIKeys and manually verify ClassyFire batch results match the merged values.

## Limitations

- Manual workflow introduces latency compared to automatic GNPS supply; batch submission to ClassyFire web service depends on external service availability.
- InChIKey must be correctly formatted and present in the DBResult file; missing or malformed InChIKeys will not retrieve annotations.
- ClassyFire batch results are tied to the version/snapshot of the ClassyFire database at the time of submission; updates to ClassyFire ontologies will not retroactively update existing augmented files.
- Requires manual export/import steps between GNPS DBResult, ClassyFire Batch service, and merge operation; scripting with pandas is recommended to avoid errors.
- Large batch submissions (thousands of InChIKeys) may experience delays or throttling by the ClassyFire Batch web service.

## Evidence

- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches"
- [readme] You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier: "You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier"
- [readme] Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file in place of the libraryID: "Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass)"
- [other] Parse the ClassyFire batch results into a structured table (CSV or TSV) indexed by InChIKey: "Parse the ClassyFire batch results into a structured table (CSV or TSV) indexed by InChIKey"
- [other] Merge the superclass, class, and subclass columns from the ClassyFire results back into the original DBResult file using InChIKey as the join key: "Merge the superclass, class, and subclass columns from the ClassyFire results back into the original DBResult file using InChIKey as the join key"
