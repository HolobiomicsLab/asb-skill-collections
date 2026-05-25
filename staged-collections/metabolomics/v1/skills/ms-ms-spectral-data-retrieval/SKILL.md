---
name: ms-ms-spectral-data-retrieval
description: Use when retrieving MS/MS spectra in the metabolomics domain using declarative MassQL queries to match compound-class-specific fragment ion signatures from large public repositories like GNPS/MassIVE, Metabolomics Workbench, and MetaboLights.
when_to_use_negative:
- Your target compounds are already well-represented in commercial spectral libraries or your dataset is small (<10 million spectra); traditional library matching will be faster and more cost-effective.
- You lack a biochemically motivated hypothesis about a characteristic fragment or neutral loss; exploratory untargeted MS/MS analysis or networking without pre-query feature definition is more appropriate.
- You need to track consecutive MS spectra from a single chromatographic feature (e.g., extracted ion chromatogram elution profile); MassQL has limited capability to leverage sequential spectra and isotope intensity distributions beyond a handful of features.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: MassQL
  role: Declarative query language and reference engine for parsing and executing fragment ion and neutral loss filters on MS data
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark parser
  role: Parses MassQL query strings into an internal data structure using context-free grammar
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Reads MS data files in mzML, mzXML, and MGF formats and constructs pandas DataFrames for querying
- name: pandas
  role: Performs efficient DataFrame filtering and data manipulations to execute MassQL filter logic
- name: Apache feather
  role: Optional caching format for serialized MS data frames to enable repeated queries without re-parsing raw files
- name: MS-Cluster
  role: Collapses redundant MS/MS spectra from query results into consensus spectra
- name: Falcon-MS
  role: Alternative tool for generating consensus MS/MS spectra from redundant observations
- name: GNPS
  role: Public repository hosting >230 million MS/MS spectra and spectral libraries for query refinement and result networking
- name: MZmine
  role: Open-source MS data processing platform with native MassQL support for integration into full workflows
  repo: https://github.com/mzmine/mzmine
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/ms-ms-spectral-data-retrieval@sha256:376515d8689726a98dd024f3d48f6ca0bbe034110a4cd443a41bdc66d55e4c1f
---

# MS/MS Spectral Data Retrieval

## Summary

Retrieve MS/MS spectra matching compound-class-specific fragment ion signatures from large public repositories (GNPS/MassIVE, Metabolomics Workbench, MetaboLights) using declarative MassQL queries. This skill enables discovery of known and novel compounds by translating chemical knowledge (e.g., phosphate fragment m/z 98.9847 ± 50 ppm, iron isotope ratios) into queryable patterns across hundreds of millions of spectra.

## When to use

You have a hypothesis about a characteristic MS/MS fragment or neutral loss associated with a compound class (e.g., organophosphate esters, siderophores, bile acids) and want to find all spectra in public data repositories exhibiting that signature. Use this skill when manual spectral library search is incomplete or when the target compounds are expected to be rare or chemically novel, represented in less than ~5% of query results.

## When NOT to use

- Your target compounds are already well-represented in commercial spectral libraries or your dataset is small (<10 million spectra); traditional library matching will be faster and more cost-effective.
- You lack a biochemically motivated hypothesis about a characteristic fragment or neutral loss; exploratory untargeted MS/MS analysis or networking without pre-query feature definition is more appropriate.
- You need to track consecutive MS spectra from a single chromatographic feature (e.g., extracted ion chromatogram elution profile); MassQL has limited capability to leverage sequential spectra and isotope intensity distributions beyond a handful of features.

## Inputs

- MassQL query string (e.g., 'MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50')
- LC-MS/MS dataset in mzML, mzXML, or MGF format
- Reference MS/MS spectral library (GNPS, Metabolomics Workbench, or MetaboLights)

## Outputs

- Tabular CSV/TSF file of matched MS/MS spectra with scan ID, precursor m/z, product ion m/z, intensity, retention time, and metadata
- Consensus MS/MS spectra (collapsed redundant observations using MS-Cluster or Falcon-MS)
- Molecular network (constructed from consensus spectra in GNPS)

## How to apply

First, refine and validate your MassQL query on a reference dataset containing known compounds from GNPS spectral libraries (e.g., 4,533 reference bile acid spectra). Construct a query string using filter clauses such as MS2PROD=<m/z>:TOLERANCEPPM=<ppm>:INTENSITYPERCENT=<%_of_base_peak> to target product ion m/z values, MS2PREC for precursor m/z, POLARITY, RTMIN/RTMAX for retention time windows, and MOBILITY for ion-mobility data if available. Parse the query using the lark parser library into an internal data structure. Load MS data files (mzML, mzXML, or MGF format) from the target repository using pyteomics, optionally caching as Apache feather files for repeated queries. Apply the query engine using pandas DataFrame filtering to retain only MS/MS scans satisfying all filter conditions simultaneously. Export matched spectra in tabular format (CSV/TSV) with scan identifiers, precursor m/z, product ion m/z, and intensity metadata. Expect that retrieval-scale queries (e.g., across >230 million spectra in GNPS/MassIVE) will return thousands to hundreds of thousands of candidate spectra, the majority (~85%) of which may represent novel compounds with no library match.

## Related tools

- **MassQL** (Declarative query language and reference engine for parsing and executing fragment ion and neutral loss filters on MS data) — https://github.com/mwang87/MassQueryLanguage
- **lark parser** (Parses MassQL query strings into an internal data structure using context-free grammar) — https://github.com/lark-parser/lark
- **pyteomics** (Reads MS data files in mzML, mzXML, and MGF formats and constructs pandas DataFrames for querying)
- **pandas** (Performs efficient DataFrame filtering and data manipulations to execute MassQL filter logic)
- **Apache feather** (Optional caching format for serialized MS data frames to enable repeated queries without re-parsing raw files)
- **MS-Cluster** (Collapses redundant MS/MS spectra from query results into consensus spectra)
- **Falcon-MS** (Alternative tool for generating consensus MS/MS spectra from redundant observations)
- **GNPS** (Public repository hosting >230 million MS/MS spectra and spectral libraries for query refinement and result networking)
- **MZmine** (Open-source MS data processing platform with native MassQL support for integration into full workflows) — https://github.com/mzmine/mzmine

## Examples

```
from lark import Lark; from pyteomics import mzml; import pandas as pd; query = 'MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50'; parser = Lark(...); tree = parser.parse(query); spectra = [s for s in mzml.read('marine_water.mzML') if check_filters(s, tree)]; results = pd.DataFrame([{'scan_id': s['index'], 'precursor_mz': s['precursorList'][0]['selectedIonList'][0]['selectedIon']['selected ion m/z'], 'product_ion': 98.9847, 'intensity': s['intensity']} for s in spectra]); results.to_csv('matched_spectra.csv')
```

## Evaluation signals

- Query execution completes without parse errors (lark successfully tokenizes and validates MassQL syntax against the formal grammar).
- Retrieved spectrum count is within expected order of magnitude for the target compound class (e.g., 338,439 spectra for organophosphate esters in a ~230 million spectrum repository indicates ~0.15% hit rate; siderophores and bile acids yielded similar percentages).
- Validation on reference compounds: all known compounds of the target class in GNPS spectral libraries (e.g., 4,533 bile acids) are present in the retrieved set; missing known compounds indicate query tolerance parameters (ppm, intensity %) are too stringent.
- Consensus spectrum annotation rate matches or exceeds historical baseline (~5%; siderophore example: 441/7,504 = 5.9% matched to GNPS libraries); lower rates suggest novel chemistry, higher rates suggest over-inclusive query filters.
- Molecular network topology shows expected clustering: putatively identified known compounds form tight clusters with consistent neutral loss signatures; orphan clusters represent novel candidates for structural elucidation.

## Limitations

- MassQL has limited capability to leverage more than a handful of MS spectra from a single chromatographic feature; consecutive MS spectra arising from a compound elution are treated independently rather than as a cohesive ion trace, potentially missing low-abundance features.
- Query results depend critically on intensity tolerance parameters; one siderophore with a low-intensity 54Fe peak (falling outside 25% intensity tolerance) was missed, demonstrating that rare isotopologues or minor adducts below the threshold are invisible to the query.
- Retrieval-scale queries return large numbers of spectra (e.g., 338,439 for organophosphate esters), and only ~15% match known compounds; the remaining 85% require manual curation, spectral networking, and often synthetic validation, making downstream annotation labor-intensive.
- Query performance and memory usage scale with repository size; caching MS data as Apache feather files mitigates repeated parsing but does not reduce the fundamental computational cost of scanning hundreds of millions of spectra.

## Evidence

- [full_text] Here we introduce a new language, the Mass Spectrometry Query Language (MassQL), and an accompanying software ecosystem: "Here we introduce a new language, the Mass Spectrometry Query Language (MassQL), and an accompanying software ecosystem"
- [full_text] MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source (for example, electrospray ionization and matrix assisted laser: "MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source (for example, electrospray ionization and matrix assisted laser"
- [full_text] The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree: "The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree"
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations: "The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations"
- [full_text] spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying: "spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying"
- [full_text] we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries: "we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries"
- [full_text] In searching over 230 million MS/MS spectra in 97,109 public data files, we retrieved 26,944 MS/MS spectra associated with the iron-characteristic isotope pattern: "In searching over 230 million MS/MS spectra in 97,109 public data files, we retrieved 26,944 MS/MS spectra associated with the iron-characteristic isotope pattern"
- [full_text] The MassQL query found 338,439: "To identify OPEs in public data, we scaled the MassQL query to all Q Exactive data in the GNPS/MassIVE data repository (which included >230 million MS/MS spectra). The MassQL query found 338,439"
- [full_text] Only 15% (51,310) of the MS/MS found by MassQL could be explained (precursor m/z match with 20 ppm mass error) by known OPEs: "Only 15% (51,310) of the MS/MS found by MassQL could be explained (precursor m/z match with 20 ppm mass error) by known OPEs"
- [full_text] We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations: "We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations"
- [full_text] Using these consensus spectra, we created a molecular network in GNPS: "Using these consensus spectra, we created a molecular network in GNPS"
- [full_text] MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising: "MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising"
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
