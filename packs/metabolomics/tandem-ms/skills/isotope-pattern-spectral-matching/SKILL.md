---
name: isotope-pattern-spectral-matching
description: Use when when you have LC/MS feature data with observed m/z and intensity values across multiple peaks (monoisotopic and isotopologues) and need to narrow candidate annotations from a metabolite database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
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

# isotope-pattern-spectral-matching

## Summary

Integrate observed isotope patterns from LC/MS features with predicted isotope signatures to assign annotation probabilities to candidate metabolites. This approach leverages the distinctive mass and intensity distribution of isotopologue peaks to disambiguate structurally similar compounds and improve annotation confidence in untargeted metabolomics.

## When to use

When you have LC/MS feature data with observed m/z and intensity values across multiple peaks (monoisotopic and isotopologues) and need to narrow candidate annotations from a metabolite database. Particularly valuable when multiple database entries share similar neutral masses within instrument tolerance (e.g., within 5 ppm), or when biochemical plausibility and adduct formation alone produce ambiguous results.

## When NOT to use

- Input features lack resolved isotope peaks (e.g., low mass resolution, poor signal-to-noise) — isotope matching will contribute minimal discriminative power.
- Analyzing singly-occurring features with no detectable isotopologues above noise threshold — isotope pattern scoring becomes uninformative.
- Database compounds have identical or near-identical chemical formulas — isotope patterns will be too similar to provide meaningful differentiation.

## Inputs

- LC/MS feature table with m/z, retention time, and intensity values
- Observed peak intensities for isotope envelope (monoisotopic + isotopologues)
- Metabolite database with chemical formulas (e.g., IPA_MS1.csv format)
- Adduct configuration file specifying adduct types and masses

## Outputs

- Annotation probability scores per feature per candidate metabolite
- Feature table with top-ranked metabolite assignments and isotope-matching likelihood component
- Posterior probability distribution over candidate annotations weighted by isotope pattern fit

## How to apply

Within the IPA Bayesian framework, isotope pattern matching works by (1) extracting the observed intensity distribution across m/z peaks for each LC/MS feature, including monoisotopic and isotopic variants; (2) computing the theoretical isotope pattern for each database candidate compound using its chemical formula; (3) calculating the probability that the observed pattern matches the predicted pattern given measurement noise and instrument resolution; (4) integrating this probability with biochemical relation scores and adduct formation likelihoods into a posterior annotation probability via Bayes' rule. Features with sharper isotope peak resolution and closer concordance between observed and predicted patterns (higher isotope-matching likelihood) contribute more strongly to the final annotation score. The method assumes accurate mass calibration and sufficient signal-to-noise ratio to resolve at least the monoisotopic and +1 (13C/15N) isotope peaks.

## Related tools

- **ipaPy2** (Executes Bayesian integration of isotope patterns, biochemical relations, and adduct formation for LC/MS feature annotation) — https://github.com/francescodc87/ipaPy2
- **Python** (Runtime environment for ipaPy2 and custom isotope pattern computation scripts)

## Examples

```
from ipaPy2 import IPA; import pandas as pd; adducts = pd.read_csv('DB/adducts.csv'); DB = pd.read_csv('DB/IPA_MS1.csv'); features = pd.read_csv('features.csv'); ipa = IPA(adducts, DB); annotations = ipa.annotate(features, ion_mode='positive')
```

## Evaluation signals

- Monoisotopic and +1 isotope peak intensities are in expected ratio given the chemical formula (e.g., for organic compounds, +1 peak is typically 0.5–2× monoisotopic intensity depending on element composition)
- The top-ranked annotation candidate has isotope pattern likelihood > threshold (typically >0.7 in Bayesian posterior), and this score is higher than for competing candidates
- Retention time of the annotated compound (if available in database) falls within ±10–20 seconds of observed feature retention time, indicating coherent annotation across multiple data dimensions
- No systematic bias in isotope pattern residuals (observed minus predicted) across the m/z range — residuals should scatter randomly around zero
- Cross-validation: independently measured MS2 fragmentation spectra or reference standards confirm the top isotope-matched annotation

## Limitations

- Accuracy depends on database chemical formulas being correct; missing or misidentified formulas in the database prevent isotope matching from improving annotation.
- Isotope pattern matching requires m/z resolution sufficient to resolve 13C/15N isotopologues (Δm ≈ 1.0033 Da); lower-resolution instruments (e.g., Q-TOF with <5 ppm mass accuracy across m/z range) may not resolve isotope envelopes clearly enough to exploit this skill.
- High dynamic range features or coeluting compounds can produce distorted isotope envelopes that do not match theoretical predictions, leading to false isotope-based rejection of correct annotations.
- Multiply-charged ions (e.g., [M+2H]2+) have reduced isotope spacing and overlapping peaks, making isotope pattern resolution and matching more difficult.
- Natural abundance variation in stable isotopes is assumed; this method is not applicable to heavily labeled samples (e.g., 13C-labeled metabolites) without reformulating the theoretical isotope model.

## Evidence

- [other] IPA is a Bayesian annotation method for LC/MS data that integrates three key information sources: biochemical relations, isotope patterns, and adduct formation to compute annotation probabilities.: "Bayesian annotation method for LC/MS data integrating biochemical relations, isotope patterns and adduct formation"
- [other] Run Bayesian inference to compute posterior annotation probabilities for each feature, integrating biochemical plausibility, observed isotope patterns, and predicted adduct formation.: "Run Bayesian inference to compute posterior annotation probabilities for each feature, integrating biochemical plausibility, observed isotope patterns, and predicted adduct formation"
- [readme] The MS1 database file must contain the following columns including formula: chemical formula (e.g., 'C6H12O6') - necessary: "formula: chemical formula (e.g., 'C6H12O6') - *necessary*"
- [readme] The adducts file contains all the information required for the computation of the adducts, including Mass and Ion_mode fields.: "The ipaPy2 library requires a file contains all the information required for the computation of the adducts. An adducts.csv file is provided with the package"
- [readme] To fully exploit the IPA method, it is strongly recommended to constantly update the database when new knowledge is gained from previous experience. Providing a retention time window for compounds previously detected with the analytical system at hand it is particularly useful.: "To fully exploit the IPA method, it is strongly recommended to constantly update the database when new knowledge is gained from previous experience. Providing a retention time window"
