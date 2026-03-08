# Recipe Publisher (Jekyll Template)

This repository is a **template** for a GitHub Pages / Jekyll recipe website.

It includes:
- a complete Jekyll site structure (layouts, includes, assets)
- a recipe collection under `_recipes/`
- a single example recipe with an example image
- optional GitHub workflows to validate recipe PRs and generate thumbnails

You can use this template to create your own recipe website repository (instance), then replace the example recipe with your own content.

---

## Quick start (create your own site)

### 1) Create a repository from this template
On GitHub, click **Use this template** and create your new repo.

### 2) Enable GitHub Pages
In your new repo:
- **Settings → Pages**
- Set **Build and deployment** to **Deploy from a branch**
- Select branch: `main` (or whichever branch you use)
- Select folder: `/ (root)`

After a minute, your site will be available at:
`https://<your-username>.github.io/<your-repo>/`

### 3) (Optional) Custom domain
If you want a custom domain, create a `CNAME` file at the repository root containing your domain, e.g.: 
`my-recipes.example.com`

Then configure your DNS according to GitHub Pages instructions.

> This template repo intentionally does NOT ship a `CNAME` file.

---

## Content structure

### Recipes
Each recipe is a Markdown file:
- `_recipes/<slug>.md`

Each recipe has:
- YAML front matter (metadata)
- a Markdown body with:
  - `{% include recipe-meta.html %}`
  - Ingredients section
  - Steps section

### Images
Recipe images live under:
- `assets/images/<slug>/main.png` (or `main.jpg`)

---

## Contributing / Updating the template
If you fork this template and customize the theme/layout, you can keep it as your own template.
If you want to pull upstream changes later, use standard git merges.

---

## AI publishing workflow

This template is designed to support an optional AI-based publishing workflow:
- provide a recipe by voice, text, URL, or image
- generate a recipe draft in the correct format
- open a Pull Request on GitHub
- review and merge manually

Detailed setup instructions for the AI publisher are available in the `docs/` folder.

---

## License
MIT (see LICENSE).