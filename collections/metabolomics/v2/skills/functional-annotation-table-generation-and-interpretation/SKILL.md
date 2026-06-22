---
name: functional-annotation-table-generation-and-interpretation
description: Use when after running CPAT, signalP, Pfam, and fimo tools on differentially expressed isoform or exon FASTA sequences, and you need to consolidate their individual outputs into a single indexed table to compare functional properties across isoforms, identify isoforms with specific domain.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_0086
  tools:
  - CPAT
  - signalP
  - pfam
  - fimo
  - IsoformSwitchAnalyzer
  - Pfam
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae175
  all_source_dois:
  - 10.1093/bioadv/vbae175
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# functional-annotation-table-generation-and-interpretation

## Summary

Merge coding potential, protein domain, signal peptide, and motif predictions into a unified functional annotation table indexed by isoform/exon identifier. This skill consolidates heterogeneous sequence-level feature predictions into a queryable artifact suitable for downstream functional interpretation and filtering.

## When to use

After running CPAT, signalP, Pfam, and fimo tools on differentially expressed isoform or exon FASTA sequences, and you need to consolidate their individual outputs into a single indexed table to compare functional properties across isoforms, identify isoforms with specific domain combinations, or filter for sequences with signal peptides and coding potential.

## When NOT to use

- Input sequences have not yet been processed through CPAT, signalP, Pfam, or fimo; run those tools first.
- Isoforms have been filtered to a single best representative per gene; the annotation table is designed to compare all differentially expressed isoforms, not collapsed sets.
- You only need individual tool outputs for separate downstream analyses and do not require cross-tool feature correlation or comparison.

## Inputs

- CPAT output table (isoform ID, coding/non-coding classification, coding score/probability)
- signalP output (isoform ID, signal peptide prediction, cleavage site position)
- Pfam fimo output or domain hit table (isoform ID, domain name, hit start, hit end, bit score, e-value)
- FIMO motif scan table (isoform ID, motif name, motif start, motif end, p-value, q-value)

## Outputs

- Unified functional annotation table (TSV/CSV) indexed by isoform/exon ID with columns for coding status, coding score, signal peptide flag, signal peptide cleavage position, Pfam domain hits (one row per domain or semicolon-delimited list), motif matches
- Annotation summary statistics (e.g., isoform count, percentage coding, percentage with signal peptides, domain frequency table, motif frequency table)

## How to apply

Load the output files from CPAT (coding scores and classification), signalP (signal peptide coordinates and predictions), fimo (motif match tables), and Pfam (domain hit tables) for the same isoform/exon set. Align and merge these tables using isoform/exon identifier as the primary key. Retain coding scores, binary coding/non-coding classification, signal peptide presence/position, all Pfam domain hits with bit scores, and motif matches with p-values. Generate summary statistics per isoform (e.g., domain count, presence of signal peptides, coding status) and validate that no isoforms are dropped during the merge (row count should match or exceed the input isoform count, accounting for one-to-many relationships from multiple domain hits per isoform). Output as a tab-delimited or CSV table with standardized column naming.

## Related tools

- **CPAT** (Predicts coding potential and classifies sequences as coding or non-coding; output merged by isoform ID)
- **signalP** (Identifies and annotates signal peptide sequences at N-terminus; prediction merged into annotation table)
- **Pfam** (Assigns protein domain annotations to predicted coding sequences; domain hits merged by isoform ID)
- **fimo** (Scans sequences for known motifs as part of functional feature identification; matches merged into annotation table)
- **IsoformSwitchAnalyzer** (Source of differentially expressed isoform/exon FASTA sequences provided as input)

## Evaluation signals

- Row count after merge equals or exceeds input isoform count (accounting for one-to-many relationships from multiple Pfam domain hits or motif matches per isoform).
- All input isoforms are present in the final table (no silent failures during join); cross-check against input FASTA sequence count.
- Columns for coding status, coding score, signal peptide flag/position, Pfam domains, and motif matches are all populated with expected data types (numeric scores, categorical flags, text domain names).
- Summary statistics show reasonable distributions (e.g., percentage coding > 0% for protein-coding transcripts, signal peptide presence aligns with biology of expressed genes).
- Spot-check: for a known coding isoform, verify CPAT coding classification is 'coding' and Pfam contains ≥1 domain hit; for a known lncRNA, verify CPAT is 'non-coding' and Pfam domain count is 0 or near-zero.

## Limitations

- Merge accuracy depends on consistent isoform/exon identifier naming across all four tools; mismatches or truncation of IDs will result in missing or orphaned rows.
- One-to-many relationships (e.g., single isoform with multiple Pfam domains) must be handled carefully during merge to avoid row multiplication or loss of information; denormalized or semicolon-delimited formats may reduce queryability.
- CPAT, signalP, Pfam, and fimo have different false-positive/false-negative rates; low-confidence predictions (e.g., Pfam domain hits with high e-values or signalP marginal predictions) may be included in the table without explicit quality filtering.
- No consensus on standardized column naming or table schema across pipelines; manual curation or custom scripting may be needed to harmonize outputs from different workflow versions.

## Evidence

- [other] Run CPAT to predict coding potential and classify sequences as coding or non-coding.: "Run CPAT to predict coding potential and classify sequences as coding or non-coding."
- [other] Run signalP to identify and annotate signal peptide sequences at the N-terminus.: "Run signalP to identify and annotate signal peptide sequences at the N-terminus."
- [other] Query Pfam database to assign protein domain annotations to predicted coding sequences.: "Query Pfam database to assign protein domain annotations to predicted coding sequences."
- [other] Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon identifier.: "Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon"
- [other] Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output.: "Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output."
- [other] Generate summary statistics and annotated sequence report.: "Generate summary statistics and annotated sequence report."
