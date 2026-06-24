"""README-based license precheck using an LLM via OpenRouter.

Before filing upstream GitHub issues asking for license clarification, this tool:
1. Fetches the repository README via the GitHub API.
2. Asks an LLM (default: deepseek/deepseek-chat via OpenRouter) to extract any
   explicitly stated license for *this* software.
3. If a license is found with high/medium confidence AND evidence text, re-tiers
   the corpus entry immediately (avoiding a noisy issue for repos that already
   state their license in the README).
4. Entries where no license is detected (or confidence is low) are flagged for
   the normal issue-wave flow.

Usage:
    python3 -m scripts.readme_license_precheck \\
        --corpus collections/metabolomics/v2/corpus.yaml

    python3 -m scripts.readme_license_precheck \\
        --corpus collections/metabolomics/v2/corpus.yaml \\
        --limit 20 \\
        --model deepseek/deepseek-chat
"""
from __future__ import annotations

import base64
import json
import os
import pathlib
import re
import urllib.error
import urllib.request
from typing import Callable

import yaml

from scripts.derive_license_tiers import classify_license_text, parse_repo
from scripts.license_tier import tier_for_license

# ---------------------------------------------------------------------------
# fetch_readme
# ---------------------------------------------------------------------------

_README_API = "https://api.github.com/repos/{}/{}/readme"
_NULL_DETECT = {"license": None, "confidence": "low", "evidence": None}


def fetch_readme(
    owner: str,
    repo: str,
    token: str | None,
    _open: Callable = urllib.request.urlopen,
) -> str | None:
    """Fetch the README for owner/repo via the GitHub API and return decoded text.

    Returns None on 404, empty content, or any other fetch failure.
    """
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(_README_API.format(owner, repo), headers=headers)
    try:
        with _open(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    except Exception:
        return None

    content = data.get("content", "")
    if not content:
        return None
    try:
        return base64.b64decode(content).decode("utf-8", "replace")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# openrouter_chat
# ---------------------------------------------------------------------------

_OR_URL = "https://openrouter.ai/api/v1/chat/completions"


def openrouter_chat(
    prompt: str,
    api_key: str,
    model: str = "deepseek/deepseek-chat",
    _open: Callable = urllib.request.urlopen,
) -> str:
    """POST prompt to OpenRouter and return the assistant's text response."""
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        _OR_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with _open(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# extract_license
# ---------------------------------------------------------------------------

_EXTRACT_PROMPT = """\
You are a license detection assistant. Given the README text of a software repository,
identify if there is an EXPLICIT license statement for THIS software (not for
dependencies or datasets it references).

Return ONLY a JSON object in this exact format — no commentary, no code fences:
{{"license": <SPDX id or short name, or null>, "confidence": "high|medium|low", "evidence": <exact sentence stating the license, or null>}}

Rules:
- "license" must be a recognized SPDX id or short name (e.g. "MIT", "Apache-2.0", "GPL-3.0",
  "CC-BY-NC-4.0") if one is clearly stated; otherwise null.
- Set confidence to "high" only if the license is stated unambiguously for THIS repo.
  Use "medium" if it is implied (e.g. a badge without body text). Use "low" if you
  are guessing.
- "evidence" is the EXACT sentence or badge text that supports the license claim, or null.
- Report a license ONLY if explicitly stated for THIS software. Ignore licenses
  mentioned for cited tools, dependencies, or datasets.

README text:
---
{readme}
---

Respond with ONLY the JSON object."""

_BRACE_RE = re.compile(r"\{.*\}", re.DOTALL)   # first '{' .. last '}', tolerant of nesting


def extract_license(readme_text: str, _chat: Callable) -> dict:
    """Ask the LLM to extract the license from readme_text.

    Returns a dict with keys: license, confidence, evidence.
    Falls back to the null-detect dict on any parse failure.
    """
    prompt = _EXTRACT_PROMPT.format(readme=readme_text[:8000])
    try:
        raw = _chat(prompt)
    except Exception:
        return dict(_NULL_DETECT)

    # Strip code fences if present
    stripped = raw.strip()
    for fence_pattern in (r"```json\s*([\s\S]*?)```", r"```\s*([\s\S]*?)```"):
        m = re.search(fence_pattern, stripped, re.DOTALL)
        if m:
            stripped = m.group(1).strip()
            break

    # Try direct parse first
    try:
        result = json.loads(stripped)
        if isinstance(result, dict) and "license" in result:
            return result
    except json.JSONDecodeError:
        pass

    # Fall back: find first {...} block in the raw response
    m = _BRACE_RE.search(raw)
    if m:
        try:
            result = json.loads(m.group(0))
            if isinstance(result, dict) and "license" in result:
                return result
        except json.JSONDecodeError:
            pass

    return dict(_NULL_DETECT)


# ---------------------------------------------------------------------------
# detected_tier
# ---------------------------------------------------------------------------

def detected_tier(license_str: str | None) -> str | None:
    """Map a detected license string to a tier string, or None if falsy.

    Tries classify_license_text() first (normalises raw README phrases to SPDX),
    then tier_for_license() on both the result and the raw string.
    """
    if not license_str or not license_str.strip():
        return None

    # Try to normalise via text classification (catches long CC/AGPL phrases)
    normalised = classify_license_text(license_str)
    if normalised:
        return tier_for_license(normalised)

    # Fall back: pass the raw string directly to tier_for_license
    return tier_for_license(license_str)


# ---------------------------------------------------------------------------
# precheck_entry
# ---------------------------------------------------------------------------

def precheck_entry(
    entry: dict,
    token: str | None,
    _readme: Callable = fetch_readme,
    _extract: Callable | None = None,
    _chat: Callable | None = None,
) -> dict:
    """Precheck a single corpus paper dict.

    Fetches the README, runs license extraction, and decides whether to retier
    the entry or flag it for the normal issue-wave.

    Returns a dict with keys:
        repo, detected_license, tier, confidence, evidence, action
    where action ∈ {"retier", "file-issue"}.
    """
    if _extract is None:
        _extract = extract_license

    parsed = parse_repo(entry.get("repo_url", ""))
    if not parsed:
        return {
            "repo": entry.get("repo_url", ""),
            "detected_license": None,
            "tier": None,
            "confidence": "low",
            "evidence": None,
            "action": "file-issue",
        }

    owner, repo = parsed
    repo_slug = f"{owner}/{repo}"

    readme_text = _readme(owner, repo, token)
    if not readme_text:
        return {
            "repo": repo_slug,
            "detected_license": None,
            "tier": None,
            "confidence": "low",
            "evidence": None,
            "action": "file-issue",
        }

    detection = _extract(readme_text, _chat)
    lic = detection.get("license")
    confidence = detection.get("confidence", "low")
    evidence = detection.get("evidence")

    # Only retier when we have a license, high/medium confidence, AND evidence text
    if lic and confidence in ("high", "medium") and evidence:
        tier = detected_tier(lic)
        return {
            "repo": repo_slug,
            "detected_license": lic,
            "tier": tier,
            "confidence": confidence,
            "evidence": evidence,
            "action": "retier",
        }

    return {
        "repo": repo_slug,
        "detected_license": lic,
        "tier": detected_tier(lic),
        "confidence": confidence,
        "evidence": evidence,
        "action": "file-issue",
    }


# ---------------------------------------------------------------------------
# run_precheck
# ---------------------------------------------------------------------------

def run_precheck(
    corpus_path: str,
    api_key: str,
    token: str | None = None,
    limit: int | None = None,
    _readme: Callable = fetch_readme,
    _chat: Callable | None = None,
) -> dict:
    """Run the README license precheck over all issue-wave candidates.

    Selects candidates the same way license_clarification_issues.candidates() does,
    runs precheck_entry for each, and mutates the corpus in-place for entries where
    a license was detected with sufficient confidence.

    Args:
        corpus_path: Path to corpus.yaml.
        api_key: OpenRouter API key (used to build a default _chat if _chat is None).
        token: GitHub token for README fetches.
        limit: Cap the number of candidates processed (None = no limit).
        _readme: Injectable README fetch function.
        _chat: Injectable LLM chat function. If None, builds one from api_key.

    Returns:
        Summary dict: {checked, retiered, still_file_issue, by_tier: {tier: count}}.
    """
    from scripts.license_clarification_issues import candidates

    if _chat is None:
        def _chat(prompt: str) -> str:
            return openrouter_chat(prompt, api_key=api_key)

    path = pathlib.Path(corpus_path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    papers = doc.get("papers", [])

    # Build a lookup from (owner, repo) → list of paper dicts in the corpus
    repo_to_papers: dict[tuple[str, str], list[dict]] = {}
    for p in papers:
        parsed = parse_repo(p.get("repo_url", ""))
        if parsed:
            repo_to_papers.setdefault(parsed, []).append(p)

    cands = candidates(corpus_path)
    if limit is not None:
        cands = cands[:limit]

    checked = 0
    retiered = 0
    still_file_issue = 0
    by_tier: dict[str, int] = {}

    for c in cands:
        owner, repo = c["owner"], c["repo"]
        # Find the matching paper(s) from the corpus
        paper_list = repo_to_papers.get((owner, repo), [])
        if not paper_list:
            continue

        # Use the first matching paper for precheck (all share the same repo)
        representative = paper_list[0]

        result = precheck_entry(
            representative,
            token=token,
            _readme=_readme,
            _chat=_chat,
        )
        checked += 1

        if result["action"] == "retier":
            tier = result["tier"]
            lic = result["detected_license"]
            evidence = result["evidence"]

            # Mutate ALL corpus papers with this repo URL
            for p in paper_list:
                p["license_tier"] = tier
                p.setdefault("access", {})["license"] = lic
                p["license_detection"] = "readme-llm"
                p["license_evidence"] = evidence

            retiered += 1
            by_tier[tier] = by_tier.get(tier, 0) + 1
        else:
            still_file_issue += 1

    # Write corpus back only if we made changes
    if retiered > 0:
        path.write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    return {
        "checked": checked,
        "retiered": retiered,
        "still_file_issue": still_file_issue,
        "by_tier": by_tier,
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", required=True, help="Path to corpus.yaml")
    ap.add_argument("--limit", type=int, default=None, metavar="N",
                    help="Max candidates to process (default: all)")
    ap.add_argument("--model", default="deepseek/deepseek-chat",
                    help="OpenRouter model id (default: deepseek/deepseek-chat)")
    args = ap.parse_args(argv)

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        import sys
        print(
            "Error: OPENROUTER_API_KEY environment variable is not set.",
            file=sys.stderr,
        )
        return 1

    def _chat(prompt: str) -> str:
        return openrouter_chat(prompt, api_key=api_key, model=args.model)

    summary = run_precheck(
        args.corpus,
        api_key=api_key,
        limit=args.limit,
        _chat=_chat,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
