# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does asari determine which mass alignment algorithm to apply based on study size?: 'Taking advantage of high mass resolution to prioritize mass separation and alignment'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional algorithm selection.: 'Scalable, performance conscious, disciplined use of memory and CPU'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mass track data from all samples, each containing m/z and full-RT-range intensity arrays: 'Build mass tracks per data bin. If the m/z range in a data bin is within 2 x tolerance ppm, the bin leads to a single mass track.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Anchor mass track pairs (isotopic or adduct differences) per sample for confidence-based alignment: 'Establish anchor mass tracks by finding m/z differences that match to either 13C/12C isotopes or Na/H adducts.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Sample count and user-specified reference sample identifier (if provided): 'The sample with the highest number of anchor mass tracks is designated as the reference sample, unless a user specifies a reference sample via input parameters.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] _mass_grid_mapping.csv file documenting aligned m/z values, sample-track associations, and consensus m/z per grid position: 'MassGrid is exported as a csv file.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MassGrid object linking aligned mass tracks across all samples with consensus m/z identifiers: 'Aignment of mass tracks across samples, resulting in the MassGrid'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Requires Python 3.8+.'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] asari mass_functions module (nn_cluster_by_mz_seeds): 'a nearest neighbor (NN) clustering is performed to establish the number of mass tracks. See [mass_functions.nn_cluster_by_mz_seeds](mass_functions.nn_cluster_by_mz_seeds).'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs): 'See [MassGrid.build_grid_sample_wise](MassGrid.build_grid_sample_wise), [MassGrid.add_sample](MassGrid.add_sample). See [MassGrid.build_grid_by_centroiding](MassGrid.build_grid_by_centroiding),'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog provided: '_No changelog found._'
