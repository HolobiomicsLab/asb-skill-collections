# Workflow Challenge: `coll_mass2adduct_workflow`


> mass2adduct is an R package that identifies and visualizes molecular adducts in mass spectrometry imaging data by computing pairwise mass differences, matching them to known chemical transformations, and enabling spatial correlation analysis.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 1 reported result: The mass2adduct package implements a pipeline that computes mass difference objects, builds histograms of those differences, matches them to known adducts using adductMatch(), and ranks results with topAdducts() to identify the most abundant adducts. Analyses 1 derived result: The pointsAdducts() function generates a scatter plot that highlights adduct ions in red and parent ions in contrasting colors, enabling visual identification of the red/blue overlap pattern between sodium adducts and their corresponding parent ions. Reconstructs 1 described mechanism (described in the paper but not separately evaluated there): The corrPairsMSI() function performs a two-tailed Pearson correlation test on each pair of peaks in the massdiff object to assess spatial correlation between parent and adduct ions. Extends the paper in 1 task beyond its reported scope: The mass2adduct package provides cardinal2msimat() for converting Cardinal MSI data objects to the msimat format compatible with the massdiff() and adductMatch() pipeline.

## Research questions

- What is the complete computational workflow for detecting and ranking molecular adducts in mass spectrometry imaging data using the mass2adduct package?
- How does the corrPairsMSI() function compute pairwise correlations between ion pairs in mass spectrometry imaging data with statistical correction?
- How can sodium adduct ions be visually distinguished from their parent ions in mass spectrometry imaging data?
- Can mass2adduct's massdiff() and adductMatch() pipeline successfully process MSI data converted from Cardinal's MSProcessedImagingExperiment or MSContinuousImagingExperiment objects using the cardinal2msimat() function?

## Methods overview

Load preprocessed MSI data from CSV into msimat object Compute all pairwise mass differences using massdiff() to identify potential adduct pairs Generate mass difference histogram using hist() to visualize distribution of observed mass differences Match histogram peaks to known chemical transformations using adductMatch() with adducts reference dataset, reporting counts and quantiles Rank mass differences by occurrence using topAdducts() and annotate with known adduct matches Validation: Verify that topAdducts() output includes counts, quantiles, and adduct name matches for top-ranked mass differences; confirm massdiff object subset excludes ion pairs without matched adducts References: source article (DOI: 10.1021/acs.analchem.0c04720) Load MSI intensity matrix from CSV and construct msimat object for downstream analysis. Generate all pairwise mass differences between observed m/z peaks to identify potential adduct candidates. Annotate ion pairs by matching observed mass differences to known chemical adducts using adducts2 reference set. Compute Pearson correlation coefficients between parent and adduct ion intensity profiles across pixels using corrPairsMSI(). Apply Bonferroni multiple-testing correction to assess statistical significance of spatial correlations at family-wise error rate. Validation: Output massdiff data frame contains non-null Estimate, P.value, and Significance columns for all annotated pairs; Bonferroni-corrected p-values are ≤ 0.05 for rows marked Significance=TRUE. References: source article (DOI: 10.1021/acs.analchem.0c04720) Subset correlation-filtered massdiff object to sodium adduct matches only Load preprocessed MSI data matrix and annotated massdiff object into R/mass2adduct environment Overlay adduct ion peaks as red filled points (pch=20) using pointsAdducts(which='adduct') Overlay parent ion peaks as blue circle outlines (pch=1) using pointsAdducts(which='parent') Validation: confirm visual output shows characteristic red/blue overlap pattern indicating ions with dual parent-adduct roles in the same sample References: source article (DOI: 10.1021/acs.analchem.0c04720) Load a Cardinal imaging experiment object (MSProcessedImagingExperiment or MSContinuousImagingExperiment) into R. Convert the Cardinal object to msimat format using cardinal2msimat() function to produce a peak-intensity matrix with m/z column names. Compute all pairwise mass differences using massdiff(), producing a three-column data.frame (parent m/z, adduct m/z, mass difference). Match each mass difference to the closest entry in a reference adduct database using adductMatch() with built-in or custom adduct table. Validation: verify that the output object is a data.frame with columns A, B, diff, and matches; confirm that at least one ion pair matches to a known adduct; inspect matches column for non-NA entries indicating successful mapping to the reference database. References: source article (DOI: 10.1021/acs.analchem.0c04720)

**Domain:** metabolomics

**Techniques:** adduct-detection, mass-spectrometry-imaging, maldi, metabolite-identification, feature-detection

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** In mass spectrometry imaging, adducts can form between target molecules such as metabolites and other substances such as matrix or salt ions. _[grounded: COMP_ADDUCTS_DATASET]_
- **(finding)** The mass2adduct package accompanies Janda et al. (2021). _[grounded: SYS_MASS2ADDUCT]_
- **(finding)** Each peak in a mass spectrum represents ions of a given mass/charge ratio (m/z) that have been detected by the instrument.
- **(finding)** In mass2adduct documentation, the term 'mass peak' is used to refer to both the ions themselves and to their nominal m/z values. _[grounded: SYS_MASS2ADDUCT]_
- **(finding)** A chemical transformation refers agnostically to the chemical difference between two ions. _[grounded: CONCEPT_CHEMICAL_TRANSFORMATION]_
- **(finding)** The abbreviation 'massdiff' refers to 'mass difference' and denotes the absolute difference in m/z values between two mass peaks. _[grounded: TOOL_MASSDIFF_FN]_
- **(finding)** An adduct refers specifically to a transformation caused by the addition of a chemical moiety, often during the MSI procedure.
- **(finding)** The precursor to an adduct is called the parent ion or parent molecule.
- **(finding)** The mass2adduct analysis looks at pairs of peaks and attempts to match their massdiffs to known chemical transformations to find adducts derived from the chemical matrix used for MALDI-MSI. _[grounded: SYS_MASS2ADDUCT]_
- **(finding)** Raw MSI data are exported as plain-text CSV files from standard MSI software such as SCiLS or MSiReader. _[grounded: TOOL_SCILS]_
- **(finding)** In the mass2adduct CSV format, columns represent mass peaks with m/z values as column names, and rows represent pixels. _[grounded: SYS_MASS2ADDUCT]_
- **(finding)** Entries in the mass2adduct data table represent intensity values for a given peak and pixel. _[grounded: SYS_MASS2ADDUCT]_
- **(finding)** The cardinal2msimat() function can convert data objects in MSProcessedImagingExperiment or MSContinuousImagingExperiment formats to mass2adduct's msimat format. _[grounded: SYS_MASS2ADDUCT]_
- **(finding)** Cardinal version 2.2 or higher is required for use with mass2adduct. _[grounded: SYS_MASS2ADDUCT]_
- **(finding)** The default plot method for an msimat object displays a mass spectrum with vertical lines representing the total intensity of each peak. _[grounded: COMP_MSIMAT]_
- **(finding)** The massdiff function returns an object of classes data.frame and massdiff. _[grounded: TOOL_MASSDIFF_FN]_
- **(finding)** In the massdiff output, column A represents the parent ion peak mass. _[grounded: TOOL_MASSDIFF_FN]_
- **(finding)** In the massdiff output, column B represents the putative adduct ion peak mass (higher than A). _[grounded: TOOL_MASSDIFF_FN]_
- **(finding)** In the massdiff output, column diff is the difference between A and B. _[grounded: TOOL_MASSDIFF_FN]_
- **(finding)** The mass2adduct package includes two built-in datasets called adducts and adducts2 that list biologically-relevant chemical species. _[grounded: SYS_MASS2ADDUCT]_
- **(finding)** Users can create custom adduct tables with the same three columns as the built-in adducts dataset. _[grounded: COMP_ADDUCTS_DATASET]_
- **(finding)** The background of likely non-meaningful mass differences is not uniformly distributed but instead has peaks at integer values.
- **(finding)** Chemical masses themselves are close to integer values, hence the differences between them should be too.
- **(finding)** The adductMatch function looks for known adducts by finding the closest-matching bin in the mass difference histogram. _[grounded: COMP_ADDUCTS_DATASET]_
- **(finding)** adductMatch reports the number of counts for each mass difference and the quantile. _[grounded: TOOL_ADDUCTMATCH]_
- **(finding)** Quantile values in adductMatch are usually quite high because the majority of mass differences have zero to few counts. _[grounded: TOOL_ADDUCTMATCH]_
- **(finding)** The topAdducts function ranks mass differences by their occurrences in descending order and reports matches to known adducts. _[grounded: COMP_ADDUCTS_DATASET]_
- **(finding)** The histogram method bins massdiff values into bins of fixed width. _[grounded: TOOL_MASSDIFF_FN]_
- **(finding)** The mass resolution of a mass spectrometer varies with the mass.
- **(finding)** adductMatch can be applied to a massdiff object to add a matches column listing the closest-matching adduct for each ion pair. _[grounded: COMP_MASSDIFF_OBJ]_
- **(finding)** The object produced by adductMatch is a subset of the original massdiff object, as ion pairs without a matching adduct are excluded. _[grounded: COMP_MASSDIFF_OBJ]_
- **(finding)** corrPairsMSI performs a correlation test on each pair of peaks in a massdiff object. _[grounded: COMP_MASSDIFF_OBJ]_
- **(finding)** corrPairsMSI uses the two-tailed Pearson method by default for correlation testing. _[grounded: COMP_MASSDIFF_OBJ]_
- **(finding)** The how=parallel option can speed up corrPairsMSI processing on computers with multiple processors. _[grounded: TOOL_CORRPAIRSMSI]_
- **(finding)** The ncores parameter in corrPairsMSI specifies the number of processors to use. _[grounded: TOOL_CORRPAIRSMSI]_
- **(finding)** corrPairsMSIchunks can be used instead of corrPairsMSI for larger datasets to avoid running out of memory. _[grounded: TOOL_CORRPAIRSMSI]_
- **(finding)** corrPairsMSIchunks splits the job into chunks that fit within a specified memory limit. _[grounded: TOOL_CORRPAIRSMSI_CHUNKS]_
- **(finding)** Using corrPairsMSIchunks results in more overhead and less speed compared to corrPairsMSI. _[grounded: TOOL_CORRPAIRSMSI]_
- **(finding)** Correlation test results in corrPairsMSI output include Estimate (correlation coefficient), P.value, and Significance. _[grounded: COMP_MASSDIFF_OBJ]_
- **(finding)** The Significance column in corrPairsMSI output indicates whether the p-value is below the threshold after Bonferroni correction. _[grounded: TOOL_CORRPAIRSMSI]_
- **(finding)** Raw p-values are reported in corrPairsMSI output without Bonferroni correction for user-conducted analysis. _[grounded: TOOL_CORRPAIRSMSI]_
- **(finding)** The pointsAdducts function annotates the original mass spectrum using a massdiff object to mark peaks in different colors. _[grounded: COMP_MASSDIFF_OBJ]_
- **(finding)** Some adduct ions may themselves be parents of further adducts. _[grounded: COMP_ADDUCTS_DATASET]_

**Speculative claims (excluded from scoring):**
- **(finding)** Common chemical transformations are more often encountered than background noise in mass difference distributions.
- **(finding)** Interesting transformations or adducts will appear as peaks in a histogram of mass difference values. _[grounded: COMP_ADDUCTS_DATASET]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Pearson correlation test
- parallel processing

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Cardinal version 2.2+ is required
- Custom adduct tables must follow the same format with three columns: name, formula, mass

## Steps

### Step `task_001`
- Title: Reproduce adduct identification and ranking from built-in mass spectrometry imaging datasets
- Task kind: `reproduction`
- Task: Execute the full mass2adduct analysis pipeline on preprocessed MSI data: compute pairwise mass differences, generate a mass difference histogram, annotate known adducts using the built-in adducts/adducts2 reference datasets, and produce a ranked table of top mass differences with adduct matches. Output the annotated massdiff object and ranked adducts summary table.
- Inputs:
  - Preprocessed MSI data matrix in CSV format with m/z values as column headers and pixel intensities as entries
  - Built-in adducts reference dataset listing biologically-relevant chemical species (name, formula, mass columns)
- Expected outputs:
  - Mass difference histogram object (massdiffhist class) showing distribution of pairwise m/z differences with labeled peaks for known adducts
  - Table of top-ranked mass differences with occurrence counts, quantiles, and matches to known adducts from adductMatch() output
  - Annotated massdiff object with added 'matches' column indicating closest-matching adduct for each ion pair
- Tools: mass2adduct, R
- Landmark output files: massdiff_object.rds, massdiff_histogram.png, adductMatch_results.csv
- Primary expected artifact: `topAdducts_ranked_table.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct corrPairsMSI() correlation filtering step on msi.csv input
- Task kind: `component_reconstruction`
- Task: Load the example msi.csv file from the mass2adduct package into an msimat object, annotate pairwise mass differences with known adducts, and apply corrPairsMSI() to compute Pearson correlations between parent and adduct ion pairs with Bonferroni multiple-testing correction. Output the annotated massdiff data frame with correlation coefficient, p-value, and corrected significance fields.
- Inputs:
  - Example MSI data matrix (msi.csv) with m/z values as column names, pixels as rows, and intensity values as entries
  - Built-in adducts reference dataset (adducts2) listing chemical species names, formulas, and mass values
- Expected outputs:
  - Annotated massdiff data frame with columns A (parent ion m/z), B (adduct ion m/z), diff (mass difference), matches (adduct name), Estimate (Pearson correlation coefficient), P.value (uncorrected), and Significance (Bonferroni-corrected boolean)
- Tools: mass2adduct, R
- Landmark output files: msi_data.rds, massdiff_pairs.csv, adduct_annotated_pairs.csv
- Primary expected artifact: `annotated_corr_massdiff.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Analyze adduct-parent ion spatial overlap using pointsAdducts() on Na adduct annotations
- Task kind: `analysis`
- Task: Generate a scatter plot annotation of the mass spectrum highlighting sodium adduct ions (red points) and their parent ions (blue outlines) from a correlation-filtered, adduct-matched massdiff object, showing the red/blue overlap pattern where some adduct ions serve as parents for further adducts.
- Inputs:
  - msimat object: preprocessed MSI data matrix with intensity values for each mass peak across all pixels
  - massdiff object annotated with adductMatch() and filtered by corrPairsMSI() for spatial correlation significance
  - correlation-tested massdiff object with Estimate, P.value, and Significance columns from corrPairsMSI()
- Expected outputs:
  - Annotated mass spectrum plot with parent ions marked as blue circle outlines and adduct ions marked as red filled points, showing overlap indicating ions with dual roles
- Tools: mass2adduct, R
- Landmark output files: massdiff_object_subset.csv, sodium_adduct_parent_child_pairs.csv
- Primary expected artifact: `sodium_adduct_annotated_spectrum.png`

### Step `task_004`
- Depends on: `task_001`
- Title: Extend mass2adduct workflow to Cardinal-exported MSI data using cardinal2msimat()
- Task kind: `extension`
- Task: Convert a Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment object to mass2adduct's msimat format using cardinal2msimat(), then apply the massdiff() and adductMatch() pipeline to identify and annotate molecular adducts in MSI data. Output an annotated mass difference table with adduct matches.
- Inputs:
  - Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment object (in-memory R object or saved .rds file)
  - Reference adduct dataset (built-in: adducts or adducts2; or user-supplied data.frame with columns: name, formula, mass)
- Expected outputs:
  - Annotated massdiff object (data.frame with columns A, B, diff, and matches) containing ion pairs matched to known adducts
- Tools: Cardinal, mass2adduct, R
- Landmark output files: msimat_object.rds, massdiff_table.csv, annotated_massdiff.csv
- Primary expected artifact: `annotated_massdiff.csv`

## Final expected outputs

- `Annotated mass spectrum plot with parent ions marked as blue circle outlines and adduct ions marked as red filled points, showing overlap indicating ions with dual roles` (type: file, tolerance: hash)
- `Annotated massdiff object (data.frame with columns A, B, diff, and matches) containing ion pairs matched to known adducts` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** implicit

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_mass2adduct_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Annotated mass spectrum plot with parent ions marked as blue circle outlines and adduct ions marked as red filled points, showing overlap indicating ions with dual roles": "<locator>",
    "Annotated massdiff object (data.frame with columns A, B, diff, and matches) containing ion pairs matched to known adducts": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
