# ICC JAPAN Website - Cloudflare Pages Deployment Guide

## 📁 Project Structure

```
iccjpn-site/
├── index.html          # Main page (SEO optimized)
├── css/
│   └── style.css       # Stylesheet (responsive)
├── js/
│   └── main.js         # JavaScript (animations & forms)
├── images/
│   └── favicon.svg     # Favicon
├── robots.txt          # For search engines
├── sitemap.xml         # Sitemap
├── DEPLOYMENT.md       # This file (Japanese)
├── DEPLOYMENT_EN.md    # This file (English)
└── SEO-CHECKLIST.md    # SEO Checklist
```

---

## 🚀 How to Deploy to Cloudflare Pages

### Method 1: GitHub Integration (Recommended)

#### Step 1: Create GitHub Repository

```bash
cd ~/projects/iccjpn-site

# Initialize Git
git init
git add .
git commit -m "Initial commit: ICC JAPAN website"

# Create repository on GitHub and push
# After creating repository at https://github.com/new:
git remote add origin https://github.com/YOUR_USERNAME/iccjpn-site.git
git branch -M main
git push -u origin main
```

#### Step 2: Create Project on Cloudflare Pages

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Left menu → Click **Pages**
3. Click **Create a project**
4. Select **Connect to Git**
5. Connect GitHub account (first time only)
6. Select `iccjpn-site` repository
7. Settings:
   - **Project name**: `iccjpn`
   - **Production branch**: `main`
   - **Build command**: (leave empty)
   - **Build output directory**: `/`
8. Click **Save and Deploy**

After deployment completes, the site will be accessible at `iccjpn.pages.dev`.

---

### Method 2: Direct Upload (Simple)

1. [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Pages**
2. **Create a project** → **Direct Upload**
3. Project name: `iccjpn`
4. **Upload assets** → Drag & drop all files from `iccjpn-site` folder
5. Click **Deploy site**

---

## 🌐 Custom Domain Setup (iccjpn.com)

### Prerequisites
- `iccjpn.com` is managed by Cloudflare DNS
- Or you can configure DNS records at another registrar

### Step 1: Add Domain in Cloudflare Pages

1. Pages project → **Custom domains** tab
2. Click **Set up a custom domain**
3. Enter `iccjpn.com`
4. Click **Activate domain**

### Step 2: DNS Configuration (if using Cloudflare DNS)

Configured automatically. If manual setup needed:

```
Type: CNAME
Name: @
Content: iccjpn.pages.dev
Proxy: On (orange cloud)
```

Also set up www subdomain:

```
Type: CNAME
Name: www
Content: iccjpn.pages.dev
Proxy: On
```

### Step 3: www → apex Redirect Setup

1. Cloudflare Dashboard → `iccjpn.com` → **Rules** → **Redirect Rules**
2. **Create rule**:
   - **Rule name**: `www to apex`
   - **When**: Hostname equals `www.iccjpn.com`
   - **Then**: Dynamic redirect to `https://iccjpn.com${http.request.uri.path}`
   - **Status code**: 301

---

## 📧 Contact Form Setup

### Formspree (Recommended - Free Tier Available)

1. Create account at [Formspree](https://formspree.io/)
2. Create new form
3. Get form ID (e.g., `xpzgdqwe`)
4. Update form action in `index.html`:

```html
<form action="https://formspree.io/f/xpzgdqwe" method="POST">
```

### Other Options
- **Cloudflare Workers**: Serverless email sending
- **Netlify Forms**: If using Netlify
- **Google Forms**: Embedded form

---

## 🔍 Google Search Console Setup

### Step 1: Add Property

1. Go to [Google Search Console](https://search.google.com/search-console/)
2. **Add property** → `https://iccjpn.com`
3. **Verify ownership** → DNS record (recommended) or HTML tag

### Step 2: Submit Sitemap

1. Search Console → **Sitemaps**
2. Enter `sitemap.xml` and submit

---

## 📊 Google Analytics Setup

### Step 1: Create GA4 Property

1. Go to [Google Analytics](https://analytics.google.com/)
2. **Admin** → **Create Property**
3. Get measurement ID (G-XXXXXXXXXX)

### Step 2: Add Code

Add this right before `</head>` in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## ⚡ Performance Optimization (Cloudflare Settings)

### Enable Auto Optimization

1. Cloudflare Dashboard → **Speed** → **Optimization**
2. Enable the following:
   - **Auto Minify**: Check JavaScript, CSS, HTML all
   - **Brotli**: Enable compression
   - **Early Hints**: Enable
   - **Rocket Loader**: Enable experimentally (disable if issues occur)

### Cache Settings

1. **Caching** → **Configuration**
2. **Browser Cache TTL**: 1 month
3. **Always Online**: Enable

---

## ✅ Post-Deployment Checklist

- [ ] Site displays at `https://iccjpn.com`
- [ ] `https://www.iccjpn.com` redirects to `iccjpn.com`
- [ ] SSL certificate is active (🔒 icon visible)
- [ ] Displays correctly on mobile
- [ ] Contact form works
- [ ] Google Search Console ownership verified
- [ ] Sitemap submitted
- [ ] Google Analytics is working

---

## 🔧 How to Update

### If using GitHub integration
```bash
# Commit changes
git add .
git commit -m "Update: describe changes"
git push
```
→ Deploys automatically

### If using direct upload
1. Pages → project → **Create new deployment**
2. Upload updated files

---

## 📞 Support

If you encounter any issues, refer to Cloudflare documentation:
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Custom Domains](https://developers.cloudflare.com/pages/platform/custom-domains/)
