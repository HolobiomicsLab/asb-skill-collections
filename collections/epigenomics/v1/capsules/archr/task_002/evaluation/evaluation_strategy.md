# Evaluation Strategy

## Direct Checks

- verify that github:GreenleafLab__ArchR repository contains source code for addMonocleTrajectory function
- verify that github:GreenleafLab__ArchR repository contains source code for addSlingShotTrajectories function
- verify that both functions accept a prepared ArchR project object as input (file_format_is R object or compatible serialization)
- verify that addMonocleTrajectory produces a trajectory embedding object with trajectory-related slots or metadata fields
- verify that addSlingShotTrajectories produces a trajectory embedding object with trajectory-related slots or metadata fields
- script_runs: execute conditional dispatch logic that selects addMonocleTrajectory OR addSlingShotTrajectories based on user parameter, without sequential execution of both
- verify output object class or type indicates valid ArchR project with trajectory information embedded

## Expert Review

- assess whether the conditional dispatch mechanism correctly implements mutual exclusivity (one tool invoked, not both) as stated in sub-task scope
- evaluate whether the trajectory embedding output is biologically interpretable and consistent with expected Monocle3 or Slingshot trajectory representation
- review whether the function signatures and parameter handling for addMonocleTrajectory and addSlingShotTrajectories match documented ArchR API
