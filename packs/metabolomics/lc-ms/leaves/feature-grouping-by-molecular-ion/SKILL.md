---
name: feature-grouping-by-molecular-ion
description: Use when after peak picking and sample alignment have produced an aligned feature table with m/z and retention time coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Centwave
  - SLAW grouping module
  - FeatureFinderMetabo
  - ADAP
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- grouping of isotopologues and adducts
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-grouping-by-molecular-ion

## Summary

Groups detected LC-MS features into clusters sharing the same molecular ion, accounting for isotopic variants (e.g., C13, N15, D) and common adduct forms ([M+H]+, [M+Na]+, [M+NH4]+). This step consolidates redundant representations of the same molecule into single feature clusters, improving downstream quantification and annotation.

## When to use

Apply this skill after peak picking and sample alignment have produced an aligned feature table with m/z and retention time coordinates. Use it when you need to reduce feature redundancy caused by naturally occurring isotopologue distributions and variable ionization/adduction chemistry, before gap-filling or final quantification table generation.

## When NOT to use

- Input data are already consolidated into a single ion per molecular species (e.g., pre-processed by another tool or manual curation).
- Analysis targets only targeted features with known identity and no need to consolidate redundant ion forms.
- LC-MS data are profile (not centroided); grouping requires accurate m/z measurements from centroided data.

## Inputs

- aligned feature table (m/z, retention time, intensity matrix)
- detected LC-MS peaks with mass-to-charge and RT coordinates

## Outputs

- grouped feature table with cluster identifiers and group membership
- isotopologue/adduct annotations per feature

## How to apply

Load the aligned feature table (output from sample alignment) containing detected m/z and retention time coordinates. Apply a grouping algorithm that clusters features by (1) matching m/z values within a tolerance corresponding to known isotopic mass shifts (C13 ≈ 1.003 Da, N15 ≈ 0.997 Da, D ≈ 1.006 Da) and adduct mass differences ([M+Na]–[M+H] ≈ 21.98 Da, [M+NH4]–[M+H] ≈ 18.03 Da), and (2) enforcing that grouped features share the same or near-identical retention time (allowing for minor drift due to alignment errors). Assign cluster identifiers to each feature and output the grouped feature table with isotopologue/adduct group membership annotations. SLAW applies this as part of its complete workflow after alignment and before gap-filling.

## Related tools

- **Centwave** (peak picking algorithm upstream of grouping; provides initial detected features fed into grouping module) — https://github.com/sneumann/xcms
- **SLAW grouping module** (implements isotopologue and adduct clustering as part of complete untargeted LC-MS workflow) — https://github.com/zamboni-lab/SLAW
- **FeatureFinderMetabo** (alternative peak picking algorithm that can feed into grouping step)
- **ADAP** (alternative peak picking algorithm that can feed into grouping step)

## Evaluation signals

- Cluster size distribution: verify that most clusters contain 1–4 members (isotopes + adducts), with outliers flagged for manual inspection.
- Retention time coherence: confirm that all features within a cluster have RT values within expected drift tolerance (typically <0.5 min for aligned data).
- Mass difference validation: spot-check cluster members to verify m/z differences match known isotopic shifts or documented adduct masses.
- Feature redundancy reduction: count total features before and after grouping; expect 20–40% reduction in redundant ions for typical untargeted metabolomics.
- Downstream quantification stability: verify that consolidated features show expected intensity relationships (e.g., C13 isotope peaks ~1–2% of M+0 intensity for natural carbon).

## Limitations

- Grouping relies on accurate m/z measurement and peak picking; poor centroiding or peak detection upstream degrades clustering fidelity.
- Algorithm assumes typical isotopic and adduct patterns; unusual ionization modes, non-standard adducts, or multiply-charged ions may not cluster correctly.
- Retention time alignment errors can cause true isotopologues/adducts from the same molecule to be assigned separate clusters if RT drift exceeds tolerance.
- Metabolites with naturally high isotopic abundance (e.g., sulfur-containing compounds with S34) may produce unexpected isotope peak patterns.
- DIA-MS data are not supported by SLAW; workflow is limited to DDA-only LC-MS experiments.

## Evidence

- [other] SLAW includes a processing step for grouping of isotopologues and adducts as part of its complete untargeted LC-MS workflow, which operates after peak picking and sample alignment.: "SLAW includes a processing step for grouping of isotopologues and adducts as part of its complete untargeted LC-MS workflow, which operates after peak picking and sample alignment."
- [other] Apply isotopologue and adduct grouping algorithm to cluster features sharing the same molecular ion with mass differences corresponding to isotopic shifts (e.g., C13, N15, D) or common adduct transformations (e.g., [M+H]+, [M+Na]+, [M+NH4]+).: "Apply isotopologue and adduct grouping algorithm to cluster features sharing the same molecular ion with mass differences corresponding to isotopic shifts (e.g., C13, N15, D) or common adduct"
- [other] Load aligned feature table (output from sample alignment step) containing detected m/z and retention time coordinates.: "Load aligned feature table (output from sample alignment step) containing detected m/z and retention time coordinates."
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion"
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
