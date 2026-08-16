---
name: organism-context-metabolic-plausibility-assessment
description: Use when when BioTransformer or another metabolism predictor has generated
  a list of candidate metabolite structures (in SMILES or InChI format) for a query
  compound, and you need to identify which candidates are most likely to occur in
  a specific organism or environment (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - BioTransformer
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer3.0jar.git
  license_tier: noncommercial
derived_from:
- doi: 10.1093/nar/gkac408
  title: BioTransformer 3.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that
  predicts small molecule metabolism
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_3_0_cq
    doi: 10.1093/nar/gkac408
    title: BioTransformer 3.0
  dedup_kept_from: coll_biotransformer_3_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkac408
  all_source_dois:
  - 10.1093/nar/gkac408
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# organism-context-metabolic-plausibility-assessment

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Rank and filter predicted metabolite candidates by their biological plausibility within a specific organismal context (mammalian, gut microbial, or soil/aquatic). This skill validates computationally predicted structures against the metabolic capacity and biochemistry of the target organism or environment, reducing false positives in metabolite identification.

## When to use

When BioTransformer or another metabolism predictor has generated a list of candidate metabolite structures (in SMILES or InChI format) for a query compound, and you need to identify which candidates are most likely to occur in a specific organism or environment (e.g., human liver, human gut microbiota, soil/aquatic microbiota). Use this skill to filter and rank candidates before querying chemical databases, so that only biologically plausible structures are retained.

## When NOT to use

- The input is a single predicted metabolite structure with no alternatives to rank; plausibility assessment is most valuable when discriminating among multiple candidates.
- The organism or environment context is not clearly specified or is non-standard (e.g., an unusual host or engineered microbiome); BioTransformer's built-in contexts (mammalian, hgut, envimicro) may not capture your specific scenario accurately.
- Your goal is rapid structure annotation without regard to metabolic realism; if you only need a list of possible products for computational screening, this skill adds unnecessary filtering overhead.

## Inputs

- predicted metabolite structures (SMILES or InChI format)
- query compound identifier
- target organism or environment context (e.g., 'mammalian', 'human gut microbial', 'soil/aquatic microbial')

## Outputs

- ranked candidate metabolite list with confidence scores
- filtered set of plausible metabolite structures retained for database matching

## How to apply

After obtaining predicted metabolite structures from BioTransformer, assess each candidate's plausibility by evaluating its compatibility with the metabolic pathways, enzyme families, and biochemical transformations known to occur in the target organism or environment. Score candidates based on: (1) whether the structural transformation matches known Phase I (oxidation/reduction), Phase II (conjugation/deconjugation), or microbial enzymatic reactions documented in the target context; (2) the evolutionary prevalence of the relevant enzyme classes in that organism; and (3) the biological relevance of the product structure (e.g., increased water solubility for Phase II products, or intermediates that feed into central metabolism). Rank candidates by confidence and filter to retain only those scoring above a context-appropriate threshold before proceeding to database lookups.

## Related tools

- **BioTransformer** (Generates predicted metabolite structures and supports metabolite identification assisted by organism-specific metabolic context (mammalian, gut microbial, environmental microbial modules)) — https://github.com/Wishartlab-openscience/Biotransformer

## Examples

```
java -jar biotransformer-3.0.0.jar -k cid -b allHuman -ismi "O[C@@H]1CC2=C(O)C=C(O)C=C2O[C@@H]1C1=CC=C(O)C(O)=C1" -osdf output.sdf -s 2 -m "292.0946;304.0946" -t 0.01 -a
```

## Evaluation signals

- Ranked candidate list includes confidence scores or plausibility ranks per candidate, with biological justification tied to documented enzymatic pathways in the target organism.
- Filtered set size is reduced compared to the raw prediction output, indicating that implausible structures have been removed.
- Downstream database queries (PubChem, ChEMBL, HMDB) on the filtered candidates return higher match rates and higher-confidence identifications compared to unfiltered candidates.
- Manual spot-checks of top-ranked candidates confirm that their structural transformations are consistent with known Phase I/II or microbial metabolism in the specified organism/environment.
- Confidence scores or filtering threshold are documented, allowing reproducibility and adjustment if downstream validation reveals false positives or false negatives.

## Limitations

- BioTransformer's metabolic rules and enzyme coverage are precomputed and may not capture rare or recently characterized biotransformation pathways specific to your organism or environment.
- Confidence scoring relies on heuristics encoded in BioTransformer and may not reflect the true metabolic likelihood in all cases; validation against authentic metabolomic or in vitro data is recommended.
- Organism contexts supported by BioTransformer are coarse (mammalian, human gut, soil/aquatic); if your target organism is a non-human mammal, plant, fungus, or specialized microbiome, predictions may be less accurate.
- Plausibility assessment does not account for kinetic factors (enzyme Km, Vmax) or saturation effects that influence which metabolites actually accumulate in vivo; structural plausibility is necessary but not sufficient for quantitative prediction.

## Evidence

- [other] BioTransformer assists scientists in metabolite identification by using metabolism predictions as input; the identification assistance mechanism operates on predicted metabolites generated from the prior metabolism prediction step.: "BioTransformer assists scientists in metabolite identification by using metabolism predictions as input; the identification assistance mechanism operates on predicted metabolites generated from the"
- [other] Score and rank candidate identifications by structural similarity, database coverage, and biological plausibility within the relevant organism/environment context (mammalian, gut microbial, or soil/aquatic).: "Score and rank candidate identifications by structural similarity, database coverage, and biological plausibility within the relevant organism/environment context (mammalian, gut microbial, or"
- [readme] BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota.: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota."
- [readme] The type of biotransformer - EC-based (ecbased), CYP450 (cyp450), Phase II (phaseII), Human gut microbial (hgut), human super transformer (superbio, or allHuman), Environmental microbial (envimicro).: "The type of biotransformer - EC-based (ecbased), CYP450 (cyp450), Phase II (phaseII), Human gut microbial (hgut), human super transformer (superbio, or allHuman), Environmental microbial (envimicro)."
