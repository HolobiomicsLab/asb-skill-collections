# Evaluation Strategy

## Direct Checks

- verify file exists in repository BioNet-XMU/DeepION or gankLei-X/DeepION containing augmentation pipeline implementation (e.g., augmentation.py, data_augmentation.py, or equivalent)
- verify script runs without error on a sample ion image input and produces exactly two augmented output images per input image
- verify COL mode augmentation outputs contain evidence of all four operations: color jitter, filtering, Poisson noise, and random missing value applied (parameter-sensitive: detection method may vary)
- verify ISO mode augmentation outputs contain all four COL operations plus intensity-dependent missing value (parameter-sensitive: intensity-dependent behavior requires tuning inspection)
- verify output format is consistent with downstream encoder module inputs (image shape, dtype, value range compatible with ResNet18 input specifications)
- file_format_is: augmented image outputs match input ion image format (e.g., PNG, NPY, TIFF, or deposited dataset format)
- row_count_equals or equivalent: exactly 2 augmented images generated per input image under each mode (COL and ISO)

## Expert Review

- assess whether color jitter parameters (brightness, contrast, saturation, hue ranges) are appropriate for ion image contrast and intensity preservation
- assess whether filtering operation (type, kernel size, cutoff frequency) preserves scientifically meaningful spatial structure in ion images
- assess whether Poisson noise level is realistic for mass spectrometry imaging instrumental characteristics and does not corrupt signal
- assess whether random missing value pattern and intensity-dependent missing value in ISO mode reflect realistic detector artifacts or intentional augmentation strategy
- assess whether augmentation preserves co-localization patterns in COL mode and isotope isotopic relationships in ISO mode as intended by the model design
