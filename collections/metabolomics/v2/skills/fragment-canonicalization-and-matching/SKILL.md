---
name: fragment-canonicalization-and-matching
description: Use when you have a collection of molecular fragments (e.g., from molecular decomposition, retrosynthesis, or synthetic planning) that must be matched to known fragment libraries or standardized representations before feeding them into a transformer assembly model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - transformer architecture
  - convolutional neural network
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmr2struct
    doi: 10.1021/acscentsci.4c01132
    title: NMR2Struct
  dedup_kept_from: coll_nmr2struct
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.4c01132
  all_source_dois:
  - 10.1021/acscentsci.4c01132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-canonicalization-and-matching

## Summary

Canonicalize and match molecular fragments to standardized representations for use in transformer-based assembly workflows. This skill converts raw fragment inputs into a consistent format suitable for training and inference in fragment-to-structure prediction models.

## When to use

Apply this skill when you have a collection of molecular fragments (e.g., from molecular decomposition, retrosynthesis, or synthetic planning) that must be matched to known fragment libraries or standardized representations before feeding them into a transformer assembly model. Use it when fragment identity and ordering matter for downstream assembly accuracy, or when you need to reconcile fragments across different databases or naming conventions.

## When NOT to use

- Input fragments are already in canonical SMILES form and perfectly aligned to known targets
- Your downstream task does not require assembly or does not use a transformer architecture
- Fragment diversity or chemical space exploration is the goal, rather than accurate deterministic assembly

## Inputs

- raw molecular fragments (SMILES, InChI, or structural objects)
- fragment-structure ground truth pairs (paired dataset)
- reference fragment library or database

## Outputs

- canonicalized fragment representations (canonical SMILES or standardized graph form)
- matched fragment-to-target structure alignments
- ordered or unordered fragment sets ready for transformer input

## How to apply

Extract or prepare fragment-structure ground truth pairs from a deposited dataset, identifying individual molecular fragments and their corresponding assembled target structures. Convert each fragment to a canonical form (e.g., canonical SMILES) to ensure consistent representation across training and inference. Implement a matching procedure that aligns input fragments against a reference fragment library using graph isomorphism or canonical string comparison. Group matched fragments by assembly target and order them (or treat as unordered sets depending on the transformer variant) before passing to the attention-based assembly module. Document any fragments that fail to match or canonicalize, as these represent potential assembly failure modes.

## Related tools

- **transformer architecture** (accepts canonicalized and matched fragment sets as input; applies attention mechanisms to model fragment relationships during assembly)
- **convolutional neural network** (integrated with transformer to encode spectroscopic data; indirectly depends on canonical fragment matching for end-to-end structure prediction)

## Evaluation signals

- All fragments in ground truth pairs successfully canonicalize to SMILES without loss of connectivity or stereochemistry
- Fragment-to-target matching achieves ≥95% recall against the reference library (i.e., fragments known to exist in targets are correctly identified)
- No duplicate or ambiguous canonical representations exist within the matched fragment set for a given assembly target
- Downstream transformer model achieves baseline or improved exact structure match rate on held-out test pairs after canonicalization
- Failure logs show low false-positive match rate and cluster canonicalization failures to specific fragment classes (e.g., rare stereoisomers, large aromatic systems)

## Limitations

- Canonicalization may collapse or lose information about local stereochemistry in fragments not yet bonded in the target structure; enforce explicit stereochemistry encoding if regiochemistry is critical.
- Fragment matching performance degrades on fragments larger than ~10 heavy atoms or with extreme branching, as graph isomorphism becomes computationally expensive and ambiguity increases.
- The skill assumes a well-curated reference library; performance on novel or out-of-distribution fragments (not present in training pairs) is not guaranteed.
- Fragments that are identical after canonicalization but arise from different synthetic routes or contexts may be conflated, losing route-specific information.

## Evidence

- [other] Extract or prepare fragment-structure ground truth pairs from the deposited dataset, identifying molecular fragments and their corresponding assembled target structures.: "Extract or prepare fragment-structure ground truth pairs from the deposited dataset, identifying molecular fragments and their corresponding assembled target structures."
- [other] Build a transformer architecture that takes an ordered or unordered set of molecular fragments as input and outputs candidate assembled molecular structures using attention mechanisms for fragment relationship modeling.: "Build a transformer architecture that takes an ordered or unordered set of molecular fragments as input and outputs candidate assembled molecular structures using attention mechanisms for fragment"
- [intro] a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [other] Train the transformer module on the fragment-structure pairs using a structure prediction loss (e.g., graph matching or canonical SMILES accuracy).: "Train the transformer module on the fragment-structure pairs using a structure prediction loss (e.g., graph matching or canonical SMILES accuracy)."
- [other] Document assembly failures and success patterns across molecular complexity ranges (atoms, branching, ring systems).: "Document assembly failures and success patterns across molecular complexity ranges (atoms, branching, ring systems)."
