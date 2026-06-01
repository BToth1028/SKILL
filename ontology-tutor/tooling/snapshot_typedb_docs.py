#!/usr/bin/env python3
"""Capture TypeDB public documentation (typedb.com/docs) to disk for offline / vector ingest.

Reads docs URL lists from typedb.com sitemap indices (skips missing sub-sitemaps).
Optionally expands coverage by crawling internal /docs/ links discovered in fetched HTML.

Output root: set env var TYPEDB_SNAPSHOT_ROOT (or pass --out); docs are written
to <root>/docs_snapshot (alongside schema snapshots under _snapshot/). No default
path is baked in, so this tool carries no machine-specific location.

Politeness: configurable delay between GETs; identifies with a neutral User-Agent string.

Note: typedb.com docs sub-sitemaps omit large trees (e.g. /docs/typeql-reference/). Default behavior follows internal /docs/ links after fetching each page so those sections are included.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import html.parser
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import yaml

ROOT_SITEMAP = "https://typedb.com/sitemap.xml"
_ENV_SNAPSHOT_ROOT = os.environ.get("TYPEDB_SNAPSHOT_ROOT", "").strip()
# No baked-in path (C:\dev external-path gate): output root is resolved from
# the TYPEDB_SNAPSHOT_ROOT env var or the --out flag at runtime.
DEFAULT_OUT = (Path(_ENV_SNAPSHOT_ROOT) / "docs_snapshot") if _ENV_SNAPSHOT_ROOT else None
USER_AGENT = "typedb-docs-snapshot/1.0 (+local ingest; contact operator)"
DEFAULT_SEEDS = (
	"https://typedb.com/docs/",
	"https://typedb.com/docs/typeql-reference/",
	"https://typedb.com/docs/guides/",
	"https://typedb.com/docs/examples/",
)
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
HREF_RE = re.compile(
	r"""href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""",
	re.I,
)


@dataclass
class PageRecord:
	url: str
	path_relative: str
	sha256: str
	bytes: int
	http_status: int
	content_type: str


@dataclass
class SnapshotResult:
	captured_at_utc: str
	dry_run: bool = False
	pages: list[PageRecord] = field(default_factory=list)
	errors: list[dict[str, str]] = field(default_factory=list)


class _LinkCollector(html.parser.HTMLParser):
	def __init__(self) -> None:
		super().__init__()
		self.links: list[str] = []

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		if tag.lower() != "a":
			return
		ad = {k: v for k, v in attrs if v is not None}
		href = ad.get("href")
		if href:
			self.links.append(href)


def _utc_iso() -> str:
	return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _request(url: str, timeout: float) -> tuple[int, str, bytes, str]:
	req = urllib.request.Request(
		url,
		headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"},
		method="GET",
	)
	with urllib.request.urlopen(req, timeout=timeout) as resp:
		final = getattr(resp, "geturl", lambda: url)()
		status = resp.status
		ctype = resp.headers.get("Content-Type", "")
		body = resp.read()
	return status, final, body, ctype


def discover_docs_sitemap_urls(timeout: float) -> list[str]:
	raw = urllib.request.urlopen(ROOT_SITEMAP, timeout=timeout).read().decode("utf-8", "replace")
	doc_maps = re.findall(
		r"<loc>(https://typedb\.com/docs/sitemap[^<]+\.xml)</loc>",
		raw,
	)
	out: list[str] = []
	for sm_url in sorted(set(doc_maps)):
		try:
			sm_raw = urllib.request.urlopen(sm_url, timeout=timeout).read()
		except urllib.error.HTTPError:
			continue
		except urllib.error.URLError:
			continue
		root = ET.fromstring(sm_raw)
		for el in root.findall(".//sm:url/sm:loc", SITEMAP_NS):
			if el.text:
				out.append(el.text.strip())
	return sorted(set(out))


def _is_docs_page_url(url: str) -> bool:
	try:
		p = urlparse(url)
	except ValueError:
		return False
	if p.scheme not in ("http", "https"):
		return False
	if p.netloc != "typedb.com":
		return False
	if not p.path.startswith("/docs/"):
		return False
	if p.path.startswith("/docs/_/"):
		return False
	if "#" in url.split(p.scheme + "://", 1)[-1]:
		pass
	low = url.lower()
	for ext in (".pdf", ".zip", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".woff", ".woff2"):
		if low.endswith(ext):
			return False
	return True


def _normalize_enqueue_url(url: str, base_final: str) -> str | None:
	joined = urljoin(base_final, url)
	p = urlparse(joined)
	if p.scheme not in ("http", "https"):
		return None
	clean = p._replace(fragment="").geturl()
	if not _is_docs_page_url(clean):
		return None
	if clean.endswith("/") or p.path.endswith(".html"):
		return clean
	if "." not in Path(p.path).name:
		return clean.rstrip("/") + "/"
	return clean


def extract_same_site_links(html: str, base_final: str) -> list[str]:
	parser = _LinkCollector()
	parser.feed(html)
	found: list[str] = []
	for href in parser.links:
		n = _normalize_enqueue_url(href, base_final)
		if n:
			found.append(n)
	return found


def url_to_relpath(final_url: str) -> str:
	p = urlparse(final_url)
	path = p.path.rstrip("/")
	prefix = "/docs"
	if not path.startswith(prefix):
		path = prefix + path
	rel = path[len(prefix) :].lstrip("/")
	if not rel:
		return "html/docs/index.html"
	if rel.endswith(".html"):
		return f"html/docs/{rel}"
	sfx = Path(rel).suffix.lower()
	if sfx in (".txt", ".md", ".xml"):
		return f"html/docs/{rel}"
	return f"html/docs/{rel}/index.html"


def _snapshot_content_allowed(final_url: str, ctype: str) -> bool:
	low = ctype.lower()
	if "text/html" in low:
		return True
	path = urlparse(final_url).path.lower()
	if path.endswith(".txt") and "text/plain" in low:
		return True
	if path.endswith(".md") and ("text/plain" in low or "text/markdown" in low):
		return True
	return False


def fetch_and_store(
	url: str,
	out_root: Path,
	timeout: float,
) -> tuple[PageRecord | None, str | None]:
	try:
		status, final, body, ctype = _request(url, timeout=timeout)
	except Exception as exc:
		return None, f"{type(exc).__name__}: {exc}"
	if not _snapshot_content_allowed(final, ctype):
		return None, f"skip unsupported Content-Type={ctype!r}"
	text = body.decode("utf-8", "replace")
	relp = url_to_relpath(final)
	target = out_root / relp
	target.parent.mkdir(parents=True, exist_ok=True)
	target.write_bytes(body)
	h = hashlib.sha256(body).hexdigest()
	rec = PageRecord(
		url=final,
		path_relative=relp.replace("\\", "/"),
		sha256=h,
		bytes=len(body),
		http_status=status,
		content_type=ctype.split(";")[0].strip(),
	)
	return rec, text


def run_snapshot(
	out_root: Path,
	timeout: float,
	delay_s: float,
	max_pages: int | None,
	deep_crawl: bool,
	seeds: Iterable[str],
	dry_run: bool,
) -> SnapshotResult:
	cap = _utc_iso()
	res = SnapshotResult(captured_at_utc=cap, dry_run=dry_run)
	initial = set(discover_docs_sitemap_urls(timeout))
	for s in seeds:
		n = _normalize_enqueue_url(s, s if s.startswith("http") else "https://typedb.com/")
		if n:
			initial.add(n)
	queue: deque[str] = deque(sorted(initial))
	seen: set[str] = set()
	while queue:
		if max_pages is not None and len(res.pages) >= max_pages:
			break
		url = queue.popleft()
		if url in seen:
			continue
		seen.add(url)
		if dry_run:
			res.pages.append(
				PageRecord(
					url=url,
					path_relative="(dry-run)",
					sha256="",
					bytes=0,
					http_status=0,
					content_type="text/plain",
				)
			)
			continue
		rec, html_or_err = fetch_and_store(url, out_root, timeout)
		if rec is None:
			res.errors.append({"url": url, "detail": html_or_err or "unknown"})
			time.sleep(delay_s)
			continue
		res.pages.append(rec)
		if deep_crawl and html_or_err and "html" in rec.content_type.lower():
			for nxt in extract_same_site_links(html_or_err, rec.url):
				if nxt not in seen:
					queue.append(nxt)
		time.sleep(delay_s)
	return res


def write_manifest(out_root: Path, result: SnapshotResult) -> None:
	payload: dict = {
		"manifest_version": "1",
		"kind": "typedb_docs_snapshot",
		"captured_at_utc": result.captured_at_utc,
		"dry_run": result.dry_run,
		"source": ROOT_SITEMAP,
		"user_agent": USER_AGENT,
		"sitemap_note": "URLs gathered from typedb.com docs sub-sitemaps; optional deep_crawl expands via HTML links.",
		"page_count": len(result.pages),
		"errors": result.errors,
	}
	if result.dry_run:
		payload["planned_urls"] = [p.url for p in result.pages]
	else:
		payload["pages"] = [
			{
				"url": p.url,
				"path_relative": p.path_relative,
				"sha256": p.sha256,
				"bytes": p.bytes,
				"http_status": p.http_status,
				"content_type": p.content_type,
			}
			for p in result.pages
		]
	manifest_path = out_root / "manifest.yaml"
	manifest_path.parent.mkdir(parents=True, exist_ok=True)
	manifest_path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> int:
	parser = argparse.ArgumentParser(description="Snapshot TypeDB documentation under typedb.com/docs/")
	parser.add_argument(
		"--out",
		type=Path,
		default=DEFAULT_OUT,
		help=f"Output directory (default: {DEFAULT_OUT})",
	)
	parser.add_argument("--timeout", type=float, default=60.0, help="HTTP timeout seconds")
	parser.add_argument("--delay", type=float, default=0.35, help="Delay between successful GETs")
	parser.add_argument("--max-pages", type=int, default=None, help="Stop after N pages (testing)")
	parser.add_argument(
		"--sitemap-only",
		action="store_true",
		help="Only URLs from typedb.com docs sub-sitemaps (skips HTML link expansion; omits typeql-reference and similar)",
	)
	parser.add_argument(
		"--seed",
		action="append",
		default=None,
		metavar="URL",
		help="Extra seed URL (repeatable); merges with built-in docs hubs (/, typeql-reference, guides, examples)",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="List sitemap+seed URLs only (no GET); deep_crawl expansion requires a real run",
	)
	args = parser.parse_args()
	if args.out is None:
		print(
			"ERROR: output root not set. Pass --out PATH or set the "
			"TYPEDB_SNAPSHOT_ROOT environment variable.",
			file=sys.stderr,
		)
		return 2
	out_root = args.out.resolve()
	out_root.mkdir(parents=True, exist_ok=True)
	merged_seeds = list(DEFAULT_SEEDS)
	if args.seed:
		merged_seeds.extend(args.seed)
	seeds_unique: list[str] = list(dict.fromkeys(merged_seeds))
	deep_crawl = not args.sitemap_only
	result = run_snapshot(
		out_root=out_root,
		timeout=args.timeout,
		delay_s=args.delay,
		max_pages=args.max_pages,
		deep_crawl=deep_crawl,
		seeds=seeds_unique,
		dry_run=args.dry_run,
	)
	write_manifest(out_root, result)
	print(f"captured_at_utc={result.captured_at_utc}")
	print(f"pages_recorded={len(result.pages)} errors={len(result.errors)} out={out_root}")
	if result.errors[:5]:
		for e in result.errors[:5]:
			print("ERROR", e)
	return 0


if __name__ == "__main__":
	sys.exit(main())
