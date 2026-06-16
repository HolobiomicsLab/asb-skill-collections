# Evaluation Strategy

## Direct Checks

- verify that github:mzmine__mzmine repository is accessible and contains README or documentation files
- file_exists: locate README.md or similar documentation artifact in mzmine/mzmine repository
- contains_substring: README or primary documentation contains explicit description of conditional routing logic for LC, GC, IMS, and MS Imaging module selection
- contains_substring: documentation specifies the input data type parameter or field that triggers routing decisions
- contains_substring: documentation describes at least one complete if-then or case-based routing rule mapping input type to processing module

## Expert Review

- assess whether the documented routing logic is complete and covers all declared module types (LC, GC, IMS, MS Imaging)
- verify that the routing dispatch mechanism correctly distinguishes between supported chromatography and imaging modalities based on standard MS data formats or metadata fields
- confirm that the routing logic is actually implemented as described in the README by sampling relevant source code (e.g., factory classes, plugin loaders, or main entry point)
