---
name: mass-accuracy-ppm-filtering
description: Use when when you have a set of candidate molecular formulae for a measured m/z value and need to rank them by how closely their theoretical m/z matches the observed value.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_3172
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-accuracy-ppm-filtering

## Summary

Filter and rank candidate molecular formulae by mass accuracy using parts-per-million (PPM) error thresholds, a key criterion in the SMART multiple linear regression scoring pipeline for m/z-based formula assignment in mass spectrometry imaging.

## When to use

When you have a set of candidate molecular formulae for a measured m/z value and need to rank them by how closely their theoretical m/z matches the observed value. Use this when PPM mass accuracy is a scoring criterion in a formula assignment or annotation workflow, particularly in spatially-resolved metabolomics where feature annotation precision lags behind LC-MS.

## When NOT to use

- When input is already a validated, annotated feature table (PPM filtering is upstream annotation step, not post-hoc validation).
- When dealing with low-resolution mass spectrometry data where mass accuracy is insufficient to distinguish between formulae (PPM filtering assumes sufficient resolution).
- When no theoretical m/z reference database or candidate formula set is available (PPM comparison requires both observed and theoretical values).

## Inputs

- observed m/z value (decimal numeric)
- candidate molecular formulae (chemical formula strings or structures)
- theoretical m/z values for each candidate (decimal numeric, precomputed)
- PPM threshold parameter (default: 5 ppm)

## Outputs

- filtered candidate formula set (formulae within PPM threshold)
- ranked formula list with PPM error scores
- confidence-scored formula network (when integrated into MLR model)

## How to apply

Calculate the mass error in PPM between the observed m/z value and the theoretical m/z of each candidate formula using the formula: PPM = ((observed_mz − theoretical_mz) / theoretical_mz) × 10^6. Filter candidate formulae to retain only those within a specified PPM threshold (default: 5 ppm in SMART). Rank the retained candidates by absolute PPM error, with lower PPM error indicating higher confidence. Include PPM values as one of three criteria in a multiple linear regression model alongside linked formulae connections and DBEdges/BioEdges relationship strength to produce a final confidence-ranked formula network.

## Related tools

- **SMART** (integrates PPM-based filtering as one of three criteria in a multiple linear regression model to score and rank candidate formulae from formula networks extracted from the KnownSet database) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
py SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- PPM error values for all returned candidates fall within the specified PPM threshold (e.g., ≤5 ppm by default).
- Candidates are ranked in ascending order of absolute PPM error, confirming that lowest-error formulae appear first.
- When integrated into the MLR model, PPM scores contribute proportionally to final formula ranking alongside linked-formulae and DBEdges/BioEdges criteria.
- The number of filtered candidates is reasonable (typically 1–10 per m/z) and does not collapse the candidate space to zero nor explode to implausibly many hits.
- Known positive formulae (from benchmarking datasets) are retained within the PPM threshold and ranked competitively vs. false positives.

## Limitations

- PPM threshold sensitivity: Too stringent a threshold (e.g., <2 ppm) may exclude correct formulae due to instrument calibration drift or isotope effects; too lenient (e.g., >10 ppm) may retain too many candidates, reducing discriminative power.
- Does not account for adduct formation, fragmentation, or neutral loss; PPM filtering is applied to the observed m/z directly and must be calibrated for the ionization mode (+/−/0 polarity) used in the experiment.
- Formula candidate set quality directly impacts output: PPM filtering cannot recover correct formulae if they are not present in the underlying KnownSet database (2.8 million formulae from HMDB, ChEMBL, PubChem, KEGG).

## Evidence

- [readme] scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values: "scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values"
- [other] Score each candidate formula using criteria including linked formulae connections, DBEdges/BioEdges relationship strength, and PPM mass accuracy values.: "Score each candidate formula using criteria including linked formulae connections, DBEdges/BioEdges relationship strength, and PPM mass accuracy values."
- [readme] PPM threshold for formula assignment (Default: 5).: "PPM threshold for formula assignment (Default: 5)."
