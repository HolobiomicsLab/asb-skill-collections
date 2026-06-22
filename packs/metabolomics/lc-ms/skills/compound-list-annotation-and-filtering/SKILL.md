---
name: compound-list-annotation-and-filtering
description: Use when after marker identification or feature selection has produced a list of discriminatory m/z features, and before pathway enrichment analysis (e.g., KEGG).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - ggplot2
  - igraph
  - Metabo_Annotation
  - Annota_Tandem
  - KEGG_Enrich_PlotPanel
  - R (>= 3.5.0)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- several R packages are utilized in the background processes, including ggfortify, ggplot2, igraph
- several R packages are utilized in the background processes, including ggplot2, igraph, MASS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_largemetabo_cq
    doi: 10.1093/bib/bbac455
    title: LargeMetabo
  dedup_kept_from: coll_largemetabo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbac455
  all_source_dois:
  - 10.1093/bib/bbac455
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-list-annotation-and-filtering

## Summary

Annotate a compound list (m/z-based identifiers) against metabolite databases and filter results by mass tolerance and database match criteria to prepare compounds for downstream enrichment or pathway analysis. This skill bridges mass spectrometry feature detection and functional interpretation.

## When to use

After marker identification or feature selection has produced a list of discriminatory m/z features, and before pathway enrichment analysis (e.g., KEGG). Use this skill when you have a set of compound identifiers (m/z values, KEGG compound IDs, or CAS numbers) and need to resolve them to named metabolites and standardize their format for enrichment databases.

## When NOT to use

- Compound list is already fully annotated and validated against a standard database (e.g., KEGG compound IDs only)—skip to enrichment directly.
- Input contains only pre-identified metabolite names without m/z or mass information—annotation lookup requires mass or spectral data.
- Mass spectrometry raw data is available and feature detection has not yet been performed—use feature detection and alignment before this skill.

## Inputs

- compound list (m/z values or compound identifiers from marker identification)
- mass tolerance parameters (masstole in Da or ppm)
- ionization mode specification ('pos' or 'neg')
- parent ion mass and MS/MS peak list (for tandem annotation; m/z & intensity pairs)

## Outputs

- annotated compound table (data frame with compound names, database IDs, m/z, and match metadata)
- filtered compound list (resolved to single ID per feature, standardized for enrichment tools)

## How to apply

Load the compound list (e.g., from the marker identification output or a user-supplied CSV with m/z or compound ID columns). Call Metabo_Annotation() for MS1-level annotation with specified mass tolerance (masstole, default 0.05) and tolerance unit (toleUnit: 0 for ppm, 1 for Da), selecting an annotation database (e.g., 'metlin' for MS1; 'kegg' for pathway-ready IDs) and ionization mode ('pos' or 'neg'). For MS/MS data, first extract parent ion mass and MS/MS peak lists (m/z & intensity pairs), then apply Annota_Tandem() with separate mass tolerances for parent (massTandem) and fragment (massmzTandem) matching, specifying ion energy level ('low(10V)' or 'high'). Filter annotation results by database match confidence and resolve ambiguous m/z assignments. Export the annotated and filtered compound list (typically as a data frame with compound names, IDs, and matched database entries) for input to KEGG_Enrich_PlotPanel().

## Related tools

- **Metabo_Annotation** (Primary function for MS1-level compound annotation; resolves m/z features to metabolite names and database IDs using specified mass tolerance and database selection) — https://github.com/LargeMetabo/LargeMetabo
- **Annota_Tandem** (Extended annotation for MS/MS data; matches parent ion mass and fragmentation patterns to improve compound identification specificity) — https://github.com/LargeMetabo/LargeMetabo
- **KEGG_Enrich_PlotPanel** (Downstream workflow step; accepts annotated and filtered compound list to configure KEGG pathway enrichment parameters) — https://github.com/LargeMetabo/LargeMetabo
- **R (>= 3.5.0)** (Runtime environment for LargeMetabo package execution) — https://www.r-project.org

## Examples

```
AnnotaMS <- AnnotaData$AnnotaMS; MetaboAResult <- Metabo_Annotation(AnnotaMS, masstole = 0.05, toleUnit = 1, annotaDB = "metlin", ionMode = "pos"); MetaboAResult$`M+H-2H2O`[1:5,]
```

## Evaluation signals

- Annotated table contains one row per input compound with resolved metabolite names and database identifiers (e.g., KEGG compound IDs or METLIN entries); no NULL or ambiguous entries remain after filtering.
- Mass tolerance criteria are consistently applied: all matched compounds fall within ±masstole (Da) or ±toleUnit ppm of the input m/z value.
- For MS/MS annotations, fragmentation pattern matches (cosine similarity or equivalent) meet database scoring thresholds; ion energy level and ionization mode match experimental configuration.
- Output data frame schema matches the expected format for downstream KEGG_Enrich_PlotPanel() input (compound ID column, fold-change or intensity columns as needed).
- No duplicate compound IDs in the filtered output; ambiguous m/z-to-metabolite mappings are resolved or flagged with low confidence scores.

## Limitations

- Annotation accuracy depends on database completeness and mass spectrometry instrument calibration; mass tolerance threshold must be tuned to instrument accuracy (typically 0.01–0.1 Da for high-resolution instruments).
- MS1-level annotation alone may produce multiple candidate metabolites per m/z; MS/MS data significantly improves specificity but requires tandem mass spectra.
- Different ionization modes ([M+H]+, [M−H]−, adducts) can complicate m/z-to-metabolite matching; ionMode and adduct specification must be explicit and validated.
- Annotation databases (METLIN, KEGG) have different coverage and curation standards; compounds absent from a chosen database will not be matched.

## Evidence

- [readme] When performing metabolite annotation for primary mass spectrometry (MS1), a compound list containing the studied m/z features should be properly provided.: "When performing metabolite annotation for primary mass spectrometry (MS1), a compound list containing the studied m/z features should be properly provided"
- [readme] Metabo_Annotation() function with masstole, toleUnit, annotaDB, and ionMode parameters.: "MetaboAResult <- Metabo_Annotation(AnnotaMS, masstole = 0.05, toleUnit = 1, annotaDB = "metlin", ionMode  = "pos")"
- [readme] For MS/MS annotation, parent ion mass and MS/MS peak list (m/z & intensity pairs) are required inputs.: "When performing metabolite annotation for tandem mass spectrometry (MS/MS), the information containing parent ion mass and MS/MS peak list (the first column is m/z value and the second column is the"
- [readme] Annota_Tandem() function with separate mass tolerance parameters for parent ions and MS/MS fragments.: "AnnotaParamTandem <- Annota_Tandem(ParentMass, TandemData, massTandem = 0.1, toleUnitTandem = 1, massmzTandem = 0.5, toleUnitmzTandem = 1, ModeTandem = "Positive", ionEnergy = "low(10V)")"
- [readme] Annotated compound output is passed to enrichment analysis workflows for pathway interpretation.: "sampleDatakegg <- EnrichData$sampleDatakegg; EnrichParam <- KEGG_Enrich_PlotPanel(sampleDatakegg, enrichDB = "kegg", pvalcutoff = 0.05, IDtype = 1, cateIdx = 1)"
