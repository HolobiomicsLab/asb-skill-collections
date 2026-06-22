---
name: shifted-dot-product-scoring
description: Use when matching query mass spectra to a spectral library in the presence of unknown post-translational modifications (PTMs) or non-enzymatic modifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- ANN-SoLo (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00359
  all_source_dois:
  - 10.1021/acs.jproteome.8b00359
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# shifted-dot-product-scoring

## Summary

Shifted dot product scoring is a sensitive mass spectrum similarity metric that accounts for mass shifts caused by post-translational modifications by comparing query spectra against library spectra over a range of mass offsets. This enables detection of peptides bearing unknown or open modifications while maintaining strict false discovery rate control.

## When to use

Apply this skill when matching query mass spectra to a spectral library in the presence of unknown post-translational modifications (PTMs) or non-enzymatic modifications. The query spectrum may represent a modified peptide whose unmodified counterpart exists in the library, but with m/z values shifted by the modification mass. Use this when you need to identify both unmodified and modified peptide-spectrum matches while controlling false discovery rate, particularly in open modification searches where the modification type is not pre-specified.

## When NOT to use

- Input spectra are already annotated with specific known modifications: use standard dot product or cosine similarity scoring without mass shifting.
- Spectral library contains only unmodified peptides and you are searching for unmodified query spectra: standard spectral library search without cascade strategy is more efficient.
- Mass spectrometry data are low-resolution or have poor mass accuracy (>50 ppm): shifted dot product mass offsets require precise m/z values to distinguish genuine modifications from noise.

## Inputs

- query spectra in mzML or mzXML format
- approximate nearest neighbor indexed spectral library
- mass offset range (Da) spanning expected modification masses
- candidate library spectrum set (pre-filtered by ANN indexing)

## Outputs

- peptide-spectrum match (PSM) identifications with scores
- mass shift annotations for matched spectra
- false discovery rate filtered PSM results

## How to apply

After approximate nearest neighbor indexing has selected a limited candidate set of library spectra, compute shifted dot product scores between the query spectrum and each candidate library spectrum across a range of mass offsets (typically spanning the modification mass search range). For each candidate, shift the query spectrum by a series of discrete mass deltas, compute the standard dot product (or cosine similarity) for each offset, and retain the maximum score across all tested shifts. This approach allows a single query to match library spectra with different mass shifts in a single pass. Apply false discovery rate filtering to the scored matches using a cascade strategy: first score unmodified matches, then iteratively score modified matches at higher mass shifts, resetting the FDR calculation at each cascade level to maximize sensitivity while maintaining strict error control.

## Related tools

- **ANN-SoLo** (spectral library search engine that implements shifted dot product scoring within a cascade search strategy for open modification identification) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (approximate nearest neighbor indexing library underlying ANN-SoLo's candidate spectrum selection) — https://github.com/facebookresearch/faiss

## Examples

```
# After indexing spectral library with ANN-SoLo, search query spectra and score with mass shifts:
# ann_solo search -i library.mgf -q query.mzML -o results.tsv -s 10 -e 200
# (implicitly applies shifted dot product scoring across mass offset range during cascade search)
```

## Evaluation signals

- Verification that shifted dot product scores increase monotonically (or remain stable) as mass offset approaches the true modification mass, then decrease as offset moves away from true modification.
- Confirmation that identified modified peptides have consistent mass shifts matching known or expected PTM masses (phosphorylation +79.97 Da, acetylation +42.01 Da, etc.).
- False discovery rate for modified matches remains ≤ target threshold (typically 1% or 5%) when computed at each cascade level independently.
- Sensitivity (% of true positive PSMs identified) should be higher with shifted dot product scoring than with unshifted dot product when modifications are present, at equivalent false discovery rate.
- Query-library spectrum pairs with high shifted dot product scores should have visually similar peak patterns when the spectra are aligned at the identified mass offset.

## Limitations

- Shifted dot product scoring increases computational cost linearly with the number of tested mass offsets; very wide modification mass search ranges (e.g., ±500 Da) may become prohibitively slow without GPU acceleration.
- The method assumes modification masses are known or can be bounded within a reasonable range; it will not detect modifications outside the pre-defined mass offset range.
- Performance degrades on low-resolution spectra with few peaks or high noise, as the dot product similarity metric becomes less discriminative.
- The cascade search strategy requires careful tuning of FDR thresholds at each level to balance sensitivity against false discovery; suboptimal thresholds can inflate error rates.

## Evidence

- [readme] shifted dot product score to sensitively match modified spectra to their unmodified counterpart: "the shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
- [intro] cascade search strategy to maximize identified unmodified and modified spectra while strictly controlling false discovery rate: "combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [intro] approximate nearest neighbor indexing selects limited candidate spectra compared to unknown query spectrum: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [intro] query spectra compared using shifted dot product scoring: "comparing each query to the selected candidate library spectra using shifted dot product scoring"
