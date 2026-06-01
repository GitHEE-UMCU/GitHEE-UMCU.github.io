"""Read repo-manifest.yml files and generate a filterable repository index page."""

import yaml
from pathlib import Path

MANIFESTS_DIR = Path("manifests")
DOCS_DIR = Path("docs")

ANALYSIS_LABELS = {
    "cost-effectiveness": "Cost-Effectiveness",
    "budget-impact": "Budget Impact",
    "burden-of-disease": "Burden of Disease",
    "epidemiology": "Epidemiology",
    "literature-review": "Literature Review",
    "data-pipeline": "Data Pipeline",
    "utility": "Utility",
}

METHOD_LABELS = {
    "markov": "Markov Model",
    "decision-tree": "Decision Tree",
    "survival": "Survival Analysis",
    "regression": "Regression",
    "descriptive": "Descriptive Statistics",
    "other": "Other",
}

LANGUAGE_LABELS = {
    "R": "R",
    "Python": "Python",
    "Stata": "Stata",
    "Excel": "Excel",
    "mixed": "Mixed",
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


def as_list(val):
    if not val:
        return []
    return [val] if isinstance(val, str) else list(val)


def tags_html(values, labels):
    if not values:
        return "<em>—</em>"
    return " ".join(
        f'<span class="repo-tag">{labels.get(v, v)}</span>' for v in values
    )


def generate_repos_page(repos):
    all_analysis = sorted({v for r in repos for v in as_list(r.get("analysis_type"))})
    all_methods = sorted({v for r in repos for v in as_list(r.get("methods"))})
    all_languages = sorted({v for r in repos for v in as_list(r.get("language"))})

    parts = ['# Repository Index\n']

    # Filter controls
    parts.append('<div class="repo-filters">')
    parts.append(
        '  <input type="text" id="repo-search" placeholder="Search by name or description…" oninput="filterRepos()">'
    )

    def select_html(elem_id, label, values, labels_map):
        opts = [f'<option value="">{label}</option>']
        opts += [f'<option value="{v}">{labels_map.get(v, v)}</option>' for v in values]
        return f'  <select id="{elem_id}" onchange="filterRepos()">{"".join(opts)}</select>'

    parts.append(select_html("filter-analysis", "All analysis types", all_analysis, ANALYSIS_LABELS))
    parts.append(select_html("filter-method", "All methods", all_methods, METHOD_LABELS))
    parts.append(select_html("filter-language", "All languages", all_languages, LANGUAGE_LABELS))
    parts.append('</div>\n')

    # Table
    parts.append('<table id="repo-table">')
    parts.append(
        "<thead><tr>"
        "<th>Repository</th><th>Description</th>"
        "<th>Analysis Type</th><th>Method</th><th>Language</th><th>Status</th>"
        "</tr></thead>"
    )
    parts.append("<tbody>")

    for repo in sorted(repos, key=lambda r: (r.get("name") or r["_repo"]).lower()):
        repo_name = repo["_repo"]
        name = repo.get("name") or repo_name
        desc = repo.get("description", "")
        github_url = f"https://github.com/GitHEE-UMCU/{repo_name}"
        docs_index = DOCS_DIR / repo_name / "index.md"

        # Use root-relative path for internal docs; absolute GitHub URL otherwise.
        # Root-relative works from any page depth, unlike ../ which is page-dependent.
        if docs_index.exists():
            link_url = f"../{repo_name}/"
            link_extra = ""
        else:
            link_url = github_url
            link_extra = ' target="_blank" rel="noopener"'

        analysis = as_list(repo.get("analysis_type"))
        methods = as_list(repo.get("methods"))
        languages = as_list(repo.get("language"))
        status = repo.get("status", "active")

        parts.append(
            f'<tr'
            f' data-analysis="{" ".join(analysis)}"'
            f' data-method="{" ".join(methods)}"'
            f' data-language="{" ".join(languages)}"'
            f' data-name="{name.lower()}"'
            f' data-desc="{desc.lower()}">'
        )
        parts.append(f'<td><a href="{link_url}"{link_extra}>{name}</a></td>')
        parts.append(f"<td>{desc}</td>")
        parts.append(f"<td>{tags_html(analysis, ANALYSIS_LABELS)}</td>")
        parts.append(f"<td>{tags_html(methods, METHOD_LABELS)}</td>")
        parts.append(f"<td>{tags_html(languages, LANGUAGE_LABELS)}</td>")
        parts.append(f"<td>{status}</td>")
        parts.append("</tr>")

    parts.append("</tbody></table>\n")

    # Client-side filtering — rows shown/hidden via data attributes
    parts.append("""\
<script>
function filterRepos() {
  var search   = document.getElementById('repo-search').value.toLowerCase();
  var analysis = document.getElementById('filter-analysis').value;
  var method   = document.getElementById('filter-method').value;
  var language = document.getElementById('filter-language').value;

  document.querySelectorAll('#repo-table tbody tr').forEach(function(row) {
    var rowAnalysis  = (row.dataset.analysis  || '').split(' ');
    var rowMethod    = (row.dataset.method    || '').split(' ');
    var rowLanguage  = (row.dataset.language  || '').split(' ');
    var rowName      = row.dataset.name  || '';
    var rowDesc      = row.dataset.desc  || '';

    var ok =
      (!search   || rowName.includes(search) || rowDesc.includes(search)) &&
      (!analysis || rowAnalysis.includes(analysis)) &&
      (!method   || rowMethod.includes(method)) &&
      (!language || rowLanguage.includes(language));

    row.style.display = ok ? '' : 'none';
  });
}
</script>""")

    (DOCS_DIR / "repos.md").write_text("\n".join(parts) + "\n")


if __name__ == "__main__":
    repos = load_manifests()
    generate_repos_page(repos)
    print(f"Generated repository index for {len(repos)} repositories.")
