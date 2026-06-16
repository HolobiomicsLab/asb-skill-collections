# Evaluation Strategy

## Direct Checks

- verify file exists for each of four built Docker images (airdpro:cli, airdpro:dev, airdpro:linux, airdpro:windows) in local Docker daemon or registry
- retrieve reported compressed size (in GB) for airdpro:cli image via 'docker images' or 'docker inspect' command; value_in_range [6, 7]
- retrieve reported compressed size (in GB) for airdpro:dev image via 'docker images' or 'docker inspect' command; value_in_range [9, 11]
- retrieve reported compressed size (in GB) for airdpro:linux image via 'docker images' or 'docker inspect' command; value_in_range [8, 10]
- retrieve reported compressed size (in GB) for airdpro:windows image via 'docker images' or 'docker inspect' command; value_in_range [4, 5]
- script_runs: docker build succeeds without error for all four image variants using Dockerfile(s) from github:CSi-Studio__AirdPro

## Expert Review

- verify that reported image sizes are consistent with documented compression method and base layers (Wine, .NET Framework 4.8, ProteoWizard bindings) across all four variants
- assess whether any image size falls outside its documented range and evaluate whether the discrepancy reflects a documentation error, image configuration drift, or legitimate variation in build artifact
