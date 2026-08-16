---
name: network-based-metabolite-identification
description: Use when when you have m/z values from spatially-resolved mass spectrometry imaging (MSI) and need to predict their molecular formulae with high precision.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SMART
  techniques:
  - LC-MS
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- we present SMART, an open-source platform designed for precise formula assignment in mass spectrometry imaging
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_cq
    doi: 10.1021/acs.analchem.4c06210
    title: SMART
  dedup_kept_from: coll_smart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06210
  all_source_dois:
  - 10.1021/acs.analchem.4c06210
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# network-based-metabolite-identification

## Summary

A method for assigning molecular formulae to mass-to-charge (m/z) values in spatially-resolved metabolomics by leveraging a large knowledge network of interconnected formulae and their biological relationships. This skill uses multiple linear regression and network scoring to achieve higher precision than traditional LC-MS annotation approaches.

## When to use

When you have m/z values from spatially-resolved mass spectrometry imaging (MSI) and need to predict their molecular formulae with high precision. Particularly useful when annotation accuracy lags behind LC-MS-based methods and you want to exploit biological and chemical relationships among candidate formulae.

## When NOT to use

- Input consists of already-annotated feature tables; the skill is for de novo formula prediction from raw m/z values.
- You require sub-1 ppm mass accuracy or have instrumental limitations that prevent reliable m/z measurement; the method's scoring relies on PPM thresholds.
- Your metabolites are predominantly from non-biological sources or synthetic compounds not represented in HMDB, ChEMBL, KEGG, or PubChem; the KnownSet database coverage determines performance.

## Inputs

- m/z values (numeric, single or in batch file format)
- SMART database file (.db)
- multiple linear regression model file (.pkl)
- polarity information (+ or -)
- PPM tolerance threshold (integer, default 5)

## Outputs

- predicted molecular formulae with scores
- database source identifiers (HMDB, ChEMBL, PubChem codes)
- precision metrics on reference datasets
- structured results file

## How to apply

Load a KnownSet database of ~2.8 million formulae interconnected by DBEdges (from HMDB, ChEMBL, PubChem) and BioEdges (from KEGG). For each m/z value of interest, apply a multiple linear regression model to extract a formula network. Score candidate formulae using three criteria: linked formulae (via DBEdges/BioEdges), edge type, and mass accuracy (PPM tolerance, typically 5 ppm). Rank candidates by composite score and return the top matches. Validate predictions against reference datasets and compute precision metrics to confirm the method achieves the reported desirable precision on your reference set.

## Related tools

- **SMART** (Core platform that constructs the KnownSet database, applies the multiple linear regression model, and scores formula candidates based on network relationships and PPM tolerance) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- Precision score matches or exceeds the reported desirable precision on reference benchmarking datasets.
- Predicted formulae are ranked by composite score (linked-formula weight + edge-type weight + mass accuracy); top-ranked predictions should align with ground truth in validation sets.
- PPM error between observed m/z and predicted formula mass falls within the user-specified threshold (default ≤5 ppm).
- DBEdges and BioEdges sourced from the same repositories (HMDB, ChEMBL, PubChem, KEGG) that trained the model; out-of-database metabolites show lower precision.
- Results are reproducible across multiple runs on the same m/z input with identical model and database versions.

## Limitations

- Accuracy of formula prediction depends on coverage and quality of the KnownSet database; metabolites absent from HMDB, ChEMBL, PubChem, and KEGG will not be reliably predicted.
- The multiple linear regression model was trained on specific reference datasets; performance may degrade on m/z distributions or metabolite classes not well-represented in training data.
- Raw SMART-database exceeds 1 Terabyte; the temporary downloadable version includes only HMDB data, which may limit precision on non-HMDB metabolites.
- PPM tolerance and model parameters must be tuned for specific instrument types and mass accuracy characteristics; default 5 ppm may not suit all platforms.

## Evidence

- [readme] KnownSet database construction and coverage: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG"
- [readme] Multiple linear regression model application: "By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest"
- [readme] Scoring criteria: "scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values"
- [readme] Precision validation: "Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision"
- [readme] Problem context and motivation: "Spatially-resolved metabolomics plays a critical role in unraveling tissue-specific metabolic complexities. Despite significance, this profound technology generates thousands of features, the"
- [readme] Database scale limitation: "Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte, users who want to use the raw SMART-database can contact us"
