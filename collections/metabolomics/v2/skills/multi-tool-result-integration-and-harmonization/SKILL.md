---
name: multi-tool-result-integration-and-harmonization
description: Use when when you have completed parallel or sequential tool runs (e.g., CPAT, signalP, Pfam, fimo) on the same set of sequences and need to create a unified functional annotation table, summary statistics, or cross-tool comparison report.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0114
  tools:
  - CPAT
  - signalP
  - pfam
  - fimo
  - IsoformSwitchAnalyzer
  - Pfam
  - R packages (edger, limma, ComplexHeatmap, ggplot2)
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Functional annotation | CPAT, signalP, pfam
- Find motif | fimo
- Isoforms | Genome wide isoform analysis | IsoformSwitchAnalyzer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiomicsintegrator_cq
    doi: 10.1093/bioadv/vbae175
    title: MultiOmicsIntegrator
  dedup_kept_from: coll_multiomicsintegrator_cq
schema_version: 0.2.0
---

# multi-tool-result-integration-and-harmonization

## Summary

Merge and harmonize annotation and analysis results from multiple specialized bioinformatics tools into unified, indexed tables indexed by sequence identifier. This skill is essential when a single research question requires orthogonal predictions (e.g., coding potential, protein domains, signal peptides) that must be reconciled into a single queryable data structure.

## When to use

When you have completed parallel or sequential tool runs (e.g., CPAT, signalP, Pfam, fimo) on the same set of sequences and need to create a unified functional annotation table, summary statistics, or cross-tool comparison report. Specifically triggered when individual tool outputs (scoring files, hit tables, motif predictions) are scattered across multiple files and indexed by common identifiers (isoform/exon IDs, sequence names) that allow join-by-key operations.

## When NOT to use

- Tool outputs are already pre-integrated (e.g., a single annotation GFF or VCF already contains all predictions) — skip to direct querying or filtering.
- Only one tool has been run and its output is already indexed — no merge is needed.
- Sequence identifiers differ across tool runs and cannot be reliably matched or reconciled — address identifier harmonization as a separate preprocessing step before merge.

## Inputs

- CPAT coding potential scores (TSV/text output with sequence identifier and coding score)
- signalP signal peptide predictions (tabular predictions with sequence ID and peptide location/probability)
- Pfam domain hit table (text file with sequence ID, domain name, E-value, coordinates)
- fimo motif match results (text output with sequence ID, motif name, p-value, coordinates)
- IsoformSwitchAnalyzer-derived FASTA file of differentially expressed isoform/exon sequences

## Outputs

- Unified functional annotation table (TSV or CSV indexed by isoform/exon identifier with columns for CPAT score, coding status, signal peptide presence/location, Pfam domain hits, motif matches)
- Summary statistics report (counts, distributions of annotation features across the sequence set)
- Annotated sequence report (optional; sequences with inline or linked annotation metadata)

## How to apply

Collect all output files from the constituent tools (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, fimo motif matches) and identify the common indexing field (isoform or exon identifier). Use a tabular merge strategy (SQL-like join or R/Python DataFrame merge) keyed on this identifier to combine all annotations into a single row per sequence. Include all score columns (e.g., CPAT coding potential score, signalP probability, Pfam E-value) and binary/categorical predictions (coding/non-coding status, signal peptide presence/absence, domain names). Generate summary statistics (e.g., count of isoforms with predicted signal peptides, distribution of coding scores) and an annotated sequence report. Validation occurs by spot-checking that the merged table has no missing values where tool runs completed successfully and that row counts match the input FASTA sequence count.

## Related tools

- **CPAT** (Predicts coding potential and classifies sequences as coding or non-coding; output scores are merged by sequence identifier)
- **signalP** (Identifies and annotates signal peptide sequences at the N-terminus; predictions are merged into the unified annotation table)
- **Pfam** (Queries database to assign protein domain annotations to predicted coding sequences; domain hits are merged by sequence ID)
- **fimo** (Scans sequences for known motifs and returns match coordinates and p-values; motif matches are merged into the unified table)
- **IsoformSwitchAnalyzer** (Upstream tool that produces differentially expressed isoform/exon FASTA sequences serving as input to the functional annotation tools)
- **R packages (edger, limma, ComplexHeatmap, ggplot2)** (Used for data merging, preprocessing, and generation of summary statistics and visual reports)

## Evaluation signals

- Merged table row count equals the number of unique isoform/exon identifiers in the input FASTA file.
- No empty/NA cells in columns corresponding to tools that completed successfully; NA values only where a tool explicitly did not return a hit.
- All common identifiers present in each input tool file appear exactly once in the merged table; no duplicate rows.
- Summary statistics (e.g., percentage of sequences with predicted signal peptides, mean CPAT coding score) are computed over the full merged set and match manual spot-checks.
- Cross-tool consistency checks pass: sequences with high CPAT coding scores also predominantly carry Pfam domain annotations; sequences with signal peptides do not appear as non-coding in CPAT.

## Limitations

- Merge reliability depends on consistent sequence identifier formats across all tool outputs; tool-specific ID formatting (e.g., truncation, version suffixes) can break joins and silently lose annotations.
- Tool run completeness is assumed; if a tool fails on a subset of sequences, those sequences will have missing annotations and must be flagged or re-run independently.
- No conflict resolution strategy is specified for contradictory predictions (e.g., one tool predicts coding, another predicts non-coding); the merged table preserves all predictions and leaves resolution to downstream interpretation.
- Large annotation tables (millions of sequences, hundreds of Pfam/motif hits per sequence) may require memory-efficient merge strategies (e.g., streaming, database loading) not described in the article.

## Evidence

- [methods] Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon identifier.: "Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon"
- [methods] The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP for signaling sequence identification.: "The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP"
- [methods] Generate summary statistics and annotated sequence report.: "Generate summary statistics and annotated sequence report."
