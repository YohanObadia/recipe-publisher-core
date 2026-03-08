
---

## `docs/github-app-setup.md`

```md
# GitHub App Setup

This document explains how to set up a GitHub App so the Recipe Publisher GPT can create branches, write recipe files, and open Pull Requests.

## Purpose

The GitHub App is the automation identity used by the GPT to interact with a site repository.

It should be able to:

- read repository contents
- create or update files
- create Pull Requests

It should **not** merge PRs automatically.

## Why use a GitHub App

A GitHub App is preferable to a personal access token when possible because:

- permissions are narrower and easier to audit
- it can be installed only on selected repositories
- it does not directly reuse your personal account token
- it issues short-lived installation tokens

## Required permissions

When creating the GitHub App, grant only these repository permissions:

- **Contents**: Read and write
- **Pull requests**: Read and write

No other permissions are required for the publishing workflow.

## Step-by-step setup

### 1. Create the GitHub App

In GitHub:

- go to **Settings**
- go to **Developer settings**
- go to **GitHub Apps**
- click **New GitHub App**

Recommended values:

- **GitHub App name**: `recipe-publisher`
- **Homepage URL**: use your repository URL or project URL
- **Webhook**: disable unless you need it later

### 2. Configure repository permissions

Under **Repository permissions**, set:

- Contents → Read and write
- Pull requests → Read and write

### 3. Set installation scope

Install the app only on the repositories that should accept recipe PRs.

Example:
- your personal recipe site repo

### 4. Generate a private key

Inside the app settings:

- generate a private key
- download the `.pem` file
- store it securely

You will also need:

- the **App ID**
- the **Installation ID** for each installed repository

## What the GPT or integration layer needs

To use the GitHub App, your automation layer must:

1. create a JWT signed with the app private key
2. exchange that JWT for an installation token
3. call GitHub’s REST API using the installation token

## Required GitHub operations

The publisher workflow needs to perform these actions:

- read the latest SHA of `main`
- create a new branch from `main`
- create or update:
  - `_recipes/<slug>.md`
  - `assets/images/<slug>/main.<ext>`
- open a Pull Request to `main`

## Recommended branch naming

For new recipes:
- `recipe/<slug>`

For recipe edits:
- `recipe-edit/<slug>`

## Safety rules

The GitHub App should be used with these operating rules:

- never push directly to `main`
- never merge automatically
- create one recipe per PR
- limit writes to:
  - `_recipes/`
  - `assets/images/`
  - optionally `.github/` when intentionally updating workflows

## Manual merge model

The intended deployment flow is:

1. GPT opens PR
2. you review and merge manually
3. GitHub Pages rebuilds the site from `main`

This keeps a single live website and avoids preview complexity.

## Optional next step

If you later want to support multiple instance repos, install the same GitHub App on each of them.
The GPT can then work across all of your recipe sites while using the same permission model.