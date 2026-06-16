# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does the logbin_expected function in cooltools perform log-binning and smoothing on a precomputed expected contact frequency table to produce a log-binned contact probability P(s) curve?: 'New functionality for smoothing P(s) and derivatives (API is not yet stable)'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Cooltools includes new functionality for smoothing P(s) and its derivatives, though the API for this smoothing mechanism is not yet stable.: 'New functionality for smoothing P(s) and derivatives (API is not yet stable)'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Precomputed expected_cis table in TSV or CSV format with columns: dist_bp, contact_frequency, n_valid (from cooler file): 'output cvd table now also includes "dist_bp", "contact_frequency", and "n_valid" columns'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Log-binned and smoothed contact probability P(s) curve as TSV file with columns: dist_bp_bin, count_avg_smoothed, and bin_count: 'now returns "count.avg.smoothed" and "count.avg.smoothed.agg", when `clr_weight_name=None, smooth=True, aggregate_smoothed=True`'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'enabling high-resolution Hi-C analysis in Python'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] cooler: 'The recently-introduced cooler format readily handles storage of high-resolution datasets'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The exact function signature, parameter names, and default values for logbin_expected are not specified in the discussion text: 'New functionality for smoothing P(s) and derivatives (API is not yet stable): `logbin_expected`, `interpolate_expected`'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No reference implementation, worked example, or integration test for logbin_expected is cited in the discussion text: 'New functionality for smoothing P(s) and derivatives (API is not yet stable)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Whether logbin_expected is intended to operate on cis-only or cis+trans contact probabilities is not stated: 'New functionality for smoothing P(s) and derivatives (API is not yet stable): `logbin_expected`, `interpolate_expected`'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The release version in which logbin_expected became available is not specified; it is mentioned only in the unreleased development notes section: 'New functionality for smoothing P(s) and derivatives (API is not yet stable): `logbin_expected`, `interpolate_expected`'
