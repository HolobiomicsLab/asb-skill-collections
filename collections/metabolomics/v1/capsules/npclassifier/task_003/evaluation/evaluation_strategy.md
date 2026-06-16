# Evaluation Strategy

## Direct Checks

- verify file 'Classifier/models_folder/models/get_models.sh' exists in the repository
- script_runs: execute get_models.sh in the Classifier/models_folder/models directory without errors
- verify TensorFlow 2.3.0 is installed and importable as a Python module
- file_exists: verify that an HDF5 model file (.h5 extension) is created after running get_models.sh
- verify the HDF5 model can be loaded using tf.keras.models.load_model() without errors
- verify the loaded model exposes a layer named exactly 'input_2048'
- verify the loaded model exposes a layer named exactly 'input_4096'
- verify the loaded model exposes a layer named exactly 'output'
- verify the model has exactly three named layers matching the required names (no extraneous layers with those names)

## Expert Review

- confirm that the HDF5 model structure is compatible with TensorFlow 2.3.0 format specifications
- confirm that the layer names and connectivity represent a valid Keras classification model architecture suitable for natural product classification
