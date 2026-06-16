# Evaluation Strategy

## Direct Checks

- file_exists: verify that train_rescore.py exists in the repository root or running_scripts/ directory
- script_runs: execute train_rescore.py with a minimal configuration (e.g., single epoch, small batch size on a subset of data) and verify it completes without runtime errors
- file_exists: verify that a checkpoint file is created in the expected output directory after training
- file_format_is: verify that checkpoint file is in PyTorch .pt or .pth format and is loadable
- contains_substring: load checkpoint and verify it contains both 'formula_encoder_state_dict' and 'rescore_head_state_dict' keys
- expert_review: verify that TCN spectrum encoder parameters remain frozen (weights unchanged) throughout training by comparing encoder weights before and after training
- expert_review: verify that FormulaEncoder and RescoreHead parameters are trainable (gradients flow) during training
- expert_review: verify that BCE (binary cross-entropy) loss is applied during training by inspecting loss computation in train_rescore.py source code
- expert_review: verify that checkpoints are saved only when formula_acc (with H) improves by checking training logs or checkpoint save conditions in code

## Expert Review

- Confirm that the rescore model architecture correctly implements a Siamese design with frozen TCN encoder, element-wise product (z_spec ⊙ z_form), and scalar logit output
- Verify that formula_acc metric is computed correctly (accuracy including hydrogen atom prediction) and that improvement-based checkpoint saving logic is correctly implemented
- Inspect train_rescore.py source to confirm BCE loss is used for binary classification (positive/negative candidate pairs) rather than alternatives
- Validate that the frozen TCN encoder prevents gradient updates to spectrum encoder weights by inspecting require_grad flags in code
