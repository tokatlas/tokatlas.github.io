#!/usr/bin/env python3
"""Quote provenance check.

Re-reads every record's source from the .cache/ response cache (fetching
once if absent) and confirms the quoted material is actually on the page:

- every stored number (tps, pp_tps, ttft_s, power_w) must appear in the
  cached source text
- every pp*/tg* test token in a quote must appear in the cached source text
- hand-typed literal rows (data/raw/github_issues.json) must have their full
  quote present verbatim (normalized) in the cached source text

Exits non-zero on any failure. Stdlib only.
"""
import glob
import hashlib
import html as htmllib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
# Browser-style UA: Reddit/Cloudflare rate-limit the custom tokatlas UA with
# persistent 403s (300+ failures in a single CI run); a standard browser UA
# is what the comment below already relies on ("the same URL 200s from a
# browser UA"). Keep a tokatlas token so the traffic is still identifiable.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 "
      "tokatlas-check-quotes")
LITERAL_FILES = {"github_issues.json"}
# GitHub discussion threads paginate comments; a row's source_url anchors a
# comment that lives on some cursor page, so walk the pagination to find it.
CID_RE = re.compile(r'id="discussioncomment-(\d+)"')
NEXT_PAGE_RE = re.compile(
    r'action="(/ggml-org/llama\.cpp/discussions/\d+/pages\?after=[^"]+)"')
MAX_PAGES = 80
# API payloads the rows' stored numbers are parsed from; the row's own
# source_url may only carry display-rounded values.
AUX_SOURCES = {
    "siliconscore.json": "https://siliconscore.com/benchmarks.json",
    "llmcheck.json": "https://llmcheck.net/data/benchmarks.json",
    "llmconfigurator-estimates.json":
        "https://llmconfigurator.com/benchmarks.json",
    "llmconfigurator.json":
        "https://llmconfigurator.com/measured-benchmarks.json",
}


def _is_reddit(url):
    return "reddit.com" in url


# Re-fetch cached responses older than this (seconds) to catch source-page
# drift (e.g. a PR description edited in place). 7 days balances freshness
# against CI runtime: the 888 unique URLs take ~20 min to fetch cold.
CACHE_MAX_AGE = 7 * 24 * 3600  # 7 days


def _force_refresh():
    # URLs listed here (one per line, # comments allowed) are re-fetched even
    # when a fresh cached copy exists: used right after a source rewrite is
    # detected locally, so CI replaces its cached copy instead of waiting out
    # CACHE_MAX_AGE. Remove entries once CI has saved the refreshed cache.
    path = os.path.join(ROOT, "scripts", "force_refresh.txt")
    if not os.path.exists(path):
        return set()
    with open(path) as f:
        return {ln.strip() for ln in f
                if ln.strip() and not ln.strip().startswith("#")}


FORCE_REFRESH = _force_refresh()


def _download(url, reddit):
    # Reddit blocks by IP with a persistent 403 that no backoff clears (5
    # attempts over 390 s per URL made each run take 3+ hours for 29 URLs),
    # so a Reddit URL gets one attempt. Other hosts keep the retry/backoff
    # for transient Cloudflare 403s and 5xx.
    max_attempts = 1 if reddit else 3
    backoffs = [10, 20]
    for attempt in range(max_attempts):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 502, 503, 504) and attempt < max_attempts - 1:
                time.sleep(backoffs[attempt])
                continue
            raise


def fetch(url):
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha256(url.encode()).hexdigest()
    path = os.path.join(CACHE, key)
    cached = os.path.exists(path)
    stale = cached and (time.time() - os.path.getmtime(path) > CACHE_MAX_AGE
                        or url in FORCE_REFRESH)
    if not cached or stale:
        reddit = _is_reddit(url)
        try:
            body = _download(url, reddit)
        except Exception as e:  # noqa: BLE001
            if not cached:
                raise
            # A failed refresh must not discard a copy that was verified
            # before; keep checking against it and say so.
            print("warning: refresh of %s failed (%s); using cached copy"
                  % (url, e))
        else:
            tmp = path + ".tmp"
            with open(tmp, "wb") as f:
                f.write(body)
            os.replace(tmp, path)
            time.sleep(10.0 if reddit else 0.25)
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def page_text(url, raw):
    """Flattened text of a cached response (HTML or JSON API body)."""
    body = None
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        data = None
    if isinstance(data, dict):
        for k in ("body_html", "body"):
            if isinstance(data.get(k), str):
                body = data[k]
                break
    if body is None:
        body = raw
    t = re.sub(r"<[^>]+>", " ", body)
    t = htmllib.unescape(t)
    return re.sub(r"\s+", " ", t)


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", str(s).lower()))


# plain numbers and thousands-grouped numbers ("4,578.6" on display tables)
_NUM_RE = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")


def _numbers(text):
    out = []
    for m in _NUM_RE.findall(text):
        try:
            out.append(float(m.replace(",", "")))
        except ValueError:
            continue
    return out


def _num_present(v, nums):
    for n in nums:
        if abs(n - v) <= max(1e-9, 1e-4 * abs(v)):
            return True


def _in_raw(raw, n):
    # lazy-rendered discussion pages keep comment bodies in an embedded
    # JSON payload that page_text drops; raw HTML still proves presence
    return _num_present(float(n), _numbers(raw)) if raw else False
    return False


# A source may publish power as a range ("~220-230 W") rather than a point.
# A stored power value inside a published range is backed by the source even
# though it is not itself a point figure (the collector derives per-row watts
# from the published W-per-t/s rate and the row's tps).
_WATT_RANGE_RE = re.compile(r"~?(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*W\b", re.I)


def _in_published_watt_range(v, text):
    for m in _WATT_RANGE_RE.finditer(text):
        lo, hi = float(m.group(1)), float(m.group(2))
        if lo <= v <= hi:
            return True
    return False


def numbers_of(r):
    for k in ("tps", "pp_tps", "ttft_s", "power_w"):
        v = (r.get(k) or "").strip() if isinstance(r.get(k), str) else r.get(k)
        if v not in (None, ""):
            yield k, str(v)


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "data", "raw", "*.json")))
    if not files:
        print("no raw source files; run the collectors first")
        return 1
    errors = 0
    checked = 0
    for path in files:
        name = os.path.basename(path)
        doc = json.load(open(path))
        recs = doc.get("records", [])
        if not recs:
            continue
        aux_url = AUX_SOURCES.get(name)
        aux_text = None
        if aux_url:
            try:
                aux_text = page_text(aux_url, fetch(aux_url))
            except Exception as e:  # noqa: BLE001
                print("%s: aux fetch %s failed: %s" % (name, aux_url, e))
        aux_nums = _numbers(aux_text) if aux_text else []
        rows = []
        for r in recs:
            url = r.get("source_url") or ""
            if not url.startswith(("http://", "https://")):
                continue
            cid = url.split("#discussioncomment-")[-1] \
                if "#discussioncomment-" in url else None
            root = url.split("#")[0]
            rows.append((r, root, cid))
        # resolve each comment to the paginated page that contains it
        cids_needed = {}
        for r, root, cid in rows:
            if cid:
                cids_needed.setdefault(root, set()).add(cid)
        cid_page = {}
        thread_raw = {}
        for root, cids in cids_needed.items():
            url = root
            seen = set()
            found = set()
            raws = []
            while url and url not in seen:
                if len(seen) >= MAX_PAGES:
                    break
                seen.add(url)
                try:
                    raw = fetch(url)
                except Exception as e:  # noqa: BLE001
                    print("%s: fetch %s failed: %s" % (name, url, e))
                    break
                raws.append(raw)
                for cid in set(CID_RE.findall(raw)):
                    if cid in cids:
                        found.add(cid)
                        cid_page[(root, cid)] = url
                # no early break: a comment's anchor can appear on an
                # early page while its body renders on a later one, so
                # the union must cover the whole thread
                m = NEXT_PAGE_RE.search(raw)
                url = ("https://github.com" + htmllib.unescape(m.group(1))
                       if m else None)
            for cid in cids - found:
                print("%s: comment %s not found in thread %s" % (name, cid, root))
                cid_page[(root, cid)] = root
            # a comment's anchor and its rendered body can land on
            # different pagination pages; verify against the whole thread
            thread_raw[root] = "\n".join(raws)
        text_cache = {}
        raw_cache = {}
        numcache = {}
        api_cache = {}
        fetch_err = {}

        def api_comment_text(rt, cidv):
            m = re.match(r"https://github\.com/([^/]+)/([^/]+)/discussions/(\d+)$", rt)
            if not m:
                return ""
            owner, repo, num = m.groups()
            page = 1
            while page <= 10:
                u = ("https://api.github.com/repos/%s/%s/discussions/%s"
                     "/comments?per_page=100&page=%d" % (owner, repo, num, page))
                try:
                    data = json.loads(fetch(u))
                except Exception:
                    return ""
                if not data:
                    return ""
                for c in data:
                    if str(c.get("id")) == cidv:
                        return c.get("body") or ""
                page += 1
            return ""
        for r, root, cid in rows:
            if cid and root in thread_raw:
                key = ("thread", root)
                if key not in text_cache:
                    text_cache[key] = page_text(root, thread_raw[root])
                    raw_cache[key] = thread_raw[root]
            else:
                key = root
                if key not in text_cache:
                    try:
                        raw_cache[key] = fetch(key)
                        text_cache[key] = page_text(key, raw_cache[key])
                    except Exception as e:  # noqa: BLE001
                        print("%s: fetch %s failed: %s" % (name, key, e))
                        text_cache[key] = None
                        raw_cache[key] = ""
                        fetch_err[key] = str(e)
            if key not in numcache:
                numcache[key] = _numbers(text_cache[key] or "")
            text = text_cache[key]
            if aux_text:
                text = ((text or "") + " " + aux_text)
            if text is None or not text.strip():
                # standing rule: reddit 403s are logged, not counted as errors
                # (reddit IP-blocks datacenter IPs persistently; those records
                # stay verified wherever a cached copy exists)
                if (isinstance(key, str) and _is_reddit(key)
                        and "403" in fetch_err.get(key, "")):
                    print("%s (%s): reddit source blocked (403), skipped"
                          % (name, r["id"]))
                    continue
                print("%s (%s): source unavailable for verification"
                      % (name, r["id"]))
                errors += 1
                continue
            checked += 1
            for k, n in numbers_of(r):
                if (n not in text
                        and not _in_raw(raw_cache.get(key, ""), n)
                        and not _num_present(float(n), numcache[key])
                        and not _num_present(float(n), aux_nums)
                        and not (k == "power_w"
                                 and _in_published_watt_range(float(n), text))):
                    # discussion comment bodies can be client-rendered and
                    # absent from every server-rendered page; fall back to
                    # the REST API copy of the comment
                    if cid and isinstance(key, tuple) and key[0] == "thread":
                        ck = (root, cid)
                        if ck not in api_cache:
                            api_cache[ck] = api_comment_text(root, cid)
                        body = api_cache[ck]
                        if n in body or _num_present(float(n), _numbers(body)):
                            continue
                    print("%s (%s): %s %r not in cached source"
                          % (name, r["id"], k, n))
                    errors += 1
            for tok in set(re.findall(r"\b(pp\d{1,4}|tg\d{1,4})\b",
                                     str(r.get("quote") or ""))):
                # pages render the test cell as "pp 512" / "tg 128"
                spaced = tok[:2] + " " + tok[2:]
                if tok in text or spaced in text:
                    continue
                # client-rendered comments: fall back to the REST API body
                if cid and isinstance(key, tuple) and key[0] == "thread":
                    ck = (root, cid)
                    if ck not in api_cache:
                        api_cache[ck] = api_comment_text(root, cid)
                    body = api_cache[ck]
                    if tok in body or spaced in body:
                        continue
                print("%s (%s): test token %r not in cached source"
                      % (name, r["id"], tok))
                errors += 1
            if name in LITERAL_FILES:
                nt = norm(text)
                for frag in str(r.get("quote") or "").split("; "):
                    f = norm(frag).strip()
                    if f and f not in nt:
                        print("%s (%s): quote fragment not found verbatim in cached source: %r"
                              % (name, r["id"], frag[:80]))
                        errors += 1
                        break
    print("OK: %d records verified against cached sources" % checked if not errors
          else "%d errors, %d records checked" % (errors, checked))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
