# Hosting Hannah's f1r3lang site on GitHub Pages

## 1. What is actually in the repo

`F1R3FLY-io/f1r3lang-io.github.io` is at a single commit (`faee214`) on `main`, 5.5 MB,
holding seven sibling directories:

```
f1r3beat-panels/  f1r3ink/  f1r3lang/  f1r3pix/  f1r3sidechat/  f1r3skein/  finding-mind/
```

The root `README.md` still describes the repo as *"F1R3GAMES — Review"* — a design-review
staging area. There is no root `index.html`, no `CNAME`, no `.nojekyll`.

`f1r3lang/` is Hannah's site, 276 KB, six pages:

| file | what it is |
|---|---|
| `index.html` | home — the SELECT-FROM-WHERE-**DO** hook, pillars, lineage |
| `language.html` | the developer tour: writes, the SQL translation table, witnessed transactions, RSpace |
| `get-started.html` | Docker node, first contract, docs links |
| `research.html` | the research programme — three rungs, generated conditions, graded where-clauses |
| `ecosystem.html` | node, interpreter, editors, LSP, community |
| `developers.html` | 153 KB — the whole of *for the Working Software Developer* rendered as HTML |

plus `css/styles.css` (all styles, brand tokens in `:root`), `js/main.js` (mobile nav +
scroll reveal), and `images/` (the `f1r3lang-logo-v1.svg` wordmark, and three legacy
Rholang logos her README marks as deletable).

`developers.html` is the piece built from what you supplied: it is
`publications/MeTTaIL4WorkingDev` as a web page, and it carries the positioning discipline
her README records — MeTTaIL never appears in copy, only in linked repo paths, and the
quantum reading stays fenced.

**The site is in good shape to publish as-is.** Every path in it is relative. There is not
one leading-slash reference in any HTML, CSS or JS file, and every local asset referenced
resolves. That means the directory relocates anywhere — repo root, subdirectory, another
repo — without a single edit.

Her README and the `og:url` on the home page both already name the target: **f1r3lang.ai**.

---

## 2. The one thing that will break the build

`f1r3lang/developers.html`, line 1303:

```html
<td style="text-align: left;"><code>{% P %}[s]</code></td>
```

GitHub Pages runs Jekyll by default. Jekyll's Liquid parser reads `{% P %}` as a tag,
finds no such tag, and **fails the build** — the deploy goes red and the page never
appears. The notation is correct and should not be changed; the fix is to turn Jekyll off
with an empty `.nojekyll` file at the site root.

The same applies repo-wide if you publish the current repo unchanged:
`f1r3beat-panels/gradient-draft.html` has 81 JSX `{{...}}` expressions that Liquid will
also try to evaluate.

This is the single most likely cause of an unexplained failed deploy here. Everything
else below is arrangement; this one is a blocker.

---

## 3. The two constraints that decide the arrangement

**A custom domain applies to a whole Pages site, at its root.** The `CNAME` file holds one
hostname and the settings page has one field. Whatever domain you attach, it serves
everything in that repo from `/`.

**This repo is not an organization site.** A user or org Pages site must be named
`<owner>.github.io` — for `F1R3FLY-io` that is `f1r3fly-io.github.io`, which already
exists as a separate repo (the Jekyll "Concurrency for the People" site). The name
`f1r3lang-io.github.io` matches nothing, so GitHub treats it as an ordinary project repo
and publishes it at:

```
https://f1r3fly-io.github.io/f1r3lang-io.github.io/
```

with Hannah's site one level further down, at `.../f1r3lang-io.github.io/f1r3lang/`.

Put those together and publishing from the current repo gives you a choice of two bad
outcomes. Attach `f1r3lang.ai` to it and the domain root 404s (there is no root
`index.html`), the language site sits at `f1r3lang.ai/f1r3lang/`, and `f1r3lang.ai/f1r3ink/`,
`/f1r3skein/`, `/finding-mind/` all serve unrelated design comps under the language's
domain. Don't attach a domain, and the public URL is a 40-character path with a redundant
`.github.io` inside it.

---

## 4. Recommended: give f1r3lang its own repo

`F1R3FLY-io/f1r3lang` is free — checked. This is the same shape as the Finding Mind
answer, and for the same reason: **one property, one repo, one domain.** Leave
`f1r3lang-io.github.io` doing what its README says it does — review and staging.

### Step 1 — create the repo and put the site at its root

The contents of `f1r3lang/` go at the **root**, so `index.html` sits next to `css/`,
`js/` and `images/`.

```bash
gh repo create F1R3FLY-io/f1r3lang --public
git clone https://github.com/F1R3FLY-io/f1r3lang.git
cd f1r3lang
cp -r /path/to/f1r3lang/. .          # the prepared directory shipped with this note
```

### Step 2 — run the finalizer

If you use the prepared directory, this is already done for `f1r3lang.ai`. Re-run it for
any other domain:

```bash
python3 deploy/finalize.py f1r3lang.ai --site .
```

It writes `.nojekyll`, `CNAME`, `404.html`, `robots.txt`, `sitemap.xml`, and inserts
`<link rel="canonical">`, `og:url`, `og:site_name` and a favicon link into all six pages.
It is idempotent and marked — its block is fenced in `<!-- deploy:begin -->` comments — so
you can run it again after any content change without accumulating duplicates. It leaves
Hannah's hand-written `og:title` and `og:description` on the home page alone and only
supplies those tags where a page lacks them.

Add `--drop-rholang-logos` when you want the three legacy SVGs gone.

### Step 3 — push and turn Pages on

```bash
git add -A && git commit -m "f1r3lang site" && git push
```

Then **Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**.

Wait for the green check on the deploy, and confirm the site loads at
`https://f1r3fly-io.github.io/f1r3lang/` **before** touching DNS. Debugging a broken build
and a half-propagated domain at the same time is avoidable.

### Step 4 — DNS

At the registrar for `f1r3lang.ai`, for the apex:

```
A     @    185.199.108.153
A     @    185.199.109.153
A     @    185.199.110.153
A     @    185.199.111.153
```

and, for IPv6, the matching AAAA records `2606:50c0:8000::153` through
`2606:50c0:8003::153`. Keep the A records even if you add AAAA. If your provider sets a
default apex record automatically, delete it first.

For `www`:

```
CNAME  www   f1r3fly-io.github.io.
```

Note the target is the **org**, not the repo — `f1r3fly-io.github.io`, with the trailing
dot. GitHub resolves which repo from the `CNAME` file.

### Step 5 — attach the domain and force HTTPS

**Settings → Pages → Custom domain → `f1r3lang.ai` → Save.** GitHub runs a DNS check and
commits the `CNAME` file itself; since the repo already has one with the same value this
is a no-op, but pull afterwards so local and remote agree.

Wait for the certificate — usually minutes, up to 24 hours — then tick **Enforce HTTPS**.
Do not tick it before the certificate provisions or the site goes unreachable in the gap.

Verify:

```bash
curl -sI https://f1r3lang.ai | head -1
curl -sI https://www.f1r3lang.ai | head -1
curl -s https://f1r3lang.ai/developers.html | head -3
```

---

## 5. If you would rather keep one repo

Workable, with three additions. Do them in this order.

1. **`.nojekyll` at the repo root.** Non-negotiable — see §2, and note that
   `finding-mind/_src/` would also be silently dropped from the output under Jekyll,
   because Jekyll excludes underscore-prefixed directories.

2. **A root `index.html`** listing the properties. Right now the Pages root is a 404, and
   whatever domain you attach inherits it.

3. **Decide what the domain is for.** If `f1r3lang.ai` is attached here it covers the
   games comps and the book too. That is defensible only if you rename the repo to
   something neutral (`f1r3fly-web`, say) and treat the domain as a portal — but then
   f1r3lang lives at `/f1r3lang/`, not at the root, and the `og:url` and canonical tags
   need that path.

The cleanest version of "one repo" is: keep it domainless as the review staging area at
`f1r3fly-io.github.io/f1r3lang-io.github.io/`, and fork each property out to its own repo
as it ships. That is what §4 does, and it is what you will end up doing for Finding Mind
anyway.

---

## 6. Keeping the site and the paper in sync

`developers.html` is a rendering of `publications/MeTTaIL4WorkingDev`. Nothing links the
two — if the paper changes, the page silently goes stale. Worth deciding now whether that
page is a **snapshot** (date it in the byline and let it drift) or a **build artifact**
(generate it from the LaTeX on each revision). Hannah's other five pages are hand-written
prose and have no such coupling.

---

## 7. Open questions

1. **`f1r3lang.ai`, confirmed?** It is in her README and in the home page's `og:url`, but
   nothing in the repo proves the domain is registered to you. The canonical host goes
   into `CNAME`, into every canonical tag, into `sitemap.xml` and `robots.txt`, and into
   every link anyone ever shares — changing it later is cheap in the files and expensive
   everywhere else.

2. **Other f1r3lang domains?** If you hold `f1r3lang.io`, `.com` or similar, the shape is
   the one from the Finding Mind note: one canonical domain serves the site, the rest
   301-redirect to it, path-preserving. Cloudflare Redirect Rules do this properly and
   free; registrar URL forwarding varies in quality and some providers only issue a 302 or
   drop the path.

3. **The favicon is a placeholder.** The finalizer points it at
   `images/f1r3lang-logo-v1.svg`, which is a wordmark and will be illegible at 16 px.
   Worth one line to Hannah asking for a mark.

4. **`developers.html` is not in the nav.** It is linked from three body positions but not
   from the header, so a visitor who does not scroll will not find the deepest page on the
   site. Deliberate, or an oversight?

5. **Six pages, one social card.** There is no `og:image` anywhere, so every share of
   every page renders as a bare text link. One 1200×630 image would fix all six.
