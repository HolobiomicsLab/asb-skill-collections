# Workflow Challenge: `coll_falcon_workflow`


> falcon is an open-source spectrum clustering tool that processes millions of MS/MS spectra through feature hashing, nearest neighbor indexing, and density-based clustering. The tool requires Python 3.8+ and is available on Linux and OSX platforms via pip installation.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

falcon implements a four-stage pipeline for large-scale tandem mass spectrum clustering. The pipeline begins by binning high-resolution spectra and converting them to low-dimensional vectors using feature hashing. Spectrum vectors then serve as input for constructing nearest neighbor indexes, which enable efficient computation of sparse pairwise distance matrices without exhaustively comparing all spectra to each other. The nearest neighbor indexes are queried to compute the sparse pairwise distance matrix, avoiding the computational burden of all-pairs comparison. Finally, density-based clustering is applied as the terminal step to group similar spectra into clusters using the sparse pairwise distance matrix as input. The software is distributed as open-source under the BSD license and can be installed via pip alongside spectrum-utils==0.3.5, with support for Python 3.8+ on Linux and OSX platforms.

## Research questions

- How are high-resolution MS/MS spectra transformed into low-dimensional vector representations suitable for nearest neighbor indexing?
- How are low-dimensional spectrum vectors used to construct nearest neighbor indexes for fast similarity searching in falcon?
- How do nearest neighbor indexes enable efficient computation of a sparse pairwise distance matrix for spectrum clustering without exhaustive all-versus-all comparison?
- How does density-based clustering use a sparse pairwise distance matrix to group similar spectra into clusters?
- Can falcon-ms be successfully installed and executed end-to-end on the reference dataset from Bittremieux et al. 2021 without errors?

## Methods overview

Load high-resolution MS/MS spectra from standard mass spectrometry file formats. Discretize m/z values into uniform bins and aggregate intensities within each bin. Normalize binned intensity vectors (e.g., by total ion current or L2-norm). Apply feature hashing to map binned vectors to fixed-size low-dimensional representations. Validation: Confirm output is a dense or sparse matrix with one row per input spectrum and consistent vector dimensionality across all spectra. References: source article (DOI: 10.1002/rcm.9153) Load hashed spectrum feature vectors from upstream feature hashing stage Construct nearest neighbor index structure using input vectors Serialize and write index to persistent storage for downstream use Validation: index file exists and is deserializable; index supports efficient neighbor query operations required for sparse distance matrix construction References: source article (DOI: 10.1002/rcm.9153) Load spectrum vectors and nearest neighbor indexes from prior indexing stage. Query each spectrum vector against nearest neighbor indexes to retrieve candidate matches within distance threshold. Compute pairwise distances only between each spectrum and retrieved candidates. Assemble distances into sparse matrix representation for memory efficiency. Validation: Verify sparse matrix row and column dimensions match spectrum count; confirm sparsity (non-zero entry ratio) is substantially lower than dense all-versus-all matrix. References: source article (DOI: 10.1002/rcm.9153) Load sparse pairwise distance matrix from nearest neighbor index output Apply density-based clustering algorithm to partition spectra based on distance relationships Assign unique cluster labels to each spectrum and organize assignments in a tabular structure Validation: Verify cluster assignments are complete (all spectra assigned), cluster labels are consistent, and output file format is parseable References: source article (DOI: 10.1002/rcm.9153) Install falcon-ms and spectrum-utils==0.3.5 dependencies via pip on Python 3.8+ Locate or retrieve the public tandem MS/MS spectrum dataset associated with Bittremieux et al. 2021 Execute falcon command-line tool to cluster spectra via feature hashing, nearest neighbor indexing, and density-based clustering Validation: Verify tool execution completes without error and output cluster assignment file is non-empty and contains valid cluster identifiers References: source article (DOI: 10.1002/rcm.9153)

**Domain:** bioinformatics

**Techniques:** clustering, tandem-ms, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The falcon spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra. _[grounded: falcon_system]_
- **(finding)** High-resolution spectra are binned and converted to low-dimensional vectors using feature hashing.
- **(finding)** Spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching.
- **(finding)** Nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without exhaustively comparing all spectra.
- **(finding)** Density-based clustering is performed to group similar spectra into clusters.
- **(finding)** The falcon software is available as open-source under the BSD license. _[grounded: falcon_system]_
- **(finding)** falcon requires Python 3.8+ and is available on the Linux and OSX platforms. _[grounded: falcon_system]_
- **(finding)** falcon can be installed via pip with the command: pip install falcon-ms spectrum-utils==0.3.5 _[grounded: falcon_system]_
- **(finding)** The primary citation for falcon is Bittremieux et al. (2021) in Rapid Communications in Mass Spectrometry. _[grounded: falcon_system]_

## Steps

### Step `task_001`
- Title: Reconstruct the Spectrum Binning and Feature Hashing Layer of the falcon pipeline
- Task kind: `component_reconstruction`
- Task: Implement the feature-hashing binning stage of falcon: convert high-resolution MS/MS spectra into low-dimensional hashed feature vectors. Output a matrix of hashed spectrum vectors suitable for nearest-neighbor indexing.
- Inputs:
  - High-resolution MS/MS spectra in mzML, mzXML, or MGF format
- Expected outputs:
  - Matrix of low-dimensional hashed feature vectors (one vector per spectrum)
- Tools: falcon, spectrum-utils==0.3.5, Python 3.8+
- Landmark output files: binned_spectra.csv, hashed_feature_vectors.npz
- Primary expected artifact: `hashed_feature_vectors.npz`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the Nearest Neighbor Index Construction Layer of the falcon pipeline
- Task kind: `component_reconstruction`
- Task: Construct serialized nearest neighbor index structures from hashed spectrum feature vectors to enable fast similarity searching in spectrum clustering. Output the index as a binary or structured file suitable for downstream distance matrix computation.
- Inputs:
  - hashed spectrum feature vectors from upstream feature hashing stage
- Expected outputs:
  - serialized nearest neighbor index structure
- Tools: falcon, Python 3.8+
- Primary expected artifact: `nn_index.pkl`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the Sparse Pairwise Distance Matrix Computation Layer of the falcon pipeline
- Task kind: `component_reconstruction`
- Task: Query nearest neighbor indexes constructed from spectrum vectors to compute a sparse pairwise distance matrix for millions of MS/MS spectra without exhaustive all-versus-all comparison.
- Inputs:
  - Spectrum vectors in low-dimensional representation (output from feature hashing stage)
  - Constructed nearest neighbor indexes
- Expected outputs:
  - Sparse pairwise distance matrix
- Tools: falcon, Python 3.8+
- Landmark output files: query_candidates.csv, sparse_distance_matrix.npz
- Primary expected artifact: `sparse_distance_matrix.npz`

### Step `task_004`
- Depends on: `task_003`
- Title: Reconstruct the Density-Based Clustering Layer of the falcon pipeline
- Task kind: `component_reconstruction`
- Task: Perform density-based clustering on a sparse pairwise distance matrix of MS/MS spectra to assign each spectrum to a cluster. Output a cluster assignment file mapping spectrum identifiers to cluster labels.
- Inputs:
  - Sparse pairwise distance matrix from nearest neighbor index construction
- Expected outputs:
  - Cluster assignment file mapping spectrum identifiers to cluster labels
- Tools: falcon, Python 3.8+, spectrum-utils==0.3.5
- Landmark output files: distance_matrix_loaded.npy, cluster_parameters_optimized.json, cluster_assignments.csv
- Primary expected artifact: `cluster_assignments.csv`

### Step `task_005`
- Title: Reproduce the end-to-end falcon clustering run on the Bittremieux et al. 2021 dataset
- Task kind: `reproduction`
- Task: Install falcon-ms and spectrum-utils==0.3.5, then execute the falcon command-line tool on the Bittremieux et al. 2021 public dataset to produce cluster assignments. Verify successful execution and non-empty output.
- Inputs:
  - Public tandem MS/MS spectrum dataset associated with Bittremieux et al. 2021 (doi:10.1002/rcm.9153)
- Expected outputs:
  - Cluster assignment output file produced by falcon command-line tool
- Tools: falcon, spectrum-utils==0.3.5, Python 3.8+
- Landmark output files: installation_log.txt, falcon_execution_log.txt
- Primary expected artifact: `cluster_assignments.txt`

## Final expected outputs

- `serialized nearest neighbor index structure` (type: file, tolerance: hash)
- `Cluster assignment file mapping spectrum identifiers to cluster labels` (type: file, tolerance: hash)
- `Cluster assignment output file produced by falcon command-line tool` (type: file, tolerance: hash)

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

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_falcon_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
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
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "serialized nearest neighbor index structure": "<locator>",
    "Cluster assignment file mapping spectrum identifiers to cluster labels": "<locator>",
    "Cluster assignment output file produced by falcon command-line tool": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
