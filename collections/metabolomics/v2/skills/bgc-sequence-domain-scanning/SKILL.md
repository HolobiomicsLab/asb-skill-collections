---
name: bgc-sequence-domain-scanning
description: Use when you have BGC sequences (in FASTA or GenBank format) from antiSMASH or other sources and need to extract biosynthetic domain composition as the primary signal for GCF (Gene Cluster Family) clustering or similarity queries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3092
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0622
  tools:
  - pyHMMER
  - BiG-SLiCE
  - PFAM 35.0
  - antiSMASH v7.0.0
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

# bgc-sequence-domain-scanning

## Summary

Scan biosynthetic gene cluster (BGC) sequences against Hidden Markov Model (HMM) databases to identify and extract biosynthetic Pfam domains, producing normalized feature vectors for downstream clustering and comparative analysis. This skill replaces traditional HMMER with the pyHMMER library for improved speed and dependency-free installation.

## When to use

Apply this skill when you have BGC sequences (in FASTA or GenBank format) from antiSMASH or other sources and need to extract biosynthetic domain composition as the primary signal for GCF (Gene Cluster Family) clustering or similarity queries. Use it as the mandatory upstream step before l2-normalization and cosine-distance clustering in BiG-SLiCE v2.

## When NOT to use

- Input is already a pre-calculated domain-feature matrix or normalized BGC feature table — skip to clustering step
- You need amino acid sequence alignment or functional annotations beyond Pfam domain presence/absence — use specialized alignment tools instead
- Your BGCs are from PFAM versions earlier than 35.0 and you require strict version compatibility — use the older HMMER-based BiG-SLiCE v1.x pipeline

## Inputs

- BGC sequences in FASTA format
- BGC sequences in GenBank format
- antiSMASH output folder
- PFAM 35.0 HMM database (bigslice-models-2022-11-30)

## Outputs

- Domain hit table (TSV with gene IDs, Pfam accessions, coordinates, e-values, bit-scores)
- Normalized domain-feature matrix (l2-normalized, TSV)
- BGC feature vectors ready for cosine-distance clustering

## How to apply

Load BGC sequence data in FASTA or GenBank format and initialize the pyHMMER interface with the PFAM 35.0 HMM database (bigslice-models-2022-11-30). Scan each BGC sequence against Pfam HMM models using pyHMMER with default e-value threshold and bit-score cutoffs to identify and extract domain hits (gene identifiers, Pfam accessions, domain coordinates, e-values, bit-scores). Aggregate hits into a feature table, then normalize domain presence/absence or bit-score vectors using l2-normalization to prepare for cosine-like distance clustering. Export the normalized domain-feature matrix and hit details to TSV output files for downstream GCF analysis or querying.

## Related tools

- **pyHMMER** (Cython-based Python binding to HMMER3 for in-memory HMM scanning without external HMMER binary dependency; enables speed-up and full pip installation) — https://github.com/althonos/pyhmmer
- **BiG-SLiCE** (Orchestrates the domain scanning workflow via pyHMMER, loads PFAM 35.0 HMM database, aggregates hits, and prepares features for l2-normalization and GCF clustering) — https://github.com/medema-group/bigslice
- **PFAM 35.0** (HMM profile database of biosynthetic and general protein families used for sequence homology detection)
- **antiSMASH v7.0.0** (Upstream tool that defines BGC sequences and class annotations consumed by this scanning skill)

## Examples

```
bigslice -i <input_folder_with_bgcs> <output_folder>
```

## Evaluation signals

- All BGC sequences produce non-empty domain hit tables with valid Pfam accessions and e-values below the specified threshold
- Normalized feature vectors sum to 1.0 (l2-norm) per BGC, confirming proper normalization
- Output TSV files are parseable and contain expected columns: gene_id, pfam_accession, domain_start, domain_end, evalue, bitscore
- Domain hit counts and bit-score distributions match the known domain composition of positive-control BGCs (e.g., well-characterized antibiotic or polyketide clusters)
- Clustering distances computed from exported feature vectors yield expected GCF groupings (e.g., known similar BGCs cluster with cosine similarity > 0.7)

## Limitations

- Domain scanning depends on PFAM 35.0 coverage; novel or recently discovered biosynthetic domains not in PFAM may be missed
- Default e-value and bit-score thresholds may be too permissive or restrictive for rare or highly divergent BGC families; no automatic threshold tuning is provided
- pyHMMER parallelization strategy differs from the HMMER binary, yielding different performance benefits on small vs. large sequence batches; not suitable for single-sequence queries in high-throughput streaming contexts
- l2-normalization converts domain hits to presence/relative abundance; raw domain counts or spatial arrangement information is lost prior to clustering
- Requires pre-download of ±271 MB gzipped PFAM 35.0 models; internet connectivity and storage constraints may affect deployment

## Evidence

- [other] BiG-SLiCE v2 replaced HMMER with pyHMMER for HMM-based domain scanning, enabling speed improvements and full pip installation without external dependencies.: "Switching from HMMER to pyHMMER (__speed-ups__, can now be fully installed via __pip__)"
- [other] Domain hits are extracted with gene identifiers, Pfam accessions, coordinates, e-values, and bit-scores, then aggregated into a feature table.: "Extract domain hits (gene identifiers, Pfam accessions, domain coordinates, e-values, bit-scores) and aggregate into a feature table."
- [readme] Clustering uses cosine-like distances via l2-normalization of domain-feature vectors.: "Clustering now uses __cosine-like__ (via l2-normalization) distances"
- [readme] pyHMMER directly interacts with HMMER internals in memory, avoiding intermediate files and enabling efficient batch processing.: "Everything happens in memory, in Python objects you have control on, making it easier to pass your inputs to HMMER without needing to write them to a temporary file."
- [other] The workflow begins by loading BGC data and initializing the pyHMMER interface with PFAM 35.0 models.: "Load BGC sequence data (FASTA or GenBank format) and initialize the pyHMMER interface with the bigslice-models-2022-11-30 PFAM 35.0 HMM database."
- [other] Normalized domain-feature matrices and hit details are exported as TSV output files.: "Export the normalized domain-feature matrix and hit details to TSV output files."
