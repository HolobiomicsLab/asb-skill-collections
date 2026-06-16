# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does the saveAnnotations function successfully write all expected output file types (global results table, ranked results, ranked spectra PDFs, and pseudo-MS/MS MGF file) to the specified directory without errors?: 'saveAnnotations(annotations, DirPath=exampleDir, saveOptions=TRUE, saveXCMSoptions=FALSE, saveRanked=TRUE, saveRankedSpec=TRUE, savePseudoMSMS=TRUE)'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The saveAnnotations function is invoked with parameters to save global annotations, ranked results, ranked spectra as PDFs, and pseudo-MS/MS spectra as MGF files to a temporary directory, with all save flags enabled to write the full set of annotation outputs.: 'saveAnnotations(annotations, DirPath=exampleDir, saveOptions=TRUE, saveXCMSoptions=FALSE, saveRanked=TRUE, saveRankedSpec=TRUE, savePseudoMSMS=TRUE)'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MetaboAnnotatoR annotations object (output from annotateRC function): 'annotations can be performed using the *annotateRC* function'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Global results table (all annotated features and top candidate per feature): 'It is possible to save the annotation results to a user-specified directory'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Ranked results table (all candidate annotations per feature with scores): 'It is also possible to inspect if there were other candidate annotations for a given feature'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Ranked spectra PDF files (one per feature showing matched ions for each candidate): 'It is possible to visualise the spectra containing the matched ions to each candidate'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Pseudo-MS/MS MGF file (pseudo-MS/MS spectra in MGF format): 'a processed dataset composed of two objects: RAMClustR (object containing the pseudo-MS/MS spectra)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] File audit report (inventory of all output files with metadata): 'It is possible to save the annotation results to a user-specified directory'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MetaboAnnotatoR: 'MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'To install this package, start R (version "4.5.0" or higher)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: 'No changelog found.'
