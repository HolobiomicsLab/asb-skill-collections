"""
Mirror a released collection directory to HuggingFace Datasets + create leaderboard Space.

Called by mirror-to-hf.yml CI workflow. Reads all config from environment variables:

  HF_TOKEN         — HuggingFace API token (required; skip if absent)
  HF_REPO          — HF Dataset repo ID (e.g. HolobiomicsLab/asb-metabolomics-v1)
  SPACE_REPO       — HF Space repo ID (e.g. HolobiomicsLab/asb-metabolomics-v1-leaderboard)
  CPATH            — Local collection directory path
  TAG              — Git release tag (e.g. metabolomics-v1)
  HF_STEP          — One of: upload_dataset | upload_space

Exit codes:
  0 — success or HF_TOKEN absent (fail-soft)
  1 — fatal error
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def upload_dataset(token: str, repo: str, cpath: Path, tag: str) -> int:
    """Upload collection directory to HF Datasets repo."""
    from huggingface_hub import HfApi, create_repo

    api = HfApi(token=token)

    try:
        create_repo(
            repo_id=repo,
            repo_type="dataset",
            token=token,
            private=False,
            exist_ok=True,
        )
        print(f"Ensured HF Dataset repo: {repo}")
    except Exception as e:
        print(f"ERROR creating HF repo: {e}", file=sys.stderr)
        return 1

    try:
        api.upload_folder(
            folder_path=str(cpath),
            repo_id=repo,
            repo_type="dataset",
            commit_message=f"Mirror release {tag} from HolobiomicsLab/asb-skill-collections",
            ignore_patterns=[".hf-space"],
        )
        print(f"Uploaded {cpath} to {repo}")
    except Exception as e:
        print(f"ERROR uploading folder: {e}", file=sys.stderr)
        return 1

    readme_path = cpath / "README_HF.md"
    if readme_path.exists():
        try:
            api.upload_file(
                path_or_fileobj=str(readme_path),
                path_in_repo="README.md",
                repo_id=repo,
                repo_type="dataset",
                commit_message=f"Update dataset card for {tag}",
            )
            print("Uploaded README_HF.md as dataset card README.md")
        except Exception as e:
            print(f"WARNING: Could not upload README card: {e}", file=sys.stderr)

    print(f"Done. View at: https://huggingface.co/datasets/{repo}")
    return 0


def upload_space(token: str, space_repo: str, cpath: Path, tag: str) -> int:
    """Upload generated Space files to HF Spaces."""
    from huggingface_hub import HfApi, create_repo

    space_src = cpath / ".hf-space"
    if not space_src.exists():
        print("WARNING: .hf-space dir not found, skipping Space creation", file=sys.stderr)
        return 0

    api = HfApi(token=token)

    try:
        create_repo(
            repo_id=space_repo,
            repo_type="space",
            space_sdk="gradio",
            token=token,
            private=False,
            exist_ok=True,
        )
        print(f"Ensured HF Space: {space_repo}")
    except Exception as e:
        print(f"ERROR creating Space: {e}", file=sys.stderr)
        return 1

    try:
        api.upload_folder(
            folder_path=str(space_src),
            repo_id=space_repo,
            repo_type="space",
            commit_message=f"Update leaderboard Space for {tag}",
        )
        print(f"Uploaded Space files from {space_src} to {space_repo}")
    except Exception as e:
        print(f"ERROR uploading Space: {e}", file=sys.stderr)
        return 1

    print(f"Done. View Space at: https://huggingface.co/spaces/{space_repo}")
    return 0


def main() -> int:
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        print("WARNING: HF_TOKEN not set. Skipping HuggingFace operation.", file=sys.stderr)
        return 0

    step = os.environ.get("HF_STEP", "upload_dataset")
    cpath = Path(os.environ.get("CPATH", "."))
    tag = os.environ.get("TAG", "unknown")

    if step == "upload_dataset":
        repo = os.environ.get("HF_REPO", "")
        if not repo:
            print("ERROR: HF_REPO env var required for upload_dataset", file=sys.stderr)
            return 1
        return upload_dataset(token=token, repo=repo, cpath=cpath, tag=tag)

    elif step == "upload_space":
        space_repo = os.environ.get("SPACE_REPO", "")
        if not space_repo:
            print("ERROR: SPACE_REPO env var required for upload_space", file=sys.stderr)
            return 1
        return upload_space(token=token, space_repo=space_repo, cpath=cpath, tag=tag)

    else:
        print(f"ERROR: Unknown HF_STEP value: {step!r}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
