# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does asari's computational performance (wall-clock time and peak memory usage) scale with increasing numbers of LC-MS samples?: 'Scalable, performance conscious, disciplined use of memory and CPU'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources.: 'Scalable, performance conscious, disciplined use of memory and CPU'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Public mzML files (minimum 100+ files) from MetaboLights or MassIVE repositories in centroided format: 'Input data are centroied mzML files from LC-MS metabolomics.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] asari software installed from PyPI or cloned from source (v1.10+): 'From PyPi repository: `pip3 install asari-metabolomics`. Add `--upgrade` to update to new versions.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] System profiling tools capable of capturing wall-clock runtime and peak memory usage: 'Asari is designed to run > 1000 samples on a laptop computer.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Scalability benchmark table (CSV or TSV) with columns: sample_count, wall_clock_time_seconds, peak_memory_mb, run_number, mean_time, std_dev_time, mean_memory, std_dev_memory: 'Asari is designed to run > 1000 samples on a laptop computer. The performance is achieved via ... Main intensity values of each sample are not kept in memory.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Wall-clock time vs. sample count plot (PNG or PDF) showing linear or near-linear scaling up to 100+ samples: 'Asari is designed to run > 1000 samples on a laptop computer.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Peak memory usage vs. sample count plot (PNG or PDF) demonstrating memory efficiency across cohort sizes: 'Main intensity values of each sample are not kept in memory.'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Summary report (text or markdown) stating mean throughput (samples/hour) per cohort and extrapolated time estimate for 1000-sample project: 'Asari is designed to run > 1000 samples on a laptop computer.'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] asari: 'Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Requires Python 3.8+.'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pymzml: 'The default method uses `pymzml` to parse mzML files.'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, performance improvements, or scalability-related fixes: '_No changelog found._'
