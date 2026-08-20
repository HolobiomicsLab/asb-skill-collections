---
name: small-molecule-structure-matching
description: Use when you have observed compounds (from LC-MS, GC-MS, or spectroscopy) and a set of predicted metabolite structures from BioTransformer, and need to assign identities to the observed compounds by matching their experimental features (mass-to-charge ratio, retention time, spectral signature) to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3407
  tools:
  - BioTransformer
  techniques:
  - LC-MS
  - GC-MS
  - NMR
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# small-molecule-structure-matching

## Summary

Match predicted metabolite structures against observed spectral, chromatographic, or mass-based features using structural similarity or mass-to-charge alignment to assign candidate identities. This skill leverages BioTransformer's metabolism predictions as the basis for metabolite identification by ranking and filtering candidate structures by probability score and experimental match criteria.

## When to use

You have observed compounds (from LC-MS, GC-MS, or spectroscopy) and a set of predicted metabolite structures from BioTransformer, and need to assign identities to the observed compounds by matching their experimental features (mass-to-charge ratio, retention time, spectral signature) to predicted structures ranked by metabolism probability.

## When NOT to use

- Input compounds are already structurally characterized by orthogonal methods (e.g., NMR, X-ray crystallography) — use direct chemical structure determination instead.
- No metabolism predictions are available for your compounds — run BioTransformer prediction first.
- Observed compounds are not expected to be metabolites of your parent molecule(s) — skill assumes the observed compound list derives from exposure to or biotransformation of known parent compounds.

## Inputs

- Predicted metabolite structures from BioTransformer (SMILES, MOL, or SDF format)
- Predicted metabolite probability or likelihood scores
- Observed compound data: mass-to-charge ratios (m/z) and/or spectral features
- Experimental compound list or chromatographic/spectral dataset

## Outputs

- Structured output table: metabolite names, predicted structures, match scores, organism context
- SDF or CSV file with annotated candidate metabolite identities
- Optionally: PubChem annotations (CID, synonyms) for each match

## How to apply

Load predicted metabolite structures from BioTransformer's metabolism prediction module, ranked by probability or likelihood score. Define your match criterion: either structural similarity (e.g., Tanimoto coefficient, substructure matching) or mass-to-charge alignment (using a specified mass tolerance, typically 0.01 Da as shown in the examples). For each observed compound, compute the match score against all predicted structures and select the top-ranked match(es) above your similarity threshold or within your mass tolerance window. Assign candidate metabolite identities and record the match score, predicted structure, metabolite name, and organism context (mammalian, gut microbiota, or environmental microbial) in a structured output table. Validate by checking whether high-scoring matches align with experimental evidence and metabolic plausibility.

## Related tools

- **BioTransformer** (Generates predicted metabolite structures and reaction types; provides the candidate pool and probability ranking for structure matching.) — https://github.com/Wishartlab-openscience/Biotransformer

## Examples

```
java -jar biotransformer-3.0.0.jar -k cid -b allHuman -ismi "O[C@@H]1CC2=C(O)C=C(O)C=C2O[C@@H]1C1=CC=C(O)C(O)=C1" -osdf ~/metabolites.sdf -s 2 -m "292.0946;304.0946" -t 0.01 -a
```

## Evaluation signals

- All observed compounds are assigned a candidate metabolite identity with match score ≥ threshold (e.g., Tanimoto ≥ 0.7 or mass difference ≤ 0.01 Da).
- High-scoring matches correspond to plausible biotransformation pathways (e.g., oxidation, conjugation) consistent with the organism module selected (mammalian, gut, or environmental).
- Candidate identities can be cross-validated against orthogonal data: retention time ordering, fragmentation patterns, or PubChem/literature annotations.
- No observed compound is left unmatched to a predicted structure when the parent compound is in the BioTransformer database and the organism module is appropriate.
- Match table is complete and properly formatted, with metabolite names, structures, scores, and organism context populated for all matches.

## Limitations

- Accuracy depends on BioTransformer's prediction quality; novel or unmapped metabolic pathways may be missed.
- Environmental microbial predictions include both aerobic and anaerobic reactions by default, which may inflate the candidate pool and reduce specificity if only one condition applies.
- Mass tolerance and similarity thresholds must be calibrated for your instrument and experimental protocol; default 0.01 Da mass tolerance may not suit all platforms.
- Structure matching does not account for metabolite stereoisomers or regio-isomers if only structure is compared; additional experimental evidence (e.g., NMR, MS/MS fragmentation) may be needed for disambiguation.
- Metabolite identification based on structure alone cannot confirm biological activity or toxicity; predicted structures require independent validation.

## Evidence

- [other] Match predicted structures against observed spectral/chromatographic features or provided experimental compound lists using structural similarity or mass-to-charge alignment.: "Match predicted structures against observed spectral/chromatographic features or provided experimental compound lists using structural similarity or mass-to-charge alignment."
- [other] Rank predicted metabolites by probability or likelihood score.: "Rank predicted metabolites by probability or likelihood score."
- [other] Assign candidate metabolite identities to observed compounds and generate a structured output table with metabolite names, predicted structures, match scores, and organism context.: "Assign candidate metabolite identities to observed compounds and generate a structured output table with metabolite names, predicted structures, match scores, and organism context."
- [readme] Identify all human metabolites (max depth = 2) of Epicatechin with masses 292.0946 Da and 304.0946 Da, with a mass tolerance of 0.01 Da.: "Identify all human metabolites (max depth = 2) of Epicatechin with masses 292.0946 Da and 304.0946 Da, with a mass tolerance of 0.01 Da."
- [intro] BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction.: "BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction."
