---
name: statistical-result-reproduction
description: Use when you have downloaded a Jupyter notebook from a published metabolomics workflow repository (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_2269
  tools:
  - R
  - Jupyter Notebook
  - MZmine3
  - Google Colab
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41596-024-01046-3
  title: FBMN-STATS
evidence_spans:
- To easily install and run Jupyter Notebook in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  dedup_kept_from: coll_fbmn_stats_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-024-01046-3
  all_source_dois:
  - 10.1038/s41596-024-01046-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-result-reproduction

## Summary

Reproduce multivariate statistical analysis results from published Jupyter notebooks on non-targeted LC-MS/MS metabolomics data to validate workflow correctness and ensure output consistency with reference files. This skill verifies that a complete analysis pipeline—including data merging, cleanup, blank removal, batch correction, and univariate/multivariate statistical analyses—executes without error and generates expected outputs.

## When to use

You have downloaded a Jupyter notebook from a published metabolomics workflow repository (e.g., FBMN-STATS), obtained the corresponding test dataset from MassIVE (MSV000082312 or MSV000085786), and need to confirm the notebook runs end-to-end on your local environment before adapting it to your own non-targeted LC-MS/MS data. Reproduction is essential when validating a new statistical pipeline or troubleshooting environment-specific dependencies.

## When NOT to use

- Your test data is already a processed/normalized feature table and you need only to apply univariate tests—use this skill only if you need to validate the complete pipeline including preprocessing steps (merging, cleanup, blank removal, batch correction).
- You are working with targeted metabolomics data or with already-published, frozen result sets that do not require re-execution—reproduction is for validating dynamic, executable notebooks.
- Your analysis environment lacks R or Jupyter Notebook dependencies and installation is not feasible—reproduction cannot succeed without the declared runtime environment.

## Inputs

- Jupyter notebook (.ipynb) containing R or Python statistical analysis code
- Non-targeted LC-MS/MS feature table (CSV or TSV format from MZmine3)
- Sample metadata file (CSV or TSV with sample IDs and treatment groups)
- Test dataset from MassIVE (MSV000082312 or MSV000085786)

## Outputs

- Batch-corrected feature matrix (CSV/TSV)
- Univariate statistical results (p-values, fold-changes, q-values)
- Multivariate analysis outputs (PCA scores, loadings; OPLS-DA models; heatmaps)
- Quality control plots (PCA score plots, heatmaps, volcano plots)
- Log file or console output documenting execution status

## How to apply

Clone the Functional-Metabolomics-Lab/FBMN-STATS repository and download the specified test dataset (MSV000082312 or MSV000085786) from MassIVE. Install R and Jupyter Notebook with all declared dependencies according to the repository's OS-specific installation guides. Open the multivariate statistical analysis notebook in Jupyter and execute all cells sequentially, ensuring no errors occur at any step. After execution completes, verify that all expected output files (result tables, plots, batch-corrected matrices) are generated in the working directory. Compare the generated outputs against the reference result files stored in the associated Google Drive folder using file checksums or manual inspection of key numerical columns (e.g., p-values, fold-change estimates, principal component scores) to confirm bit-for-bit or numerical equivalence within expected floating-point precision.

## Related tools

- **Jupyter Notebook** (Interactive environment for executing multivariate statistical analysis workflows in R or Python) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **R** (Statistical computing language used to implement data merging, cleanup, batch correction, and multivariate analyses (PCA, OPLS-DA)) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **MZmine3** (Used upstream to generate the feature tables and metadata that serve as inputs to the statistical notebooks)
- **Google Colab** (Alternative cloud-based runtime environment for executing the R or Python notebooks without local installation) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Evaluation signals

- All notebook cells execute without errors or warnings; no exceptions thrown during data merging, cleanup, blank removal, batch correction, or statistical analysis steps.
- Expected output files are present in the working directory (batch-corrected feature matrix, univariate results, PCA/OPLS-DA models, plots) with non-empty content.
- Key numerical columns (p-values, adjusted p-values, fold-changes, PC1/PC2 scores) in generated outputs match reference files in the Google Drive folder within acceptable floating-point tolerance (e.g., ±1e-6 relative error).
- Quality control plots (PCA score plots, heatmaps) are generated and visually consistent with published figures and reference plots in the Google Drive.
- Working directory is properly set and all intermediate and final outputs are saved to the designated location; file timestamps confirm recent execution.

## Limitations

- GitHub rendering of Jupyter notebooks may be incomplete due to file size or complex outputs; for full code visibility, download and open locally or use provided Google Colab links.
- Google Colab runtimes disconnect after 90 minutes of idleness or 12 hours of continuous use, requiring re-execution of the entire notebook; disk space is limited to 77 GB per user, which may constrain larger datasets.
- Code transfer from GitHub to other environments (RStudio, text editors) may lose formatting or HTML content; use the Google Colab or local Jupyter version to ensure accurate copying.
- Previous GNPS Quickstart output does not generate the reformatted feature tables required by these notebooks, leading to incorrect input schema; users must use GNPS 2 or compatible preprocessing tools.
- Package installation in Colab must occur every notebook session (unlike local Jupyter, where packages install once), extending execution time.

## Evidence

- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data: "Using the notebooks provided here, one can perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] Open and execute the multivariate statistical analysis notebook, ensuring all cells run without errors.: "Open and execute the multivariate statistical analysis notebook in Jupyter, ensuring all cells run without errors."
- [other] Verify that all expected output files are generated and match the reported results stored in the project Google Drive.: "Verify that all expected output files are generated and match the reported results stored in the project Google Drive."
- [readme] The result files of the notebook can be found in the Google Drive: "The result files of the notebook can be found in the Google Drive: - [Google Drive Link for the files](https://drive.google.com/drive/folders/1qHAdvDGr9Kre0SK3AMc1Dzfu6XeFE48A?usp=sharing)"
- [readme] MASSIVE Datasets from which all the files were selected for MZmine3: MSV000082312 and MSV000085786: "MASSIVE Datasets from which all the files were selected for MZmine3: [MSV000082312](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=8a8139d9248b43e0b0fda17495387756) and [MSV000085786]"
- [readme] To easily install and run Jupyter Notebook in R, follow the steps in the document according to your preferred OS: "To easily install and run Jupyter Notebook in R, [follow the steps in the document according to your preferred OS](https://github.com/Functional-Metabolomics-Lab/FBMN-STATS/tree/main/Jupyter-Notebook-"
- [readme] GitHub might not display Jupyter notebooks correctly due to file size or complex outputs. Download the notebook and open it with Jupyter Notebook/JupyterLab: "GitHub might not display Jupyter notebooks correctly due to file size or complex outputs. For a complete view, download the notebook and open it with Jupyter Notebook/JupyterLab"
- [readme] The main problem with the Colab environment is when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect.: "Although Colab is easier to use and is all Cloud-based, the main problem with the Colab environment is when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the"
