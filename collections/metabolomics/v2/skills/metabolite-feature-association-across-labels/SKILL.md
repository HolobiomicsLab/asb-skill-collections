---
name: metabolite-feature-association-across-labels
description: Use when after PuInc_seeker has identified putative incorporations (m/z
  features showing significant fold-change and p-value signals between labeled and
  unlabeled sample groups) and you need to assign base peaks—the most intense isotopologue
  signals—and validate isotope-pair mass gaps match.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - geoRge
  - R
  - XCMS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5b03628
  title: geoRge
evidence_spans:
- library(geoRge)
- hits <- database_query(geoRgeR = s2, adducts = negative, db = db)
- This is an R Markdown document
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_george_cq
    doi: 10.1021/acs.analchem.5b03628
    title: geoRge
  dedup_kept_from: coll_george_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5b03628
  all_source_dois:
  - 10.1021/acs.analchem.5b03628
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-association-across-labels

## Summary

Identify base-peak isotopologue groupings from putative stable isotope incorporations by linking enriched features across unlabeled and labeled sample cohorts using atomic mass differences and mass accuracy constraints. This skill bridges isotope-tagged metabolite detection to metabolite identification by establishing which m/z peaks correspond to the same molecular entity under different labeling conditions.

## When to use

Apply this skill after PuInc_seeker has identified putative incorporations (m/z features showing significant fold-change and p-value signals between labeled and unlabeled sample groups) and you need to assign base peaks—the most intense isotopologue signals—and validate isotope-pair mass gaps match theoretical labeled/unlabeled atomic mass differences (e.g., 13C vs 12C = 1.003355 Da). Use when processing LC/MS untargeted metabolomics data with stable isotope labeling (e.g., 13C-glucose) and mass accuracy is ≤ 6.5 ppm.

## When NOT to use

- Input data has not undergone PuInc_seeker filtering or lacks fold-change and p-value pre-filtering; basepeak_finder expects pre-validated putative incorporations, not raw peak lists.
- Sample cohorts lack clear labeled vs. unlabeled group separation or are missing one of the two labeling conditions; the function requires paired sample class tags (ULtag and Ltag) to establish isotope pairs.
- Mass accuracy of the LC/MS instrument is substantially worse than 6.5 ppm (e.g., low-resolution TOF or quadrupole data); isotope mass gaps smaller than ~1 Da cannot be reliably resolved.

## Inputs

- geoRge object produced by PuInc_seeker (containing putative incorporation features with m/z, RT, fold-change, p-value, and sample class annotations)
- XCMS dataset (XCMSet object with peak-picked, aligned, and grouped features from unlabeled and labeled LC/MS runs)

## Outputs

- geoRge object with base-peak isotopologue annotations (m/z, intensity, isotope-pair mass gaps, sample class tags)
- annotated feature list mapping base peaks to isotope siblings with validated mass accuracy

## How to apply

Execute basepeak_finder on the output geoRge object from PuInc_seeker, specifying: unlabeled atomic mass (12.0), labeled atomic mass (13.003355), mass accuracy tolerance (6.5 ppm), and base-peak minimum intensity threshold (2000). The function scans each putative incorporation feature, locates the highest-intensity m/z signal within the tolerance window, validates that the mass gap between unlabeled and labeled isotopologue peaks matches the theoretical difference, and flags the peak pair as a confirmed base-peak association. Filter candidate peaks by intensity to eliminate noise; reject m/z pairs where the mass offset deviates beyond the specified ppm tolerance, as these indicate artifacts or distinct metabolites rather than isotope pairs. The resulting geoRge object annotates each base peak with m/z, intensity, and isotope-pair relationships, enabling downstream database queries and metabolite assignment.

## Related tools

- **geoRge** (Core R package providing basepeak_finder function to identify and annotate base-peak isotopologue groupings with mass accuracy and intensity filters) — https://github.com/jcapelladesto/geoRge
- **XCMS** (Upstream peak picking, alignment, and grouping of LC/MS features from raw mzXML files; produces XCMSet input object) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **R** (Execution environment for geoRge and downstream statistical/visualization workflows)

## Examples

```
s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0, L.atomM=13.003355, ppm.s=6.5, Basepeak.minInt=2000)
```

## Evaluation signals

- Resulting geoRge object contains base-peak m/z values with intensity ≥ 2000 and non-null isotope-pair annotations (labeled m/z, unlabeled m/z, mass gap).
- Mass gap between each unlabeled–labeled m/z pair deviates from theoretical 13C–12C difference (1.003355 Da) by ≤ 6.5 ppm; computed as |observed_gap − 1.003355| / 1.003355 × 1e6 ≤ 6.5.
- All base-peak m/z entries retain sample class tags (ULtag and Ltag) matching input; no cross-contamination of labeled features into unlabeled group or vice versa.
- Intensity of base peaks in the identified isotope pairs is consistent with expected fold-change patterns from PuInc_seeker (labeled >> unlabeled for 13C incorporation, or vice versa depending on experimental design).
- Output geoRge object is suitable for downstream database_query without null or malformed isotope-pair fields; all m/z and intensity values are numeric and within biologically plausible ranges (e.g., 50–1500 m/z for small metabolites).

## Limitations

- basepeak_finder assumes that the highest-intensity m/z within the tolerance window is the true base peak; in complex mixtures or isomeric features at similar m/z, this assumption may fail.
- Mass accuracy tolerance (6.5 ppm in the mtbls213 example) must be tuned to the specific LC/MS platform and may not be universally applicable; high-resolution instruments can use tighter tolerances, while low-resolution instruments may require relaxation.
- The function requires explicit paired sample class labeling (ULtag and Ltag); metabolomics datasets without clear unlabeled/labeled group annotation cannot be processed.
- Putative incorporations filtered by PuInc_seeker's fold-change (1.5×) and p-value (0.05) thresholds may miss weak labeling signals or low-abundance metabolites; downstream base-peak identification is limited by upstream filter stringency.
- No changelog is maintained in the geoRge repository, making version-to-version API changes difficult to track; users upgrading from geoRge 0.x to 1.0+ should verify function arguments via help(basepeak_finder).

## Evidence

- [other] basepeak_finder function operates on PuInc_seeker output and uses unlabeled atom mass (12.0), labeled atom mass (13.003355), mass accuracy tolerance (6.5 ppm), and minimum intensity threshold (2000): "basepeak_finder function operates on PuInc_seeker output and uses unlabeled atom mass (12.0), labeled atom mass (13.003355), mass accuracy tolerance (6.5 ppm), and minimum intensity threshold (2000)"
- [other] Apply basepeak_finder to the PuInc_seeker output with unlabelled atomic mass 12.0, labelled atomic mass 13.003355, mass accuracy tolerance 6.5 ppm, and base-peak minimum intensity threshold 2000, matching the same sample tags and position logic.: "Apply basepeak_finder to the PuInc_seeker output with unlabelled atomic mass 12.0, labelled atomic mass 13.003355, mass accuracy tolerance 6.5 ppm, and base-peak minimum intensity threshold 2000"
- [other] Validate that the resulting geoRge object contains identified base peaks with m/z, intensity, and isotope-pair annotations.: "Validate that the resulting geoRge object contains identified base peaks with m/z, intensity, and isotope-pair annotations"
- [readme] s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0,L.atomM=13.003355, ppm.s=6.5,Basepeak.minInt=2000): "s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0,L.atomM=13.003355, ppm.s=6.5,Basepeak.minInt=2000)"
- [readme] geoRge: a computational tool for stable isotope labelling detection in LC/MS-based untargeted metabolomics: "geoRge: a computational tool for stable isotope labelling detection in LC/MS-based untargeted metabolomics"
