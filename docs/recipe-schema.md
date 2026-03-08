# Recipe Schema

This document defines the canonical recipe structure used by this template.

All recipes generated manually or through the Recipe Publisher should conform to this schema.

---

## Repository paths

### Recipe Markdown file

```text
_recipes/<slug>.md
```

### Main image file

```text
assets/images/<slug>/main.png
```

or

```text
assets/images/<slug>/main.jpg
```

Generated images should default to `main.png`.

Uploaded images should preserve their extension:
- png -> `main.png`
- jpg/jpeg -> `main.jpg`

---

## Slug rules

The slug is derived from the recipe title unless explicitly specified.

It must be:
- lowercase
- ASCII only
- kebab-case

Valid pattern:

```text
[a-z0-9]+(-[a-z0-9]+)*
```

Examples:
- `gateau-amandes`
- `banana-bread`
- `salade-de-lentilles`

---

## Front matter schema

Each recipe file must include YAML front matter.

### Required fields

```yaml
layout: page
title: <string>

meal_type: <enum>

Chef:
  person: <string>
  note: <string>

portions: <int>
prep_time_minutes: <int>
cook_time_minutes: <int>

image:
  path: /assets/images/<slug>/main.<ext>
  thumbnail: /assets/images/<slug>/main.<ext>
  photos:
    - /assets/images/<slug>/main.<ext>

video:
  type: youtube
  url: ""

ingredients:
  - name: <string>
    quantity: <string>
    unit: <string>
    note: <string>
```

---

## Allowed `meal_type` values

```text
Entrée
Plat
Dessert
Goûter
Petit-déjeuner
Apéritif
Boisson
```

---

## Ingredient object shape

Each ingredient must be an object with the following keys:
- `name`
- `quantity`
- `unit`
- `note`

Example:

```yaml
ingredients:
  - name: Flour
    quantity: "200"
    unit: "g"
    note: ""
  - name: Eggs
    quantity: "2"
    unit: ""
    note: ""
```

This structure is plain text metadata only.
It does not imply icons, pictograms, emojis, or visual ingredient substitution.

---

## Body structure

After front matter, the recipe body must contain:
1. a blank line
2. the metadata include
3. the recipe sections in the recipe language

### Required include

```liquid
{% include recipe-meta.html %}
```

### Required sections

In French, typically:

```md
## Ingrédients
- ...

## Étapes
1. ...
2. ...
```

In English, for example:

```md
## Ingredients
- ...

## Steps
1. ...
2. ...
```

### Optional section

```md
## Notes
...
```

Only include notes when useful.

---

## Example recipe

```md
---
layout: page
title: Banana Bread
meal_type: Dessert
Chef:
  person: Example Author
  note: ""
portions: 8
prep_time_minutes: 15
cook_time_minutes: 50
image:
  path: /assets/images/banana-bread/main.png
  thumbnail: /assets/images/banana-bread/main.png
  photos:
    - /assets/images/banana-bread/main.png
video:
  type: youtube
  url: ""
ingredients:
  - name: Flour
    quantity: "250"
    unit: "g"
    note: ""
  - name: Bananas
    quantity: "3"
    unit: ""
    note: "ripe"
  - name: Eggs
    quantity: "2"
    unit: ""
    note: ""
---

{% include recipe-meta.html %}

## Ingredients
- 250 g flour
- 3 ripe bananas
- 2 eggs

## Steps
1. Preheat the oven to 180°C.
2. Mash the bananas.
3. Mix all ingredients together.
4. Pour into a loaf tin.
5. Bake for about 50 minutes.
```

---

## Validation expectations

A recipe is considered valid when:
- required front matter fields are present
- types and structure match expectations
- the image path matches the actual image filename
- the body contains the metadata include
- the body contains an ingredients section
- the body contains a steps section
- there are at least two steps

---

## Canonical rendering model

Recipes in this template use:
- `layout: page`
- `recipe-meta.html` as a metadata include
- Markdown body for the main content