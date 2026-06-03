#!/usr/bin/env python3
"""Small Semantic Scholar Graph API helper for Claude paper queries.

Loads S2_API_KEY from /home/qiao/dockerai/AI-Scientist-v2/.env by default.
Never prints the key.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

DEFAULT_ENV_PATH = Path("/home/qiao/dockerai/AI-Scientist-v2/.env")
BASE_URL = "https://api.semanticscholar.org/graph/v1"
DEFAULT_FIELDS = ",".join(
    [
        "paperId",
        "externalIds",
        "url",
        "title",
        "abstract",
        "venue",
        "publicationVenue",
        "year",
        "publicationDate",
        "authors",
        "citationCount",
        "referenceCount",
        "influentialCitationCount",
        "isOpenAccess",
        "openAccessPdf",
        "fieldsOfStudy",
        "s2FieldsOfStudy",
        "tldr",
    ]
)


class S2Error(RuntimeError):
    pass


def load_dotenv_value(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        if name.strip() != key:
            continue
        return value.strip().strip('"').strip("'")
    return None


def get_api_key(env_path: Path) -> str | None:
    return os.getenv("S2_API_KEY") or load_dotenv_value(env_path, "S2_API_KEY")


def s2_get(path: str, *, api_key: str | None, params: dict[str, Any]) -> dict[str, Any]:
    headers = {"X-API-KEY": api_key} if api_key else {}
    try:
        response = requests.get(
            f"{BASE_URL}{path}",
            headers=headers,
            params=params,
            timeout=30,
        )
    except requests.exceptions.Timeout as exc:
        raise S2Error("Semantic Scholar request timed out after 30 seconds.") from exc
    except requests.exceptions.SSLError as exc:
        raise S2Error("Semantic Scholar TLS/SSL error. Check CA certificates, proxy, or VPN.") from exc
    except requests.exceptions.ConnectionError as exc:
        raise S2Error("Semantic Scholar connection error. Check outbound network, proxy, VPN, or DNS.") from exc

    if response.status_code == 401:
        raise S2Error("Semantic Scholar rejected S2_API_KEY with HTTP 401. Verify the key in the .env file.")
    if response.status_code == 429:
        raise S2Error("Semantic Scholar rate limit hit with HTTP 429. Slow down or retry later.")
    if response.status_code >= 400:
        snippet = response.text[:400].replace("\n", " ")
        raise S2Error(f"Semantic Scholar HTTP {response.status_code}: {snippet}")
    return response.json()


def compact_paper(paper: dict[str, Any]) -> dict[str, Any]:
    authors = paper.get("authors") or []
    return {
        "paperId": paper.get("paperId"),
        "title": paper.get("title"),
        "year": paper.get("year"),
        "venue": paper.get("venue"),
        "publicationDate": paper.get("publicationDate"),
        "authors": [a.get("name") for a in authors[:12] if a.get("name")],
        "citationCount": paper.get("citationCount"),
        "influentialCitationCount": paper.get("influentialCitationCount"),
        "referenceCount": paper.get("referenceCount"),
        "externalIds": paper.get("externalIds"),
        "url": paper.get("url"),
        "isOpenAccess": paper.get("isOpenAccess"),
        "openAccessPdf": paper.get("openAccessPdf"),
        "fieldsOfStudy": paper.get("fieldsOfStudy"),
        "tldr": paper.get("tldr"),
        "abstract": paper.get("abstract"),
    }


def search(args: argparse.Namespace) -> dict[str, Any]:
    api_key = get_api_key(args.env)
    if args.require_key and not api_key:
        raise S2Error(f"S2_API_KEY not found in environment or {args.env}.")
    payload = s2_get(
        "/paper/search",
        api_key=api_key,
        params={
            "query": args.query,
            "limit": args.limit,
            "offset": args.offset,
            "fields": args.fields,
        },
    )
    papers = [compact_paper(p) for p in payload.get("data", [])]
    return {
        "query": args.query,
        "total": payload.get("total"),
        "offset": payload.get("offset", args.offset),
        "limit": args.limit,
        "apiKeyLoaded": bool(api_key),
        "papers": papers,
    }


def paper(args: argparse.Namespace) -> dict[str, Any]:
    api_key = get_api_key(args.env)
    if args.require_key and not api_key:
        raise S2Error(f"S2_API_KEY not found in environment or {args.env}.")
    paper_id = quote(args.paper_id, safe=":/")
    payload = s2_get(
        f"/paper/{paper_id}",
        api_key=api_key,
        params={"fields": args.fields},
    )
    result = compact_paper(payload)
    result["apiKeyLoaded"] = bool(api_key)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Query Semantic Scholar Graph API without printing secrets.")
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV_PATH, help="Path to .env containing S2_API_KEY")
    parser.add_argument("--require-key", action="store_true", help="Fail if S2_API_KEY is not loaded")
    parser.add_argument("--fields", default=DEFAULT_FIELDS, help="Comma-separated S2 fields")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search papers by text query")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--offset", type=int, default=0)
    search_parser.set_defaults(func=search)

    paper_parser = subparsers.add_parser("paper", help="Fetch one paper by S2 id, DOI:<doi>, ARXIV:<id>, etc.")
    paper_parser.add_argument("paper_id")
    paper_parser.set_defaults(func=paper)

    args = parser.parse_args()
    if hasattr(args, "limit") and not (1 <= args.limit <= 100):
        parser.error("--limit must be between 1 and 100")
    try:
        result = args.func(args)
    except S2Error as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    time.sleep(0.2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
