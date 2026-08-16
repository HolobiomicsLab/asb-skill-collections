---
name: spectral-library-matching-with-taxonomy
description: Use when you have MS/MS spectra (.mgf) and candidate metabolite annotations
  (with m/z, retention time, chemical identifiers) linked to a known organism or taxon,
  and you want to rank annotations by both spectral similarity AND biochemical likelihood
  in that organism's lineage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3697
  tools:
  - R
  - Docker
  - tima (Taxonomically Informed Metabolite Annotation)
  - LOTUS (Natural Products Database)
  - SIRIUS (v5/v6)
  - GNPS-FBMN
  - R (with tidyverse, Spectra, MetaboCoreUtils)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
evidence_spans:
- '[![r-universe badge](https://taxonomicallyinformedannotation.r-universe.dev/tima/badges/version?&color=blue&style=classic.png)]'
- '[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white.png)]'
- '[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white.png)](https://hub.docker.com/r/adafede/tima-r/)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tima_cq
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_tima_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fpls.2019.01329
  all_source_dois:
  - 10.3389/fpls.2019.01329
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-matching-with-taxonomy

## Summary

This skill integrates taxonomic provenance information into mass spectrometry spectral library matching to weight and rank metabolite annotations. By filtering candidates against organism-specific metabolic plausibility and phylogenetic relatives, it reduces false positives and improves annotation confidence in metabolomics workflows.

## When to use

You have MS/MS spectra (.mgf) and candidate metabolite annotations (with m/z, retention time, chemical identifiers) linked to a known organism or taxon, and you want to rank annotations by both spectral similarity AND biochemical likelihood in that organism's lineage. Use this when high-confidence metabolite identification is critical and false-positive annotations from chemically implausible metabolites would mislead downstream interpretation.

## When NOT to use

- Sample organism/taxon is unknown or unspecified — the taxonomic filtering step requires explicit organism context.
- You are analyzing environmental or mixed-community samples without clear organismal assignment — taxonomic filtering assumes single or well-defined taxon per sample.
- You have already validated annotations through independent biochemical assays or orthogonal methods — this skill is a computational filter, not a substitute for ground truth.

## Inputs

- MS/MS spectra in .mgf format with feature identifiers
- Feature quantification table (.csv/.tsv) with feature ID, retention time, m/z, and sample intensity columns
- Sample metadata (.csv/.tsv) linking samples to organisms/taxa
- Candidate metabolite annotations with chemical identifiers (SMILES, InChI, PubChem CID, etc.)
- Taxonomic reference database (e.g., NCBI taxonomy)
- Structure-organism pairs library (e.g., LOTUS with >650k pairs, ISDB, HMDB)

## Outputs

- Scored and ranked metabolite annotation table with combined confidence × taxonomic weight scores
- Filtered candidate list restricted to biochemically plausible metabolites for the organism
- Annotation confidence scores reflecting both spectral similarity and taxonomic likelihood

## How to apply

First, load the organism/taxon context for each sample and retrieve or pre-compute spectral similarity scores against a reference library (LOTUS, ISDB, HMDB, or custom). For each candidate annotation, query whether the putative metabolite is biochemically documented in the sample's taxon or its phylogenetic neighbors using the taxonomic reference database. Assign a taxonomic weight score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon). Finally, combine the spectral annotation confidence (e.g., cosine similarity) with the taxonomic weight to produce a final ranked annotation table. This filtering step eliminates chemically implausible matches before final output.

## Related tools

- **tima (Taxonomically Informed Metabolite Annotation)** (End-to-end R package and Docker container implementing the complete annotation workflow with taxonomic weighting, spectral library matching, and interactive Shiny app for parameter configuration) — https://github.com/taxonomicallyinformedannotation/tima
- **LOTUS (Natural Products Database)** (Provides >650k structure-organism pairs as default reference library for taxonomic filtering and metabolic plausibility scoring) — https://lotusnprod.github.io/lotus-manuscript/
- **SIRIUS (v5/v6)** (Generates candidate molecular formulas and annotations (via CSI:FingerId, ZODIAC, CANOPUS, COSMIC) that can be integrated as external annotations prior to taxonomic weighting)
- **GNPS-FBMN** (Produces spectral similarity network annotations and cluster assignments that can be incorporated as candidate metabolites for taxonomic re-ranking)
- **R (with tidyverse, Spectra, MetaboCoreUtils)** (Core statistical and data-wrangling environment for filtering, scoring, and ranking metabolite candidates by taxonomic and spectral metrics) — https://taxonomicallyinformedannotation.r-universe.dev/tima

## Examples

```
```r
tima::validate_inputs(
  features = "data/source/example_features.csv",
  spectra = "data/source/example_spectra.mgf",
  metadata = "data/source/example_metadata.tsv",
  feature_col = "row ID",
  filename_col = "filename",
  organism_col = "ATTRIBUTE_species"
)
tima::run_app()
```
```

## Evaluation signals

- Ranked annotations output a combined score (annotation confidence × taxonomic weight) for all candidates; verify that metabolites with high taxonomic weight in the sample's organism/relatives appear near the top of the ranked list.
- Biochemically implausible metabolites (those not documented in the organism or phylogenetic neighbors) should be assigned low or zero taxonomic weight; cross-check the output table against the structure-organism pairs library to confirm filtering occurred.
- Spectral similarity scores (cosine, dot-product, or equivalent) and taxonomic weights are independently tracked in the output; verify that low-similarity annotations are not artificially boosted by high taxonomic weight, and vice versa.
- Sample metadata columns (organism/taxon) are correctly mapped to feature rows; spot-check a subset of samples to confirm the right organism context was used for each annotation ranking.
- If external annotations (SIRIUS, GNPS) are provided, verify that they are integrated into the candidate set before taxonomic filtering, not applied after, so all candidates receive equal taxonomic scrutiny.

## Limitations

- Taxonomic database completeness: rare or non-model organisms may have incomplete metabolic coverage in LOTUS, ISDB, or HMDB, leading to false negatives (plausible metabolites marked as implausible). The skill assumes the reference database is representative of the sample organism's known biochemistry.
- Phylogenetic distance cutoff: determining which phylogenetic relatives to include in the 'biochemically plausible' set is a design choice; overly broad relatives may admit false positives, while overly narrow definitions may exclude true metabolites from distant clades.
- Mixed or unidentified communities: samples from environmental or clinical cohorts lacking clear organism assignment cannot be reliably filtered by taxonomy; the skill is designed for organisms or cultivated/controlled samples with known taxon.
- Spectral quality dependence: poor-quality MS/MS spectra or fragmentation patterns atypical for the organism may yield low spectral similarity scores that cannot be rescued by high taxonomic weight, leading to low-confidence annotations.
- Lack of changelog: the tima repository does not maintain a published changelog, making it difficult to track which versions incorporated which improvements to the weighting algorithm or taxonomic database versions used.

## Evidence

- [other] Filter candidate annotations by taxonomic relevance: for each candidate, determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its biological neighbors.: "Filter candidate annotations by taxonomic relevance: for each candidate, determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its"
- [other] Weight each annotation by a taxonomic score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon or phylogenetic relatives).: "Weight each annotation by a taxonomic score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon or phylogenetic"
- [other] Rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table.: "Rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table."
- [readme] Feature quantification table (.csv/.tsv) - Peak areas/heights across samples (example) - Must contain: feature ID, retention time, m/z, and sample intensity columns: "Feature quantification table (.csv/.tsv) - Peak areas/heights across samples (example) - Must contain: feature ID, retention time, m/z, and sample intensity columns"
- [readme] The initial work is available at https://doi.org/10.3389/fpls.2019.01329, with many improvements made since then.: "The initial work is available at https://doi.org/10.3389/fpls.2019.01329, with many improvements made since then."
- [readme] We provide LOTUS (>650k pairs) as default. External annotations - SIRIUS (v5/v6), GNPS-FBMN results. Custom spectral libraries - For in-house compound matching.: "We provide LOTUS (>650k pairs) as default. External annotations - SIRIUS (v5/v6), GNPS-FBMN results. Custom spectral libraries - For in-house compound matching."
