# Evaluation Strategy

## Direct Checks

- verify file_exists: mzmine repository root at github:mzmine__mzmine contains a modules/ or src/ directory listing all module implementations
- verify file_format_is: module inventory (generated or extracted from source tree) is a structured table or JSON file mapping module name to supported data types (LC, GC, IMS, MS Imaging)
- verify contains_substring: module inventory explicitly lists at least one module for each of LC, GC, IMS, and MS Imaging (e.g., 'LC' or 'liquid chromatography', 'GC' or 'gas chromatography', 'IMS' or 'ion mobility', 'imaging' or 'MALDI')
- verify script_runs: automated audit script (e.g., Java reflection, AST parser, or build manifest parser) executes without error on mzmine source tree and produces complete module enumeration
- verify output_matches_reference: enumerated module set is byte-for-byte consistent with official mzmine documentation (README, manual, or API docs) module inventory, if published

## Expert Review

- confirm that each of the four separation/ionisation types (LC, GC, IMS, MS Imaging) is genuinely supported by at least one distinct processing module (not merely claimed in prose; module must have active implementation)
- assess whether the enumerated modules collectively cover the 'entire MS data analysis workflow' (data import, preprocessing, feature detection, alignment, annotation, export) or if critical stages are missing
- determine whether any separation/ionisation type is covered only by a single module (architectural fragility) or has redundant/complementary implementations
