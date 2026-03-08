---
layout: page
title: "Toutes les recettes"
permalink: /recettes/
---


{% assign all_recipes = site.recipes | sort: 'title' %}
{% assign meal_types = "Entrée,Plat,Dessert,Goûter,Petit-déjeuner,Apéritif,Boisson" | split: "," %}

{% for meal in meal_types %}
  {% assign group = all_recipes | where: "meal_type", meal %}
  {% if group.size > 0 %}
  <h2>{{ meal }}{% if meal == "Plat" %}s{% endif %}</h2>
  <ul class="recipe-list">
    {% for recipe in group %}
      <li class="recipe-list-item">
        <a href="{{ recipe.url | relative_url }}">
          {{ recipe.title }}
        </a>
        <span class="recipe-list-meta">
          {% if recipe.Chef and recipe.Chef.person %}
            – de {{ recipe.Chef.person }}
          {% endif %}
          {% if recipe.portions %}
            · {{ recipe.portions }} pers.
          {% endif %}
          {% if recipe.prep_time_minutes %}
            · {{ recipe.prep_time_minutes }} min prép.
          {% endif %}
        </span>
      </li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %}

{% comment %}
On pourrait ajouter une catégorie "Autres" si certaines recettes n'ont pas de meal_type
en parcourant all_recipes et en filtrant via where_exp, mais pour l’instant on suppose
que chaque recette est bien catégorisée.
{% endcomment %}
