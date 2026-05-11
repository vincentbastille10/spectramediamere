# ⬡ Spectra Media AI — Landing Page

Premium AI web studio landing page for **spectramedia.online**.

---

## Stack

- Pure HTML / CSS / Vanilla JS (no build step)
- Vercel Python serverless for `/api/contact`
- Mailjet for transactional email
- Vercel-ready: push to GitHub → deploy

---

## Deploy

### 1. Push to GitHub

```bash
git init
git remote add origin https://github.com/vincentbastille10/spectramediamere.git
git add .
git commit -m "init: Spectra Media AI landing page"
git push -u origin main
```

### 2. Connect to Vercel

- Import repo from Vercel dashboard
- Framework Preset: **Other**
- Root Directory: `/`

### 3. Add Environment Variables in Vercel

| Key | Value |
|-----|-------|
| `MJ_API_KEY` | Your Mailjet API key |
| `MJ_SECRET_KEY` | Your Mailjet Secret key |

---

## Update Betty Demo

To change the demo iframe URL, edit `index.html`:

```html
<iframe
  src="https://YOUR_BETTY_DEMO_URL"
  ...
```

---

## Project Structure

```
/
  index.html         ← Main landing page
  style.css          ← All styles
  script.js          ← Interactions & form
  vercel.json        ← Vercel config
  robots.txt         ← SEO
  sitemap.xml        ← SEO
  README.md

/api/
  contact.py         ← Mailjet email endpoint

/public/
  /images/           ← Add OG image: og-cover.jpg
  /videos/           ← Optional background videos
```

---

## Customization

### Contact email
Edit `RECIPIENT_EMAIL` in `api/contact.py`.

### Colors
Edit CSS variables in `style.css` under `:root`.

### Sections
All major sections have IDs: `#studio`, `#mybetty`, `#demo`, `#contact`.

---

© 2026 Spectra Media AI
