---
name: isotopic-peak-removal
description: Use when after loading raw FT-ICR MS peak lists with assigned molecular formulas when you have detected peaks across multiple m/z values that correspond to isotopic variants of the same parent compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0081
  tools:
  - pandas
  - NumPy
  - Formularity
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- requires the Python dependencies NumPy [40], pandas [41, 42]
- It requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index... It requires the Python dependencies NumPy
- it has been designed to work with the output file (in .csv format) generated directly by Formularity [24] which uses FT-ICR MS data in .xml format
- it has been designed to work with the output file (in .csv format) generated directly by Formularity [24]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
---

# isotopic-peak-removal

## Summary

Remove isotopic peaks (primarily ¹³C) from FT-ICR MS peak-abundance matrices to eliminate redundant molecular signals and reduce noise before downstream analysis. This filtering step prevents overrepresentation of naturally occurring isotopic variants of the same compound.

## When to use

Apply this skill after loading raw FT-ICR MS peak lists with assigned molecular formulas when you have detected peaks across multiple m/z values that correspond to isotopic variants of the same parent compound. This is especially critical when the downstream analysis goal is compound-level (rather than isotope-level) interpretation, such as chemodiversity assessment, biochemical transformation networks, or statistical comparison of molecular compositions across samples.

## When NOT to use

- The goal is isotope-ratio analysis or tracing (e.g., ¹³C labeling experiments); isotope peaks are the primary signal of interest.
- Input data are already de-isotoped or derived from tandem MS with neutral loss annotation; redundant isotope removal may have already occurred upstream.
- Raw m/z values are provided without assigned molecular formulas; isotopic peak identification requires formula assignment.

## Inputs

- CSV file containing detected peaks with columns: m/z values, molecular formulas, peak intensities, isotopic annotations or isotopic carbon labels

## Outputs

- Filtered peak-abundance matrix (CSV) with isotopic peaks removed, retaining only monoisotopic peaks for each unique molecular formula

## How to apply

Iterate through the detected peaks and identify isotopic variants by checking the peak annotations for isotopic carbon labeling (¹³C) or equivalent isotopic markers in the assigned molecular formula field. Remove all peaks flagged as isotopic variants, retaining only the monoisotopic (M) peak for each compound. The rationale is that ¹³C peaks are naturally occurring and predictable from elemental composition; including them inflates apparent molecular diversity and can bias subsequent normalization and statistical analyses. This filtering must occur before m/z-based and error-threshold filtering to avoid propagating redundant signals through the pipeline.

## Related tools

- **pandas** (Load, filter, and manipulate the peak CSV file to identify and remove rows with isotopic peak annotations)
- **Formularity** (Assign and annotate molecular formulas to m/z peaks, providing the isotopic carbon and isotopic labeling information needed to flag isotopic variants)

## Evaluation signals

- Peak count decreases by a predictable fraction (typically 1–5% for natural samples, reflecting the expected ¹³C abundance); large deletions suggest over-filtering.
- Remaining peaks are all monoisotopic forms; verify no peaks with ¹³C, ²H, ¹⁸O, or other isotopic labels remain in the output matrix.
- Elemental composition (e.g., number of carbons) of retained peaks is stable across filtering; no systematic bias toward lighter or heavier formulas.
- Downstream diversity metrics (e.g., NOSC, DBE distributions) and Van Krevelen diagrams show expected molecular composition without artificial clustering at +1.003 m/z intervals.
- Comparison with external reference datasets (e.g., known metabolite databases) confirms that retained peaks match expected monoisotopic masses within measurement tolerance (0.5 ppm).

## Limitations

- Isotopic peak detection depends on accurate molecular formula assignment; if formula errors are high (>0.5 ppm), isotopic variants may be misidentified or missed.
- Natural samples with high carbon content will have higher natural ¹³C abundance; filtering may remove a larger proportion of peaks than in low-carbon samples, potentially introducing composition bias.
- The skill assumes that isotopic annotations are unambiguous in the input CSV; if multiple isotopic labels are present or mixed with adducts/fragments, manual curation or post-filtering validation is required.
- Does not address isotopic interference from multiply charged ions or unresolved doublets; requires sufficient mass resolution from the FT-ICR instrument.

## Evidence

- [other] Filter peaks by m/z range (user-defined) and remove isotopic peaks (13C).: "Filter peaks by m/z range (user-defined) and remove isotopic peaks (13C)."
- [methods] detected peaks are filtered by their m/z values (based on the user's input): "detected peaks are filtered by their m/z values (based on the user's input)"
- [methods] isotopic presence (13C peaks): "isotopic presence (13C peaks)"
- [other] MetaboDirect applies multiple sequential filters (isotopic carbon removal, m/z-based filtering, formula assignment error thresholds): "applies multiple sequential filters (isotopic carbon removal, m/z-based filtering, formula assignment error thresholds)"
