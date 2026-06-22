---
name: microbe-compound-identification
description: Use when you have collected MS/MS spectra from a microbial sample (pure culture, environmental isolate, or mixed community) and need to assign chemical identities to observed m/z features while simultaneously resolving which microbial taxa are likely producers of each metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - microbeMASST
  - metadataMASST
  - GNPS_MASST
  - microbe_masst
  - Fast Search API
  - MZmine
derived_from:
- doi: 10.1038/s41538-022-00137-3
  title: foodMASST
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_foodmasst_2_cq
    doi: 10.1038/s41538-022-00137-3
    title: foodMASST
  dedup_kept_from: coll_foodmasst_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41538-022-00137-3
  all_source_dois:
  - 10.1038/s41538-022-00137-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# microbe-compound-identification

## Summary

Identify metabolites and trace their origins to specific microbial taxa using single-spectrum mass spectrometry searches against curated microbe-specific reference libraries. This skill enables taxonomically informed annotation of microbial metabolomics data by leveraging domain-specific mass spectral databases integrated with NCBI taxonomy lineage information.

## When to use

You have collected MS/MS spectra from a microbial sample (pure culture, environmental isolate, or mixed community) and need to assign chemical identities to observed m/z features while simultaneously resolving which microbial taxa are likely producers of each metabolite. Use this skill when a single spectrum query against microbe-specific reference data is sufficient for your research question; if you have dozens of spectra to process simultaneously across multiple domains (microbe, plant, food, tissue), use batch search instead.

## When NOT to use

- Input is already a curated feature table or annotated compound list — use this skill to perform initial spectrum-to-compound annotation, not to post-process existing identifications.
- You need simultaneous batch search across non-microbial domains (plants, tissues, food) — use jobs.py with batch search API instead of single-spectrum queries.
- Your spectra come from non-microbial sources or environmental samples where plant, tissue, or food contamination is the primary concern — use domain-specific MASSTs (plantMASST, tissueMASST, foodMASST) appropriate to your sample type.

## Inputs

- Single MS/MS spectrum (in .mgf format or Universal Spectrum Identifier / USI)
- Search parameters: cosine similarity threshold, m/z tolerance, minimum peak match count

## Outputs

- Ranked list of spectral matches from microbeMASST reference library (with cosine scores)
- Taxonomic lineage information for matched spectra (kingdom, phylum, class, order, family, genus, species, strain)
- GNPS library annotations (Level 2 MSI) for matched compounds
- Sample-level match counts and dataset distribution (via _matches.tsv, _library.tsv, _datasets.tsv)
- Interactive HTML and JSON tree visualizations of taxonomic assignment

## How to apply

Deploy the microbeMASST standalone web application (hosted at https://masst.gnps2.org/microbemasst/) or clone and run the code from GNPS_MASST and robinschmid/microbe_masst repositories. Input a single MS/MS spectrum (in .mgf format or as a USI reference) and configure search parameters: minimum cosine similarity score (typical range 0.6–0.7), m/z tolerance (e.g., 0.1 Da for high-resolution instruments), and minimum number of matching peaks (typically 6–10 depending on spectral quality). The search queries the indexed microbeMASST reference library, which currently covers 8 kingdoms, 20 phyla, 48 classes, 124 orders, 278 families, 561 genera, 1379 species, and 542 strains. Review the returned matches ranked by cosine score; cross-reference library matches (enabling Level 2 MSI annotation) with sample-level counts to infer producer taxa. Optionally aggregate outputs using metadataMASST for visualization across multiple spectra.

## Related tools

- **GNPS_MASST** (Hosts the standalone web application code and deployment infrastructure for microbeMASST and other domain-specific MASSTs) — https://github.com/mwang87/GNPS_MASST
- **microbe_masst** (Contains the microbeMASST-specific implementation, batch search job runner (jobs.py), taxonomic lineage data, and reference library curation logic) — https://github.com/robinschmid/microbe_masst
- **metadataMASST** (Aggregates and visualizes search outputs from single or batch microbeMASST queries for multi-spectrum analysis and cross-domain comparison) — https://masst.gnps2.org/metadatamasst/
- **Fast Search API** (Powers batch spectrum queries against indexed GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN data for high-throughput microbe compound identification) — https://fasst.gnps2.org/fastsearch/
- **MZmine** (Upstream tool for preprocessing raw MS data and exporting .mgf spectra for input to microbeMASST queries) — https://github.com/mzmine/mzmine

## Examples

```
# Query a single spectrum via USI or .mgf file using the microbeMASST web interface at https://masst.gnps2.org/microbemasst/, or programmatically via batch run: python code/jobs.py (after adding entries to jobs_list with cosine_threshold=0.7, mz_tolerance=0.1, and minimum_peaks=6)
```

## Evaluation signals

- Returned matches have cosine similarity scores above your configured threshold and show clear peak alignment between query and reference spectra (inspect interactive HTML tree or JSON structure).
- Matched compounds are chemically consistent with known microbial natural products (e.g., secondary metabolites, antibiotics, pigments) and the taxonomic lineages returned are biologically plausible producers of those compounds.
- Library matches (when present) are ranked higher than non-library matches, enabling MSI Level 2 annotation confidence for your compound of interest.
- If the same metabolite is matched across multiple NCBI taxonomy IDs, inspect the strain/species coverage in the lineage files to confirm representation across the expected producer taxa.
- Re-running the same spectrum with relaxed search parameters (lower cosine threshold, higher m/z tolerance) should yield a superset of matches; if not, check API logs or re-run via batch jobs.py with skip_existing=False to detect transient failures.

## Limitations

- microbeMASST reference library is limited to currently indexed and curated microbial spectra; novel or rare compounds may lack matches despite being biologically relevant.
- Single-spectrum queries do not provide quantitative abundance or co-occurrence information; use batch search with metadataMASST for multi-spectrum ecological context.
- Fast Search API can experience transient failures on first run; the README recommends running jobs.py multiple times (with skip_existing=True) to capture all possible matches.
- Taxonomic assignment is only as informative as the lineage metadata associated with reference spectra; spectra from uncultured or poorly annotated environmental samples will yield incomplete or ambiguous producer lineages.
- Search parameters (cosine threshold, m/z tolerance, peak match count) must be manually tuned based on instrument resolution and spectral quality; no automated parameter selection is provided.

## Evidence

- [other] microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database: "microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database"
- [readme] The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
- [readme] microbeMASST currently covers 8 kingdoms, 20 phyla, 48 classes, 124 orders, 278 families, 561 genera, 1379 species, and 542 strains: "microbeMASST | 8 | 20 | 48 | 124 | 278 | 561 | 1379 | 542"
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] A _library.tsv file will be generated. This contains a list of spectra from the GNPS libraries found to match your spectrum of interest. This enables a Level 2 annotation according the Metabolomics Standards Initiative.: "A _library.tsv file will be generated. This contains a list of spectra from the GNPS libraries found to match your spectrum of interest. This enables a Level 2 annotation according the Metabolomics"
- [readme] Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question.: "Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question."
- [readme] Due to the Fast Search API some of the entries will fail. Nevertheless sequent re-runs should catch all the possible matches.: "Due to the Fast Search API some of the entries will fail. Nevertheless sequent re-runs should catch all the possible matches."
