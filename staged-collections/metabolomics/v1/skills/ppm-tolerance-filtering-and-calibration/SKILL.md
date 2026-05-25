---
name: ppm-tolerance-filtering-and-calibration
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to apply mass accuracy filtering using parts-per-million (ppm) tolerance windows to match observed m/z values against expected fragment ions or precursors in high-resolution mass spectrometry datasets.
when_to_use_negative:
- Your instrument has not been recently mass-calibrated and you do not know its actual mass error profile; applying an arbitrary ppm window could yield spurious matches or miss true features.
- You are filtering data that has already been deconvoluted or centroided by vendor software into discrete peaks; applying ppm tolerance to pre-processed peak lists requires verification that m/z values are still in the original instrument's mass space.
- The query targets low-abundance isotope peaks (e.g., ⁵⁴Fe with <25% expected intensity relative to ⁵⁶Fe) in samples with high chemical noise; a single fixed ppm and intensity threshold may miss these due to random fluctuations or miss-calibration, as documented for the IIMN method.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3375
- http://edamontology.org/topic_3520
tools:
- name: MassQL
  role: Query language and reference engine for specifying and executing m/z filtering with ppm tolerance across MS/MS repositories
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark
  role: Parser library for translating MassQL query strings (with TOLERANCEPPM parameters) into executable parse trees
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Python library for reading MS data files (mzML, mzXML, MGF) and extracting m/z and intensity arrays for tolerance-based filtering
- name: pandas
  role: DataFrame library for vectorized m/z filtering and intensity thresholding operations on MS/MS spectra
- name: MZmine
  role: Open-source desktop software with native MassQL integration for interactive query design and ppm tolerance tuning on reference datasets before scaling
  repo: https://github.com/mzmine/mzmine
- name: MS-DIAL
  role: Open-source MS/MS analysis platform supporting MassQL queries with configurable ppm tolerance windows
- name: GNPS/MassIVE
  role: Public MS/MS repository hosting 230+ million spectra; provides both a repository for scaling ppm-tolerance queries and spectral libraries for reference-based query refinement
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_s41592_full/skills/ppm-tolerance-filtering-and-calibration/SKILL.md
    - outputs/audit_s41592_full/skills/ppm-tolerance-filtering-and-calibration/skill.md
    merged_at: '2026-05-25T07:33:56.421786+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/ppm-tolerance-filtering-and-calibration@sha256:5e4a84204174b2cb5a93cca37c32687cbd77265bd9c4b635a43a459308664913
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# ppm-tolerance-filtering-and-calibration

## Summary

Apply mass accuracy filtering using parts-per-million (ppm) tolerance windows to match observed m/z values against expected fragment ions or precursors in high-resolution mass spectrometry datasets. This skill is essential for reducing false positives when querying large repositories of LC-MS/MS data, particularly when searching for specific molecular signatures across heterogeneous instrument types and ionization sources.

## When to use

When executing a MassQL query (or equivalent fragment ion search) on raw LC-MS/MS data and you need to specify the mass accuracy window for product ion or precursor m/z matching. Use this skill if your instrument's typical mass error is known or calibrated (e.g., Q Exactive typically achieves ≤5 ppm), and you want to balance specificity (tighter tolerance = fewer false matches) against sensitivity (looser tolerance = risk of including unrelated ions). Particularly relevant when scaling a refined query from a reference dataset (with known compounds) to an entire public repository containing millions of MS/MS spectra.

## When NOT to use

- Your instrument has not been recently mass-calibrated and you do not know its actual mass error profile; applying an arbitrary ppm window could yield spurious matches or miss true features.
- You are filtering data that has already been deconvoluted or centroided by vendor software into discrete peaks; applying ppm tolerance to pre-processed peak lists requires verification that m/z values are still in the original instrument's mass space.
- The query targets low-abundance isotope peaks (e.g., ⁵⁴Fe with <25% expected intensity relative to ⁵⁶Fe) in samples with high chemical noise; a single fixed ppm and intensity threshold may miss these due to random fluctuations or miss-calibration, as documented for the IIMN method.

## Inputs

- LC-MS/MS dataset in mzML, mzXML, or MGF format
- MassQL query string with MS2PROD, TOLERANCEPPM, and INTENSITYPERCENT parameters
- Target m/z value (e.g., 98.9847 for H₄PO₄⁺ phosphate fragment)
- Instrument mass accuracy specification or calibration data (ppm)

## Outputs

- Filtered MS/MS spectra matching the ppm tolerance window
- Tabular export (CSV/TSV) with scan IDs, precursor m/z, product ion m/z, intensity, and metadata
- Count of matched MS/MS scans and unique molecular features
- Optionally: Apache feather-format cached data for repeated querying

## How to apply

First, establish the appropriate ppm tolerance window based on your instrument's calibration and mass accuracy specification. In the MassQL reference engine, the TOLERANCEPPM parameter defines a symmetric window around the target m/z (e.g., MS2PROD=98.9847:TOLERANCEPPM=50 matches product ions between 98.9722–98.9972 m/z, accounting for ±50 ppm mass error). Parse the MassQL query string using the lark library to construct an internal query tree that encodes both the target m/z and the tolerance window. Load MS/MS spectra from mzML, mzXML, or MGF format files using pyteomics, storing them in pandas DataFrames indexed by m/z. Apply filtering by iterating through each MS/MS scan and retaining only those with a peak intensity at the target m/z ± TOLERANCEPPM that meets the INTENSITYPERCENT threshold (e.g., ≥50% of base peak). Export matched spectra with their scan identifiers, precursor m/z, observed product ion m/z, and intensity values. When scaling from a reference dataset to a large repository, start with a tighter tolerance window on known compounds to refine the query, then relax tolerance judiciously (e.g., from 25 ppm to 50 ppm) if sensitivity is needed, monitoring for a sharp rise in uncharacterized results (>85% unknown) as a sign of over-relaxation.

## Related tools

- **MassQL** (Query language and reference engine for specifying and executing m/z filtering with ppm tolerance across MS/MS repositories) — https://github.com/mwang87/MassQueryLanguage
- **lark** (Parser library for translating MassQL query strings (with TOLERANCEPPM parameters) into executable parse trees) — https://github.com/lark-parser/lark
- **pyteomics** (Python library for reading MS data files (mzML, mzXML, MGF) and extracting m/z and intensity arrays for tolerance-based filtering)
- **pandas** (DataFrame library for vectorized m/z filtering and intensity thresholding operations on MS/MS spectra)
- **MZmine** (Open-source desktop software with native MassQL integration for interactive query design and ppm tolerance tuning on reference datasets before scaling) — https://github.com/mzmine/mzmine
- **MS-DIAL** (Open-source MS/MS analysis platform supporting MassQL queries with configurable ppm tolerance windows)
- **GNPS/MassIVE** (Public MS/MS repository hosting 230+ million spectra; provides both a repository for scaling ppm-tolerance queries and spectral libraries for reference-based query refinement)

## Examples

```
from massql.query import QuerySpecifier; from pyteomics import mzml; query = QuerySpecifier('MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50'); reader = mzml.read('marine_water_sample.mzML'); matches = [scan for scan in reader if any(abs(peak[0] - 98.9847) * 1e6 / 98.9847 <= 50 and peak[1] >= 0.5 * max_intensity for peak in scan['m/z array'])]
```

## Evaluation signals

- The number of matched MS/MS spectra should be stable and reproducible across re-runs with identical ppm tolerance and intensity threshold parameters.
- When you reduce TOLERANCEPPM (e.g., 50 → 25 ppm), the count of matched spectra should decrease monotonically; a sharp cliff or non-monotonic behavior suggests query parsing or filtering logic errors.
- Manual inspection of a random sample of matched spectra should confirm that the observed product ion m/z lies within the stated tolerance window (e.g., if TOLERANCEPPM=50 and target=98.9847, no matched peak should be >98.9972 m/z).
- When applied to a reference dataset with known positive controls (e.g., 3 known OPEs), the query should recover all positive controls with ≥95% sensitivity; failure suggests the tolerance window is too tight or the intensity threshold excludes low-abundance fragments.
- Comparison of sensitivity (proportion of known compounds retrieved) vs. specificity (proportion of retrieved spectra that match a known chemical formula within ±20 ppm) should show a trade-off; if specificity drops below 10% (>90% uncharacterized results), the tolerance window is likely too permissive for the target compound class.

## Limitations

- MassQL and single ppm-tolerance windows have limited capability to leverage multiple consecutive MS spectra arising from a single chromatographic feature; transient mass calibration drift across a LC run may cause the same analyte to fall outside the tolerance window in late-eluting scans.
- A single compound with anomalously low intensity for a key fragment (e.g., ⁵⁴Fe peak at <25% relative to expected) will be missed if the INTENSITYPERCENT threshold does not accommodate biological or instrumental variability in isotope ratios.
- The ppm tolerance window is symmetric around the target m/z; if mass calibration exhibits systematic drift (e.g., consistently higher m/z at high mass), a symmetric window may waste tolerance space on one side and miss true peaks on the other.
- Applying a fixed ppm tolerance across different instrument types (e.g., quadrupole time-of-flight vs. Orbitrap) can be suboptimal; each instrument has different mass accuracy profiles, and query refinement on one instrument type may not transfer directly to another.

## Evidence

- [full_text] MS2PROD=<m/z>, MS2PROD=163.1
- [other] Execute MassQL phosphate product-ion MS2 query (MS2PROD=98.9847, TOLERANCEPPM=50, INTENSITYPERCENT=50)
- [other] Apply the query engine to filter all MS/MS scans, retaining only those with a product ion at m/z 98.9847 ± 50 ppm and peak intensity ≥ 50% of base peak.
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats
- [full_text] The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree
- [full_text] we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries
- [full_text] Thereafter, when using the refined MassQL queries to search repository data, more than 594,000 putative bile acids MS/MS spectra were retrieved
- [full_text] MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%