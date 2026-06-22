---
name: inchikey-identifier-normalization
description: Use when gNPS has stopped supplying ClassyFire ontology information for spectral library matches (as of the ConCISE documentation snapshot) and you need to manually retrieve chemical classifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3307
  tools:
  - SIRIUS
  - NPClassifier
  - GNPS
  - Fiehn Labs ClassyFire Batch
  - ConCISE
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]
- use NPClassifier instead of ClassyFire by checking the box in the GUI
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# inchikey-identifier-normalization

## Summary

Normalize and standardize InChIKey identifiers extracted from spectral library match results to enable cross-referencing with external chemical classification databases. This skill is essential when GNPS library matches lack embedded ontology data and manual ClassyFire enrichment is required.

## When to use

Apply this skill when GNPS has stopped supplying ClassyFire ontology information for spectral library matches (as of the ConCISE documentation snapshot) and you need to manually retrieve chemical classifications. Specifically, use it after extracting InChIKey values from GNPS DBResult files and before submitting them to the Fiehn Labs ClassyFire Batch identifier service for ontology enrichment.

## When NOT to use

- GNPS library match data already includes embedded ClassyFire or NPClassifier ontology columns — use NPClassifier flag instead.
- Input identifiers are not InChIKeys but rather other chemical identifiers (SMILES, CAS numbers, compound names) — those require different normalization logic.
- Your workflow does not require consensus classification across in silico and library match sources — ConCISE's full pipeline is unnecessary.

## Inputs

- GNPS DBResult file (spectral library match output)
- InChIKey identifier list (extracted from DBResult file)

## Outputs

- Normalized InChIKey identifier list
- GNPS DBResult file enriched with ClassyFire ontology columns (superclass, class, subclass)

## How to apply

Extract InChIKey identifiers from the GNPS DBResult file output of spectral library matching. Normalize the identifiers to ensure consistency in format and remove duplicates. Submit the normalized InChIKey list to the Fiehn Labs' ClassyFire Batch service (https://cfb.fiehnlab.ucdavis.edu/). Retrieve the resulting ClassyFire ontology classifications (superclass, class, subclass columns). Merge the retrieved ontology data back into the original GNPS DBResult file using InChIKey as the join key, ensuring column names match ConCISE's expected schema (superclass, class, subclass). This enriched file can then be used as the libraryID input to ConCISE's consensus classification workflow.

## Related tools

- **GNPS** (Source of spectral library matches and DBResult files containing InChIKey identifiers) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **Fiehn Labs ClassyFire Batch** (External service for batch retrieval of ClassyFire ontology classifications indexed by InChIKey) — https://cfb.fiehnlab.ucdavis.edu/
- **ConCISE** (Downstream tool that consumes the enriched DBResult file with normalized InChIKey-linked ontologies) — https://github.com/Zquinlan/conCISE

## Evaluation signals

- All InChIKey values in the extracted list are present, non-null, and follow the standard InChIKey format (27-character alphanumeric strings with hyphens).
- No duplicate InChIKeys remain in the normalized list after deduplication.
- Successfully matched InChIKeys from the enriched file correspond 1:1 with rows in the original GNPS DBResult file.
- Retrieved ClassyFire ontology columns (superclass, class, subclass) contain non-null values for >95% of matched InChIKeys, indicating successful batch lookup.
- The enriched DBResult file can be loaded into ConCISE without schema or column-name errors, confirming proper alignment with ConCISE's expected input structure.

## Limitations

- Batch submission to Fiehn Labs ClassyFire service may fail or timeout for very large InChIKey lists (threshold not specified in documentation).
- Some InChIKeys may not have corresponding entries in the ClassyFire database, resulting in missing ontology data for those compounds.
- InChIKey normalization relies on correct extraction from the GNPS DBResult file; if the DBResult format changes or identifiers are corrupted, normalization cannot recover them.
- Manual re-merging of ClassyFire results into the original DBResult file introduces risk of column misalignment or row offset errors if not performed carefully.

## Evidence

- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches"
- [readme] You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier: "You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier"
- [readme] Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass): "Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass)"
- [readme] you can use this file in place of the libraryID: "you can use this file in place of the libraryID"
