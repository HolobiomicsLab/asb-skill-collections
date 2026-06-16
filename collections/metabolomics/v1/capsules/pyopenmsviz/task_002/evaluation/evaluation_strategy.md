# Evaluation Strategy

## Direct Checks

- file_exists: verify that the pyopenms_viz package source code is accessible at github.com/OpenMS/pyopenms_viz
- file_format_is: verify that Configuration Classes Layer files (.py format) exist in the repository structure
- file_format_is: verify that Core Base Layer files (.py format) exist in the repository structure
- file_format_is: verify that Extension Layer files for Bokeh, Matplotlib, and Plotly (.py format) each exist in the repository structure
- contains_substring: verify that source code contains a routing mechanism (function or method) that accepts a 'backend=' keyword argument
- contains_substring: verify that the routing mechanism dispatches to exactly three distinct backend implementations (Bokeh, Matplotlib, Plotly)
- script_runs: verify that a minimal instantiation script (backend= keyword call) executes without error when backend='bokeh', backend='matplotlib', and backend='plotly' are each specified
- output_matches_reference: verify that each backend call produces an object of the correct type (bokeh Figure, matplotlib Axes, plotly Figure), no canonical answer—any of three distinct backend-specific types is valid

## Expert Review

- Confirm that the identified routing mechanism correctly implements the advertised control flow from Configuration Classes Layer → Core Base Layer → one of three Extension Layers
- Assess whether the dispatcher logic is architecturally sound and follows recognized orchestrator patterns for pluggable backends
- Evaluate the completeness of the three backend implementations: do Bokeh, Matplotlib, and Plotly each receive all necessary data and parameters from the Core Base Layer?
