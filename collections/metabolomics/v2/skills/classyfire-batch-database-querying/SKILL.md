---
name: classyfire-batch-database-querying
description: Use when you have a GNPS DBResult file with InChIKey identifiers but
  lack corresponding ClassyFire superclass, class, and subclass taxonomy annotations—particularly
  when GNPS spectral library matches no longer include this ontology information by
  default.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - ClassyFire
  - GNPS
  - ClassyFire Batch
  - ConCISE
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- use NPClassifier instead of ClassyFire by checking the box in the GUI
- You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire
  Batch identifier
- Currently GNPS has stopped supplying classyfire ontology information for spectral
  library matches
- Currently GNPS has stopped supplying classyfire ontology information for spectral
  library matches.
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

# ClassyFire Batch Database Querying

## Summary

Restore chemical ontology annotations (superclass, class, subclass) to GNPS spectral library matches by batch-submitting InChIKeys to the Fiehn Labs ClassyFire Batch service and merging results back into DBResult files. This skill addresses the gap created when GNPS stopped supplying ClassyFire annotations automatically.

## When to use

Use this skill when you have a GNPS DBResult file with InChIKey identifiers but lack corresponding ClassyFire superclass, class, and subclass taxonomy annotations—particularly when GNPS spectral library matches no longer include this ontology information by default.

## When NOT to use

- GNPS DBResult file already contains populated superclass/class/subclass columns from GNPS directly.
- You are working with library matches from GNPS releases where ClassyFire annotations were supplied automatically and you do not need to update them.
- Input InChIKey column is empty, malformed, or missing entirely.

## Inputs

- GNPS DBResult file (TSV or CSV)
- InChIKey column (extracted or referenced)

## Outputs

- Augmented GNPS DBResult file with ClassyFire superclass, class, subclass columns
- ClassyFire batch results table (CSV or TSV, indexed by InChIKey)

## How to apply

Extract the InChIKey column from your GNPS DBResult file using pandas or equivalent structured data tools. Export the InChIKey list to a format compatible with the Fiehn Labs ClassyFire Batch service (https://cfb.fiehnlab.ucdavis.edu/). Submit the batch and retrieve the returned superclass, class, and subclass taxonomy fields. Parse the ClassyFire results into a structured table (CSV or TSV) indexed by InChIKey. Perform a left join merge on the original DBResult file using InChIKey as the join key, ensuring correct column naming (superclass, class, subclass) to match expected schema. Verify row counts and non-null proportions in merged columns before saving the augmented file.

## Related tools

- **GNPS** (Source of DBResult files containing InChIKey identifiers and spectral library matches; the platform that previously supplied ClassyFire annotations) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ClassyFire Batch** (Batch querying service for retrieving chemical ontology (superclass, class, subclass) annotations indexed by InChIKey) — https://cfb.fiehnlab.ucdavis.edu/
- **ConCISE** (Downstream consensus classification tool that can ingest the augmented DBResult file with ClassyFire columns as input) — https://github.com/Zquinlan/conCISE

## Examples

```
# Extract InChIKeys, submit to ClassyFire Batch at https://cfb.fiehnlab.ucdavis.edu/, retrieve results, then merge back:
import pandas as pd
gnps_result = pd.read_csv('GNPS_DBResult.tsv', sep='\t')
classyfire_results = pd.read_csv('classyfire_batch_results.csv', index_col='InChIKey')
merged = gnps_result.merge(classyfire_results[['superclass', 'class', 'subclass']], left_on='InChIKey', right_index=True, how='left')
merged.to_csv('GNPS_DBResult_with_ClassyFire.tsv', sep='\t', index=False)
```

## Evaluation signals

- Row count in merged DBResult file matches input DBResult row count (no rows dropped during join).
- Merged superclass, class, and subclass columns contain non-null values for all or nearly all rows (check for unexpected NaN or empty string proportions).
- Spot-check: verify 5–10 random InChIKey→superclass/class/subclass mappings by manual lookup in ClassyFire to confirm correctness.
- Column names exactly match expected schema ('superclass', 'class', 'subclass') with no trailing whitespace or case mismatches.
- No duplicate InChIKey values in the join key; verify uniqueness before and after merge.

## Limitations

- ClassyFire Batch service may have rate limits or temporary unavailability; batch submission may fail for very large InChIKey sets.
- InChIKey format must be correct and complete; malformed or truncated keys will not match in ClassyFire and return no annotation.
- ClassyFire ontology is static at query time; changes or updates to ClassyFire taxonomy between queries are not managed by this workflow.
- The workaround is manual and labor-intensive compared to automatic GNPS annotation; recommended only when GNPS no longer supplies the data natively.

## Evidence

- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches"
- [readme] Manually pull classyfire data and copy InChiKey's from GNPS DBResult into Fiehn Labs classyfire Batch: "Manually pull classyfire data for your library match data. You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' [classyfire Batch]"
- [readme] Merge results back with correct column names and use in place of libraryID: "Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file in place of the libraryID"
- [other] Workflow steps from task card document the extraction, submission, parsing, and merge process: "Load the GNPS DBResult file and extract the InChIKey column using pandas... Parse the ClassyFire batch results into a structured table (CSV or TSV) indexed by InChIKey... Merge the superclass, class,"
