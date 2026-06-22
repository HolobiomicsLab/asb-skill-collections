---
name: candidate-metabolite-ranking
description: Use when when you have generated a set of predicted metabolite structures from BioTransformer's metabolism prediction engine and need to assign identity to observed compounds from LC-MS/MS, spectral, or chromatographic experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - BioTransformer
derived_from:
- doi: 10.1186/s13321-019-0375-2
  title: BioTransformer 1.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that predicts small molecule metabolism
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_1_0_cq
    doi: 10.1186/s13321-019-0375-2
    title: BioTransformer 1.0
  dedup_kept_from: coll_biotransformer_1_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-019-0375-2
  all_source_dois:
  - 10.1186/s13321-019-0375-2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# candidate-metabolite-ranking

## Summary

Rank predicted metabolite structures by probability or likelihood score to prioritize candidate identities for matching against observed experimental data. This skill transforms raw BioTransformer metabolism predictions into a prioritized list suitable for structural similarity matching and mass-to-charge alignment.

## When to use

When you have generated a set of predicted metabolite structures from BioTransformer's metabolism prediction engine and need to assign identity to observed compounds from LC-MS/MS, spectral, or chromatographic experiments. Use this skill when the number of predicted metabolites exceeds the number of observed compounds, or when you need to reduce false positives by focusing validation effort on high-confidence predictions.

## When NOT to use

- Input is a single observed compound with no predicted metabolite set (ranking requires ≥2 predictions to prioritize).
- Predicted structures have no associated probability or likelihood score from the biotransformer engine (ranking requires a quantitative confidence metric).
- You are performing de novo metabolite discovery without a predictive model (this skill assumes predictions have already been generated; use prediction-based workflows if not).

## Inputs

- Parent compound (SMILES string, MOL file, or SDF file)
- Predicted metabolite structures with associated probability/likelihood scores from BioTransformer biotransformer module
- Observed compound list (masses, formulas, or spectral features)
- Target organism context (mammals, hgut, envimicro)

## Outputs

- Ranked metabolite list (CSV or SDF format)
- Candidate metabolite assignments with match scores
- Structured output table with metabolite names, predicted structures, ranking scores, and organism context

## How to apply

After generating predicted metabolite structures using BioTransformer's metabolism prediction module for your target organism(s) (mammals, gut microbiota, or soil/aquatic microbiota), rank the output by the probability or likelihood score assigned by the biotransformer module. Sort predictions in descending order of confidence. Then match the top-ranked predicted structures against observed spectral/chromatographic features or provided experimental compound lists using structural similarity metrics or mass-to-charge alignment with a specified tolerance (default 0.01 Da per the README). Assign candidate metabolite identities to observed compounds and generate a structured output table containing metabolite names, predicted structures, match scores, ranking position, and organism context. The ranking acts as a filter step: only predictions above a user-defined confidence threshold proceed to experimental validation.

## Related tools

- **BioTransformer** (Generates predicted metabolite structures and assigns probability/likelihood scores; enables ranking by confidence for candidate metabolite prioritization) — https://github.com/Wishartlab-openscience/Biotransformer

## Examples

```
java -jar biotransformer-3.0.0.jar -k cid -b allHuman -ismi "O[C@@H]1CC2=C(O)C=C(O)C=C2O[C@@H]1C1=CC=C(O)C(O)=C1" -osdf output.sdf -s 2 -m "292.0946;304.0946" -t 0.01 -a
```

## Evaluation signals

- Ranked predictions are sorted in descending order of probability/likelihood score with no inversions or gaps.
- Output table contains exactly one match score per predicted metabolite; all scores fall within expected range [0, 1] or equivalent confidence metric.
- Candidate metabolites matched to observed compounds have match scores above the specified threshold (default mass tolerance 0.01 Da); unmatched predictions are clearly flagged or excluded.
- For true-positive metabolites (if experimental validation is available), the true structure ranks in the top N predictions (where N is user-defined, typically ≤5 for high-confidence ranking).
- Output file format (CSV or SDF) conforms to schema: metabolite name, SMILES or structure, predicted rank, match score, organism, parent compound context.

## Limitations

- Ranking confidence depends entirely on the biotransformer module's probability scoring; poor-quality or untrained prediction engines will produce unreliable ranks.
- Mass-to-charge matching requires accurate experimental mass measurements; spectra with low mass resolution or calibration errors will produce false negatives even for top-ranked predictions.
- Environmental microbial degradation predictions use data from EAWAG's Biodegradation and Biocatalysis Database, licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0; commercial use requires explicit license from EnviPath.
- Ranking does not account for organism-specific enzyme availability or pathway feasibility; a high-ranked prediction may be enzymatically infeasible in the target organism.

## Evidence

- [other] 3. Rank predicted metabolites by probability or likelihood score.: "Rank predicted metabolites by probability or likelihood score."
- [other] 4. Match predicted structures against observed spectral/chromatographic features or provided experimental compound lists using structural similarity or mass-to-charge alignment.: "Match predicted structures against observed spectral/chromatographic features or provided experimental compound lists using structural similarity or mass-to-charge alignment."
- [other] 5. Assign candidate metabolite identities to observed compounds and generate a structured output table with metabolite names, predicted structures, match scores, and organism context.: "Assign candidate metabolite identities to observed compounds and generate a structured output table with metabolite names, predicted structures, match scores, and organism context."
- [intro] BioTransformer assists scientists in metabolite identification, based on the metabolism prediction.: "BioTransformer assists scientists in metabolite identification, based on the metabolism prediction."
- [readme] -t,--mTolerance                     Mass tolerance for metabolite identification (default is 0.01).: "Mass tolerance for metabolite identification (default is 0.01)."
