# Evaluation Strategy

## Direct Checks

- verify file 'build-docker.sh' exists in github:CSi-Studio__AirdPro repository
- script_runs: execute build-docker.sh without errors
- verify Docker image 'airdpro:cli' exists after build completion
- value_in_range: Docker image airdpro:cli size is between 5.5 GB and 7.5 GB (parameter-sensitive to base Ubuntu 22.04 + Wine + .NET Framework 4.8 layers)
- verify Docker image airdpro:cli is built from Ubuntu 22.04 base (inspect image layers or Dockerfile)

## Expert Review

- Assess whether multi-stage build architecture follows best practices for minimizing final image size while maintaining functionality
- Verify that airdpro:cli image is functional for CLI batch processing (requires domain knowledge of AirdPro vendor file conversion workflow)
