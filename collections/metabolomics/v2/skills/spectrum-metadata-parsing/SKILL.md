---
name: spectrum-metadata-parsing
description: Use when a user submits one or more MS/MS spectra (via .mgf file, USI list, or direct upload) and the downstream analysis requires dispatching to a specific domain-specific MASST tool (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, or metadataMASST).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3071
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
  - Fast Search API
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
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  - build: coll_microbemasst
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst
schema_version: 0.2.0
---

# spectrum-metadata-parsing

## Summary

Extract and validate domain-context metadata from user-submitted mass spectra to enable conditional routing to the appropriate domain-specific MASST application. This skill bridges raw spectrum input and domain-aware search by parsing taxonomic, sample-type, or knowledge-domain annotations embedded in spectral data.

## When to use

Apply this skill when a user submits one or more MS/MS spectra (via .mgf file, USI list, or direct upload) and the downstream analysis requires dispatching to a specific domain-specific MASST tool (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, or metadataMASST). Use it when domain context is present in spectrum metadata (e.g., NCBI taxonomy IDs, sample origin annotations) but must be explicitly extracted and validated before routing.

## When NOT to use

- Spectrum is already pre-sorted into a single domain-specific MASST queue (metadata parsing has already occurred upstream).
- Input is a pre-computed batch search result (e.g., _matches.tsv, _library.tsv, or _count_domain.tsv files); skip directly to result aggregation.
- User has explicitly selected a single domain-specific MASST tool and no domain ambiguity exists in the input.

## Inputs

- MS/MS spectrum file (.mgf format from MZmine or GNPS molecular networking)
- USI list (.csv or .tsv containing Universal Spectrum Identifiers)
- Spectrum metadata fields (NCBI taxonomy IDs, sample origin, organism annotations)
- Domain lineage reference tables (NCBI taxonomy coverage per domain-specific MASST)

## Outputs

- Parsed domain-context label (microbial, plant, tissue, microbiome, food, or metadata-aggregated)
- Validated metadata subset conforming to target domain-specific MASST scope
- Routing decision (target web application endpoint or Fast Search API job configuration)
- Search parameter set tailored to the routed domain

## How to apply

Parse spectrum file headers and metadata fields to extract domain-context selectors—such as organism kingdom, phylum, or sample type (microbial, plant, tissue, microbiome, food, or aggregated metadata). Validate extracted metadata against the lineage tables and scope definitions for each domain-specific MASST (e.g., microbeMASST covers 8 kingdoms, 20 phyla, 1379 species; plantMASST covers 1 kingdom, 11 classes, 3712 species). If metadata is ambiguous or missing, apply a fallback strategy (e.g., user prompt, metadataMASST aggregation, or rejection). Pass validated domain context to the conditional routing logic that maps it to the correct standalone web application endpoint or Fast Search API call. Adjust search parameters (cosine score threshold, m/z tolerance, minimum matching peaks) according to domain-specific recommendations before submitting to the routed tool.

## Related tools

- **GNPS_MASST** (Underlying code repository and runtime environment for all six domain-specific MASST standalone web applications; provides conditional routing logic and Fast Search API integration) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (Domain-specific target for microbial spectra (8 kingdoms, 20 phyla, 1379 species coverage); routed to when metadata indicates microbial origin) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific target for plant spectra (1 kingdom, 11 classes, 3712 species coverage); routed to when metadata indicates plant origin) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific target for tissue/organism spectra; routed to when sample type indicates eukaryotic tissue origin) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific target for microbiome-sourced spectra; routed to when sample origin indicates multi-organism community context) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific target for food and food-associated spectra; routed to when sample type indicates food origin) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (Aggregation and visualization target when domain context is ambiguous or when aggregated results across all domains are desired) — https://masst.gnps2.org/metadatamasst/
- **Fast Search API** (Batch search engine invoked via jobs.py; executes spectrum-to-library matching across GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN indexed data) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (Batch execution and metadata routing orchestrator; parses input spectra, applies search parameters, and dispatches to multiple domain-specific MASSTs) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py

## Examples

```
python code/jobs.py  # After adding entries to files list as ("input_dir/spectrum.mgf", "output_dir/prefix") and setting cosine_score=0.7, mz_tolerance=0.1, min_peaks=6; re-run until skip_existing=True yields no new outputs
```

## Evaluation signals

- Extracted domain-context label is present in exactly one of: {microbial, plant, tissue, microbiome, food, metadata-aggregated}; no ambiguous or null values remain after parsing.
- Extracted NCBI taxonomy IDs (if present) match entries in the lineage table of the target domain-specific MASST tool (e.g., microbeMASST lineages folder for microbes).
- Spectrum is successfully routed to the correct web application endpoint as evidenced by job submission logs or API response codes (HTTP 200 for valid domain context).
- Batch search parameters (cosine score, m/z tolerance, minimum peaks) conform to domain-specific conventions documented in the routed tool (e.g., default thresholds used in published studies).
- Output files generated match the expected set for the routed domain (_microbe.html, _plant.json, _counts_domain.tsv, etc.); presence and absence patterns confirm correct routing decision.

## Limitations

- Metadata extraction is dependent on spectrum file format compliance and completeness; malformed or missing metadata fields may trigger fallback to metadataMASST aggregation rather than precise routing.
- The six domain-specific MASSTs have non-overlapping lineage scope (e.g., microbeMASST and plantMASST do not share taxonomy coverage); a single spectrum with mixed (e.g., microbe + plant) origins cannot be routed to both simultaneously via this skill alone.
- Fast Search API failures during batch runs require re-execution of jobs.py multiple times with skip_existing=True flag; transient API failures may cause incomplete metadata parsing on first attempt.
- Python 3.10 is required for jobs.py execution; version mismatches will prevent metadata parsing and routing steps from completing.

## Evidence

- [other] Parse user-submitted spectrum metadata and extract the domain-context selection (e.g., microbial, plant, tissue, microbiome, food, or metadata aggregation).: "Parse user-submitted spectrum metadata and extract the domain-context selection (e.g., microbial, plant, tissue, microbiome, food, or metadata aggregation)"
- [readme] The six domain-specific MASSTs allow users to search one spectrum at a time with different taxonomic or sample-type scopes.: "standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
- [readme] microbeMASST and plantMASST lineage coverage defines the scope of metadata validation.: "microbeMASST | 8 | 20 | 48 | 124 | 278 | 561 | 1379 | 542 |\n| plantMASST | 1 | 1 | 11 | 81 | 319 | 1796 | 3712 | NA |"
- [readme] jobs.py accepts .mgf files, GNPS molecular networking outputs, and USI lists as spectrum input formats.: "You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs provided either via a .csv or .tsv file"
- [readme] Batch search requires parameter tuning and re-runs until no new output is generated.: "Make sure to run jobs.py a couple of times, until no new output is generated by having the option: skip_existing=True"
