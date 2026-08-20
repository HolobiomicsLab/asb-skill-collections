---
name: paired-omics-bgc-metabolite-linking-workflow
description: 'Use when you have paired genomic and metabolomic data from the same
  microbial strains and want to link biosynthetic gene clusters (BGCs) to the metabolite
  features they plausibly encode — mine BGCs from assembled genomes with antiSMASH,
  tokenize BGC domains with iPRESTO/Pfam and cluster them into gene cluster families
  (GCFs) with BiG-SCAPE, build an MS/MS molecular network from paired LC-MS/MS data
  with GNPS to obtain molecular families (MFs), then score GCF-MF co-occurrence across
  strains (NPLinker-style Metcalf/hypergeometric scoring) to produce a ranked table
  of candidate BGC-metabolite links for natural-product discovery.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 6
  member_skills:
  - biosynthetic-gene-cluster-detection-and-annotation
  - genomic-bgc-extraction-antismash
  - biosynthetic-gene-cluster-annotation
  - biosynthetic-gene-cluster-tokenization
  - bgc-tokenization-with-pfam-domains
  - gene-tokenization-representation
  - pfam-domain-pattern-recognition
  - statistical-sub-cluster-detection
  - gcf-assignment-from-distance-matrix
  - gene-cluster-family-formation-and-similarity-clustering
  - big-slice-workflow-execution
  - bgc-sequence-domain-scanning
  - spectral-similarity-network-generation
  - metabolomic-spectral-annotation-and-molecular-family-clustering
  - metabolomic-molecular-family-networking-gnps
  - spectral-similarity-network-building
  - bgc-mf-link-scoring
  - link-scoring-metcalf-algorithm
  - gcf-mf-link-scoring
  - gcf-mf-link-scoring-computation
  - strain-correlation-hypergeometric-adjustment
  - genomic-metabolomic-link-ranking
  - statistical-enrichment-analysis
  - gcf-mf-hierarchical-aggregation
  member_tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
  - iPRESTO
  - BiG-SLiCE
  - pyHMMER
  - antiSMASH v7.0.0
  - MZmine2
  - Optimus
  - Cytoscape
  - IOKR
  coverage_gaps: []
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Paired-Omics BGC <-> Metabolite Linking (genome mining + molecular networking -> ranked links)

## Summary

Assembled genomes + paired LC-MS/MS in, a ranked BGC-metabolite link table out: antiSMASH BGC detection, iPRESTO/Pfam domain tokenization, BiG-SCAPE gene cluster family clustering, GNPS molecular networking, and NPLinker-style genomic-metabolomic co-occurrence scoring.


## When to use

Use when you have paired genomic and metabolomic data from the same microbial strains and want to link biosynthetic gene clusters (BGCs) to the metabolite features they plausibly encode — mine BGCs from assembled genomes with antiSMASH, tokenize BGC domains with iPRESTO/Pfam and cluster them into gene cluster families (GCFs) with BiG-SCAPE, build an MS/MS molecular network from paired LC-MS/MS data with GNPS to obtain molecular families (MFs), then score GCF-MF co-occurrence across strains (NPLinker-style Metcalf/hypergeometric scoring) to produce a ranked table of candidate BGC-metabolite links for natural-product discovery.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — bgc_mine

**Goal:** assembled genomes -> detected BGCs (antiSMASH genome mining)

**EDAM operation:** operation_0436

**Inputs:** fasta · **Outputs:** genbank/antismash-bgc

**Candidate leaf skills:** `biosynthetic-gene-cluster-detection-and-annotation` (primary), `genomic-bgc-extraction-antismash`, `biosynthetic-gene-cluster-annotation`

**Tools (primary):** antiSMASH, BiG-SCAPE, NPLinker, GNPS, MIBiG

**Other candidate tools:** Python, conda, pip, BigScape, pyHMMER, BiG-SLiCE, PFAM 35.0

**Grounding:** 4 KB(s); DOIs: 10.1093/gigascience/giaa154, 10.1101/2024.10.11.617756, 10.1186/s40168-022-01444-3, 10.1371/journal.pcbi.1008920

### Stage 2 — bgc_tokenize

**Goal:** GenBank BGC records -> Pfam-domain tokens and sub-cluster motifs (iPRESTO)

**EDAM operation:** operation_3096

**Inputs:** genbank/antismash-bgc · **Outputs:** tsv/bgc-domain-tokens

**Candidate leaf skills:** `biosynthetic-gene-cluster-tokenization` (primary), `bgc-tokenization-with-pfam-domains`, `gene-tokenization-representation`, `pfam-domain-pattern-recognition`, `statistical-sub-cluster-detection`

**Tools (primary):** iPRESTO

**Other candidate tools:** Pfam

**Grounding:** 1 KB(s); DOIs: 10.1371/journal.pcbi.1010462

### Stage 3 — gcf_cluster

**Goal:** BGCs -> gene cluster families (BiG-SCAPE similarity clustering)

**EDAM operation:** operation_3432

**Inputs:** genbank/antismash-bgc, tsv/bgc-domain-tokens · **Outputs:** tsv/gcf-table

**Candidate leaf skills:** `gcf-assignment-from-distance-matrix` (primary), `gene-cluster-family-formation-and-similarity-clustering`, `big-slice-workflow-execution`, `bgc-sequence-domain-scanning`

**Tools (primary):** BiG-SLiCE, pyHMMER, antiSMASH v7.0.0

**Other candidate tools:** antiSMASH, BiG-SCAPE, NPLinker, GNPS, MIBiG, Flask, PFAM 35.0

**Grounding:** 3 KB(s); DOIs: 10.1093/gigascience/giaa154, 10.1101/2024.10.11.617756, 10.1371/journal.pcbi.1008920

### Stage 4 — mf_network

**Goal:** paired LC-MS/MS spectra -> molecular families (GNPS feature-based molecular networking)

**EDAM operation:** operation_3767

**Inputs:** mgf/gnps-fbmn · **Outputs:** tsv/mf-table

**Candidate leaf skills:** `spectral-similarity-network-generation` (primary), `metabolomic-spectral-annotation-and-molecular-family-clustering`, `metabolomic-molecular-family-networking-gnps`, `spectral-similarity-network-building`

**Tools (primary):** MZmine2, Optimus, GNPS, Cytoscape

**Other candidate tools:** antiSMASH, BiG-SCAPE, NPLinker, MIBiG, Python, conda, pip, BigScape, q2-qemistree, SIRIUS, CSI:FingerID, ZODIAC, GNPS FBMN, ClassyFire

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.jnatprod.7b00737, 10.1038/s41589-020-00677-3, 10.1101/2024.10.11.617756, 10.1186/s40168-022-01444-3 …

### Stage 5 — link_score

**Goal:** GCFs + MFs + strain co-occurrence -> ranked GCF-MF links (NPLinker Metcalf/hypergeometric scoring)

**EDAM operation:** operation_3357

**Inputs:** tsv/gcf-table, tsv/mf-table · **Outputs:** tsv/gcf-mf-scores

**Candidate leaf skills:** `bgc-mf-link-scoring` (primary), `link-scoring-metcalf-algorithm`, `gcf-mf-link-scoring`, `gcf-mf-link-scoring-computation`, `strain-correlation-hypergeometric-adjustment`

**Tools (primary):** NPLinker, antiSMASH, BiG-SCAPE, MIBiG, GNPS

**Other candidate tools:** Python, conda, pip, BigScape, NumPy or SciPy

**Grounding:** 3 KB(s); DOIs: 10.1101/2024.10.11.617756, 10.1186/s40168-022-01444-3, 10.1371/journal.pcbi.1008920

### Stage 6 — report

**Goal:** consolidate scored links + provenance into a ranked BGC-metabolite link table

**EDAM operation:** operation_3695

**Inputs:** tsv/gcf-mf-scores, tsv/gcf-table · **Outputs:** tsv

**Candidate leaf skills:** `genomic-metabolomic-link-ranking` (primary), `statistical-enrichment-analysis`, `gcf-mf-hierarchical-aggregation`

**Tools (primary):** NPLinker, BiG-SCAPE, IOKR, antiSMASH, GNPS

**Other candidate tools:** MIBiG

**Grounding:** 2 KB(s); DOIs: 10.1101/2024.10.11.617756, 10.1371/journal.pcbi.1008920

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
