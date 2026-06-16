# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does the peak quality filtering mechanism using SNR (>2), peak shape goodness-of-fit, and minimum peak height (default 1e5 with >20% prominence) thresholds reduce the number of detected features in the feature table?: 'Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Asari applies peak quality filtering by tracking selectivity metrics on m/z, chromatography, and annotation databases to refine detected features after composite map peak detection.: 'Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Full unfiltered peak list from composite track peak detection (JSON format with SNR, goodness_fitting, peak_height, prominence, apex, left_base, right_base, parent_masstrack_id, mz, rtime fields): 'The peaks passing the thresholds (default SNR > 2 and peakshape > 0.5) are reported in a JSON format, with link to the composite mass track identifier.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Composite mass tracks with aligned intensity vectors across all samples after RT calibration: 'composite mass tracks, where the intensity values are summed on corresponding mass tracks across all samples after RT calibration.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RT alignment dictionaries (rt_cal_dict) mapping sample scan numbers to reference sample scan numbers: 'The retention time is converted from scan numbers to seconds. The features have peak positions and boundaries on the composite mass tracks, which are translated to positions on the individual'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Filtered feature table (preferred_Feature_table.tsv) containing only peaks meeting SNR > 2, peakshape > 0.5, and minimum peak height criteria with sample-specific peak areas: 'The recommended feature table is `preferred_Feature_table.tsv`. All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Row count comparison report showing number of peaks in full_Feature_table.tsv vs. preferred_Feature_table.tsv: 'All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people).'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] QC summary metrics including SNR distribution, peakshape distribution, and peak height distribution of retained peaks: 'The detected elution peaks are evaluated for peakshape, cSelectivity and SNR. The default filters are set low for these values, so that users can decide on their filtering on the feature table.'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy.signal.find_peaks: 'Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] asari peaks module: 'See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list), [peaks.__peaks_cSelectivity_stats_](peaks.__peaks_cSelectivity_stats_),'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history is documented: '_No changelog found._'
