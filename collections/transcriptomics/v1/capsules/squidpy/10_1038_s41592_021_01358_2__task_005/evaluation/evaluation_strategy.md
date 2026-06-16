# Evaluation Strategy

## Direct Checks

- verify file exists: squidpy/im/_container.py (ImageContainer implementation)
- verify file exists: squidpy/im/_features.py (calculate_image_features implementation)
- script_runs: load a test spatially resolved dataset with tissue image using squidpy.im.ImageContainer without errors
- script_runs: execute im.calculate_image_features with dask lazy computation enabled (e.g., passing compute=False or equivalent parameter) without errors
- verify output_matches_reference: intermediate computation objects before collection are dask arrays (type check: dask.array.Array or dask.dataframe.DataFrame), robust to different dask versions
- verify output_matches_reference: final feature outputs after materialization are correctly integrated into AnnData.obs or AnnData.obsm as numpy arrays or DataFrames
- script_runs: verify AnnData object structure is valid after feature materialization (obsm/obs dimensions match n_obs)
- file_format_is: output AnnData object is HDF5-based (.h5ad) or zarr-backed, with no dask arrays remaining in final artifact

## Expert Review

- confirm that dask lazy evaluation semantics are correctly preserved during im.calculate_image_features pipeline (no premature materialization)
- confirm that feature values computed via dask lazy execution match those computed with eager evaluation (numerical accuracy and consistency)
- confirm that memory efficiency gains from lazy computation are realizable on a moderately sized tissue image dataset
