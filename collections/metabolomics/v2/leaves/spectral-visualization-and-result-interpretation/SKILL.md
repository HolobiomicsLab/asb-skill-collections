---
name: spectral-visualization-and-result-interpretation
description: Use when after peak clustering, network filtering, and database matching
  have identified candidate metabolites and their associated peak networks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0593
  tools:
  - Python
  - PyINETA
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c03966
  title: PyINETA
evidence_spans:
- pyINETA is a Python package
- python run_pyineta.py <options>
- This is the documentation for the PyINETA package version 2.0.0.
- '.. automodule:: pyineta.finding :members:'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c03966
  all_source_dois:
  - 10.1021/acs.analchem.4c03966
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-visualization-and-result-interpretation

## Summary

Generate visual representations of INADEQUATE NMR spectra, peak networks, and metabolite matches to communicate pipeline results and validate peak-to-metabolite assignments. This skill interprets the clustering and matching outputs to produce figures and summary reports suitable for downstream analysis or publication.

## When to use

After peak clustering, network filtering, and database matching have identified candidate metabolites and their associated peak networks. Use this skill to inspect whether matched peak networks align with expected compound signatures, to verify that network topology matches database entries, and to produce publication-ready figures summarizing metabolite identifications.

## When NOT to use

- When no peak networks have been identified (filtering step produced empty output).
- When matching to the database has not yet been performed; visualization requires both query networks and reference database entries.
- When the goal is exploratory peak picking or clustering optimization rather than final result communication; use intermediate diagnostic plots from the picking or clustering modules instead.

## Inputs

- Filtered peak networks (output from finding module)
- Matched metabolite assignments (output from matching module)
- Simulated INADEQUATE database spectra with peak coordinates and connectivity information
- Configuration file specifying output directory and figure generation preferences

## Outputs

- Visualization figures (PNG, PDF, or other raster/vector format) showing overlay or side-by-side comparison of query peak networks and matched database metabolite spectra
- Summary report or metadata file listing matched metabolites, their corresponding query networks, and match quality indicators
- Single-network detailed plots for high-confidence or ambiguous identifications

## How to apply

Invoke the plotting module with the filtered peak networks and matched database metabolite entries as input. The module generates side-by-side or overlay visualizations of query peak networks against simulated INADEQUATE database spectra, allowing visual confirmation that peaks and their connectivities match the database entry. Configure figure output via the -f FIGURE flag in run_pyineta.py (yes/no); specify individual networks and metabolites for detailed inspection using the singleplot step with -n NET and -d DBNAME parameters. Evaluate success by examining peak alignment, network topology correspondence, and whether connection patterns in the query match the reference database structure.

## Related tools

- **PyINETA** (Provides the plotting module that generates visualizations of peak networks and metabolite matches; invoked via run_pyineta.py with -s plot or -s singleplot steps) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime environment for executing the PyINETA plotting module and post-processing visualization outputs)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -o example1_output -s plot -f yes
```

## Evaluation signals

- Figures display query peak networks with coordinates and connectivity patterns overlaid or adjacent to simulated database spectra for the matched metabolite.
- Peak positions in query spectra align within expected tolerance (typically <1–5 ppm or method-specific cutoff) to the matched database entry.
- Network connectivity topology (which peaks are connected via INADEQUATE J-couplings) visually matches between query and reference.
- Summary report lists all matched metabolites with associated query network identifiers and match confidence scores or metrics from the matching module.
- Single-network plots can be regenerated for any combination of network ID and database metabolite without error, confirming bidirectional traceability between networks and identifications.

## Limitations

- Visualization quality depends on peak picking and clustering accuracy upstream; poor peak detection or network fragmentation will produce uninformative or misleading figures.
- The simulated INADEQUATE database is a reference construct; real metabolites may exhibit spectral shifts, line broadening, or minor peak variations due to solvent, pH, or sample matrix effects that prevent perfect visual alignment even for true identifications.
- No changelog is maintained for the PyINETA package, so visualization output format or behavior changes across versions may not be documented.

## Evidence

- [intro] which it then matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra: "matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra"
- [other] Generate visualization outputs via the plotting module and export final metabolite identifications.: "Generate visualization outputs via the plotting module and export final metabolite identifications"
- [methods] Plotting module documentation reference in methods: "Plotting
--------
.. automodule:: pyineta.plotting"
- [readme] Optional flag for figure generation in run_pyineta.py: "-f FIGURE, --figure FIGURE
                        Optional: Generate figures- yes or no. Default: Yes"
- [readme] Single-network plotting capability with network and database metabolite specification: "-n NET, --net NET     Required with -s singlePlot: Specify which Network you
                        want to plot.
  -d DBNAME, --dbname DBNAME
                        Required with -s singlePlot:"
