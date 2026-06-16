# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does performing peak detection on a single composite map rather than on individual samples improve computational efficiency in metabolomics data processing?: 'Peak detection on a composite map instead of repeated on individual samples'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Asari implements peak detection using scipy.signal.find_peaks on a composite map constructed from summed mass tracks across all samples, reducing the number of peak-detection algorithm calls from N (one per sample) to one (composite), thereby improving scalability and computational efficiency.: 'Peak detection on a composite map instead of repeated on individual samples'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Aligned mass tracks per sample with m/z and full-length intensity arrays: 'intensity_track is np.array(full RT length). This increases storage for processed samples, but simplifies i) CMAP construction'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Retention time calibration dictionaries (rt_cal_dict) mapping sample scan numbers to reference coordinates: 'The RT alignment dictionaries only keep differing values and set within sample RT boundaries. This is efficient by ignoring unnecessary tracking'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mass grid structure with aligned m/z values across all samples: 'Aignment of mass tracks across samples, resulting in the MassGrid'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Composite mass tracks (summed intensity arrays) indexed by consensus m/z and full RT scan length: 'composite mass tracks, where the intensity values are summed on corresponding mass tracks across all samples after RT calibration'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Feature list with detected elution peaks on composite tracks: peak apex (scan), peak area, height, baseline boundaries, cSelectivity, SNR, goodness_fitting, and parent_masstrack_id: 'The peaks passing the thresholds (default SNR > 2 and peakshape > 0.5) are reported in a JSON format, with link to the composite mass track identifier'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Execution log confirming single peak-detection pass on composite map vs. N per-sample passes: 'Peak detection on a composite map instead of repeated on individual samples'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Trackable and scalable Python program for high-resolution metabolomics data processing.'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy.signal.find_peaks: 'Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy.signal.detrend: 'detrend (scipy.signal.detrend) is performed on the mass track'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: '_No changelog found._'
