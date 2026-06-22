---
name: hmm-profile-database-querying
description: Use when when you have BGC sequences (FASTA or GenBank format) or protein sequences and need to annotate them with biosynthetic or functional domains from a curated pHMM database (e.g., PFAM 35.0).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0346
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_3511
  tools:
  - pyHMMER
  - BiG-SLiCE
  - PFAM 35.0
  - HMMER3
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
---

# hmm-profile-database-querying

## Summary

Query biological sequences against profile hidden Markov model (pHMM) databases to identify homologous domains and functional annotations. This skill enables fast, memory-efficient HMM-based domain detection on biosynthetic gene clusters or protein sequences using Python bindings to HMMER3, replacing slower CLI-based approaches.

## When to use

When you have BGC sequences (FASTA or GenBank format) or protein sequences and need to annotate them with biosynthetic or functional domains from a curated pHMM database (e.g., PFAM 35.0). Use this skill when you need domain hit coordinates, e-values, bit-scores, and normalized feature vectors for downstream clustering or similarity analysis, and when you want to avoid external HMMER binary dependencies or temporary file I/O.

## When NOT to use

- Input sequences are already annotated with domain calls from another tool—use the existing annotations directly rather than re-scanning.
- You require alignment output or multiple sequence alignment of domain regions—pyHMMER returns hit coordinates and scores but does not generate MSAs by default.
- Your pHMM database is not available in binary format or your HMMER version is incompatible with the pyHMMER bindings you have installed.

## Inputs

- BGC sequences in FASTA or GenBank format
- Protein sequences in FASTA or DigitalSequence objects
- Profile HMM database (e.g., PFAM 35.0 models from bigslice-models-2022-11-30)

## Outputs

- Domain hit table (gene identifier, Pfam accession, domain coordinates, e-value, bit-score)
- Normalized domain-feature matrix (l2-normalized; rows = sequences, columns = Pfam domains or bit-scores)
- TSV export of BGCs, GCFs, and hit details for visualization and downstream clustering

## How to apply

Load BGC or protein sequences into memory (FASTA or GenBank format) and initialize a pyHMMER interface with the target pHMM database (e.g., bigslice-models-2022-11-30 containing PFAM 35.0 HMMs). Scan each sequence against the HMM models using pyHMMER's hmmsearch or hmmscan with default e-value and bit-score cutoffs to extract domain hits (Pfam accessions, coordinates, e-values, bit-scores). Aggregate hits into a feature table indexed by gene/sequence identifier. Normalize the resulting domain presence/absence or bit-score vectors using l2-normalization to prepare for cosine-like distance metrics in downstream clustering. Export the normalized feature matrix and raw hit details to TSV format for reproducibility and downstream analysis.

## Related tools

- **pyHMMER** (Cython-based Python bindings to HMMER3 for fast, in-memory HMM scanning without external binary dependencies) — https://github.com/althonos/pyhmmer
- **BiG-SLiCE** (Biosynthetic gene cluster clustering engine that uses pyHMMER for domain detection on BGCs and exports normalized domain-feature matrices for GCF construction) — https://github.com/medema-group/bigslice
- **PFAM 35.0** (Curated profile HMM database used for domain annotation in BiG-SLiCE v2.0)
- **HMMER3** (Underlying sequence analysis tool and profile HMM library; pyHMMER provides direct Cython bindings to HMMER internals) — http://hmmer.org/

## Examples

```
from pyhmmer.plan7 import HMM, SequenceFile
from pyhmmer.hmmer import hmmsearch
hmmdb = HMMFile('pfam35.0.h3m')
seqs = SequenceFile('bgcs.fasta')
hits = hmmsearch(hmmdb, seqs)
for hit in hits:
    print(hit.accession, hit.bitscore, hit.evalue)
```

## Evaluation signals

- Domain hit table contains non-empty rows for all input sequences or a documented subset; check for presence of Pfam accessions, coordinates, and bit-scores meeting the cutoff threshold.
- Normalized feature matrix has l2-norm = 1.0 (or close, within floating-point tolerance) for each row, confirming cosine-distance compatibility.
- E-values and bit-scores are consistent with HMMER3 output ranges (e-values ≥ 0, bit-scores typically > 0 for significant hits).
- TSV exports are machine-readable and parseable; row and column counts match the number of input sequences and Pfam domains, respectively.
- Memory usage stays constant or grows linearly with input size (no temporary file artifacts); runtime is faster than equivalent CLI HMMER commands on the same hardware.

## Limitations

- pyHMMER speed-ups depend on pre-built wheels for your CPU architecture (x86-64, Arm64); non-UNIX and exotic CPU targets may require compilation or fallback to CLI HMMER.
- Domain detection depends on e-value and bit-score cutoffs; the article does not specify how cutoffs are tuned for different Pfam subsets (e.g., biosynthetic vs. sub-Pfam), so threshold sensitivity should be validated per use case.
- L2-normalization assumes domain hit counts or bit-scores are comparable across sequences; skewed distributions or sequences with very few or many domains may require additional scaling.
- pHMM databases must be downloaded separately (e.g., ~271 MB gzipped for bigslice-models-2022-11-30); updates require manual re-download and re-indexing.

## Evidence

- [readme] Switching from HMMER to pyHMMER for speed improvements and full pip installation: "Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer) (__speed-ups__, can now be fully installed via __pip__)"
- [readme] pyHMMER provides in-memory HMM scanning without intermediate files: "**no intermediate files**: Everything happens in memory, in Python objects you have control on, making it easier to pass your inputs to HMMER without needing to write them to a temporary file."
- [other] Domain hits are extracted and aggregated into a feature table: "Extract domain hits (gene identifiers, Pfam accessions, domain coordinates, e-values, bit-scores) and aggregate into a feature table."
- [other] L2-normalization prepares domain features for cosine-like distance clustering: "Normalize domain presence/absence or bit-score vectors using l2-normalization to prepare for downstream cosine-like distance clustering."
- [readme] BiG-SLiCE v2 uses PFAM 35.0 for domain annotation: "pHMM databases have been updated to __PFAM 35.0__"
- [readme] TSV export capability for pre-calculated results: "Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)"
