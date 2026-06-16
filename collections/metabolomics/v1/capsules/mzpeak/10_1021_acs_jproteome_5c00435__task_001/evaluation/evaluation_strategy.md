# Evaluation Strategy

## Direct Checks

- verify file exists at github:mobiusklein__mzpeak_prototyping repository root
- verify Rust build succeeds: `cargo build --release` or equivalent command runs without error
- verify command-line converter tool executable is produced after build
- verify converter accepts at least one supported input format (e.g., mzML file) as a command-line argument
- verify converter produces an output file with .mzpeak or expected mzPeak file extension
- file_format_is: output file conforms to mzPeak specification structure (multiple language implementations can read it, or byte structure matches specification)
- output_matches_reference: converted file can be read back by the Rust library without error

## Expert Review

- expert review: assess whether the output mzPeak file preserves semantic integrity and mass spectrometry metadata fidelity from the input format (e.g., m/z values, intensities, scan structure are accurately represented)
- expert review: confirm that at least one supported input format is documented or determinable from the repository structure (e.g., mzML, mzXML, or other proteomics format)
