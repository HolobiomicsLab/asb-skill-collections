---
name: m-z-metabolite-annotation-mapping
description: 'Use when when you have a spatial metabolomics or LC-MS dataset with detected m/z features (as a feature matrix or SpaMTP Seurat object) and need to assign metabolite identities. Specifically: you have observed m/z values, you know the ionization polarity and expected adduct form (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - SpaMTP
  - R
  - Seurat
  - Cardinal
  - RefineLipids
  - SearchAnnotations
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
---

# m/z-metabolite-annotation-mapping

## Summary

Maps mass-to-charge (m/z) ratios from full-scan MS data to metabolite identities by searching against a reference database (e.g. LipidMaps, HMDB) with specified mass tolerance and adduct type. This is the primary step for converting raw m/z features into annotated metabolite identities in spatial metabolomics and LC-MS workflows.

## When to use

When you have a spatial metabolomics or LC-MS dataset with detected m/z features (as a feature matrix or SpaMTP Seurat object) and need to assign metabolite identities. Specifically: you have observed m/z values, you know the ionization polarity and expected adduct form (e.g. M+K, M+H), and you have access to a curated metabolite mass database. This is a prerequisite for any downstream pathway analysis, differential metabolite expression, or metabolite-based tissue characterization.

## When NOT to use

- You have already-annotated metabolite names (not m/z values) — use these directly for downstream analysis instead.
- Your m/z values are from low-resolution MS (e.g. unit-resolution quadrupole) where ppm-based matching is not reliable — consider integer m/z binning or wider tolerance windows and accept lower specificity.
- You lack a suitable reference database for your sample type or organism — annotation will fail or produce false positives; first curate or acquire a domain-appropriate database.
- Your ionization mode or adduct type is unknown or highly variable — run separate annotations for each likely adduct and manually reconcile, or use exploratory neutral-loss analysis first.

## Inputs

- SpaMTP Seurat object with m/z features in rows and spatial/sample coordinates in columns
- Feature intensity matrix (CSV or RDS) with m/z values as row names
- Reference metabolite database (Lipidmaps_db, HMDB_db, or custom formatted database)
- Ionization mode and adduct specification (e.g. 'positive', 'M+K')
- Mass tolerance threshold in ppm (integer, typically 5–15)

## Outputs

- SpaMTP Seurat object with annotated feature metadata ([redacted-email] slot containing metabolite names, InChI keys, or other database identifiers)
- Annotation summary table mapping m/z values to metabolite identities, database IDs, and confidence scores
- Count of successfully annotated m/z features and count of unannotated features
- Optional: RefineLipids output simplifying lipid nomenclature into common lipid classes (e.g. SM, PE, TG)

## How to apply

Load your m/z feature matrix into a SpaMTP Seurat object (or compatible data structure). Call AnnotateSM() with parameters: db= (reference database, e.g. Lipidmaps_db or HMDB_db), ppm_error= (mass tolerance in parts per million, typically 5–15 ppm for high-resolution MS), adducts= (expected adduct(s), e.g. 'M+K' or 'M+H'), and polarity= (ionization mode, 'positive' or 'negative'). The function computes the theoretical m/z for each metabolite in the reference database under the specified adduct and polarity, then matches observed m/z values within the ppm tolerance window. Extract counts and identities from the returned object's feature metadata slot ([redacted-email]). Validate by checking SearchAnnotations() to confirm high-confidence matches and by cross-referencing with domain knowledge about expected metabolites in your tissue/sample type.

## Related tools

- **SpaMTP** (Core R package providing AnnotateSM() function for m/z-to-metabolite mapping and metabolite annotation statistics; implements database search and adduct matching logic.) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Underlying data structure (Seurat class object) that stores m/z features, spatial coordinates, and metadata; AnnotateSM returns annotated Seurat objects.) — https://satijalab.org/seurat/
- **Cardinal** (Parent R package for MS imaging data manipulation; SpaMTP inherits visualization and mass spectrum handling functions including ImageMZPlot().) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **RefineLipids** (Optional downstream function within SpaMTP that simplifies lipid nomenclature of annotations into common lipid categories after AnnotateSM mapping.) — https://github.com/GenomicsMachineLearning/SpaMTP
- **SearchAnnotations** (SpaMTP utility function for post-hoc validation and lookup of specific annotated metabolites by name in the returned Seurat object.) — https://github.com/GenomicsMachineLearning/SpaMTP

## Examples

```
bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = 'M+K', polarity = 'positive')
```

## Evaluation signals

- Non-zero count of annotated m/z features returned; verify that the count is reasonable given database size and m/z range coverage.
- Feature metadata slot (Seurat@assays$[redacted-email]) contains new columns with metabolite names, database accessions, and/or InChI keys for annotated features.
- Spot-check: use SearchAnnotations() to retrieve known metabolites (e.g. common lipids, ATP) and confirm they appear with correct m/z and adduct form.
- Annotation specificity check: inspect mass error (Δm/z in ppm) for matched features; all should fall within the specified ppm_error threshold (e.g. ≤15 ppm).
- Tissue-type concordance: annotated metabolites should be biochemically plausible for the tissue (e.g. brain lipids in neural tissue, urinary nucleotides in bladder).
- Cross-validation: compare AnnotateSM annotations against orthogonal methods (e.g. pseudo-MS/MS, targeted metabolomics if available) or literature expectations for the sample type.

## Limitations

- Annotation accuracy depends critically on the completeness and correctness of the reference database; rare or newly discovered metabolites will not be annotated.
- Mass tolerance (ppm_error) must be optimized for your instrument's mass accuracy; too tight tolerance misses true metabolites, too loose tolerance produces false positives.
- Multiple isomers and isobars can have identical m/z and adduct form, leading to ambiguous or false annotations without additional orthogonal data (e.g. retention time, MS/MS fragmentation, or imaging spatial correlation).
- The AnnotateSM function does not perform in-source fragmentation or neutral-loss filtering; structural variants and in-source dimers may not be handled correctly.
- Pseudo MS/MS-based refinement and refinement with paired targeted metabolic data are marked as 'To come!' in the SpaMTP methods, meaning they are not yet implemented for automated disambiguation.
- Requires pre-formatted reference databases (Lipidmaps_db, HMDB_db); loading and validating custom databases requires manual curation and format compliance.

## Evidence

- [methods] AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = 'M+K', polarity = 'positive'): "AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = 'M+K', polarity = 'positive')"
- [readme] mass-to-charge ratio (m/z) metabolite annotation: "mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical analysis"
- [other] Extract the count of successfully annotated m/z features from the returned SpaMTP object and verify that annotations are stored in the feature metadata slot.: "Extract the count of successfully annotated m/z features from the returned SpaMTP object and verify that annotations are stored in the feature metadata slot."
- [other] Generate a summary table showing the m/z values and their corresponding metabolite annotations from the Lipidmaps_db.: "Generate a summary table showing the m/z values and their corresponding metabolite annotations from the Lipidmaps_db."
- [methods] Runs lipid nomenclature simplification on annotations; RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes: "Runs lipid nomenclature simplification on annotations; RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes"
- [readme] SpaMTP is an R package designed for the integrative analysis of spatial metabolomics and spatial transcriptomics data.: "SpaMTP is an R package designed for the integrative analysis of spatial metabolomics and spatial transcriptomics data."
- [methods] Pseudo MS/MS-Based Refinement section marked as 'To come!': "## 3) Pseudo MS/MS-Based Refinement

To come!"
