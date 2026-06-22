---
name: protein-domain-homology-search-and-annotation
description: Use when after predicting coding potential (via CPAT) on differentially expressed isoforms and you need to assign functional annotations based on protein domain homology.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0346
  edam_topics:
  - http://edamontology.org/topic_0078
  - http://edamontology.org/topic_0080
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
---

# protein-domain-homology-search-and-annotation

## Summary

Annotate predicted protein sequences with known functional domains by querying the Pfam database, enabling functional characterization of differentially expressed isoforms. This skill identifies conserved protein domain homology regions to infer molecular function and classify sequences by domain composition.

## When to use

Apply this skill after predicting coding potential (via CPAT) on differentially expressed isoforms and you need to assign functional annotations based on protein domain homology. Use when your input consists of FASTA sequences of predicted coding isoforms from IsoformSwitchAnalyzer output and you want to characterize their functional domains to support downstream functional interpretation.

## When NOT to use

- Input sequences are nucleotide-only and have not been translated or classified for coding potential.
- Functional annotation goal is limited to signal peptide or coding potential prediction only, with no need for domain classification.
- Pre-computed domain annotations already exist and you only need to integrate them with other annotations.

## Inputs

- Differentially expressed isoform/exon FASTA sequences
- CPAT coding potential classification results
- IsoformSwitchAnalyzer output

## Outputs

- Pfam domain annotation table (indexed by isoform/exon identifier)
- Unified functional annotation table (CPAT scores, signalP predictions, Pfam domains, motif matches)
- Annotated sequence report with domain assignments

## How to apply

Run the predicted coding sequences through Pfam domain search to query against known protein domain databases and assign protein domain annotations to each sequence. The workflow loads differentially expressed isoform FASTA sequences, applies CPAT to classify coding vs. non-coding sequences, then runs Pfam queries on coding sequences to detect conserved domain hits. Merge the Pfam domain annotation results (domain identifiers, positions, and scores) into a unified functional annotation table indexed by isoform/exon identifier. Domain hits are typically filtered by default Pfam scoring thresholds to retain high-confidence matches. Evaluate correctness by verifying that all coding sequences received domain assignments or were correctly marked as lacking recognized domains, and that domain annotations are present in the merged output table.

## Related tools

- **Pfam** (Query predicted coding sequences against Pfam database to assign protein domain homology annotations and identify conserved functional domains)
- **CPAT** (Predict coding potential and classify isoform sequences as coding or non-coding prior to Pfam domain annotation)
- **signalP** (Identify signal peptide sequences at N-terminus to complement domain annotation in functional characterization workflow)
- **IsoformSwitchAnalyzer** (Generate differentially expressed isoform/exon FASTA sequences that serve as input for domain annotation pipeline)
- **fimo** (Scan sequences for known motifs as part of broader functional feature identification alongside domain annotation)

## Evaluation signals

- All predicted coding sequences (CPAT-classified) receive Pfam domain hit entries or are explicitly marked as having no domain matches in the output table
- Pfam domain annotations are indexed correctly by isoform/exon identifier and align with corresponding FASTA sequence records
- Unified functional annotation table contains non-null entries for Pfam domain columns and integrates consistently with CPAT scores, signalP predictions, and motif matches
- Domain hit positions and confidence scores (e-values, bit scores) are present and within expected ranges for the Pfam database query
- Annotated sequence report displays domain assignments with interpretable domain family names and descriptions for downstream functional interpretation

## Limitations

- Pfam annotations depend on sequence quality and completeness; partial or low-complexity coding sequences may fail to identify expected domains.
- Domain assignment reflects only known, curated Pfam domain families; novel or rapidly evolving domains may not be detected.
- The workflow assumes correctly predicted coding sequences from CPAT; false positive coding predictions will propagate incorrect domain annotations.
- Integration with other annotation results (signalP, motif matches) requires compatible indexing schemes; mismatched identifiers can lead to incomplete or fragmented annotation tables.

## Evidence

- [other] Query Pfam database to assign protein domain annotations to predicted coding sequences.: "Query Pfam database to assign protein domain annotations to predicted coding sequences."
- [other] The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP for signaling sequence identification.: "The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP"
- [other] Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon identifier.: "Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon"
- [other] Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output.: "Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output."
