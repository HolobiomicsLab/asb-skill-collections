---
name: metabolite-identifier-annotation
description: Use when you have observed compounds (from LC-MS/MS, GC-MS, NMR, or other analytical techniques) with unknown identity and you want to assign candidate metabolite structures by comparing them to computationally predicted metabolism pathways.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - BioTransformer
  - PubChem
  - EAWAG Biodegradation and Biocatalysis Database
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-identifier-annotation

## Summary

This skill leverages BioTransformer's metabolism prediction engine to assign candidate metabolite identities to observed compounds by ranking predicted structures and matching them against experimental spectral or mass-to-charge data. It bridges computational prediction and experimental validation, enabling systematic annotation of unknown metabolites with structure, organism context, and confidence scores.

## When to use

Use this skill when you have observed compounds (from LC-MS/MS, GC-MS, NMR, or other analytical techniques) with unknown identity and you want to assign candidate metabolite structures by comparing them to computationally predicted metabolism pathways. Triggers include: (1) detected m/z peaks or chromatographic features without spectral library matches; (2) a known parent compound and interest in identifying its in vivo or environmental metabolites; (3) need to contextualize metabolites by organism (mammals, gut microbiota, soil/aquatic microbiota).

## When NOT to use

- Input compound is not a small molecule or is outside BioTransformer's chemical space (e.g., large proteins, nucleic acids, or highly exotic synthetic compounds with no precedent in biotransformation databases).
- Observed compounds are already confidently identified by orthogonal methods (e.g., direct comparison to authentic standards via NMR or X-ray crystallography); use this skill for *candidate* assignment, not validation of already-known structures.
- Organism context does not match available BioTransformer modules (e.g., you need metabolism in a specialized bacterial strain not covered by ecbased, hgut, or envimicro; or you need plant or fungal metabolism, which BioTransformer does not support).

## Inputs

- parent compound (SMILES string, MOL file, or SDF file)
- observed compound list with masses (whitespace- or semicolon-separated list of m/z values)
- biotransformer module selection (ecbased, cyp450, phaseII, hgut, superbio, allHuman, or envimicro)
- optional: mass tolerance threshold (Da)
- optional: number of transformation steps (integer ≥ 1)
- optional: experimental spectral or chromatographic feature data

## Outputs

- structured metabolite table (CSV or SDF format) containing: metabolite names, predicted structures (MOL/SMILES), match scores, organism context, transformation step pathway
- mass-matched metabolite candidates ranked by probability or likelihood
- annotated metabolite information (PubChem CID, synonyms, common names if -a flag used)
- SDF or CSV file with predicted metabolite structures and metadata

## How to apply

First, initialize BioTransformer 3.0.0 and select the appropriate biotransformer module (e.g., allHuman, hgut, envimicro) matching your organism(s) of interest. Input the parent compound as SMILES, MOL, or SDF and generate predicted metabolite structures across 1–n transformation steps (default=1). Rank predictions by likelihood score or biotransformation probability. Next, match predicted structures against your observed compounds using structural similarity metrics or mass-to-charge alignment with a specified mass tolerance (default 0.01 Da). Assign the best-matching predicted metabolite to each observed compound, and optionally annotate with PubChem metadata (CID, synonyms, common names). Generate a structured CSV or SDF output table containing metabolite names, structures, match scores, organism context, and transformation pathway information. Success is indicated by: (1) coverage of observed masses within the specified tolerance; (2) chemical plausibility of assigned transformations; (3) consistency between predicted structure and experimental spectral features.

## Related tools

- **BioTransformer** (Core prediction and metabolite identification engine; generates predicted metabolite structures and assists in candidate assignment to observed compounds) — https://github.com/Wishartlab-openscience/Biotransformer
- **PubChem** (Optional annotation source for metabolite names, synonyms, and compound identifiers (CID) via -a flag)
- **EAWAG Biodegradation and Biocatalysis Database** (Underlying data source for environmental microbial degradation predictions (envimicro module)) — https://envipath.org/

## Examples

```
java -jar biotransformer-3.0.0.jar -k cid -b allHuman -ismi "O[C@@H]1CC2=C(O)C=C(O)C=C2O[C@@H]1C1=CC=C(O)C(O)=C1" -osdf metabolites.sdf -s 2 -m "292.0946;304.0946" -t 0.01 -a
```

## Evaluation signals

- All observed m/z values are matched to predicted metabolite masses within the specified tolerance (default ≤ 0.01 Da); check output CSV/SDF for zero or near-zero gaps.
- Assigned metabolites represent chemically plausible biotransformations (e.g., oxidation, reduction, conjugation) consistent with known Phase I/II or microbial pathways for the target organism.
- Match scores or likelihood rankings are above a user-defined threshold (e.g., top 3 candidates reported for each observed mass); cross-validate against experimental spectral features (fragmentation patterns, retention time shifts).
- Output structure files (SDF) are parseable and contain valid MOL blocks; metabolite names and organism contexts are non-empty and consistent with selected BioTransformer module.
- Identified metabolites can be traced back to known biotransformation rules (CYP450 oxidation, UDP-glucuronidation, sulfation, etc.) as documented in BioTransformer's rule base.

## Limitations

- BioTransformer's predictions are limited to small molecule metabolism and do not cover large macromolecular substrates (proteins, lipids, nucleic acids).
- Prediction accuracy depends on the completeness of training data; rare or novel biotransformations not yet documented in underlying databases (EAWAG BBD, PPS, literature rules) will not be predicted.
- Environmental microbial module (envimicro) requires commercial licensing for use beyond academic/research scope; CC-BY-NC-SA 4.0 license restricts commercial redistribution (EnviPath data).
- Mass tolerance and structural similarity thresholds must be tuned by user; overly stringent thresholds may miss true metabolites, while loose thresholds introduce false candidates.
- No built-in mechanism to rank candidates by experimental likelihood (e.g., spectral fit, retention index); user must perform manual curation or integrate external scoring (e.g., in silico MS/MS fragmentation prediction).

## Evidence

- [other] BioTransformer assists scientists in metabolite identification by leveraging its metabolism predictions as the basis for candidate structure assignment to observed compounds.: "BioTransformer assists scientists in metabolite identification by leveraging its metabolism predictions as the basis for candidate structure assignment to observed compounds."
- [other] Match predicted structures against observed spectral/chromatographic features or provided experimental compound lists using structural similarity or mass-to-charge alignment.: "Match predicted structures against observed spectral/chromatographic features or provided experimental compound lists using structural similarity or mass-to-charge alignment."
- [readme] This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota.: "This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota."
- [readme] Identify all human metabolites (max depth = 2) of Epicatechin with masses 292.0946 Da and 304.0946 Da, with a mass tolerance of 0.01 Da.: "Identify all human metabolites (max depth = 2) of Epicatechin with masses 292.0946 Da and 304.0946 Da, with a mass tolerance of 0.01 Da."
- [readme] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons"
- [other] Load BioTransformer version 3.0.0 and initialize the metabolism prediction module for the target organism(s) (mammals, gut microbiota, or soil/aquatic microbiota).: "Load BioTransformer version 3.0.0 and initialize the metabolism prediction module for the target organism(s) (mammals, gut microbiota, or soil/aquatic microbiota)."
- [other] Rank predicted metabolites by probability or likelihood score.: "Rank predicted metabolites by probability or likelihood score."
