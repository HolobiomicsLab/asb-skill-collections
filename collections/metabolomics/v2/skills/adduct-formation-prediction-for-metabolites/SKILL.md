---
name: adduct-formation-prediction-for-metabolites
description: Use when when you have unidentified LC/MS features (m/z, retention time, intensity) and need to disambiguate which metabolites they represent by accounting for the fact that observed m/z values may correspond to different adduct forms (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - ipaPy2
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# adduct-formation-prediction-for-metabolites

## Summary

Predict and integrate adduct ion formation for LC/MS features to improve metabolite annotation accuracy. This skill uses an adducts library parameterized by mass shift, charge, ionization mode, and chemical formula change to compute expected m/z values and assign annotation probabilities within a Bayesian framework.

## When to use

When you have unidentified LC/MS features (m/z, retention time, intensity) and need to disambiguate which metabolites they represent by accounting for the fact that observed m/z values may correspond to different adduct forms (e.g., [M+H]+, [M+Na]+, [M-H]−) rather than the neutral mass alone. Use this skill as part of a probabilistic annotation workflow to integrate adduct information with biochemical relations and isotope patterns.

## When NOT to use

- If your features are already confirmed by tandem MS (MS/MS) fragmentation — orthogonal methods (e.g., spectral library matching) may be more direct.
- If your database lacks adduct specifications (adductsPos, adductsNeg columns) — you must configure these first or this skill cannot rank adduct hypotheses.
- If your instrument mass accuracy is poor (>>5 ppm) or uncalibrated — predicted m/z values will fall outside the match tolerance and all adduct predictions will score low.

## Inputs

- LC/MS feature table (m/z, retention time, intensity)
- MS1 database (pandas DataFrame or CSV with columns: id, name, formula, adductsPos, adductsNeg, optional RT range and prior knowledge pk)
- Adducts library (CSV file with columns: name, calc, Charge, Mult, Mass, Ion_mode, Formula_add, Formula_ded, Multi)

## Outputs

- Annotated feature table with top candidate metabolites per feature
- Per-feature annotation probabilities integrating adduct predictions
- Predicted m/z values for each candidate–adduct pair

## How to apply

Load or construct an adducts.csv file containing columns for adduct name (e.g., 'M+H'), calculated m/z formula (e.g., 'M+1.007276'), charge, multiplicity, exact mass shift, ionization mode (positive/negative), and chemical formula additions/deductions. For each candidate metabolite in your MS1 database, specify which adducts are plausible in positive and negative modes (e.g., 'M+H;M+Na;M+2H;2M+H'). During Bayesian inference, ipaPy2 computes predicted m/z values for each candidate–adduct pair by applying the mass shift and charge from the adducts library, then compares observed feature m/z against predicted values within instrument mass accuracy tolerance (typically ≤5 ppm for high-resolution instruments). Adduct predictions are weighted by prior knowledge (pk) and biochemical plausibility, contributing to the posterior annotation probability for each feature. The choice of adducts per compound should reflect your sample type and ionization conditions; update the adducts file and per-compound adduct lists as you gain instrument-specific experience.

## Related tools

- **ipaPy2** (Bayesian annotation framework that integrates adduct predictions with isotope patterns and biochemical relations to compute posterior annotation probabilities) — https://github.com/francescodc87/ipaPy2
- **Python** (Programming language for loading, parsing, and manipulating adducts files and MS1 databases within the ipaPy2 workflow)

## Examples

```
import pandas as pd; adducts = pd.read_csv('DB/adducts.csv'); DB = pd.read_csv('DB/IPA_MS1.csv'); from ipaPy2 import IPA; ipa = IPA(adducts, DB); annotations = ipa.annotate(features_mz, features_rt, features_intensity, ionization_mode='positive')
```

## Evaluation signals

- Predicted m/z values for candidate–adduct pairs match observed feature m/z within calibrated mass tolerance (≤5 ppm for high-resolution instruments).
- Adduct predictions are chemically plausible for the ionization mode (e.g., no [M+H]− in positive mode, no [M-H]+ in negative mode).
- Top-ranked annotations have higher posterior probabilities when adduct matches are observed compared to when adducts are absent or mismatched.
- Features with retention time annotations (RT column in database) show higher probabilities when observed RT falls within the expected window; absent or mismatched RT should lower probability.
- Annotation probabilities sum to ~1.0 across top candidates per feature, indicating proper Bayesian normalization.

## Limitations

- Adduct formation is ionization-mode specific and instrument-dependent; exotic adducts (in-source fragments, cluster ions) require manual database curation.
- High-mass or multiply-charged compounds (e.g., [2M+H]+, [M+2H]2+) increase complexity; the method assumes the adducts file is complete and accurate.
- Poor mass calibration (>5 ppm drift) will cause predicted m/z values to fall outside match tolerance, yielding low or zero annotation probabilities regardless of true adduct identity.
- The method relies on a well-curated MS1 database; missing compounds or incomplete adduct specifications per compound will bias or fail annotations.

## Evidence

- [other] IPA is a Bayesian annotation method for LC/MS data that integrates three key information sources: biochemical relations, isotope patterns, and adduct formation to compute annotation probabilities.: "IPA is a Bayesian annotation method for LC/MS data that integrates three key information sources: biochemical relations, isotope patterns, and adduct formation to compute annotation probabilities."
- [readme] **1. Adducts file (required)**
<br />
The ipaPy2 library requires a file contains all the information required for the computation of the adducts. An adducts.csv file is provided with the package [here](DB/adducts.csv). The file contains the most common adducts. If any exotic adduct (or in-source fragment) needs to be considered, the user must modify the file accordingly. The format required for the adducts file is shown below.: "The ipaPy2 library requires a file contains all the information required for the computation of the adducts. An adducts.csv file is provided with the package. The file contains the most common"
- [readme] **adductsPos**: list of adducts that should be considered in Positive mode for this entry (e.g.,'M+Na;M+H;M+') - *necessary*
- **adductsNeg**: list of adducts that should be considered in Negative mode for this entry (e.g.,'M-H;M-2H') - *necessary*: "list of adducts that should be considered in Positive mode for this entry (e.g.,'M+Na;M+H;M+') - *necessary*; list of adducts that should be considered in Negative mode for this entry"
- [readme] One of the most powerful features of the IPA method is that it is able to integrate the knowledge gained from previous experiments in the annotation process. There are three files that are used as the IPA database:: "One of the most powerful features of the IPA method is that it is able to integrate the knowledge gained from previous experiments in the annotation process."
- [readme] To fully exploit the IPA method, it is strongly recommended to constantly update the database when new knowledge is gained from previous experience. Providing a retention time window for compounds previously detected with the analytical system at hand it is particularly useful.: "To fully exploit the IPA method, it is strongly recommended to constantly update the database when new knowledge is gained from previous experience. Providing a retention time window for compounds"
