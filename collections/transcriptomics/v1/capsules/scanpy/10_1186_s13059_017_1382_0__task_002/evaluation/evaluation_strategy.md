# Evaluation Strategy

## Direct Checks

- verify that scanpy source code repository (github:scverse/scanpy) is accessible and contains pp module functions
- verify that dask_support documentation or implementation exists in the scanpy codebase
- script_runs: execute a Python script that imports scanpy, creates a Dask-backed AnnData object, calls at least one pp module function (e.g., pp.normalize_total or pp.pca), and completes without raising an exception
- verify returned object is a valid AnnData instance with obs and var DataFrames populated
- verify that the operation does not trigger full matrix materialization into memory by checking Dask task graph remains unevaluated (robust to parameter choices in function calls)

## Expert Review

- confirm that the Dask task graph remains lazy (unevaluated) after the pp module operation, indicating no eager loading of the full matrix occurred
- assess whether the obs/var structure is preserved correctly and matches expectations for the specific pp function called
