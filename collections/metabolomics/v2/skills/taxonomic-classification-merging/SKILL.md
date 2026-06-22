---
name: taxonomic-classification-merging
description: Use when you have a GNPS DBResult file with spectral library matches that lack ClassyFire superclass, class, and subclass annotations, and you need to augment those matches with standardized chemical taxonomy for consensus classification or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0089
  - http://edamontology.org/topic_3172
  tools:
  - GNPS
  - Fiehn Labs ClassyFire Batch
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
---

# taxonomic-classification-merging

## Summary

Restore chemical taxonomy annotations to spectral library matches by batch-retrieving ClassyFire ontologies for InChIKeys and merging superclass, class, and subclass columns back into GNPS DBResult files. This skill addresses the gap left when GNPS stopped automatically supplying ClassyFire ontology information for spectral library matches.

## When to use

Apply this skill when you have a GNPS DBResult file with spectral library matches that lack ClassyFire superclass, class, and subclass annotations, and you need to augment those matches with standardized chemical taxonomy for consensus classification or downstream analysis.

## When NOT to use

- Input DBResult file already contains populated ClassyFire superclass, class, and subclass columns — merging would create duplicates or overwrite existing annotations.
- InChIKeys are missing or malformed in the input DBResult file — batch submission requires valid InChIKey identifiers.
- Downstream workflow requires NPClassifier ontologies instead of ClassyFire — use NPClassifier batch service and reformat column names accordingly.

## Inputs

- GNPS DBResult file (TSV or CSV format with InChIKey column)
- InChIKey list (extracted or exported from DBResult file)

## Outputs

- Augmented GNPS DBResult file with added superclass, class, subclass columns
- Merged taxonomy table indexed by InChIKey

## How to apply

Extract the InChIKey column from the GNPS DBResult file using pandas or equivalent table manipulation. Submit the InChIKey list to the Fiehn Labs' ClassyFire Batch identifier service (https://cfb.fiehnlab.ucdavis.edu/), which returns a structured result table indexed by InChIKey with superclass, class, and subclass taxonomy. Parse the batch results into a structured format (CSV or TSV) and perform a join merge operation on the original DBResult file using InChIKey as the common key. Insert the retrieved superclass, class, and subclass columns into the DBResult file with correct column naming (case-sensitive: 'superclass', 'class', 'subclass'). Save the augmented file for use in downstream tools like ConCISE for consensus annotation workflows.

## Related tools

- **Fiehn Labs ClassyFire Batch** (batch retrieval service that accepts InChIKey lists and returns ClassyFire ontology annotations (superclass, class, subclass) indexed by InChIKey) — https://cfb.fiehnlab.ucdavis.edu/
- **GNPS** (source of DBResult spectral library match files containing InChIKey identifiers; no longer supplies ClassyFire ontology annotations automatically) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ConCISE** (downstream consensus classification tool that consumes augmented DBResult files with ClassyFire taxonomy columns) — https://github.com/Zquinlan/conCISE
- **pandas** (table manipulation and merge operations for extracting InChIKeys and joining ClassyFire results back into DBResult)

## Examples

```
import pandas as pd; gnps_df = pd.read_csv('GNPS_DBResult.tsv', sep='\t'); inchikeys = gnps_df['InChIKey'].tolist(); # submit inchikeys to https://cfb.fiehnlab.ucdavis.edu/, download results as classyfire_batch_results.csv; cf_df = pd.read_csv('classyfire_batch_results.csv'); merged = gnps_df.merge(cf_df[['InChIKey','superclass','class','subclass']], on='InChIKey', how='left'); merged.to_csv('GNPS_DBResult_augmented.tsv', sep='\t', index=False)
```

## Evaluation signals

- Augmented DBResult file contains exactly three new columns with names 'superclass', 'class', 'subclass' (case-sensitive) populated with non-empty values for all rows with valid InChIKeys.
- Row count of augmented file equals original DBResult file (no rows lost or duplicated during merge).
- All InChIKey values in the augmented file retain their original values and row order is preserved.
- No null or NaN values appear in the superclass, class, subclass columns for rows that had successful ClassyFire matches (check for ClassyFire batch job completion status).
- Spot-check: sample 5–10 InChIKeys from the augmented file against the Fiehn Labs ClassyFire web interface to verify returned taxonomy matches the merged values.

## Limitations

- ClassyFire Batch service may reject or fail to classify a subset of InChIKeys; failures must be handled by re-submission, filtering, or manual curation.
- InChIKey duplicates in the DBResult file will produce duplicate rows in the merged output — deduplication may be necessary before or after merging.
- Column name correctness is strict: typos or case mismatches in superclass, class, subclass column names will cause downstream tools like ConCISE to fail to recognize them.
- Fiehn Labs ClassyFire Batch service availability and response time are external dependencies; batch jobs may be queued or rate-limited.

## Evidence

- [readme] GNPS has stopped supplying ClassyFire ontology information for spectral library matches; manual workaround involves copying InChIKeys to Fiehn Labs' ClassyFire Batch identifier and merging results back with correct column names.: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI"
- [other] The manual workflow: load GNPS DBResult, extract InChIKey column, submit to ClassyFire Batch, parse results, merge by InChIKey, save augmented file.: "1. Load the GNPS DBResult file and extract the InChIKey column using pandas. 2. Copy or export the InChIKey list to a format suitable for batch submission to Fiehn Lab ClassyFire Batch identifier"
- [readme] ConCISE uses ClassyFire ontologies supplied by GNPS for library matches and in silico annotations to find consensus annotations.: "ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations."
