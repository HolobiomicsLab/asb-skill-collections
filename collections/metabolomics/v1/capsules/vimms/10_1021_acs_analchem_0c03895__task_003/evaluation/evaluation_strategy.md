# Evaluation Strategy

## Direct Checks

- verify that github:glasgowcompbio__vimms repository can be cloned and contains the vimms package with Chemicals, IndependentMassSpectrometer, Controller, and Environment classes
- verify file_exists: vimms package exports Chemicals, IndependentMassSpectrometer, Controller, and Environment from canonical import paths
- script_runs: instantiate a Chemicals object with a formula sampler (e.g., UniformMZFormulaSampler with min_mz=100, max_mz=600) and sample 100 chemicals with ms_levels=2, robust to parameter choices for chemical count and m/z bounds
- script_runs: instantiate IndependentMassSpectrometer with polarity='positive' and sampled chemicals object without error
- script_runs: instantiate a TopNController (or equivalent fixed controller) with polarity='positive' and N=5, isolation_width=1.0 without error
- script_runs: instantiate Environment with IndependentMassSpectrometer, Controller, min_time=0, max_time=1200, call env.run() without error
- output_matches_reference: Environment.run() produces a scan list (verify scan list is non-empty and contains at least one scan object with attributes matching the expected architecture: MS level, m/z values, intensity values, retention time)
- verify file_format_is: Environment provides write_mzML() method to export generated scans to mzML format, multiple defensible approaches for mzML schema validation

## Expert Review

- verify that the three-stage orchestration (Chemicals → IndependentMassSpectrometer → Controller → Environment) correctly implements the intended fixed control loop architecture and that the scan list reflects appropriate fragmentation strategy behavior
- verify that the scan list output is consistent with the TopNController strategy (e.g., MS1 scans followed by MS2 scans targeting top N peaks) and reflects correct ionization polarity
