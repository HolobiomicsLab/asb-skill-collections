---
name: genomic-database-identifier-mapping
description: Use when your gene expression matrix or pathway collection uses identifier formats incompatible with your enrichment analysis tool (e.g., gene symbols vs. Entrez IDs), or you need to reconcile gene sets from multiple sources (Reactome, KEGG) that employ different naming conventions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_0092
  tools:
  - fgsea
  - R
  - ggplot2
  - org.Mm.eg.db
  - reactome.db
  - data.table
derived_from:
- doi: 10.1101/060012
  title: fgsea
evidence_spans:
- '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)
- R-package for fast preranked gene set enrichment analysis
- fgsea is an R-package for fast preranked gene set enrichment analysis
- library(ggplot2)
- ggplot(data=merge(...)) + geom_point(aes(x=logPvalFull, y=logPvalRed))
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fgsea
    doi: 10.1101/060012
    title: fgsea
  dedup_kept_from: coll_fgsea
schema_version: 0.2.0
---

# genomic-database-identifier-mapping

## Summary

Map gene identifiers between biological databases (e.g., gene symbols to Entrez IDs) to enable cross-platform analysis and enrichment computations. This skill is essential when working with heterogeneous gene expression datasets or pathway databases that use different identifier schemes.

## When to use

Your gene expression matrix or pathway collection uses identifier formats incompatible with your enrichment analysis tool (e.g., gene symbols vs. Entrez IDs), or you need to reconcile gene sets from multiple sources (Reactome, KEGG) that employ different naming conventions. Apply this skill before running GSEA or other pathway analyses when the gene identifiers in your ranked statistics do not match those in your pathway definitions.

## When NOT to use

- Gene identifiers in your stats vector and pathway collection are already identical and validated (mapping is redundant).
- You lack access to appropriate organism-specific annotation packages for your study organism.
- Your analysis intentionally requires keeping identifiers separate (e.g., cross-species comparative analysis where identifier schemes must remain distinct).

## Inputs

- Gene expression matrix (ExpressionSet or numeric matrix with gene identifiers as rownames)
- Pathway collection (list of character vectors, each element a pathway name with member gene identifiers)
- Ranked statistics (named numeric vector with gene identifiers as names)
- Organism-specific annotation database (e.g., org.Mm.eg.db, org.Hs.eg.db)

## Outputs

- Harmonized gene expression matrix with consistent identifier scheme
- Pathway collection with remapped identifiers matching ranked statistics
- Ranked statistics vector with identifiers in target scheme
- Mapping report (number mapped, unmapped, duplicates removed)

## How to apply

Load the source gene identifier column from your expression matrix or pathway collection. Use organism-specific annotation packages (e.g., org.Mm.eg.db for mouse) to programmatically map identifiers to a target scheme. Remove unmapped genes and duplicates (genes with identical mapped identifiers after consolidation). Verify coverage by computing the proportion of successfully mapped identifiers and cross-check against expected gene counts. Join the mapped identifiers back to your ranked statistics or pathway definitions before running fgsea, ensuring all genes in both the stats vector and pathway collection use the same identifier scheme.

## Related tools

- **org.Mm.eg.db** (Organism-specific annotation package for mouse gene symbol-to-Entrez ID mapping)
- **reactome.db** (Reactome pathway database with gene identifiers requiring mapping to rank statistics scheme)
- **data.table** (Fast join and consolidation of mapped identifiers with expression data)
- **fgsea** (Fast preranked GSEA requiring harmonized identifiers between stats and pathways) — https://github.com/ctlab/fgsea

## Examples

```
library(org.Mm.eg.db); mapped_ids <- mapIds(org.Mm.eg.db, keys=rownames(es), keytype='SYMBOL', column='ENTREZID'); es <- es[!duplicated(mapped_ids), ]; names(exampleRanks) <- mapIds(org.Mm.eg.db, keys=names(exampleRanks), keytype='SYMBOL', column='ENTREZID')
```

## Evaluation signals

- Verify no NA or empty identifier values remain after mapping; check that 100% of pathway genes are present in the ranked statistics vector.
- Compare pathway gene counts before and after mapping; loss >10% of genes may indicate poor annotation coverage or schema mismatch.
- Run fgsea on mapped data and confirm enrichment scores and p-values are computed for all pathways without missing-gene warnings.
- Cross-validate a small subset of mapped identifiers by manual lookup in the annotation database or a reference resource (e.g., NCBI Gene).
- Ensure no duplicate genes exist after consolidation; verify that duplicated() returns FALSE for all identifiers in the final ranked statistics vector.

## Limitations

- Annotation packages may be outdated; gene symbols and Entrez IDs evolve, potentially losing or mislabeling identifiers in older databases.
- Genes without mappings in the annotation resource are silently dropped, reducing pathway coverage; low mapping rates (<80%) may indicate organism mismatch or use of non-standard identifier schemes.
- Multi-gene duplications or identifier ambiguity (one symbol mapping to multiple Entrez IDs) require manual curation; automated collapsing may lose biologically distinct isoforms.
- Cross-species mapping is not supported by organism-specific packages; comparative analyses require separate, validated mapping strategies.

## Evidence

- [methods] Organism-specific annotation packages enable mapping: "library(org.Mm.eg.db)"
- [methods] Reactome database requires identifier harmonization: "Package reactome.db is required to be installed"
- [methods] Filter to remove genes with invalid or empty identifiers: "es <- es[!grepl("///", rownames(es)), ]
es <- es[rownames(es) != "", ]"
- [methods] Remove duplicated genes after mapping consolidation: "es <- es[!duplicated(fData(es)$`Gene ID`), ]"
- [readme] Pathway collection uses gene identifiers requiring mapping: "Loading example pathways and gene-level statistics:
data(examplePathways)
data(exampleRanks)"
