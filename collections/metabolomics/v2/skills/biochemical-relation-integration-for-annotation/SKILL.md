---
name: biochemical-relation-integration-for-annotation
description: Use when when you have LC/MS feature data (m/z, retention time, intensity) that must be annotated against a metabolic database and you have access to (or can construct) knowledge about biochemical reaction networks, expected isotope patterns, and instrument-specific adduct formation rules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
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

# biochemical-relation-integration-for-annotation

## Summary

Integrate biochemical reaction networks, isotope patterns, and adduct formation rules into a Bayesian probabilistic framework to assign annotation probabilities to LC/MS features, improving confidence in metabolite identification by leveraging prior knowledge of metabolic pathways and instrument-specific ionization behavior.

## When to use

When you have LC/MS feature data (m/z, retention time, intensity) that must be annotated against a metabolic database and you have access to (or can construct) knowledge about biochemical reaction networks, expected isotope patterns, and instrument-specific adduct formation rules. Use this skill when shallow mass-to-charge matching produces ambiguous candidate lists and you want to re-rank them using metabolic plausibility and ion formation chemistry.

## When NOT to use

- Input is already a validated, manually curated feature annotation table requiring no probabilistic re-ranking.
- Your metabolic database lacks reaction network or prior knowledge (pk) fields; Bayesian integration requires biochemical context beyond mass alone.
- You need deterministic (non-probabilistic) one-to-one mass matching; this skill is designed for ambiguous, many-to-many candidate scenarios.

## Inputs

- LC/MS feature table (m/z, retention time, intensity, observed isotope pattern)
- Adducts configuration file (CSV: name, mass shift, charge, ion mode, formula add/deduce)
- MS¹ metabolic database (pandas DataFrame: id, name, formula, RT range, adducts per ion mode, reaction IDs)
- Biochemical reaction network or reaction ID annotations

## Outputs

- Feature annotation table with posterior probabilities for each candidate metabolite
- Top-ranked metabolite assignments per feature
- Bayesian posterior scores for confidence filtering

## How to apply

Load LC/MS feature data and configure three data sources within the IPA Bayesian framework: (1) an adducts library (CSV with name, mass shift, charge, ionization mode, and chemical formulas for added/deducted fragments); (2) an MS¹ database (pandas DataFrame with compound ID, name, chemical formula, retention time window, and per-ion-mode adduct lists); and (3) a reactions file encoding biochemical relations (reaction IDs linked to compounds via KEGG). Run Bayesian inference to compute posterior probabilities for each feature–candidate pair by integrating: observed m/z against predicted adduct masses, observed isotope patterns against theoretical patterns (computed from chemical formula), and presence of observed features in a connected biochemical network. The framework assigns higher posterior probability to candidates whose predicted isotopologues match observed intensity ratios and whose metabolic neighbors are also detected in the sample. Output a feature table with ranked annotation candidates and their posterior probabilities, allowing you to set a confidence threshold (e.g., posterior > 0.7) to filter ambiguous assignments.

## Related tools

- **ipaPy2** (Core implementation of the Integrated Probabilistic Annotation method; performs Bayesian inference over LC/MS features using biochemical relations, isotope patterns, and adduct formation.) — https://github.com/francescodc87/ipaPy2
- **Python** (Language for running ipaPy2 and manipulating feature and database DataFrames.)

## Examples

```
from ipaPy2 import IPA; import pandas as pd; adducts = pd.read_csv('DB/adducts.csv'); database = pd.read_csv('DB/IPA_MS1.csv'); features = pd.read_csv('features.csv'); ipa = IPA(database, adducts); results = ipa.annotate(features)
```

## Evaluation signals

- Posterior probabilities sum to 1.0 (or close, within numerical precision) across all candidates for each feature, confirming proper Bayesian normalization.
- Features with known reference standards or spike-in compounds achieve posterior probability ≥ 0.7 for the correct metabolite, confirming discriminative power.
- Isotope pattern predictions (from chemical formula) have peak intensity ratios within ≤10% of observed ratios for top-ranked candidates, verifying isotope integration fidelity.
- Annotated features whose metabolic neighbors (linked via reaction network) are also present in the dataset receive higher posterior probabilities than isolated candidates, confirming biochemical network effect.
- Retention time windows in the database (if provided) exclude candidates falling outside the observed RT ± tolerance window, and posterior probabilities reflect this constraint.

## Limitations

- Quality of annotation depends critically on the completeness and accuracy of the metabolic database (MS¹ table) and reaction network; KEGG/MoNa/NPA databases used in the README example may not cover all sample-specific compounds or modified metabolites.
- Isotope pattern integration assumes isotopic composition follows natural abundance; biological enrichment (e.g., ¹³C or ¹⁵N labeling) will produce patterns mismatched to theoretical predictions and lower posterior probabilities.
- Adduct formation rules are instrument- and solvent-dependent; the provided adducts.csv covers 'most common' adducts but exotic in-source fragments or unusual ion suppression patterns are user-configurable and may not be pre-loaded.
- Bayesian priors (pk field, prior knowledge on compound presence) are user-defined and subjective; poor prior calibration can bias rankings toward or away from likely candidates.
- The method does not integrate MS² fragmentation spectra natively in the core annotation step (MS² IDs are stored in the database but used for post-hoc validation only in the current README example).

## Evidence

- [other] IPA is a Bayesian annotation method for LC/MS data that integrates three key information sources: biochemical relations, isotope patterns, and adduct formation to compute annotation probabilities.: "IPA is a Bayesian annotation method for LC/MS data that integrates three key information sources: biochemical relations, isotope patterns, and adduct formation"
- [other] Run Bayesian inference to compute posterior annotation probabilities for each feature, integrating biochemical plausibility, observed isotope patterns, and predicted adduct formation.: "Run Bayesian inference to compute posterior annotation probabilities for each feature, integrating biochemical plausibility, observed isotope patterns, and predicted adduct formation"
- [readme] The IPA method requires a pandas dataframe containing the database against which the annotation is performed. This dataframe must contain the following columns in this exact order (optional columns can have empty fields): id, name, formula, inchi, smiles, RT, adductsPos, adductsNeg, description, pk, MS2, reactions.: "The IPA method requires a pandas dataframe containing the database against which the annotation is performed. This dataframe must contain the following columns in this exact order: id, name, formula,"
- [readme] The ipaPy2 library requires a file contains all the information required for the computation of the adducts. An adducts.csv file is provided with the package. The file contains the most common adducts.: "The ipaPy2 library requires a file contains all the information required for the computation of the adducts. An adducts.csv file is provided with the package"
- [readme] pk: previous knowledge on the likelihood of this compound to be present in the sample analyse. The value has to be between 1 (compound highly likely to be present in the sample) and 0 (compound cannot be present in the sample).: "pk: previous knowledge on the likelihood of this compound to be present in the sample. The value has to be between 1 and 0"
- [readme] To fully exploit the IPA method, it is strongly recommended to constantly update the database when new knowledge is gained from previous experience. Providing a retention time window for compounds previously detected with the analytical system at hand it is particularly useful.: "To fully exploit the IPA method, it is strongly recommended to constantly update the database when new knowledge is gained from previous experience"
