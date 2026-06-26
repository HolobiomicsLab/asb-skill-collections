---
name: lcms-feature-probability-scoring
description: Use when you have an untargeted LC/MS feature table (m/z, retention time,
  intensity columns) and need to move beyond single-hit matching to probabilistic
  annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - ipaPy2
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btad455
  title: ipaPy2
evidence_spans:
- Python implementation of the Integrated Probabilistic Annotation (IPA)
- github.com__francescodc87__ipaPy2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ipapy2_cq
    doi: 10.1093/bioinformatics/btad455
    title: ipaPy2
  dedup_kept_from: coll_ipapy2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad455
  all_source_dois:
  - 10.1093/bioinformatics/btad455
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-feature-probability-scoring

## Summary

Apply Bayesian inference to assign annotation probabilities to LC/MS features by integrating biochemical relations, isotope patterns, and adduct formation. This skill produces a ranked feature table with posterior probabilities for candidate metabolites, enabling confidence-calibrated metabolomics annotation.

## When to use

You have an untargeted LC/MS feature table (m/z, retention time, intensity columns) and need to move beyond single-hit matching to probabilistic annotation. Use this skill when you want to leverage prior knowledge about expected adducts, isotope signatures, and metabolic pathway connectivity to disambiguate features that map to multiple database entries.

## When NOT to use

- Your data is already manually curated or single-hit matched to a reference library with high confidence (posterior probability >0.95); probabilistic re-scoring adds no value.
- The LC/MS features come from a targeted method with a small, highly specific compound list; Bayesian integration of broad database knowledge introduces noise.
- You lack retention time calibration or expected adduct information for your instrument/sample; the method requires these priors to function; generic defaults will underperform.

## Inputs

- LC/MS feature table (CSV/TSV with m/z, retention time in seconds, intensity columns)
- Adducts database (CSV: name, calc formula, charge, mass, ion_mode, formula_add, formula_ded, multiplicity)
- MS¹ compound database (CSV: id, name, formula, inchi, smiles, RT range, adductsPos, adductsNeg, pk prior score, reactions list)
- Optional: MS² spectral database (for fragment annotation cross-validation)
- Optional: biochemical reactions network (for pathway-based probability refinement)

## Outputs

- Annotated feature table with posterior annotation probabilities per feature
- Ranked list of candidate metabolites per feature with assigned adduct and probability score
- Feature-to-reaction mappings (if biochemical relations enabled)

## How to apply

Load your LC/MS feature data (m/z, retention time, intensity) and configure three database files: an adducts CSV specifying ion-mode-specific mass shifts and charge states; an MS¹ database with compound ID, formula, retention time windows (if known), applicable adducts per ionization mode, and prior knowledge (pk) scores between 0–1 reflecting likelihood the compound appears in your sample; optionally, a reactions file for biochemical relation lookup. Run Bayesian inference via ipaPy2, which computes posterior annotation probabilities for each feature by: (1) enumerating all possible [compound, adduct] pairs consistent with the observed m/z within mass tolerance; (2) scoring each pair using observed isotope pattern fit (13C, ¹⁸O signatures); (3) incorporating prior knowledge and retention time plausibility; (4) integrating biochemical pathway context (e.g., compounds co-occurring in known reactions receive higher joint probability). Output is an annotated feature table ranked by posterior probability, with top candidate metabolites, adduct assignments, and confidence scores.

## Related tools

- **ipaPy2** (Bayesian inference engine for computing posterior annotation probabilities by integrating adduct, isotope, and biochemical likelihood scores) — https://github.com/francescodc87/ipaPy2
- **Python** (Scripting language for data loading, database configuration, and output parsing)

## Examples

```
import pandas as pd
from ipaPy2 import IPA
adducts = pd.read_csv('DB/adducts.csv')
db = pd.read_csv('DB/IPA_MS1.csv')
features = pd.read_csv('features.csv')  # m/z, RT, intensity
ipa = IPA(adducts=adducts, ms1_db=db)
result = ipa.annotate(features, ppm_tol=5, rt_window_scale=1.0)
result.to_csv('annotated_features.csv')
```

## Evaluation signals

- All features in input table appear in output with assigned probabilities; no rows silently dropped (data integrity check).
- Posterior probabilities for each feature sum to ≤1.0 and top candidate has probability >0.5 for majority of well-ionizable compounds (probability calibration).
- Features with m/z matching multiple database entries show lower individual probabilities than features with unique m/z matches (Bayesian discrimination working).
- Isotope pattern scores for assigned adducts are within ±5 ppm of theoretical m/z; features with poor isotope fit receive lower posterior scores (isotope refinement validated).
- Known biochemical reaction pairs (e.g., ATP and ADP in same pathway) show positively correlated posteriors when co-detected (pathway coherence check).

## Limitations

- Method requires accurate mass calibration (±5 ppm or better for meaningful isotope discrimination); poor calibration degrades isotope pattern scoring and posterior confidence.
- Prior knowledge (pk scores) and retention time windows must be empirically tuned to your specific instrument, chromatography, and sample type; generic database defaults will underperform on novel matrices.
- Biochemical relation integration assumes reaction networks are complete and accurate; missing or erroneous pathway data can mislead probability estimates.
- No changelog documented in repository; version stability and backward compatibility not explicitly tracked.
- Performance scales with database size; large custom databases (>10,000 entries) may incur computational overhead; sparse adduct/isotope filtering recommended.

## Evidence

- [other] IPA is a Bayesian annotation method for LC/MS data that integrates three key information sources: biochemical relations, isotope patterns, and adduct formation to compute annotation probabilities.: "IPA is a Bayesian annotation method for LC/MS data that integrates three key information sources: biochemical relations, isotope patterns, and adduct formation to compute annotation probabilities."
- [other] Run Bayesian inference to compute posterior annotation probabilities for each feature, integrating biochemical plausibility, observed isotope patterns, and predicted adduct formation.: "Run Bayesian inference to compute posterior annotation probabilities for each feature, integrating biochemical plausibility, observed isotope patterns, and predicted adduct formation."
- [readme] The IPA method requires a pandas dataframe containing the database against which the annotation is performed. This dataframe must contain the following columns in this exact order (optional columns can have empty fields): id, name, formula, inchi, smiles, RT, adductsPos, adductsNeg, description, pk, MS2, reactions: "The IPA method requires a pandas dataframe containing the database against which the annotation is performed. This dataframe must contain the following columns in this exact order (optional columns"
- [readme] One of the most powerful features of the IPA method is that it is able to integrate the knowledge gained from previous experiments in the annotation process.: "One of the most powerful features of the IPA method is that it is able to integrate the knowledge gained from previous experiments in the annotation process."
- [readme] the pk has to be between 1 (compound highly likely to be present in the sample) and 0 (compound cannot be present in the sample).: "the pk has to be between 1 (compound highly likely to be present in the sample) and 0 (compound cannot be present in the sample)."
