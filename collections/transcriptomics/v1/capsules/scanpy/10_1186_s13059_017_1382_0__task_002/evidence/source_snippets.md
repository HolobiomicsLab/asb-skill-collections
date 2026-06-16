# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?: 'Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Scanpy includes preprocessing capabilities as part of its toolkit for single-cell gene expression analysis, designed to work with the anndata data structure.: 'It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] AnnData object with Dask-backed expression matrix (dask.array.Array in adata.X): '⚡ indicates support of the type as chunk in a dask {class}`~dask.array.Array`'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Scanpy source code and API reference (pp module functions): 'Filtering of highly-variable genes, batch-effect correction, per-cell normalization, preprocessing recipes.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] AnnData object with processed expression data, retaining Dask-backed or sparse structure without full materialization: 'Any transformation of the data matrix that is not a *tool*.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Verification report confirming obs/var structure integrity and memory efficiency: 'Different APIs have different levels of support for array types, and this page lists the supported array types for each function'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Scanpy: 'Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] anndata: 'built jointly with anndata'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Python: 'type annotations on function parameters'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] pytest: 'We use pytest to test scanpy. To run the tests, simply run `hatch test`'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Hatch: 'Using one of the predefined environments in hatch.toml is as simple as running `hatch test`'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: '_No changelog found._'
