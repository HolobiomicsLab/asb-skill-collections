---
name: metabolite-class-visualization-by-statistical-significance
description: Use when after running omu_summary statistical comparison on count data
  with assigned hierarchical class annotations (KEGG, KO_Number, Prokaryote, or Eukaryote),
  use this skill to visualize log2FoldChange and adjusted p-values for metabolites
  grouped by class.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - omu
  - ggplot2
  - KEGGREST
  license_tier: restricted
derived_from:
- doi: 10.1128/mra.00129-19
  title: omu metabolomics count data tool
evidence_spans:
- Omu is an R package that enables rapid analysis of Metabolomics data sets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omu_metabolomics_count_data_tool_cq
    doi: 10.1128/mra.00129-19
    title: omu metabolomics count data tool
  dedup_kept_from: coll_omu_metabolomics_count_data_tool_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00129-19
  all_source_dois:
  - 10.1128/mra.00129-19
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-class-visualization-by-statistical-significance

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate a volcano plot visualization of metabolites stratified by hierarchical class and statistical significance (log2FoldChange and adjusted p-value) from omu_summary differential abundance output. This skill enables rapid interpretation of which metabolite classes are enriched or depleted in comparative metabolomics studies.

## When to use

After running omu_summary statistical comparison on count data with assigned hierarchical class annotations (KEGG, KO_Number, Prokaryote, or Eukaryote), use this skill to visualize log2FoldChange and adjusted p-values for metabolites grouped by class. Particularly useful when you want to highlight specific metabolite classes (e.g., Organic acids vs. Carbohydrates) with distinct colors and shapes to identify which functional groups drive treatment differences.

## When NOT to use

- Input count data has not been assigned hierarchical class annotations using assign_hierarchy()
- Statistical comparison has not been run via omu_summary() or omu_anova(); raw counts lack fold-change and p-value columns
- No biological groups or treatment factor exists to compare (unpaired or single-sample studies)

## Inputs

- omu_summary output object (data frame with log2FoldChange, p-value, adjusted p-value, and Class columns)
- hierarchical class metadata assigned to count dataframe

## Outputs

- ggplot2 volcano plot object with metabolites colored/shaped by Class
- customizable volcano plot compatible with ggplot2 themes and layers

## How to apply

First, ensure your count dataframe has hierarchical class data assigned using assign_hierarchy() with your chosen identifier. Run omu_summary() with parameters numerator, denominator, Factor, log_transform=TRUE, p_adjust='BH', and test_type='welch' to generate log2FoldChange and adjusted p-values. Pass the omu_summary output to plot_volcano() with column='Class' to stratify points by metabolite class. Use strpattern parameter to filter which classes appear (e.g., c('Organic acids', 'Carbohydrates')), and customize fill, color, alpha, and shape vectors to assign visual properties to each class. The resulting ggplot2 object is compatible with theme customization (e.g., theme_bw(), panel.grid removal) for publication-ready output.

## Related tools

- **omu** (R package providing plot_volcano(), omu_summary(), and assign_hierarchy() functions for metabolomics analysis and visualization) — github.com/connor-reid-tiffany/Omu
- **ggplot2** (Provides ggplot2 object rendering and theme customization for volcano plot output)
- **KEGGREST** (Supplies hierarchical class metadata via KEGG API when using assign_hierarchy(identifier='KEGG'))

## Examples

```
plot_volcano(omu_summary_output, column='Class', strpattern=c('Organic acids', 'Carbohydrates'), fill=c('firebrick2','white','dodgerblue2'), color=c('black','black','black'), alpha=c(1,1,1), shape=c(21,21,21)) + theme_bw() + theme(panel.grid=element_blank())
```

## Evaluation signals

- Volcano plot is a valid ggplot2 object; verify with is.ggplot() or by applying ggplot2 themes without error
- Points are stratified by Class column; verify by checking that each class label appears as a distinct visual group (color/shape combination)
- Strpattern filtering works correctly; verify that only specified classes appear in the plot (e.g., 'Organic acids' and 'Carbohydrates' only, no others)
- Axes correctly display log2FoldChange (x-axis) and -log10(adjusted p-value) (y-axis); verify scale and label consistency
- Customized fill, color, alpha, and shape vectors are applied; verify by visual inspection that colors, point opacity, and markers match specified parameters

## Limitations

- Requires pre-computed omu_summary output; does not perform statistical testing internally
- Only visualizes metabolites assigned to recognized hierarchical identifiers (KEGG, KO_Number, Prokaryote, Eukaryote); unassigned metabolites may be dropped or cause errors
- strpattern filtering is substring-based; metabolite classes must match exactly or contain the pattern; typos or partial matches may yield unexpected subsets
- ggplot2 themes are applied post-hoc; theme choices do not affect underlying data, only aesthetic rendering

## Evidence

- [other] omu_summary statistical comparison enables volcano plot visualization: "Call plot_volcano on the omu_summary output with column='Class', strpattern=c('Organic acids', 'Carbohydrates'), fill=c('firebrick2','white','dodgerblue2'), color=c('black','black','black'),"
- [other] assign_hierarchy precondition and KEGG identifier support: "Assign hierarchical class data to the count dataframe using assign_hierarchy with identifier='KEGG' and keep_unknowns=TRUE."
- [other] omu_summary parameters for statistical testing: "Run omu_summary statistical comparison with numerator='Strep', denominator='Mock', Factor='Treatment', log_transform=TRUE, p_adjust='BH', and test_type='welch' to obtain log2FoldChange and adjusted"
- [other] ggplot2 compatibility and theme customization: "The figure is a ggplot2 object, so it is compatible with any ggplot2 themes"
- [other] Theme application for final output: "Apply ggplot2 theme customization with theme_bw() and theme(panel.grid=element_blank()) to produce the final volcano plot ggplot2 object."
