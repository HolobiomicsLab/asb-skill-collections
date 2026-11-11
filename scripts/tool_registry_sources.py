"""Package registries the tool-licence resolver may consult, read through a cache.

Each registry declared in governance/tool_registries.yaml has an `index_shape`
that says how its metadata is obtained:

- `packages_map`  one bulk JSON document with a `packages` mapping (Bioconda's
                  channeldata.json).
- `records_list`  one bulk JSON array of package records (r-universe, which
                  mirrors Bioconductor).
- `rds_matrix`    one bulk R serialised character matrix (CRAN's packages.rds).
- `name_list`     a bulk list of names, then one request per matched package.
- `per_name`      one request per name, made only for names the resolver has a
                  reason to ask about (PyPI, bio.tools).

Every answer is written to the cache directory before it is used, so a second
run is offline and gives the same result. A refusal (HTTP 403 or 429) stops the
run instead of being read as "no such package".
"""
from __future__ import annotations

import gzip
import json
import pathlib
import re
import struct
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "asb-skill-collections tool-licence-resolver"
# Bulk documents are a few megabytes; per-package answers far less. A PyPI answer
# for a project with thousands of releases can exceed the cap, and is then
# treated as unavailable rather than read in part.
MAX_BULK_BYTES = 80_000_000
MAX_PER_NAME_BYTES = 6_000_000
PER_NAME_PAUSE_S = 1.0


class RegistryRefused(RuntimeError):
    """A registry refused the request (HTTP 403 or 429): stop rather than guess."""


def normalize(text) -> str:
    """Lower-case alphanumerics only: the comparison key for names."""
    return re.sub(r"[^a-z0-9]", "", str(text or "").lower())


class Fetcher:
    """Cached GET with a size cap, a pause between per-name requests, and counts."""

    def __init__(self, cache_dir, offline: bool = False, pause: float = PER_NAME_PAUSE_S):
        self.cache = pathlib.Path(cache_dir)
        self.offline = offline
        self.pause = pause
        self.requests: dict[str, int] = {}
        self.bytes: dict[str, int] = {}
        self._last = 0.0

    def get(self, url: str, key: str, max_bytes: int, paced: bool = False) -> bytes | None:
        path = self.cache / key
        if path.is_file():
            return path.read_bytes()
        miss = self.cache / (key + ".missing")
        if miss.is_file() or self.offline:
            return None
        if paced:
            wait = self.pause - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
        host = urllib.parse.urlparse(url).netloc
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                       "Accept": "application/json"})
        self.requests[host] = self.requests.get(host, 0) + 1
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = response.read(max_bytes + 1)
        except urllib.error.HTTPError as exc:
            self._last = time.monotonic()
            if exc.code in (403, 429):
                raise RegistryRefused(f"{host} answered {exc.code} for {url}") from exc
            if exc.code == 404:
                self.cache.mkdir(parents=True, exist_ok=True)
                miss.write_text("404\n", encoding="utf-8")
            return None
        except (urllib.error.URLError, TimeoutError, OSError):
            self._last = time.monotonic()
            return None
        self._last = time.monotonic()
        self.bytes[host] = self.bytes.get(host, 0) + len(data)
        if len(data) > max_bytes:
            self.cache.mkdir(parents=True, exist_ok=True)
            miss.write_text("too large\n", encoding="utf-8")
            return None
        self.cache.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return data

    def get_json(self, url, key, max_bytes, paced=False):
        data = self.get(url, key, max_bytes, paced)
        if data is None:
            return None
        try:
            return json.loads(data)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None


# --------------------------------------------------------------------------- #
# R serialisation, enough of it to read CRAN's packages.rds                   #
# --------------------------------------------------------------------------- #

class _RdsReader:
    """XDR R serialisation (format versions 2 and 3), the subset a character matrix uses."""

    _CONSTANTS = {254, 242, 241, 253, 252, 251, 247}

    def __init__(self, data: bytes):
        self.b = data
        self.p = 0
        self.refs: list = []

    def _int(self) -> int:
        value = struct.unpack(">i", self.b[self.p:self.p + 4])[0]
        self.p += 4
        return value

    def _length(self) -> int:
        n = self._int()
        if n == -1:
            n = (self._int() << 32) + self._int()
        return n

    def item(self):
        flags = self._int()
        kind = flags & 0xFF
        has_attr, has_tag = flags & (1 << 9), flags & (1 << 10)
        if kind in self._CONSTANTS:
            return None
        if kind == 255:
            index = flags >> 8 or self._int()
            return self.refs[index - 1]
        if kind == 1:
            symbol = ("sym", self.item())
            self.refs.append(symbol)
            return symbol
        if kind in (2, 3, 5, 6, 17):
            if has_attr:
                self.item()
            tag = self.item() if has_tag else None
            head, rest = self.item(), self.item()
            node = [(tag[1] if tag else None, head)]
            return node + rest if isinstance(rest, list) else node
        if kind == 9:
            n = self._int()
            if n == -1:
                return None
            text = self.b[self.p:self.p + n].decode("utf-8", "replace")
            self.p += n
            return text
        if kind in (10, 13):
            n = self._length()
            out = list(struct.unpack(f">{n}i", self.b[self.p:self.p + 4 * n]))
            self.p += 4 * n
        elif kind == 14:
            n = self._length()
            out = list(struct.unpack(f">{n}d", self.b[self.p:self.p + 8 * n]))
            self.p += 8 * n
        elif kind in (16, 19, 20):
            out = [self.item() for _ in range(self._length())]
        else:
            raise ValueError(f"unsupported R object type {kind}")
        if has_attr:
            return ("attr", out, self.item())
        return out


def read_rds_matrix(data: bytes) -> list[dict]:
    """Rows of a gzip-compressed R character matrix, as ``{column: value}``."""
    raw = gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data
    if raw[:2] != b"X\n":
        raise ValueError("not an XDR R serialisation")
    reader = _RdsReader(raw)
    reader.p = 2
    version = reader._int()
    reader._int()
    reader._int()
    if version == 3:
        encoding_length = reader._int()
        reader.p += encoding_length
    obj = reader.item()
    if not (isinstance(obj, tuple) and obj[0] == "attr"):
        raise ValueError("packages.rds is not a matrix")
    values, attrs = obj[1], dict(obj[2])
    nrow, ncol = attrs["dim"]
    columns = attrs["dimnames"][1]
    return [{columns[c]: values[c * nrow + r] for c in range(ncol)} for r in range(nrow)]


# --------------------------------------------------------------------------- #
# Registries                                                                  #
# --------------------------------------------------------------------------- #

def _flatten(value):
    if isinstance(value, dict):
        for nested in value.values():
            yield from _flatten(nested)
    elif isinstance(value, (list, tuple)):
        for nested in value:
            yield from _flatten(nested)
    elif value is not None:
        yield str(value)


class Registry:
    """One declared registry: lookup by normalised name, then the fields the resolver reads."""

    def __init__(self, spec: dict, fetcher: Fetcher):
        self.spec = spec
        self.id = spec["id"]
        self.fetcher = fetcher
        self._index: dict | None = None

    @property
    def scope(self) -> str:
        return self.spec.get("scope", "life_science")

    @property
    def ecosystem(self) -> str | None:
        return self.spec.get("ecosystem")

    def _bulk(self) -> dict:
        """``{normalized_name: (canonical, record)}`` for bulk registries."""
        if self._index is not None:
            return self._index
        shape = self.spec["index_shape"]
        key = f"{self.id}-{shape}.json"
        index: dict = {}
        if shape == "packages_map":
            payload = self.fetcher.get_json(self.spec["index_url"], key, MAX_BULK_BYTES) or {}
            for name, record in (payload.get("packages") or {}).items():
                index.setdefault(normalize(name), (name, record))
        elif shape == "records_list":
            payload = self.fetcher.get_json(self.spec["index_url"], key, MAX_BULK_BYTES) or []
            field = self.spec.get("name_field", "Package")
            for record in payload:
                if isinstance(record, dict) and record.get(field):
                    index.setdefault(normalize(record[field]), (record[field], record))
        elif shape == "rds_matrix":
            derived = self.fetcher.cache / key
            if derived.is_file():
                rows = json.loads(derived.read_text(encoding="utf-8"))
            else:
                data = self.fetcher.get(self.spec["index_url"], f"{self.id}-index.rds", MAX_BULK_BYTES)
                keep = set(self.spec.get("keep_fields") or [])
                rows = [{k: v for k, v in row.items() if k in keep}
                        for row in (read_rds_matrix(data) if data else [])]
                if rows:
                    derived.write_text(json.dumps(rows), encoding="utf-8")
            field = self.spec.get("name_field", "Package")
            for record in rows:
                if record.get(field):
                    index.setdefault(normalize(record[field]), (record[field], record))
        elif shape == "name_list":
            payload = self.fetcher.get_json(self.spec["index_url"], f"{self.id}-index.json",
                                            MAX_BULK_BYTES) or []
            for name in payload:
                index.setdefault(normalize(name), (name, None))
        self._index = index
        return index

    def word_share(self, tokenize) -> dict:
        """``{word: share of the registry's package descriptions holding it}``.

        Words most packages use (`user`, `command`, `algorithm`) say nothing about
        which package is meant; the identity rule discounts them.
        """
        if getattr(self, "_word_share", None) is not None:
            return self._word_share
        counts: dict[str, int] = {}
        records = [r for _, r in self._bulk().values() if r] \
            if self.spec["index_shape"] != "per_name" else []
        for record in records:
            for w in tokenize(self.text(record)):
                counts[w] = counts.get(w, 0) + 1
        n = max(1, len(records))
        self._word_share = {w: c / n for w, c in counts.items()}
        return self._word_share

    def bulk_size(self) -> int | None:
        if self.spec["index_shape"] == "per_name":
            return None
        return len(self._bulk())

    def lookup(self, names, allow_request: bool = True) -> list[tuple[str, dict]]:
        """Packages whose normalised name equals one of ``names``.

        ``allow_request`` False keeps a per-name registry to its cache: the caller
        has no evidence that would let it use the answer, so it does not ask.
        """
        keys = []
        for name in names:
            key = normalize(name)
            if key and key not in keys:
                keys.append(key)
        shape = self.spec["index_shape"]
        found: list[tuple[str, dict]] = []
        if shape == "per_name":
            for name in names:
                record = self._per_name(name, allow_request)
                if record is not None and all(normalize(c) != normalize(record[0]) for c, _ in found):
                    found.append(record)
            return found
        index = self._bulk()
        for key in keys:
            if key in index:
                canonical, record = index[key]
                if record is None and shape == "name_list":
                    url = self.spec["package_url"].format(name=urllib.parse.quote(canonical))
                    record = self.fetcher.get_json(url, f"{self.id}-{key}.json",
                                                   MAX_PER_NAME_BYTES) or {}
                if all(normalize(c) != key for c, _ in found):
                    found.append((canonical, record or {}))
        return found

    def _per_name(self, name, allow_request) -> tuple[str, dict] | None:
        key = normalize(name)
        if not key:
            return None
        cache_key = f"{self.id}-{key}.json"
        fetcher = self.fetcher
        if not allow_request and not (fetcher.cache / cache_key).is_file():
            return None
        url = self.spec["package_url"].format(name=urllib.parse.quote(str(name).strip()))
        payload = fetcher.get_json(url, cache_key, MAX_PER_NAME_BYTES, paced=True)
        if payload is None:
            return None
        if self.spec.get("answer_shape") == "biotools_search":
            hits = [tool for tool in (payload.get("list") or [])
                    if normalize(tool.get("name")) == key or normalize(tool.get("biotoolsID")) == key]
            if len(hits) != 1:
                return None
            return hits[0].get("biotoolsID") or hits[0].get("name"), hits[0]
        info = payload.get("info") if isinstance(payload, dict) else None
        if not info or normalize(info.get("name")) != key:
            return None
        return info.get("name"), info

    # ------------------------------------------------------------------ #
    # Fields of one record                                               #
    # ------------------------------------------------------------------ #

    def licence_strings(self, record) -> list[str]:
        """The licence statement(s) to read, most specific first."""
        fmt = self.spec["license_format"]
        if fmt == "pypi_info":
            expression = record.get("license_expression")
            if expression:
                return [expression]
            declared = (record.get("license") or "").strip()
            classifiers = [c.split("::")[-1].strip() for c in record.get("classifiers") or []
                           if c.startswith("License ::") and "OSI Approved ::" in c
                           or c.startswith("License ::") and c.count("::") == 1]
            out = []
            if declared and "\n" not in declared and len(declared) <= 100:
                out.append(declared)
            if classifiers:
                out.append(" OR ".join(classifiers) if len(classifiers) > 1 else classifiers[0])
            return out
        if fmt == "biotools":
            value = record.get("license")
            return [value] if value else []
        value = record.get(self.spec["license_field"])
        return [value] if value else []

    def repo_values(self, record) -> list[str]:
        values: list[str] = []
        for field in self.spec.get("repo_fields") or []:
            values.extend(_flatten(record.get(field)))
        return [v for v in values if v]

    def homepage(self, record) -> str | None:
        field = self.spec.get("homepage_field")
        value = record.get(field) if field else None
        return str(value) if value else None

    def text(self, record) -> str:
        return "\n".join(str(record.get(f)) for f in self.spec.get("text_fields") or []
                         if record.get(f))

    def dois(self, record) -> set[str]:
        out = set()
        for publication in record.get("publication") or []:
            if isinstance(publication, dict) and publication.get("doi"):
                out.add(str(publication["doi"]).lower())
        return out

    def is_data_package(self, record) -> bool:
        """Bioconductor data packages describe a dataset, not the software named after it."""
        views = str(record.get("biocViews") or "")
        if not views.strip() or re.search(r"\bSoftware\b", views):
            return False
        return bool(re.search(r"\b(ExperimentData|AnnotationData|ExperimentHub|AnnotationHub|"
                              r"Workflow|\w+_Data)\b", views))

    def restricts_use(self, record) -> bool:
        """CRAN's own flag that a licence restricts use."""
        return str(record.get("License_restricts_use") or "").lower() == "yes"

    def address(self, canonical, record) -> str:
        template = self.spec.get("address") or ""
        return template.format(name=canonical)
