# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does squidpy.gr.spatial_neighbors correctly construct and store a CSR graph in an AnnData object with expected keys and structure when applied to a bundled example dataset?: 'Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data. It builds on scanpy and anndata, providing streamlined APIs for feature extraction, spatial statistics'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure.: 'providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] squidpy installation (from PyPI, conda, or git) and Python >= 3.11 environment: 'Squidpy requires Python version >= 3.11 to run. Install Squidpy by running:: pip install squidpy'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Bundled example dataset (e.g., squidpy.datasets.visium or squidpy.datasets.imc): 'datasets.visium, datasets.imc'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] AnnData object with spatial graph stored in obsp as CSR matrices with keys 'spatial_neighbors' (adjacency) and 'spatial_distances' (distance matrix): 'adj and dst are square sparse matrices of shape (n_obs, n_obs) with matching sparsity structure'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Verification report confirming correct matrix shape, sparsity, dtype, and diagonal properties: 'dst should have a zero diagonal, and adj should only have a non-zero diagonal when set_diag=True'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Squidpy: 'Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] scanpy: 'It builds on scanpy and anndata'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] anndata: 'It builds on scanpy and anndata'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'Spatial Single Cell Analysis in Python'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] pip: 'pip install squidpy'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, API changes, or deprecations found: '_No changelog found._'
