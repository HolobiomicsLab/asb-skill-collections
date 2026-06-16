# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does MetaMiner successfully identify the AmfS lantibiotic (core peptide TGSQVSLLVCEYSSLSVVLCTP) when run on S. griseus genomic data with MSV000080102 spectral data in lantibiotic class search mode?: 'NPDtools – Natural Product Discovery tools – is a toolkit containing various pipelines for _in silico_ analysis of natural product mass spectrometry data'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input, indicating that raw nucleotide sequence format supports lantibiotic discovery.: 'While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] S.griseus_fragment.fasta reference genome sequence file: 'a search of `test_data/metaminer/msms/AmfS.mgf` spectrum against `test_data/metaminer/fasta/S.griseus_fragment.fasta` genome fragment'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] LC-MS/MS spectral data from MSV000080102 in centroided MGF, mzXML, mzML, or mzData format: 'For metabolomic data, MetaMiner works with liquid chromatography–tandem mass spectrometry data (LS-MS/MS). Spectra files must be centroided and in an open spectrum format (MGF, mzXML, mzML or mzData)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] significant_matches.tsv tab-separated report with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq: 'All the detected RiPPs are reported in plain text tab-separated value files (`.tsv`). Each file starts with a header line containing column descriptions'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Verified identification of AmfS lantibiotic with core sequence TGSQVSLLVCEYSSLSVVLCTP and modified sequence T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP: 'you will see identification of a lantibiotic with "TGSQVSLLVCEYSSLSVVLCTP" original sequence and "T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP" sequence after modifications in'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MetaMiner: 'MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Dereplicator: 'matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ProteoWizard: 'MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NPDtools: 'The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] joblib: 'For parallel processing of multiple spectra or/and sequence files, MetaMiner requires `joblib` Python library'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting what versions or features are bundled in this NPDtools distribution: '_No changelog found._'
