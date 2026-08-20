---
name: pfam-domain-hit-extraction
description: Use when you have BGC sequences (in FASTA or GenBank format) and need
  to identify conserved biosynthetic domains to build a feature vector for BGC similarity
  clustering or to annotate gene functions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3092
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_0621
  tools:
  - pyHMMER
  - PFAM
  - BiG-SLiCE
  - PFAM 35.0
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/gigascience/giaa154
  title: BiG-SLiCE
evidence_spans:
- Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer)
- pHMM databases have been updated to __PFAM 35.0__
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

# PFAM Domain Hit Extraction from BGC Sequences

## Summary

Extract biosynthetic protein domains and their annotations from BGC sequences by scanning against PFAM 35.0 HMM models using pyHMMER, producing a normalized feature table for downstream clustering. This skill replaces the slower external HMMER binary with an in-process Cython-bound implementation, enabling reproducible domain detection without intermediate files.

## When to use

You have BGC sequences (in FASTA or GenBank format) and need to identify conserved biosynthetic domains to build a feature vector for BGC similarity clustering or to annotate gene functions. This is the entry point when you want to detect Pfam hits that will later be l2-normalized for cosine-like distance clustering in BiG-SLiCE v2.

## When NOT to use

- Input is already a pre-computed normalized feature table — skip to clustering.
- You require HMMER binary outputs (multiple fixed-width tabular files) — use external HMMER instead of pyHMMER.
- Your workflow must run on Windows or non-UNIX systems — HMMER and pyHMMER do not support these platforms.

## Inputs

- BGC sequences in FASTA format
- BGC sequences in GenBank format
- PFAM 35.0 HMM database (bigslice-models-2022-11-30)

## Outputs

- Domain hit table (gene ID, Pfam accession, coordinates, e-value, bit-score)
- L2-normalized domain-feature matrix (TSV)
- Hit details export (TSV)

## How to apply

Load BGC sequences and initialize the pyHMMER interface with the bigslice-models-2022-11-30 PFAM 35.0 HMM database. Scan each BGC sequence against Pfam HMM models using pyHMMER's hmmscan with default e-value and bit-score cutoffs to identify domain hits. For each domain match, extract the gene identifier, Pfam accession, domain coordinate boundaries, e-value, and bit-score. Aggregate hits into a feature table where rows are genes/domains and columns track presence/absence or bit-score magnitudes. Apply l2-normalization to each feature vector to prepare for downstream cosine-like distance-based clustering. Export the normalized domain-feature matrix and raw hit details to TSV format for external analysis or input to BiG-SLiCE clustering.

## Related tools

- **pyHMMER** (In-process Cython-bound HMMER3 interface; performs domain scanning against HMM profiles without external binaries or intermediate files.) — https://github.com/althonos/pyhmmer
- **BiG-SLiCE** (Orchestrates the full BGC clustering pipeline; wraps pyHMMER-based domain extraction and applies l2-normalization for cosine-like distance clustering.) — https://github.com/medema-group/bigslice
- **PFAM 35.0** (Reference HMM profile database containing biosynthetic and sub-Pfam models; fetched via bigslice-models-2022-11-30.)

## Examples

```
from pyhmmer.plan7 import HMMFile; from pyhmmer.easel import SequenceFile; hmmdb = HMMFile('bigslice-models-2022-11-30/biosynthetic.hmm'); seqs = SequenceFile('input_bgc.fasta'); hits = [h for query in seqs for h in hmmsearch(hmmdb, [query])]
```

## Evaluation signals

- Each domain hit has a valid Pfam accession matching the PFAM 35.0 database.
- E-values and bit-scores fall within expected ranges (e.g., e-value ≤ threshold, bit-score ≥ 0).
- L2-normalized feature vectors have unit norm (L2 norm ≈ 1.0 ± small floating-point error).
- Feature matrix row count equals the total number of unique domain hits; column count equals number of unique genes/sequences.
- TSV export files parse without formatting errors and contain no null or missing critical fields (accession, coordinates, scores).

## Limitations

- Domain detection sensitivity and specificity depend on PFAM 35.0 model quality and the chosen e-value/bit-score thresholds; these are not tuned for every BGC type.
- L2-normalization compresses absolute bit-score magnitude into the unit sphere, which may reduce discriminative power for very weak domain hits.
- pyHMMER is restricted to UNIX-like systems (Linux, macOS); Windows users must use external HMMER binaries or alternative platforms.
- No changelog is available in the provided sources, so parameter or output format changes between versions may not be explicitly documented.

## Evidence

- [other] Scan each BGC sequence against the Pfam HMM models using pyHMMER with default e-value threshold and bit-score cutoffs to identify biosynthetic domains.: "Scan each BGC sequence against the Pfam HMM models using pyHMMER with default e-value threshold and bit-score cutoffs to identify biosynthetic domains."
- [other] Extract domain hits (gene identifiers, Pfam accessions, domain coordinates, e-values, bit-scores) and aggregate into a feature table.: "Extract domain hits (gene identifiers, Pfam accessions, domain coordinates, e-values, bit-scores) and aggregate into a feature table."
- [other] Normalize domain presence/absence or bit-score vectors using l2-normalization to prepare for downstream cosine-like distance clustering.: "Normalize domain presence/absence or bit-score vectors using l2-normalization to prepare for downstream cosine-like distance clustering."
- [readme] Switching from HMMER to pyHMMER (speed-ups, can now be fully installed via pip): "Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer) (__speed-ups__, can now be fully installed via __pip__)"
- [readme] no intermediate files: Everything happens in memory, in Python objects you have control on, making it easier to pass your inputs to HMMER without needing to write them to a temporary file.: "no intermediate files: Everything happens in memory, in Python objects you have control on, making it easier to pass your inputs to HMMER without needing to write them to a temporary file."
- [readme] Clustering now uses cosine-like (via l2-normalization) distances: "Clustering now uses __cosine-like__ (via l2-normalization) distances"
