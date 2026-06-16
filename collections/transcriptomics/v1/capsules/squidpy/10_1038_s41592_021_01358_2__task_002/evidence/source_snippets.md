# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does the PynndescentKNNBuilder class implement graph construction by subclassing GraphBuilderCSR and integrating pynndescent as its nearest-neighbor backend?: 'Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics that enable scalable analysis of spatial molecular data.: 'It builds on scanpy and anndata, providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Spatial coordinates as a numpy array of shape (n_obs, n_dims): 'Build it like any other builder: import squidpy as sq; sq.gr.spatial_neighbors_from_builder(adata, PynndescentKNNBuilder(n_neighs=6))'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] CSR sparse adjacency matrix (adj) of shape (n_obs, n_obs) with float32 dtype and binary indicator values: 'adj = csr_matrix((np.ones_like(row_indices, dtype=np.float32), (row_indices, col_indices)), shape=(n_obs, n_obs))'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] CSR sparse distance matrix (dst) of shape (n_obs, n_obs) with float64 dtype containing pairwise Euclidean distances: 'dst = csr_matrix((dists, (row_indices, col_indices)), shape=(n_obs, n_obs))'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Validation report confirming matrix shape, sparsity consistency, diagonal correctness, and CSR format validity: 'adj.setdiag(1.0 if self.set_diag else adj.diagonal()); dst.setdiag(0.0)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] pynndescent: 'The [pynndescent](https://github.com/lmcinnes/pynndescent) library provides an approximate nearest-neighbor search backend'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] scipy.sparse: 'csr_matrix objects and should reuse Squidpy's CSR-specific postprocessors'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] numpy: 'np.repeat(np.arange(n_obs), self.n_neighs); np.ones_like(row_indices, dtype=np.float32)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'Spatial Single Cell Analysis in Python'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] pytest: 'This package uses [pytest][] for automated testing.'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting implementation details, API signatures, or expected behavior of PynndescentKNNBuilder: '_No changelog found._'
