---
name: metabolite-annotation-at-scale
description: Use when you have extracted a large feature set of m/z values (hundreds
  to tens of thousands) from a Cardinal MSImagingExperiment object or similar MS dataset
  and need to assign putative metabolite identities using public structural databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SpaMTP
  - R
  - dplyr
  - Cardinal
  - Seurat
  - HMDB Database
  - Lipidmaps Database
  techniques:
  - LC-MS
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- For plotting + DE plots
- '## Install and Import *R* Libraries'
- library(dplyr)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-annotation-at-scale

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematic annotation of thousands to hundreds of thousands of mass-to-charge (m/z) values against public metabolite databases (HMDB, Lipidmaps) using tolerance-based matching with user-specified adducts and polarity filters. This skill enables structural identification of metabolites in large MS imaging and LC-MS datasets by matching observed m/z features to database entries within a defined parts-per-million (ppm) error threshold.

## When to use

You have extracted a large feature set of m/z values (hundreds to tens of thousands) from a Cardinal MSImagingExperiment object or similar MS dataset and need to assign putative metabolite identities using public structural databases. Use this skill when you have chosen a specific ppm error tolerance (e.g., 3 ppm for high-resolution instruments, 15 ppm for lower resolution), defined your expected ionization state (M-H, M+H, M+Cl, M+K, etc.), and want to filter and rank candidate annotations by mass accuracy.

## When NOT to use

- Your m/z values are already annotated and you are seeking to refine or validate existing assignments (use RefineLipids or pathway-correlation filters instead).
- You lack prior knowledge of expected adducts or polarity and have not performed exploratory mass-defect or isotope-pattern analysis to constrain the search space.
- Your ppm tolerance is wider than the mass accuracy of your instrument (e.g., requesting ppm_error=15 for Orbitrap data at 5 ppm resolution will yield spuriously high false-positive rates).
- You are working with untargeted LC-MS data with high chemical diversity and have not pre-filtered to a relevant metabolite class or biochemical pathway, risking combinatorial explosion of candidate matches.

## Inputs

- Cardinal MSImagingExperiment object with featureData m/z values
- Extracted m/z feature vector (numeric)
- Metabolite database object (HMDB_db or Lipidmaps_db)
- User-specified parameters: ppm_error (numeric, e.g. 3 or 15), adducts (character vector, e.g. c('M-H', 'M+Cl')), polarity (character, 'negative' or 'positive')

## Outputs

- Annotated data.frame with columns: observed_mz, database_match_name, ppm_error, adduct, (optionally) metabolite_id, inchi_key, molecular_weight
- Summary statistics (row count, mean ppm_error, adduct distribution)
- Seurat object with annotation metadata added to assay or meta.data slot

## How to apply

Extract all m/z features from your MS dataset using featureData() or equivalent accessor; call AnnotateSM() or AnnotateBigData() with your chosen database (HMDB_db or Lipidmaps_db), specifying ppm_error tolerance and a vector of adducts matching your experimental polarity. The function performs bidirectional mass-matching: for each observed m/z, it calculates the theoretical m/z of database metabolites under each specified adduct transformation, then returns all matches within the ppm window ranked by mass error. Inspect the output data.frame for required columns (observed_mz, database_match_name, ppm_error, adduct); optionally filter further using CalculateAnnotationStatistics() to compute annotation quality metrics and apply lipid nomenclature simplification via RefineLipids() if your dataset is lipid-rich. Verify reproducibility by confirming row counts match expected annotation yields and examining the ppm_error distribution.

## Related tools

- **SpaMTP** (R package providing AnnotateSM, AnnotateBigData, CalculateAnnotationStatistics, RefineLipids, and SearchAnnotations functions for metabolite annotation and refinement at scale) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Cardinal** (Provides MSImagingExperiment object structure, featureData() accessor, and foundational spatial MS data handling for m/z feature extraction and annotation workflows) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **Seurat** (Underlying S4 object framework used by SpaMTP to store and integrate annotated metabolite data with metadata; enables downstream statistical and visualization analyses) — https://satijalab.org/seurat/
- **HMDB Database** (Public metabolite structure database (HMDB_db object) used for mass-matching and metabolite identity lookup in AnnotateSM/AnnotateBigData)
- **Lipidmaps Database** (Public lipid structure database (Lipidmaps_db object) for targeted annotation of lipid-rich samples; complementary to HMDB for MS imaging studies)

## Examples

```
bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = c('M+H', 'M+K'), polarity = 'positive')
```

## Evaluation signals

- Output data.frame row count matches expected annotation yield (e.g., 67,060 annotated m/z values for HMDB with ppm=3 and M-H/M+Cl adducts on 767,528 features indicates ~8.7% successful annotation rate; compare against internal positive/negative control standards).
- ppm_error distribution is centered near zero with 95% of matches within the user-specified tolerance (e.g., if ppm_error=3, verify that 95%+ of rows have ppm_error ≤ 3); values clustered far from zero suggest mass calibration drift or wrong adduct selection.
- Adduct composition matches experimental expectations (e.g., M-H and M+Cl dominate in negative ESI mode; presence of M+H adducts in negative mode is a red flag indicating annotation failure or polarity mismatch).
- Presence and non-null cardinality of required columns (observed_mz, database_match_name, ppm_error, adduct); absence indicates incomplete function execution.
- Reproducibility check: re-running AnnotateSM/AnnotateBigData with identical parameters on the same input produces identical output data.frame (bit-for-bit) or minor floating-point variance only; row count must be exactly reproducible.

## Limitations

- PPM tolerance must be calibrated to instrument mass accuracy; mismatched thresholds (too loose or too strict) yield high false-positive or false-negative rates respectively, and the article does not provide automated calibration methods.
- Public databases (HMDB, Lipidmaps) have incomplete coverage of known metabolites and may lack recently discovered or uncommon structural variants; annotation absence does not prove absence of the metabolite.
- Ambiguous or isobaric database entries (multiple metabolites with identical or near-identical m/z) are not resolved by mass matching alone; further discrimination requires tandem MS data (MS/MS) or retention time information, for which the article notes 'Pseudo MS/MS-Based Refinement' and 'Refinement with Paired Targeted Metabolic Data' sections are 'To come!'
- Adduct selection must be guided by prior knowledge of ionization conditions (ESI mode, solvent pH, buffer additives); incorrect adduct specification yields zero or spurious matches.
- Scaling to very large m/z feature sets (>1 million) may incur computational overhead; the article does not document runtime or memory complexity for AnnotateBigData.

## Evidence

- [other] How many m/z values from the HMDB database can be annotated using AnnotateBigData with ppm_error=3 and M-H/M+Cl negative adducts?: "How many m/z values from the HMDB database can be annotated using AnnotateBigData with ppm_error=3 and M-H/M+Cl negative adducts?"
- [other] Extract all m/z values from the Cardinal MSImagingExperiment object using featureData(). Call AnnotateBigData with parameters: db=HMDB_db, ppm_error=3, adducts=c('M-H','M+Cl'), polarity='negative'.: "Extract all m/z values from the Cardinal MSImagingExperiment object (767,528 features) using featureData(). 2. Call AnnotateBigData with parameters: db=HMDB_db, ppm_error=3, adducts=c('M-H','M+Cl'),"
- [other] Verify the row count equals the reported 67,060 annotated m/z values and inspect output structure to confirm presence of observed_mz, database_match_name, ppm_error, and adduct columns.: "Return the annotated results data.frame and verify the row count equals the reported 67,060 annotated m/z values. 4. Inspect the output structure to confirm presence of observed_mz,"
- [readme] SpaMTP is an R package designed for the integrative analysis of spatial metabolomics and spatial transcriptomics data with three major functionalities which include m/z metabolite annotation, various downstream statistical analysis including differential metabolite expression and pathway analysis, and integrative spatial-omics analysis.: "SpaMTP is an R package designed for the integrative analysis of spatial metabolomics and spatial transcriptomics data. SpaMTP inherits functionalities from two well established R packages (Cardinal"
- [other] Runs lipid nomenclature simplification on annotations; RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes.: "RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes"
- [other] AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15 with M+K adduct specified): "AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15"
- [other] Pseudo MS/MS-Based Refinement and Refinement with Paired Targeted Metabolic Data sections marked as 'To come!' indicating incomplete development of advanced refinement strategies.: "## 3) Pseudo MS/MS-Based Refinement

To come!"
