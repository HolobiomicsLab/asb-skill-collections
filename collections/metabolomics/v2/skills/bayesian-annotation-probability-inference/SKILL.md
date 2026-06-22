---
name: bayesian-annotation-probability-inference
description: Use when you have LC/MS feature data (m/z, retention time, intensity) and need to assign metabolite annotations with confidence scores rather than binary peak-to-compound matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - ipaPy2
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

# bayesian-annotation-probability-inference

## Summary

Apply Bayesian inference to compute posterior annotation probabilities for LC/MS features by integrating biochemical relations, isotope patterns, and adduct formation. This skill assigns confidence-ranked metabolite candidates to each observed m/z feature using prior knowledge and instrument-specific adduct libraries.

## When to use

Use this skill when you have LC/MS feature data (m/z, retention time, intensity) and need to assign metabolite annotations with confidence scores rather than binary peak-to-compound matches. Particularly valuable when multiple candidate compounds have similar m/z values, or when isotope patterns and adduct multiplicity are observable in your feature set, allowing Bayesian integration of these orthogonal signals to disambiguate annotations.

## When NOT to use

- Input is already a validated feature table with assigned metabolite identities (skill is for annotation inference, not refinement of existing annotations).
- Your database lacks chemical formulas or adduct information; Bayesian integration requires these to compute predicted m/z under each adduct form.
- You have no prior knowledge of compound–compound biochemical relationships and do not need to leverage reaction networks; a simpler mass-matching tool may suffice.

## Inputs

- LC/MS feature table (m/z, retention time, intensity)
- MS1 metabolite reference database (pandas DataFrame or CSV with columns: id, name, formula, RT, adductsPos, adductsNeg, pk, reactions)
- Adducts configuration file (CSV with adduct name, mass shift, charge, ionization mode)

## Outputs

- Feature table with assigned top metabolite candidate per feature
- Posterior annotation probabilities for each feature–metabolite pair
- Ranked list of candidate metabolites per feature

## How to apply

Load LC/MS feature data into ipaPy2 along with a metabolite reference database (MS1 file with chemical formulas, expected adducts per ionization mode, and optionally retention time windows and biochemical reaction networks). Configure the adduct library (adducts.csv) to match your instrument's ionization mode and common in-source fragments. Run Bayesian inference, which computes a posterior probability for each feature–compound pair by combining: (1) the predicted m/z under each possible adduct form, (2) the observed isotope pattern envelope, (3) biochemical plausibility from reaction network connectivity, and (4) prior knowledge (pk) weights per compound. The output is a ranked feature table where each feature is assigned a top candidate metabolite and its posterior probability; use this probability as a confidence threshold (e.g., retain only annotations with posterior > 0.5) to filter low-confidence hits.

## Related tools

- **ipaPy2** (Python library implementing Bayesian annotation inference; handles adduct prediction, isotope pattern integration, and posterior probability computation) — https://github.com/francescodc87/ipaPy2
- **Python** (Language in which ipaPy2 is implemented and executed)

## Examples

```
import pandas as pd; from ipaPy2 import IPA; DB = pd.read_csv('DB/IPA_MS1.csv'); adducts = pd.read_csv('DB/adducts.csv'); ipa = IPA(DB, adducts, ionMode='positive'); results = ipa.annotate(features_mz, features_rt, features_intensity)
```

## Evaluation signals

- Posterior probabilities are in valid range [0, 1] and sum sensibly (if summed over all candidates for a feature, close to 1.0)
- Features with high-confidence isotope pattern matches to predicted adduct envelopes receive higher posterior probabilities
- Retention time window filtering (if provided in the database) correctly prunes candidates outside the RT window, reducing their posterior probability
- Top-ranked candidates for known spike-in or standard compounds match expected identities with posterior > 0.7
- Mass error between observed m/z and predicted m/z for top-ranked candidates is within instrument resolution (e.g., <5 ppm for Orbitrap)

## Limitations

- Requires a well-curated reference database with accurate chemical formulas and realistic adduct lists; garbage-in-garbage-out—missing or incorrect adduct specifications will produce misleading probabilities.
- Isotope pattern integration assumes accurate intensity ratios in the observed feature envelope; very low signal-to-noise or overlapping peaks will degrade pattern matching.
- Biochemical relation integration (reaction network connectivity) only improves annotation if the database includes reaction IDs and the sample is expected to contain metabolically related compounds; not all LC/MS experiments benefit from this signal.
- Prior knowledge (pk) weights must be manually set per compound; no automatic prior learning is implemented, so probabilities remain subjective without domain expertise.
- Does not handle MS/MS fragmentation spectra directly (though optional MS2 IDs can be linked in the database for manual follow-up); annotation is based on MS1 data only.

## Evidence

- [other] IPA is a Bayesian annotation method for LC/MS data that integrates three key information sources: biochemical relations, isotope patterns, and adduct formation to compute annotation probabilities.: "Bayesian annotation method for LC/MS data integrating biochemical relations, isotope patterns and adduct formation"
- [readme] The IPA method requires a pandas dataframe containing the database against which the annotation is performed. This dataframe must contain the following columns in this exact order (optional columns can have empty fields): id, name, formula, inchi, smiles, RT, adductsPos, adductsNeg, description, pk, MS2, reactions: "IPA method requires a pandas dataframe containing the database against which the annotation is performed. This dataframe must contain the following columns: id, name, formula, inchi, smiles, RT,"
- [readme] The ipaPy2 library requires a file contains all the information required for the computation of the adducts. An adducts.csv file is provided with the package. The file contains the most common adducts.: "ipaPy2 library requires a file contains all the information required for the computation of the adducts. An adducts.csv file is provided with the package"
- [other] Run Bayesian inference to compute posterior annotation probabilities for each feature, integrating biochemical plausibility, observed isotope patterns, and predicted adduct formation.: "Bayesian inference to compute posterior annotation probabilities for each feature, integrating biochemical plausibility, observed isotope patterns, and predicted adduct formation"
- [readme] To fully exploit the IPA method, it is strongly recommended to constantly update the database when new knowledge is gained from previous experience. Providing a retention time window for compounds previously detected with the analytical system at hand it is particularly useful.: "strongly recommended to constantly update the database when new knowledge is gained. Providing a retention time window is particularly useful"
