---
name: genomic-bgc-extraction-antismash
description: Use when when you have genomic DNA sequences (from isolates or metagenomes) and need to identify and characterize biosynthetic gene clusters as input for downstream natural product linkage analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0436
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3172
  tools:
  - nplinker
  - Python
  - conda
  - pip
  - AntiSMASH
  - BigScape
  - NPLinker
derived_from:
- doi: 10.1186/s40168-022-01444-3
  title: NPClassScore
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader] and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
- '[![github repo badge](https://img.shields.io/badge/github-nplinker-000.svg?color=blue)](https://github.com/NPLinker/nplinker)'
- Python version ≥3.11
- conda create -n npl-3.11 python=3.11
- pip install nplinker
- antismash directory contains a collection of AntiSMASH BGC data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassscore_cq
    doi: 10.1186/s40168-022-01444-3
    title: NPClassScore
  dedup_kept_from: coll_npclassscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-022-01444-3
  all_source_dois:
  - 10.1186/s40168-022-01444-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# genomic-bgc-extraction-antismash

## Summary

Extract biosynthetic gene clusters (BGCs) from genomic sequences using AntiSMASH, a specialized tool for predicting and annotating secondary metabolite biosynthesis regions. This is a prerequisite step for linking genomic BGC data to metabolomics output in natural product discovery workflows.

## When to use

When you have genomic DNA sequences (from isolates or metagenomes) and need to identify and characterize biosynthetic gene clusters as input for downstream natural product linkage analysis. Use this skill before attempting to correlate genomic BGCs with metabolomics spectra via tools like NPLinker.

## When NOT to use

- Input is already pre-annotated BGC data in a linked or processed form; use direct ingestion instead of re-running AntiSMASH.
- Genomic sequences are highly fragmented or very low quality; AntiSMASH requires contiguous sequence regions to identify meaningful BGC predictions.
- The analysis scope is metabolomics-only without any genomic component; AntiSMASH extraction is unnecessary if no BGC–spectrum linkage is planned.

## Inputs

- genomic DNA sequences (FASTA or GenBank format)
- sequence metadata (strain identifiers, sample provenance)

## Outputs

- AntiSMASH BGC annotations and predictions
- BGC feature coordinates and cluster boundaries
- secondary metabolite biosynthesis pathway predictions
- antismash directory (loaded by NPLinker)

## How to apply

Prepare genomic sequences in standard formats (typically FASTA or GenBank). Run AntiSMASH on these sequences; NPLinker can trigger this automatically if the `antismash` output directory does not already exist in the working directory. AntiSMASH outputs structured BGC annotations and coordinates. These results are then loaded into NPLinker via the `antismash` subdirectory during `npl.load_data()`, allowing subsequent scoring and linking of BGCs to GNPS spectra and molecular families using metcalf or other scoring methods. The BGC data structure integrates with the LinkGraph to enable integrated genomics–metabolomics analysis.

## Related tools

- **AntiSMASH** (primary tool for automatic detection and annotation of biosynthetic gene clusters from genomic sequences)
- **NPLinker** (orchestrates loading and integration of AntiSMASH BGC output with GNPS spectra and molecular families for linkage analysis) — https://github.com/NPLinker/nplinker
- **BigScape** (optional clustering and comparison of BGCs; NPLinker can run BigScape automatically if the bigscape directory does not exist)

## Examples

```
# Automatically via NPLinker: npl = NPLinker('nplinker.toml'); npl.load_data() # loads AntiSMASH output from antismash/ subdirectory
```

## Evaluation signals

- AntiSMASH completes without errors and generates a populated antismash directory with BGC prediction files.
- BGC coordinates and feature annotations are successfully parsed and loaded into NPLinker's data model (accessible via npl.gcfs).
- Subsequent npl.get_links() calls on the extracted GCFs return non-empty LinkGraph objects with scored link tuples.
- The number and distribution of predicted BGCs are consistent with the genomic input (e.g., GC-rich secondary metabolite operons are detected).
- LinkGraph exports contain properly cross-referenced GCF, spectrum, and molecular family entities without missing or null fields.

## Limitations

- AntiSMASH predictions depend on homology to known biosynthetic domains; novel or highly divergent BGCs may be missed or under-annotated.
- BGC extraction quality depends on input sequence quality, assembly contiguity, and presence of complete operons; fragmented or incomplete sequences yield incomplete predictions.
- The document notes no explicit discussion of AntiSMASH limitations, failure modes, or parameter tuning; refer to AntiSMASH documentation for detailed interpretation of confidence thresholds and output types.

## Evidence

- [other] NPLinker requires input genomic data in the form of AntiSMASH BGC predictions: "antismash directory contains a collection of AntiSMASH BGC data"
- [other] AntiSMASH is invoked automatically as part of the NPLinker workflow if required output does not exist: "NPLinker can run BigScape automatically if the `bigscape` directory does not exist"
- [methods] BGC data extracted by AntiSMASH is loaded into NPLinker's data model during initialization: "Call npl.load_data() to load GNPS spectra, molecular families, annotations, and AntiSMASH BGC data from the gnps and antismash subdirectories"
- [methods] Extracted BGCs are accessible as GCF objects within NPLinker and are used for downstream scoring and link computation: "Call npl.get_links(npl.gcfs[:3], 'metcalf') to compute metcalf-scored links between the first three GCFs and other entities"
