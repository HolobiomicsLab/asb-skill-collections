---
name: routing-module-testing-and-validation
description: Use when when you have implemented conditional routing logic in the GNPS_MASST codebase and need to verify that spectrum submissions with explicit domain-context selections (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
  - jobs.py
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_microbemasst
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst
schema_version: 0.2.0
---

# routing-module-testing-and-validation

## Summary

Validate that conditional routing logic correctly maps user-submitted MS/MS spectra to the appropriate domain-specific MASST application (microbe, plant, tissue, microbiome, food, or metadata) based on domain-context metadata. This skill ensures spectrum dispatch accuracy across all six standalone web applications before deployment.

## When to use

When you have implemented conditional routing logic in the GNPS_MASST codebase and need to verify that spectrum submissions with explicit domain-context selections (e.g., microbial, plant, tissue, microbiome, food metadata) are routed to the correct standalone web application endpoint without cross-domain contamination or silent routing failures.

## When NOT to use

- Input spectrum lacks explicit domain-context metadata or user selection — routing validation requires clear domain intent, not inference
- Routing module has not yet been implemented in code — this skill validates existing logic, not design or architecture
- Goal is to test batch search functionality (.mgf parsing, cosine scoring, peak matching) rather than conditional dispatch — use batch search validation instead

## Inputs

- MS/MS spectrum file (.mgf format from MZmine or GNPS molecular networking workflow)
- User-submitted spectrum with domain-context metadata field (e.g., 'DOMAIN=microbial')
- List of Uniform Spectrum Identifiers (USIs) in .csv or .tsv format with domain assignments
- Routing rule specification document defining conditional mappings between domain contexts and application endpoints

## Outputs

- Routing test report indicating pass/fail status for each domain-context → application mapping
- Log of routed spectrum IDs, declared domain context, and assigned application endpoint
- Cross-domain contamination check (verification that spectra submitted to domain A were not retrieved from domain B's indexed data)
- Application-specific results (.html, .json, .tsv files) confirming correct domain-specific search execution

## How to apply

Execute representative spectrum submissions (in .mgf or USI format) across each of the six domain-specific MASST applications with explicit domain-context metadata attached. For each test submission, verify that the routing module correctly parses the domain-context selection from spectrum metadata, applies the conditional mapping logic to select the intended application endpoint, and returns results from the correct domain-specific database. Compare the dispatched application against the declared domain context; if mismatch occurs, trace the routing rules defined in GNPS_MASST to identify which conditional branch failed. Repeat across all six domains (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST) to ensure exhaustive coverage of routing rules.

## Related tools

- **GNPS_MASST** (Source codebase containing the conditional routing logic, endpoint definitions, and integration layer for all six domain-specific MASST applications; primary artifact under test) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (One of six target routing endpoints; receives routed spectra with 'microbial' domain context) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (One of six target routing endpoints; receives routed spectra with 'plant' domain context) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (One of six target routing endpoints; receives routed spectra with 'tissue' domain context) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (One of six target routing endpoints; receives routed spectra with 'microbiome' domain context) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (One of six target routing endpoints; receives routed spectra with 'food' domain context) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (One of six target routing endpoints; receives aggregated or metadata-driven spectrum submissions for cross-domain visualization) — https://masst.gnps2.org/metadatamasst/
- **jobs.py** (Batch submission script that executes spectrum searches across all domain-specific MASSTs; useful for high-volume routing validation) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py

## Examples

```
python code/jobs.py  # with entries in the files list set to test spectra and output_prefix mapped to routing_validation_results, after setting skip_existing=True for idempotent re-runs
```

## Evaluation signals

- Routing accuracy: 100% of test spectra with declared domain context X are dispatched to application X and return domain X-specific indexed results (not results from other domains)
- Endpoint resolution: Each routed spectrum resolves successfully to the correct standalone web application URL without HTTP 404, 502, or timeout errors
- Metadata preservation: Domain-context metadata field is correctly parsed and consumed by the routing logic without data loss or truncation
- Cross-domain isolation: Spectra routed to domain A produce zero matches from domain B's curated dataset, indicating isolation of indexed data by domain
- Output consistency: All six domain-specific output formats (.html, .json, .tsv files) are generated and named with correct domain suffix (e.g., _microbe.html, _plant.json)

## Limitations

- Routing module is dependent on correct spectrum metadata submission by users; malformed or missing domain-context fields will cause routing failures that are user-side, not module-side
- Fast Search API used by jobs.py batch script may fail on some submissions; the README notes 'Due to the Fast Search API some of the entries will fail' and recommends re-running jobs.py multiple times until no new output is generated
- Testing is limited to the six currently implemented domains (microbe, plant, tissue, microbiome, food, metadata); future domain additions will require routing rule updates and re-validation
- Routing validation does not assess search quality (cosine scoring, mz tolerance, peak matching thresholds) — those are orthogonal to dispatch correctness

## Evidence

- [other] Routing module mapping: "Implement conditional routing logic that maps domain context to the corresponding standalone web application endpoint or module."
- [other] Six domain-specific targets: "Validate routing rules against all six domain-specific MASST applications defined in the GNPS_MASST repository."
- [other] Test execution across domains: "Test routing module with representative spectrum submissions across each domain to confirm correct application dispatch."
- [readme] Standalone application architecture: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
- [readme] Domain list enumeration: "This includes microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST. Aggregated search outputs can be generated and visualized using metadataMASST."
- [readme] Batch search input formats: "You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs provided either via a .csv or .tsv file."
- [readme] API failure and retry pattern: "Due to the Fast Search API some of the entries will fail. Nevertheless sequent re-runs should catch all the possible matches."
