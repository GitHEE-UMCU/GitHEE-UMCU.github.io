# How to Add Your Repository

Every repository in the GitHEE-UMCU organization can contribute its documentation to this site. Here's how.

---

## Step 1 — Create your repo from the template

When creating a new GitHub repository, select **`repo-template`** as the template. This gives you the correct folder structure and automated workflows out of the box.

---

## Step 2 — Fill out repo-manifest.yml

Open `repo-manifest.yml` in the root of your repo and fill in the fields:

| Field | What to write |
|-------|---------------|
| `name` | Short human-readable name |
| `description` | One sentence: what the repo does |
| `analysis_type` | Pick from the list below |
| `methods` | Pick from the list below |
| `language` | R, Python, Stata, Excel, or mixed |
| `contact` | Your name or email |
| `status` | `active`, `archived`, or `prototype` |

### Allowed values

**analysis_type**

| Value | Meaning |
|-------|---------|
| `cost-effectiveness` | Economic evaluation comparing costs and outcomes |
| `budget-impact` | Estimating financial impact of a policy or intervention |
| `burden-of-disease` | Quantifying disease prevalence, incidence, or impact |
| `epidemiology` | Studying disease distribution and determinants |
| `literature-review` | Systematic or narrative review of existing evidence |
| `data-pipeline` | Cleaning, linking, or transforming data |
| `utility` | Reusable functions, tools, or templates |

**methods**

| Value | Meaning |
|-------|---------|
| `markov` | State-transition Markov model |
| `decision-tree` | Decision tree / decision analytic model |
| `survival` | Survival or time-to-event analysis |
| `regression` | Regression modelling (any type) |
| `descriptive` | Descriptive statistics or reporting |
| `other` | Anything else |

---

## Step 3 — Write docs/index.md

This file becomes the landing page for your repo on this site. A template is already provided when you create from `repo-template`.

If you skip this step, your `README.md` is used as a fallback.

---

## How updates work

Push to `main` — the site updates automatically within a few minutes. No manual steps needed.

The workflow triggers on changes to:

- `README.md`
- `docs/**`
- `repo-manifest.yml`

---

## Questions?

See the [organization contributing guide](https://github.com/GitHEE-UMCU/.github/blob/main/CONTRIBUTING.md) or contact the organization admin.
