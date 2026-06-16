# Evaluation Strategy

## Direct Checks

- verify file exists in fgsea package: examplePathways (list or data.frame format)
- verify file exists in fgsea package: exampleRanks (named numeric vector or data.frame format)
- script_runs: R script executing fgsea(examplePathways, exampleRanks, eps=1e-10) completes without error
- field_present: result table contains columns 'pathway', 'pval', 'padj', 'ES', 'NES'
- row_count_equals: result table has at least 1 row (at least one pathway analyzed)
- file_exists: enrichment plot PNG/PDF for pathway '5991130_Programmed_Cell_Death' generated
- file_exists: GSEA table for top pathways (by adjusted p-value) generated as CSV or TSV
- value_in_range: all 'pval' values in result table are numeric and >= 0
- value_in_range: all 'padj' values in result table are numeric and >= 0
- contains_substring: result table pathway column contains '5991130_Programmed_Cell_Death' (if pathway is named in examplePathways)

## Expert Review

- verify NES (normalized enrichment score) magnitudes and signs are biologically plausible for the pathways tested
- verify enrichment plot for '5991130_Programmed_Cell_Death' displays running enrichment score, gene positions, and phenotype labels in standard GSEA format
- verify top pathways by adjusted p-value are ranked consistently with statistical significance (lower adjusted p-value = higher ranking)
- verify adaptive Monte-Carlo p-value estimation with eps=1e-10 produces p-values of appropriate precision (no artificial floor effects)
