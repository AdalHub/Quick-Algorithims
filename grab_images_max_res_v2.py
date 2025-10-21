import argparse, hashlib, os, re, sys, time
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse, urljoin
import requests
from tqdm import tqdm
from playwright.sync_api import sync_playwright

def sanitize_filename(name: str, default="image"):
    name = re.sub(r"[^\w\-\.]+", "_", name.strip()).strip("._")
    return name or default

def unique_path(outdir, base, ext):
    path = os.path.join(outdir, f"{base}{ext}")
    if not os.path.exists(path):
        return path
    i = 2
    while True:
        p = os.path.join(outdir, f"{base}_{i}{ext}")  # <- fixed quote/brace
        if not os.path.exists(p):
            return p
        i += 1

def parse_srcset(srcset: str):
    if not srcset: return []
    cands = []
    for part in srcset.split(","):
        item = part.strip()
        if not item: continue
        bits = item.split()
        url = bits[0]
        desc = bits[1] if len(bits) > 1 else ""
        width = None
        if desc.endswith("w"):
            try: width = int(desc[:-1])
            except: width = None
        elif desc.endswith("x"):
            try: width = int(float(desc[:-1]) * 1000)
            except: width = None
        cands.append((width or 0, url))
    return sorted(cands, key=lambda x: x[0], reverse=True)

def is_imgix(url: str):
    try: host = urlparse(url).netloc
    except: return False
    return "imgix.net" in host

def replace_query(url: str, **updates):
    pu = urlparse(url)
    q = dict(parse_qsl(pu.query, keep_blank_values=True))
    for k, v in updates.items():
        if v is None: q.pop(k, None)
        else: q[k] = v
    return urlunparse((pu.scheme, pu.netloc, pu.path, pu.params, urlencode(q, doseq=True), pu.fragment))

def strip_sizes(url: str):
    pu = urlparse(url)
    q = dict(parse_qsl(pu.query, keep_blank_values=True))
    for k in list(q.keys()):
        if k.lower() in {"w","h","width","height","fit"}:
            q.pop(k, None)
    return urlunparse((pu.scheme, pu.netloc, pu.path, pu.params, urlencode(q, doseq=True), pu.fragment))

def generate_imgix_candidates(url: str):
    out, seen = [], set()
    stripped = replace_query(strip_sizes(url), auto="format")
    for u in [
        stripped,
        replace_query(stripped, w="4096", fit="min", dpr="2"),
        replace_query(stripped, w="2048", fit="min", dpr="2"),
    ]:
        if u not in seen: seen.add(u); out.append(u)
    # bump width if small
    q = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
    try: w = int(q.get("w")) if q.get("w") else None
    except: w = None
    if (w or 0) < 1600:
        u = replace_query(url, w="1600")
        if u not in seen: seen.add(u); out.append(u)
    return out

def head_size(session: requests.Session, url: str, timeout=15):
    try:
        r = session.head(url, allow_redirects=True, timeout=timeout)
        r.raise_for_status()
        size = r.headers.get("Content-Length")
        if size is not None:
            return int(size), r.url
        r2 = session.get(url, stream=True, allow_redirects=True, timeout=timeout)
        r2.raise_for_status()
        size = r2.headers.get("Content-Length")
        r2.close()
        return (int(size) if size else None), r.url
    except requests.RequestException:
        return None, url

def download_file(session: requests.Session, url: str, outpath: str, timeout=30):
    with session.get(url, stream=True, allow_redirects=True, timeout=timeout) as r:
        r.raise_for_status()
        with open(outpath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: f.write(chunk)

def guess_ext_from_url(url: str):
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    return ext if ext in {".jpg",".jpeg",".png",".webp",".gif",".avif"} else ""

def guess_ext_from_ct(ct: str):
    if not ct: return ""
    ct = ct.lower().split(";")[0].strip()
    return {
        "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/png": ".png",
        "image/webp": ".webp", "image/gif": ".gif", "image/avif": ".avif",
    }.get(ct, "")

def smart_best_candidate(session, base_url, src, srcset):
    candidates = []
    for width, u in parse_srcset(srcset):
        candidates.append(urljoin(base_url, u))
    if src:
        candidates.append(urljoin(base_url, src))
    all_candidates = []
    for u in candidates or []:
        if is_imgix(u): all_candidates += generate_imgix_candidates(u)
        else: all_candidates.append(u)
    deduped, seen = [], set()
    for u in all_candidates or candidates or []:
        if u not in seen: seen.add(u); deduped.append(u)
    if not deduped: return None, None

    best_url, best_final, best_size = None, None, -1
    for u in deduped:
        size, final_u = head_size(session, u)
        if size is None:
            if best_url is None:
                best_url, best_final = u, final_u
            continue
        if size > best_size:
            best_size, best_url, best_final = size, u, final_u
    return best_url, (best_final or best_url)

def scroll_until_stable(page, pause=0.5, max_rounds=40):
    prev_count = -1
    stable_rounds = 0
    for _ in range(max_rounds):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(pause)
        count = page.evaluate("() => document.images.length")
        if count == prev_count:
            stable_rounds += 1
            if stable_rounds >= 3: break
        else:
            stable_rounds = 0
        prev_count = count

JS_COLLECT = """
(args) => {
  const { includeBackgrounds, hostFilter } = args || {};
  const urls = [];
  const add = (u, meta) => {
    if (!u || typeof u !== 'string') return;
    try {
      const url = new URL(u, location.href).href;
      if (hostFilter && !(new URL(url)).host.includes(hostFilter)) return;
      urls.push({ url, ...meta });
    } catch {}
  };
  const parseStyleBG = (styleVal) => {
    if (!styleVal) return [];
    const rx = /url\\((?:\\"([^\\"]+)\\"|'([^']+)'|([^\\)]+))\\)/g;
    let m, out = [];
    while ((m = rx.exec(styleVal)) !== null) {
      const raw = m[1] || m[2] || m[3];
      if (raw) out.push(raw.trim());
    }
    return out;
  };
  const seenNodes = new Set();
  const walk = (root) => {
    if (!root || seenNodes.has(root)) return;
    seenNodes.add(root);
    const imgs = root.querySelectorAll ? root.querySelectorAll('img,picture,source') : [];
    imgs.forEach((el) => {
      if (el.tagName === 'IMG') {
        const id = el.id || '';
        const alt = el.alt || '';
        const src = el.getAttribute('src') || '';
        const srcset = el.getAttribute('srcset') || '';
        const currentSrc = el.currentSrc || '';
        add(currentSrc || src, { kind: 'img', id, alt, srcset, src });
        if (srcset) {
          srcset.split(',').forEach(s => {
            const u = s.trim().split(/\\s+/)[0];
            add(u, { kind: 'img_srcset', id, alt, srcset, src });
          });
        }
      } else if (el.tagName === 'SOURCE') {
        const srcset = el.getAttribute('srcset') || '';
        const type = el.getAttribute('type') || '';
        if (srcset) {
          srcset.split(',').forEach(s => {
            const u = s.trim().split(/\\s+/)[0];
            add(u, { kind: 'source', type, srcset });
          });
        }
      }
    });
    if (includeBackgrounds) {
      const all = root.querySelectorAll ? root.querySelectorAll('*') : [];
      all.forEach((el) => {
        const style = getComputedStyle(el).backgroundImage;
        parseStyleBG(style).forEach(u => add(u, { kind: 'background' }));
        const inline = el.getAttribute && el.getAttribute('style');
        if (inline && /background-image/i.test(inline)) {
          parseStyleBG(inline).forEach(u => add(u, { kind: 'background_inline' }));
        }
      });
    }
    if (root.shadowRoot) walk(root.shadowRoot);
    const children = root.children || [];
    for (const c of children) if (c.shadowRoot) walk(c.shadowRoot);
  };
  walk(document);
  const seen = new Set(), out = [];
  for (const item of urls) {
    try {
      const abs = new URL(item.url, location.href).href;
      if (!seen.has(abs)) { seen.add(abs); out.push({ url: abs, meta: item }); }
    } catch {}
  }
  return out;
}
"""


def click_load_more_until_done(page, *, xpath="", text="Load More", max_clicks=200, wait_after=1.0):
    """
    Repeatedly clicks a 'Load More' button until it's gone/disabled or no new images appear.
    Prefers explicit XPath; otherwise tries by role/text and text locator fallbacks.
    """
    def button_locator():
        if xpath:
            return page.locator(f"xpath={xpath}")
        # try the most robust text-based strategies
        loc = page.get_by_role("button", name=text, exact=False)
        if loc.count() == 0:
            loc = page.locator("button", has_text=text)
        return loc

    clicks = 0
    prev_img_count = page.evaluate("() => document.images.length")

    while clicks < max_clicks:
        btn = button_locator()
        try:
            if btn.count() == 0:
                break
            # pick the first visible one, if multiple
            visible = btn.first
            if not visible.is_visible() or not visible.is_enabled():
                break

            # click and wait a moment for network/render
            visible.click()
            clicks += 1
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(wait_after)

            # did new images appear?
            new_img_count = page.evaluate("() => document.images.length")
            if new_img_count <= prev_img_count:
                # maybe lazy load needs a scroll nudge
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(wait_after)
                new_img_count = page.evaluate("() => document.images.length")

            # if still no change AND button vanished/disabled, stop
            if new_img_count <= prev_img_count:
                # check visibility again
                if btn.count() == 0 or not visible.is_visible() or not visible.is_enabled():
                    break

            prev_img_count = new_img_count

        except Exception:
            # if anything goes wrong (detached, timeout, etc.), stop safely
            break

    return clicks


def main():
    ap = argparse.ArgumentParser(description="Download max-res images from a page (DOM + Shadow DOM)")
    ap.add_argument("url", help="Target page URL")
    ap.add_argument("-o","--out", default="downloads")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--user-agent", default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    ap.add_argument("--max", type=int, default=0)
    ap.add_argument("--host-filter", default="")
    ap.add_argument("--include-backgrounds", action="store_true")
    ap.add_argument("--wait-selector", default="")
    ap.add_argument("--load-more-xpath", default="", help="XPath to the Load More button (click until exhausted)")
    ap.add_argument("--load-more-text", default="Load More", help="Button text to click if xpath not provided")
    ap.add_argument("--load-more-max", type=int, default=200, help="Safety cap on number of clicks")
    ap.add_argument("--load-more-wait", type=float, default=1.0, help="Seconds to wait after each click")

    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(user_agent=args.user_agent, viewport={"width": 1500, "height": 1100})
        page = context.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=120000)

        # click "Load More" to reveal all items first
        if args.load_more_xpath or args.load_more_text:
            clicked = click_load_more_until_done(
                page,
                xpath=args.load_more_xpath,
                text=args.load_more_text,
                max_clicks=args.load_more_max,
                wait_after=args.load_more_wait,
            )
            print(f"Clicked 'Load More' {clicked} time(s).")

        # now do a final scroll pass to hydrate any lazy images
        scroll_until_stable(page)


        if args.wait_selector:
            try: page.wait_for_selector(args.wait_selector, timeout=20000)
            except: pass
        scroll_until_stable(page)

        raw_items = page.evaluate(JS_COLLECT, {"includeBackgrounds": args.include_backgrounds, "hostFilter": args.host_filter})
        collected = []
        for it in raw_items:
            url = it.get("url") or ""
            meta = it.get("meta") or {}
            if not url: continue
            collected.append({
                "url": url,
                "src": url,
                "srcset": meta.get("srcset",""),
                "id": meta.get("id",""),
                "alt": meta.get("alt",""),
            })
        print(f"Found {len(collected)} image candidates (DOM + Shadow DOM{' + backgrounds' if args.include_backgrounds else ''}).")

        session = requests.Session()
        session.headers.update({"User-Agent": args.user_agent})

        seen_final = set()
        items = []
        base_url = page.url

        for c in collected:
            src = c["src"]
            srcset = c["srcset"]
            best, final_u = smart_best_candidate(session, base_url, src, srcset)
            if not best:
                continue
            if final_u in seen_final:
                continue
            seen_final.add(final_u)
            base_name = sanitize_filename(c["id"] or c["alt"]) or hashlib.sha1(final_u.encode("utf-8")).hexdigest()[:12]
            items.append((best, final_u, base_name))

        if args.max and len(items) > args.max:
            items = items[:args.max]

        print(f"Preparing to download {len(items)} images at max resolution…")

        for best, final_u, base_name in tqdm(items, unit="img"):
            ext = guess_ext_from_url(final_u)
            if not ext:
                try:
                    r = session.head(final_u, allow_redirects=True, timeout=args.timeout)
                    ext = guess_ext_from_ct(r.headers.get("Content-Type","")) or ".jpg"
                except:
                    ext = ".jpg"
            outpath = unique_path(args.out, base_name, ext)
            try:
                download_file(session, final_u, outpath, timeout=args.timeout)
            except requests.RequestException:
                try:
                    download_file(session, best, outpath, timeout=args.timeout)
                except requests.RequestException as e:
                    sys.stderr.write(f"\nFailed: {final_u} ({e})\n")

        browser.close()
    print(f"Done. Saved files to: {os.path.abspath(args.out)}")

if __name__ == "__main__":
    main()
