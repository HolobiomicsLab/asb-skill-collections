---
name: cross-domain-metadata-integration
description: Use when when you have conducted batch MS/MS searches across one or more
  domain-specific MASST tools and need to combine their hit scores, metadata annotations,
  and taxonomic lineages into a single coherent result set for comparative analysis
  or publication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - jobs.py
  - Fast Search API
  - GNPS_MASST
  techniques:
  - MS-imaging
  license_tier: open
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- Aggregated search outputs can be generated and visualized using metadataMASST
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_microbemasst_cq
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41564-023-01575-9
  all_source_dois:
  - 10.1038/s41564-023-01575-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-domain-metadata-integration

## Summary

Consolidates and visualizes aggregated mass spectrometry search results from multiple domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into unified metadata structures and interactive visualizations. This skill enables cross-domain interpretation of molecular matches and taxonomic/ecological overlap across curated biological repositories.

## When to use

When you have conducted batch MS/MS searches across one or more domain-specific MASST tools and need to combine their hit scores, metadata annotations, and taxonomic lineages into a single coherent result set for comparative analysis or publication. Specifically: after generating domain-specific .json/.html tree outputs from jobs.py, or when merging results from multiple domain repositories (GNPS, MassIVE, Metabolomics Workbench, Metabolights, NORMAN) and require unified visualization of cross-domain matches, sample overlap, and scoring distributions.

## When NOT to use

- Input consists of only single-domain results (i.e., only microbeMASST or only plantMASST); cross-domain integration provides no additional signal.
- You seek domain-specific curation or taxonomic filtering that metadataMASST does not expose; use individual domain-MASST web applications instead.
- Raw MS/MS spectra have not yet been searched; first run batch search via jobs.py against Fast Search API.

## Inputs

- aggregated _matches.tsv (all spectra matching results across indexed databases)
- aggregated _library.tsv (GNPS library matches for Level 2 MSI annotation)
- aggregated _datasets.tsv (unique sample counts per indexed dataset)
- per-domain _count_domain.tsv files (microbe, plant, tissue, microbiome, food)
- batch search output JSON trees from individual domainMASSTs

## Outputs

- consolidated metadata table with merged hits, scores, and lineage annotations
- interactive HTML visualization(s) of aggregated result (domain overlap, hit distribution)
- JSON structure encoding cross-domain match graph and metadata hierarchy
- domain-wise summary report (e.g., match counts, score distributions per domain)

## How to apply

Load the aggregated search outputs (typically _matches.tsv, _library.tsv, _datasets.tsv, and per-domain _count_domain.tsv files) from the batch search into metadataMASST. The tool processes and consolidates hits by merging cosine scores, m/z matches, and metadata annotations across the different domain sources. Adjust integration parameters such as minimum cosine score threshold (typically 0.6–0.7 for MS/MS) and m/z tolerance (default 0.5 Da) based on your mass spectrometry instrument resolution and biological specificity goals. Generate visualization outputs (e.g., hit distribution histograms, domain-overlap Venn diagrams, score ranking tables) and export in structured formats (interactive HTML trees, JSON for downstream processing). The rationale is that domain-specific MASSTs each curate different NCBI taxonomy lineages and sample metadata; integration reveals which molecular features are present across multiple biological domains, improving confidence in annotations and enabling ecosystem-scale metabolomics interpretation.

## Related tools

- **metadataMASST** (primary integration and visualization engine; consolidates and visualizes aggregated cross-domain search results) — https://masst.gnps2.org/metadatamasst/
- **microbeMASST** (domain-specific MASST for microbial metabolomics; produces indexed hits and taxonomic lineages for bacteria/archaea integration) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (domain-specific MASST for plant metabolomics; produces indexed hits and plant taxonomic lineages for integration) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (domain-specific MASST for tissue and organ metabolomics; produces hits and tissue metadata for cross-domain matching) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (domain-specific MASST for microbiome metabolomics; produces ecological and taxonomic metadata for integration) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (domain-specific MASST for food metabolomics; produces food source and provenance metadata for cross-domain matching) — https://masst.gnps2.org/foodmasst2/
- **jobs.py** (batch search pipeline that generates aggregated domain MASST outputs (_matches.tsv, _library.tsv, _datasets.tsv, per-domain _count_domain.tsv) for integration) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py
- **Fast Search API** (underlying search infrastructure leveraged by jobs.py to execute batch MS/MS spectrum matching against GNPS, MassIVE, Metabolomics Workbench, Metabolights, and NORMAN databases) — https://fasst.gnps2.org/fastsearch/
- **GNPS_MASST** (parent repository containing code and logic for domain-specific MASST web applications and metadataMASST integration workflows) — https://github.com/mwang87/GNPS_MASST

## Examples

```
python jobs.py --input_file batch_spectra.mgf --output_prefix results/cross_domain --min_cosine_score 0.6 --mz_tolerance 0.5 --skip_existing=True
```

## Evaluation signals

- Verify that _matches.tsv, _library.tsv, and all _count_domain.tsv files are successfully loaded and deduplicated (no duplicate spectra IDs across domains).
- Check that cosine scores are correctly merged and ranked: scores from the same spectrum matched across multiple domains should show consistent ordering within metadataMASST output.
- Confirm that domain-overlap visualizations (e.g., HTML tree or Venn diagram) show non-empty intersection sets when multiple domains report hits for the same query spectrum.
- Validate that lineage information (kingdom, phylum, class, order, family, genus, species) is preserved and correctly attributed to matched spectra in consolidated metadata.
- Inspect exported JSON structure for completeness: all input domain source labels, metadata fields, and score tuples should be present and queryable.

## Limitations

- metadataMASST assumes pre-indexed data across domain-specific MASSTs; newly submitted spectra or datasets require re-running the batch search pipeline (jobs.py) and multiple re-runs due to Fast Search API transient failures.
- Domain lineage coverage is uneven: microbeMASST currently covers ~1,379 microbial species and 542 strains; plantMASST covers ~3,712 plant species but no strains; tissue and microbiome/food MASST lineage depths are not quantified in the article.
- Cross-domain integration does not perform de novo curation or conflict resolution: if the same spectrum is annotated with conflicting taxonomic assignments across domains, metadataMASST surfaces all annotations without algorithmic prioritization.
- Batch search performance and completeness depend on Fast Search API availability; retry logic (skip_existing=True) is recommended but not guaranteed to catch all matches in a single execution.

## Evidence

- [other] metadataMASST takes aggregated search outputs from domain-specific MASSTs... and generates visualized aggregated results: "metadataMASST takes aggregated search outputs from domain-specific MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST) and generates visualized aggregated results as its"
- [other] Process and consolidate search results using metadataMASST to merge hits, scores, and metadata across domain sources: "Process and consolidate search results using metadataMASST to merge hits, scores, and metadata across domain sources."
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST."
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN and generate multiple outputs for all listed domainMASSTs simultaneously: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed."
- [readme] Make sure to run jobs.py **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`. Due to the Fast Search API some of the entries will fail.: "Make sure to run jobs.py **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`. Due to the Fast Search API some of the entries will fail."
