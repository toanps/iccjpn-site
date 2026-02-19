# agent.md — iccjpn-site

## What This Is
Static company website for **株式会社ICC JAPAN** — Vietnamese engineer recruitment to Japan.
Targets Japanese employers (hiring managers, HR). No Vietnamese version needed.

**Live URL:** https://iccjpn.com
**GitHub repo:** https://github.com/toanps/iccjpn-site.git
**Hosting:** Cloudflare Pages (auto-deploys on `git push` to `main`)

---

## Project Structure

```
iccjpn-site/
├── index.html          # Main page (homepage)
├── faq.html            # FAQ page
├── news.html           # News page
├── 404.html            # Custom 404
├── css/style.css       # All styles (responsive)
├── js/main.js          # Animations, form handling, success state
├── images/
│   ├── logo.png        # Company logo
│   ├── og-image.jpg    # OG image 1200×630px (for social share)
│   └── favicon.svg     # Favicon
├── robots.txt          # Search engine crawl rules
├── sitemap.xml         # All 3 pages + priorities
├── _redirects          # Cloudflare Pages redirects (www → apex 301)
├── _headers            # Cloudflare Pages HTTP headers
├── DEPLOYMENT.md       # Deploy guide (Japanese)
├── DEPLOYMENT_EN.md    # Deploy guide (English) ← read this first
├── SEO-CHECKLIST.md    # SEO status + remaining owner actions
└── agent.md            # This file
```

---

## Deployment

**Platform: Cloudflare Pages** (NOT Netlify)

```bash
# Deploy = just push to GitHub
git add .
git commit -m "describe change"
git push
# → Cloudflare Pages auto-deploys within ~30 seconds
```

See `DEPLOYMENT_EN.md` for first-time setup (GitHub → Cloudflare Pages connection).

---

## Company Info

| Field | Value |
|-------|-------|
| Company | 株式会社ICC JAPAN |
| Representative | 代表取締役 カオ テイ トウ |
| Address | 〒560-0051 大阪府豊中市永楽荘1－9－21 |
| Phone | 06-6152-8838 |
| Contact email | contact@iccjpn.com |
| Founded | 2019年3月8日 |
| Capital | 5,000,000円 |
| Staff | 3名 |
| License | 有料職業事業紹介許可番号 27-ユ-302779 |
| Pricing | 初期費用25万円（税別）+ サポート費月額2万円（税別・1年間） |

---

## Tech Stack

- Pure HTML/CSS/JS — no framework, no build step
- Google Fonts (Noto Sans JP)
- Schema.org JSON-LD (Organization + EmploymentAgency)
- Google Analytics 4: **G-J0CHSYTLVM** ✅ (added 2026-02-19)
- Contact form: Formspree (⚠️ see below — needs form ID)

---

## Contact Form Status ⚠️ ACTION NEEDED

The form in `index.html` currently uses a placeholder:

```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

**To activate:**
1. Sign up at https://formspree.io (free tier: 50 submissions/month)
2. Create a new form → set notification email to `contact@iccjpn.com`
3. Copy the form ID (looks like `xabcd123`)
4. Replace `YOUR_FORM_ID` in `index.html` line ~527
5. Push to GitHub → deployed

**Form features already in place:**
- `_next` redirect → `/?success=true` (shows success message on page)
- `_subject` → "【ICC JAPAN】お問い合わせ"
- `_gotcha` honeypot (spam protection)
- Success div (`#formSuccess`) shown by JS when `?success=true` in URL

---

## SEO Work Done (2026-02-19)

### All pages (index, faq, news)
- ✅ Canonical tags
- ✅ hreflang (ja)
- ✅ Open Graph tags (og:title, og:description, og:image, og:url)
- ✅ Twitter Card tags
- ✅ GA4 snippet (G-J0CHSYTLVM)
- ✅ JS loaded with `defer`

### index.html
- ✅ Hero image: lazy-load + width/height dimensions
- ✅ Copyright updated to 2025
- ✅ FAQ/News links in footer
- ✅ Canonical tag

### faq.html
- ✅ FAQPage JSON-LD schema (rich results)
- ✅ Improved meta description
- ✅ Footer sitemap links

### news.html
- ✅ Improved meta description
- ✅ Footer sitemap links

### 404.html
- ✅ `noindex, nofollow`

### sitemap.xml
- ✅ Rewritten: all 3 pages, lastmod, priority

### OG Image
- ✅ `images/og-image.jpg` — 1200×630px dark navy, ICC JAPAN branding

---

## Remaining Owner Actions

| Task | Priority | Notes |
|------|----------|-------|
| Replace `YOUR_FORM_ID` in index.html | 🔴 HIGH | Formspree signup required |
| Google Search Console registration | 🔴 HIGH | Submit sitemap.xml |
| Replace GA4 measurement ID | ✅ Done | G-J0CHSYTLVM |
| Google Business Profile | 🟡 MED | Local SEO boost |
| Deploy to Cloudflare Pages | 🔴 HIGH | Push repo to GitHub, connect CF Pages |

---

## History

| Date | What Changed |
|------|-------------|
| 2026-02-06 | Logo, address update (豊中市), representative name, company details, pricing overhaul |
| 2026-02-19 | Full SEO audit (Opus 4.6): OG tags, canonical, hreflang, JSON-LD schemas, sitemap, GA4 |
| 2026-02-19 | GA4 real ID (G-J0CHSYTLVM) added to all 3 pages |
| 2026-02-19 | Contact form: reverted Netlify Forms → Formspree (site is Cloudflare Pages, not Netlify) |

---

## Key Rules for Future Work

1. **Deployment = Cloudflare Pages** — never Netlify, never GitHub Pages
2. **Contact form = Formspree** — not Netlify Forms (Netlify-specific, won't work on CF Pages)
3. **Language = Japanese only** — no Vietnamese version, targets Japanese employers
4. **No build step** — pure static files, edit HTML/CSS/JS directly
5. **Always `git push` after edits** — Cloudflare auto-deploys
6. **SEO-CHECKLIST.md** — keep it updated when making changes
7. **Do not change company info** (name, address, pricing) without confirming with Toan

---

## Useful Commands

```bash
cd ~/projects/iccjpn-site

# Check what's changed
git status
git diff

# Deploy
git add -A && git commit -m "your message" && git push

# Find text across all HTML files
grep -rn "search term" *.html

# Validate sitemap
cat sitemap.xml

# Check SEO status
cat SEO-CHECKLIST.md
```
