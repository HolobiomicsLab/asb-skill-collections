# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Can spectrum_utils load a publicly deposited mass spectrometry spectrum via Universal Spectrum Identifier (USI) and annotate it with fragment ion types for visualization?: 'Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] spectrum_utils provides capabilities for spectrum loading from online resources via USI and annotating observed spectrum fragments using the ProForma 2.0 specification, supporting both data retrieval and fragment annotation workflows.: 'Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism. ... Annotating observed spectrum fragments using the ProForma 2.0'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Universal Spectrum Identifier (USI) string for a public tandem MS spectrum (e.g., mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555): 'usi = "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555"'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] ProForma 2.0 peptide sequence string with optional modifications (e.g., VLHPLEGAVVIIFK or EM[Oxidation]EVEES[Phospho]PEK): 'peptide = "VLHPLEGAVVIIFK"'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Fragment ion mass tolerance value and mode (e.g., 10 ppm or 0.05 Da): 'spectrum.annotate_proforma(peptide, 10, "ppm", ion_types="abyIm")'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] PNG image file containing the annotated mass spectrum with b and y ions highlighted and labeled: 'plt.savefig("proforma_ex1.png", bbox_inches="tight", dpi=300, transparent=True)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] spectrum_utils: 'spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'spectrum_utils is a Python package'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] matplotlib: 'fig, ax = plt.subplots(figsize=(12, 6))'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] ProForma 2.0: 'fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No version or changelog information is available to confirm which version of spectrum_utils was used or what changes may have been made to the plotting and annotation API.: 'No changelog found.'
