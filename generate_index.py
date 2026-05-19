"""Read repo-manifest.yml files and generate category index pages for MkDocs."""

import yaml
from pathlib import Path
from collections import defaultdict

MANIFESTS_DIR = Path("manifests")
DOCS_DIR = Path("docs")

CATEGORIES = {
    "analysis_type": {
        "dir": "by-analysis",
        "labels": {
            "cost-effectiveness": "Cost-Effectiveness Analysis",
            "budget-impact": "Budget Impact Analysis",
            "burden-of-disease": "Burden of Disease",
            "epidemiology": "Epidemiology",
            "literature-review": "Literature Review",
            "data-pipeline": "Data Pipeline",
            "utility": "Utility / Reusable Code",
        },
    },
    "methods": {
        "dir": "by-method",
        "labels": {
            "markov": "Markov Model",
            "decision-tree": "Decision Tree",
            "survival": "Survival Analysis",
            "regression": "Regression",
            "descriptive": "Descriptive Statistics",
            "other": "Other",
        },
    },
    "language": {
        "dir": "by-language",
        "labels": {
            "R": "R",
            "Python": "Python",
            "Stata": "Stata",
            "Excel": "Excel",
            "mixed": "Mixed",
        },
    },
}


def load_manifests():
    repos = []
    if not MANIFESTS_DIR.exists():
        return repos
    for f in sorted(MANIFESTS_DIR.glob("*.yml")):
        with open(f) as fh:
            data = yaml.safe_load(fh) or {}
        data["_repo"] = f.stem
        repos.append(data)
    return repos


def repo_line(repo):
    name = repo.get("name") or repo["_repo"]
    desc = repo.get("description", "")
    repo_name = repo["_repo"]
    github_url = f"https://github.com/GitHEE-UMCU/{repo_name}"
    docs_index = DOCS_DIR / repo_name / "index.md"

    link = f"[{name}](../{repo_name}/index.md)" if docs_index.exists() else f"[{name}]({github_url})"
    status = repo.get("status", "active")
    status_tag = f" _{status}_" if status != "active" else ""
    contact = f" · _{repo['contact']}_" if repo.get("contact") else ""

    return f"- {link}{status_tag} — {desc}{contact}"


def generate_category_pages(repos):
    for field, config in CATEGORIES.items():
        out_dir = DOCS_DIR / config["dir"]
        out_dir.mkdir(parents=True, exist_ok=True)

        grouped = defaultdict(list)
        for repo in repos:
            values = repo.get(field) or []
            if isinstance(values, str):
                values = [values]
            for v in values:
                grouped[v].append(repo)

        for key, label in config["labels"].items():
            page_repos = sorted(grouped.get(key, []), key=lambda r: (r.get("name") or r["_repo"]).lower())
            lines = [f"# {label}\n"]
            if page_repos:
                lines += [repo_line(r) for r in page_repos]
            else:
                lines.append("_No repositories tagged with this category yet._")
            (out_dir / f"{key}.md").write_text("\n".join(lines) + "\n")


def generate_all_repos_page(repos):
    lines = ["# All Repositories\n"]
    if repos:
        for repo in sorted(repos, key=lambda r: (r.get("name") or r["_repo"]).lower()):
            lines.append(repo_line(repo))
    else:
        lines.append("_No repositories found._")
    (DOCS_DIR / "all-repos.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    repos = load_manifests()
    generate_category_pages(repos)
    generate_all_repos_page(repos)
    print(f"Generated index pages for {len(repos)} repositories.")
