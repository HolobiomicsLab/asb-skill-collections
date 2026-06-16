# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What are the required layer names that a converted Keras model must expose after transformation to HDF5 TensorFlow 2.3.0 format for use in the NP Classifier pipeline?: 'Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output"'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The NP Classifier model conversion process requires the resulting HDF5 TF2 model to expose three specific layer names: two input layers named 'input_2048' and 'input_4096', and one output layer named 'output'.: 'Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output"'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] NP-Classifier repository from github.com/mwang87/NP-Classifier: 'github.com/mwang87/NP-Classifier'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] TensorFlow 2.3.0 installed environment: 'tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] HDF5 TF2 model file with verified layer names (input_2048, input_4096, output): 'Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output"'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Verification report listing confirmed layer names and structural compliance: 'Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output"'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] get_models.sh: 'cd Classifier/models_folder/models
sh ./get_models.sh'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] TensorFlow 2.3.0: 'tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'Make sure you have python installed'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting model preparation, layer naming conventions, or version history of the conversion process: '_No changelog found._'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The discussion section provides no details on expected model file location, output directory structure, or naming convention for the converted HDF5 file: 'No changelog found.'
