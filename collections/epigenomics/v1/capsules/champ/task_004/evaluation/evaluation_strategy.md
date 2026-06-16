# Evaluation Strategy

## Direct Checks

- verify file exists: EPICSimData dataset loadable via data(EPICSimData) in R/ChAMP environment
- script_runs: champ.Block(arraytype='EPIC') executes without error on EPICSimData input
- verify output_matches_reference: Block.GUI() graphical output displays zero differentially methylated blocks detected for EPICSimData, as expected for simulation dataset with no true signal
- verify file_format_is: Block.GUI() output is a valid interactive Shiny/Plotly web interface (HTML or R Shiny object)

## Expert Review

- Confirm that the simulation design of EPICSimData is appropriate for a null-signal test case (i.e., that the dataset was intentionally constructed to contain no true differentially methylated blocks)
- Assess whether zero blocks detected is the correct expected outcome given EPICSimData's documented provenance and construction parameters
