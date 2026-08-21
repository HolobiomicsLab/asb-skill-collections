---
name: galaxy-w4m-lcms-processing-workflow
description: Use when running the Workflow4Metabolomics LC-MS pipeline end to end
  on a Galaxy instance — MSnbase import, xcms peak detection, correspondence, alignment
  and gap filling, CAMERA annotation, three-table conformance, batch correction, statistics
  — in the stage order the wrappers' datatypes enforce.
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  - GC-MS
  stage_count: 10
  member_skills:
  - xcms-data-import-preprocessing
  - mzml-file-import-xcms
  - mass-spectrometry-data-format-import
  - parameter-tuning-metabolomics
  - peak-picking-parameter-configuration
  - chromatographic-alignment-parameter-selection
  - lc-ms-profile-data-segmentation
  - chromatographic-peak-detection-wavelet
  - chromatographic-profile-quality-assessment
  - lc-ms-feature-grouping-by-retention-time
  - mass-chromatogram-alignment
  - retention-time-correction-and-alignment
  - retention-time-alignment-correction
  - missing-peak-imputation-fillpeaks
  - spectral-feature-clustering-by-intensity-correlation
  - metabolite-mass-to-charge-ratio-matching
  - adduct-fragment-table-construction
  - feature-metadata-parsing-and-integration
  - metadata-structure-checking
  - cross-table-metadata-harmonization
  - batch-effect-correction-qc-reference
  - batch-effect-correction-and-adjustment
  - compound-reliability-rsd-filtering
  - pls-pls-da-classification-modeling
  - metabolomic-biomarker-pathway-association
  member_tools:
  - MSnbase readMSData
  - Mz(X)ML Shaper
  - IPO for xcmsSet
  - IPO for group and retcor
  - xcms findChromPeaks
  - xcms refineChromPeaks
  - xcms findChromPeaks Merger
  - xcms groupChromPeaks
  - xcms adjustRtime
  - xcms fillChromPeaks
  - CAMERA.annotate
  - CAMERA.groupFWHM
  - CAMERA.groupCorr
  - CAMERA.findIsotopes
  - CAMERA.findAdducts
  - CAMERA.combinexsAnnos
  - Check Format
  - Table Merge
  - W4M concatenate
  - xcms get a sampleMetadata file
  - Normalization
  - Parsec batch correction
  - Batch Dispersion
  - Intensity Check
  - Biosigner
  - mixmodel
  - Metabolites Correlation Analysis
  - Heatmap
  edam_operations:
  - http://edamontology.org/operation_3214
  - http://edamontology.org/operation_3215
  - http://edamontology.org/operation_3432
  - http://edamontology.org/operation_3434
  - http://edamontology.org/operation_3435
  - http://edamontology.org/operation_3441
  - http://edamontology.org/operation_3632
  - http://edamontology.org/operation_3695
  - http://edamontology.org/operation_3891
  coverage_gaps:
  - 'parameter_optimisation: no leaf in the collection declares IPO; the stage is
    bound to generic parameter-tuning leaves'
  - 'statistics: no leaf declares Biosigner or the other W4M statistics wrappers'
  - no leaf in the collection declares Workflow4Metabolomics or Galaxy as the execution
    platform; the platform itself is unrepresented in the corpus
  derived_from_workflows: []
  bound_by: index
  provenance_tier: repository
  repo_url: https://github.com/workflow4metabolomics/tools-metabolomics
  license_tier: open
  tool_license:
    tier: open
    requires_ack: false
    ref: GPL-3.0
    url: https://github.com/workflow4metabolomics/tools-metabolomics/blob/master/LICENSE.txt
  verified_against:
    repo_ref: master
    observed: '2026-08-21'
schema_version: 0.3.0
---

# galaxy-w4m-lcms-processing-workflow

The Workflow4Metabolomics LC-MS line as one pipeline: ten stages, each bound to
leaf skills already in this collection and to the Galaxy tool that performs it.

## When to use

You are running, reviewing or reproducing a metabolomics analysis on a
Workflow4Metabolomics Galaxy instance, and you want the whole route from raw
open-format files to statistics rather than one step of it.

## When not to use

- The analysis is MS/MS annotation-led — molecular networking, spectral library
  matching, SIRIUS. That is `untargeted-lcmsms-annotation`, a different pipeline
  with different tools.
- You are working locally with xcms in R. The stage order still holds, but the
  Galaxy datatypes and the three-table interchange format do not apply.
- The data are NMR, or isotope-labelling and flux data. The same repository ships
  those tools, but they form separate chains that share only the three-table
  format.

## Why this stage order

It is not a convention. Each Galaxy wrapper declares the datatype it accepts and
the datatype it emits, and the chain below is the only order those declarations
permit. Two consequences are worth naming because they surprise people:
`adjustRtime` consumes a *grouped* object, so correspondence runs before
alignment and is then repeated against the corrected retention times; and
`fillChromPeaks` accepts only `rdata.xcms.group`, so gap filling cannot be moved
after annotation.

| stage | W4M tools | emits |
| --- | --- | --- |
| `import_raw` | `MSnbase readMSData`, `Mz(X)ML Shaper` | rdata.msnbase.raw |
| `parameter_optimisation` | `IPO for xcmsSet`, `IPO for group and retcor` | ipo-parameters |
| `peak_detection` | `xcms findChromPeaks`, `xcms refineChromPeaks`, `xcms findChromPeaks Merger` | rdata.xcms.findchrompeaks |
| `correspondence` | `xcms groupChromPeaks` | rdata.xcms.group |
| `rt_alignment` | `xcms adjustRtime`, `xcms groupChromPeaks` | rdata.xcms.group |
| `gap_filling` | `xcms fillChromPeaks` | rdata.xcms.fillpeaks |
| `annotation` | `CAMERA.annotate`, `CAMERA.groupFWHM`, `CAMERA.groupCorr`, `CAMERA.findIsotopes`, `CAMERA.findAdducts`, `CAMERA.combinexsAnnos` | rdata.camera, three-table |
| `table_conformance` | `Check Format`, `Table Merge`, `W4M concatenate`, `xcms get a sampleMetadata file` | three-table |
| `normalisation` | `Normalization`, `Parsec batch correction`, `Batch Dispersion`, `Intensity Check` | three-table |
| `statistics` | `Biosigner`, `mixmodel`, `Metabolites Correlation Analysis`, `Heatmap` | statistics, pdf |

## Stages

### `import_raw`

Raw open-format files -> an MSnbase object the xcms chain accepts.

- **after:** —
- **in → out:** mzML, mzXML, netCDF → rdata.msnbase.raw
- **W4M tools:** `MSnbase readMSData`, `Mz(X)ML Shaper`
- **EDAM:** `operation_3215`
- **leaf skills:**
  - `xcms-data-import-preprocessing` *(primary)*
  - `mzml-file-import-xcms`
  - `mass-spectrometry-data-format-import`
- **grounding:** 2 source DOI(s)

### `parameter_optimisation`

Design-of-experiments search for peak-picking, grouping and alignment parameters.

- **after:** —
- **in → out:** mzML → ipo-parameters
- **W4M tools:** `IPO for xcmsSet`, `IPO for group and retcor`
- **EDAM:** `operation_3435`
- **leaf skills:**
  - `parameter-tuning-metabolomics` *(primary)*
  - `peak-picking-parameter-configuration`
  - `chromatographic-alignment-parameter-selection`
- **grounding:** 3 source DOI(s)

### `peak_detection`

Detect chromatographic peaks per sample and merge the per-sample objects.

- **after:** `import_raw`, `parameter_optimisation`
- **in → out:** rdata.msnbase.raw → rdata.xcms.findchrompeaks
- **W4M tools:** `xcms findChromPeaks`, `xcms refineChromPeaks`, `xcms findChromPeaks Merger`
- **EDAM:** `operation_3441`
- **leaf skills:**
  - `lc-ms-profile-data-segmentation` *(primary)*
  - `chromatographic-peak-detection-wavelet`
  - `chromatographic-profile-quality-assessment`
- **grounding:** 3 source DOI(s)

### `correspondence`

Group peaks across samples into features.

- **after:** `peak_detection`
- **in → out:** rdata.xcms.findchrompeaks → rdata.xcms.group
- **W4M tools:** `xcms groupChromPeaks`
- **EDAM:** `operation_3632`
- **leaf skills:**
  - `lc-ms-feature-grouping-by-retention-time` *(primary)*
  - `mass-chromatogram-alignment`
- **grounding:** 1 source DOI(s)

### `rt_alignment`

Correct retention-time drift, then repeat correspondence against the corrected times.

- **after:** `correspondence`
- **in → out:** rdata.xcms.group → rdata.xcms.group
- **W4M tools:** `xcms adjustRtime`, `xcms groupChromPeaks`
- **EDAM:** `operation_3632`
- **leaf skills:**
  - `retention-time-correction-and-alignment` *(primary)*
  - `retention-time-alignment-correction`
- **grounding:** 2 source DOI(s)

### `gap_filling`

Integrate the areas of peaks missing from the feature matrix.

- **after:** `rt_alignment`
- **in → out:** rdata.xcms.group → rdata.xcms.fillpeaks
- **W4M tools:** `xcms fillChromPeaks`
- **EDAM:** `operation_3214`
- **leaf skills:**
  - `missing-peak-imputation-fillpeaks` *(primary)*
- **grounding:** 1 source DOI(s)

### `annotation`

Group features into pseudospectra and annotate isotopes and adducts.

- **after:** `gap_filling`
- **in → out:** rdata.xcms.fillpeaks → rdata.camera, three-table
- **W4M tools:** `CAMERA.annotate`, `CAMERA.groupFWHM`, `CAMERA.groupCorr`, `CAMERA.findIsotopes`, `CAMERA.findAdducts`, `CAMERA.combinexsAnnos`
- **EDAM:** `operation_3432`
- **leaf skills:**
  - `spectral-feature-clustering-by-intensity-correlation` *(primary)*
  - `metabolite-mass-to-charge-ratio-matching`
  - `adduct-fragment-table-construction`
- **grounding:** 1 source DOI(s)

### `table_conformance`

Make the dataMatrix, sampleMetadata and variableMetadata agree before any statistics.

- **after:** `annotation`
- **in → out:** three-table → three-table
- **W4M tools:** `Check Format`, `Table Merge`, `W4M concatenate`, `xcms get a sampleMetadata file`
- **EDAM:** `operation_3891`
- **leaf skills:**
  - `feature-metadata-parsing-and-integration` *(primary)*
  - `metadata-structure-checking`
  - `cross-table-metadata-harmonization`
- **grounding:** 3 source DOI(s)

### `normalisation`

Normalise intensities and correct batch and drift effects using the pooled QC samples.

- **after:** `table_conformance`
- **in → out:** three-table → three-table
- **W4M tools:** `Normalization`, `Parsec batch correction`, `Batch Dispersion`, `Intensity Check`
- **EDAM:** `operation_3434`
- **leaf skills:**
  - `batch-effect-correction-qc-reference` *(primary)*
  - `batch-effect-correction-and-adjustment`
  - `compound-reliability-rsd-filtering`
- **grounding:** 3 source DOI(s)

### `statistics`

Univariate, multivariate and signature analysis on the corrected matrix.

- **after:** `normalisation`
- **in → out:** three-table → statistics, pdf
- **W4M tools:** `Biosigner`, `mixmodel`, `Metabolites Correlation Analysis`, `Heatmap`
- **EDAM:** `operation_3695`
- **leaf skills:**
  - `pls-pls-da-classification-modeling` *(primary)*
  - `metabolomic-biomarker-pathway-association`
- **grounding:** 2 source DOI(s)

## Grounding

Every stage carries the DOIs and KB slugs of the leaves bound to it; ground a
stage with the collection's `/ground` recipe against those slugs.

The pipeline *structure* is grounded differently from the leaves: it was read off
the tool wrappers in `workflow4metabolomics/tools-metabolomics` at `master` on
2026-08-21, not distilled from a paper. `provenance.structure_source` in
`workflow.yaml` records that.

## Verification contract

- Each stage's output datatype is the one the next stage declares as its input.
  A Galaxy invocation that type-checks has already verified most of this.
- The second correspondence pass ran after alignment; a workflow with one
  grouping step is missing it.
- The three tables agree on identifiers and order before `normalisation`. See
  `w4m-three-table-format-conformance`.
- `xcms process history` matches the exported workflow.
- Feature counts are reported after gap filling, not after correspondence; the
  two differ and only the first describes the matrix the statistics saw.

## Coverage gaps

The corpus does not cover this pipeline evenly, and the bindings say where:

- **Parameter optimisation** — no leaf declares IPO. The stage is bound to
  generic parameter-tuning leaves, which describe the activity but not the tool.
- **Statistics** — no leaf declares Biosigner or the other W4M statistics
  wrappers. The bound leaves cover PLS-DA and biomarker association generically.
- **The platform** — no leaf declares Workflow4Metabolomics or Galaxy. The
  collection knows the methods this pipeline runs and not the platform that runs
  them.

Of the 16 DOIs the wrappers cite, 2 are already in the collection's corpus. The
other 14 are candidates for corpus expansion, which would close the gaps above
at their source rather than by rebinding.

## Provenance

Structure from the tool wrappers; leaf bindings by lexical retrieval over
`skills_index.json` constrained to leaves that declare the relevant tool, then
checked by hand. `bound_by: index`. No ASB rerun; no per-paper workflow DAG
contributed structure, so `derived_from_workflows` is empty and no benchmark
ablation is required.
