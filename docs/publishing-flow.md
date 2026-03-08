# Publishing Flow

This document describes the intended end-to-end publishing flow for recipe sites built from this template.

## Goal

The system should let a user provide a recipe conversationally and publish it with minimal manual effort while preserving repository structure and review control.

The publishing workflow should support:

- audio input
- text input
- URL-based ingestion
- optional image upload
- optional generated image

The result should be a Pull Request that the user merges manually.

---

## High-level flow

1. Intake
2. Extraction
3. Normalization
4. Validation
5. Clarification
6. Approval
7. GitHub write operations
8. Pull Request
9. Manual merge
10. GitHub Pages deployment

---

## 1. Intake

The user may provide:

- spoken instructions or a voice note
- plain text
- a URL to an existing recipe
- an image to use as the main recipe image
- a request to generate a recipe image

Audio should be transcribed before extraction.

---

## 2. Extraction

If the source is a URL, the system should fetch the page and attempt to extract:

- title
- ingredients
- steps
- servings
- prep time
- cook time
- author

Preferred extraction order:

1. structured metadata
2. semantically marked HTML
3. heuristic fallback extraction

The extracted recipe should then be normalized into the template’s schema.

---

## 3. Normalization

The recipe must be converted into the repository format:

### Files
- `_recipes/<slug>.md`
- `assets/images/<slug>/main.<ext>`

### Recipe front matter
- layout
- title
- meal_type
- Chef
- portions
- prep_time_minutes
- cook_time_minutes
- image
- video
- ingredients

### Body
- metadata include
- ingredients section
- steps section
- optional notes

The slug must be normalized to lowercase ASCII kebab-case.

---

## 4. Validation

Before any GitHub write operation, the recipe must pass validation.

### Hard validation
Must pass before branch creation or file writing:
- title present
- valid slug
- valid meal_type
- Chef.person present
- portions / prep / cook are integers
- ingredients non-empty
- correct image path and extension
- body includes metadata include and recipe sections
- at least two steps
- for create mode, recipe file does not already exist

### Soft validation
Ask the user only when necessary:
- oven temperature missing for a baking recipe
- servings missing
- timing missing and materially important
- source author unclear
- instructions too vague to be useful

---

## 5. Clarification

If required, ask the smallest number of questions needed to complete the recipe cleanly.

Examples:
- “How many servings?”
- “What oven temperature should I use?”
- “Should I attribute this to the site author or to you?”

---

## 6. Approval

Before opening the Pull Request, the system should show a concise final summary:

- title
- slug
- language
- meal type
- Chef attribution
- portions
- prep/cook times
- image name and extension
- ingredient count
- step count

The user must explicitly confirm with:

`APPROVE PR`

No PR should be opened before this confirmation.

---

## 7. GitHub write operations

After approval, the system should:

1. read the latest `main` branch SHA
2. create a new branch
3. create or update the recipe Markdown file
4. create or update the image file
5. open a Pull Request to `main`

Branch naming convention:
- new recipe: `recipe/<slug>`
- edit: `recipe-edit/<slug>`

---

## 8. Pull Request

The Pull Request should contain:

- recipe title
- a short summary of what was created or changed
- assumptions made, if any
- source attribution
- URL if relevant

One recipe should correspond to one PR.

---

## 9. Manual merge

The user reviews and merges manually in GitHub.

No automatic merge is part of the intended system.

---

## 10. Deployment

After merge:

- GitHub Pages rebuilds the live site
- any post-merge workflows can run
- the recipe becomes visible on the live site

This template is intentionally designed around a single canonical live website, not preview environments.

---

## Edit flow

Editing an existing recipe follows the same pattern with one important difference:

- changes should be minimal and targeted

The edit flow is:

1. read existing recipe
2. parse front matter and body
3. apply requested change
4. validate again
5. show a diff summary
6. request `APPROVE PR`
7. open PR

---

## Design principles

The publishing flow is based on these principles:

- deterministic output over creative variation
- minimal manual cleanup
- repository conventions are the source of truth
- single-site deployment model
- manual merge for control