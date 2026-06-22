---
name: biosynthetic-gene-cluster-annotation
description: Use when when you have BGC sequences in FASTA or GenBank format and need to identify and extract biosynthetic Pfam domains for feature-based clustering, similarity search, or functional characterization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3092
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_3371
  tools:
  - pyHMMER
  - BiG-SLiCE
  - PFAM 35.0
derived_from:
- doi: 10.1093/gigascience/giaa154
  title: BiG-SLiCE
evidence_spans:
- Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_big_slice_cq
    doi: 10.1093/gigascience/giaa154
    title: BiG-SLiCE
  dedup_kept_from: coll_big_slice_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa154
  all_source_dois:
  - 10.1093/gigascience/giaa154
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biosynthetic-gene-cluster-annotation

## Summary

Annotate biosynthetic domains within BGC sequences by scanning against PFAM 35.0 HMM models using pyHMMER, producing normalized domain-feature vectors for downstream clustering and comparative analysis. This skill leverages the pyHMMER library to replace external HMMER binaries, enabling in-memory processing without intermediate files.

## When to use

When you have BGC sequences in FASTA or GenBank format and need to identify and extract biosynthetic Pfam domains for feature-based clustering, similarity search, or functional characterization. Use this skill if you are building a domain-feature matrix for cosine-like distance-based BGC clustering or querying a BGC against a Gene Cluster Family database.

## When NOT to use

- Input is already a pre-calculated domain-feature matrix or normalized vector table — skip directly to clustering.
- BGC sequences are not in FASTA or GenBank format and cannot be parsed by the pyHMMER interface.
- You require domain annotations from non-PFAM sources (e.g. custom HMM databases or protein family databases other than Pfam 35.0).

## Inputs

- BGC sequences in FASTA format
- BGC sequences in GenBank format
- PFAM 35.0 HMM model database (bigslice-models-2022-11-30)
- pyHMMER interface configuration

## Outputs

- Domain hit table (gene identifiers, Pfam accessions, coordinates, e-values, bit-scores)
- Normalized domain-feature matrix (l2-normalized vectors)
- TSV export of pre-calculated BGC domain annotations
- TSV export of GCF-level domain profiles

## How to apply

Load BGC sequences (FASTA or GenBank format) and initialize the pyHMMER interface with PFAM 35.0 HMM models from the bigslice-models-2022-11-30 database. Scan each BGC sequence against the Pfam HMM profiles using pyHMMER with default e-value and bit-score cutoffs to identify biosynthetic domains. Extract domain hits (gene identifiers, Pfam accessions, domain coordinates, e-values, bit-scores) and aggregate into a domain-feature table. Normalize the resulting domain presence/absence or bit-score vectors using l2-normalization to prepare for cosine-like distance clustering. Export the normalized domain-feature matrix and detailed hit information to TSV output files for downstream analysis.

## Related tools

- **pyHMMER** (Cython-based Python interface to HMMER3 that performs in-memory HMM-based domain scanning against PFAM profiles without external binary dependencies or intermediate files) — https://github.com/althonos/pyhmmer
- **BiG-SLiCE** (Orchestrates the biosynthetic domain detection workflow, manages PFAM 35.0 HMM databases, normalizes domain features via l2-normalization, and exports results to TSV) — https://github.com/medema-group/bigslice
- **PFAM 35.0** (Provides the HMM profiles for biosynthetic and general protein domain detection; updated version used by BiG-SLiCE v2)

## Examples

```
from pyhmmer.plan7 import HMMFile; from pyhmmer.easel import SequenceFile; hits = hmmsearch(HMMFile('PFAM_35.0.hmm'), SequenceFile('bgc.fasta')); normalized_scores = l2_normalize(extract_bitscore_vector(hits)); export_to_tsv(normalized_scores, 'bgc_domain_features.tsv')
```

## Evaluation signals

- Domain hit table contains expected columns (gene ID, Pfam accession, e-value, bit-score, domain coordinates) with no missing or malformed entries.
- E-values and bit-scores fall within biologically plausible ranges (e-values ≤ default threshold, bit-scores > 0 for significant hits).
- Normalized domain-feature vectors have l2-norm equal to 1.0 (or near 1.0 accounting for floating-point precision).
- TSV exports are parseable and contain consistent row counts across related output files (e.g., BGC and GCF tables).
- Cosine-like distances computed between pairs of normalized domain vectors fall in the range [0, 1] and exhibit expected similarity patterns (e.g., identical BGCs have distance ≈ 0).

## Limitations

- HMM-based annotation is limited to Pfam 35.0 profiles; novel or non-canonical biosynthetic domains not represented in PFAM may be missed.
- E-value and bit-score cutoffs are set to defaults; sequences near the detection boundary may be incorrectly included or excluded, requiring manual review for edge cases.
- L2-normalization assumes domain feature vectors are comparable; highly imbalanced domain compositions (e.g., very short vs. very long BGCs) may distort cosine-like distance metrics.
- The skill does not perform sequence alignment or phylogenetic placement; domain hits are purely presence/absence or quantitative (bit-score) without evolutionary context.

## Evidence

- [other] Scan each BGC sequence against the Pfam HMM models using pyHMMER with default e-value threshold and bit-score cutoffs to identify biosynthetic domains.: "Scan each BGC sequence against the Pfam HMM models using pyHMMER with default e-value threshold and bit-score cutoffs to identify biosynthetic domains."
- [other] Normalize domain presence/absence or bit-score vectors using l2-normalization to prepare for downstream cosine-like distance clustering.: "Normalize domain presence/absence or bit-score vectors using l2-normalization to prepare for downstream cosine-like distance clustering."
- [readme] Clustering now uses __cosine-like__ (via l2-normalization) distances: "Clustering now uses __cosine-like__ (via l2-normalization) distances"
- [readme] Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer) (__speed-ups__, can now be fully installed via __pip__): "Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer) (__speed-ups__, can now be fully installed via __pip__)"
- [readme] pHMM databases have been updated to __PFAM 35.0__: "pHMM databases have been updated to __PFAM 35.0__"
- [other] Extract domain hits (gene identifiers, Pfam accessions, domain coordinates, e-values, bit-scores) and aggregate into a feature table.: "Extract domain hits (gene identifiers, Pfam accessions, domain coordinates, e-values, bit-scores) and aggregate into a feature table."
