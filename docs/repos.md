# Repository Index

<div class="repo-filters">
  <input type="text" id="repo-search" placeholder="Search by name or description…" oninput="filterRepos()">
  <select id="filter-analysis" onchange="filterRepos()"><option value="">All analysis types</option></select>
  <select id="filter-method" onchange="filterRepos()"><option value="">All methods</option></select>
  <select id="filter-language" onchange="filterRepos()"><option value="">All languages</option></select>
</div>

<table id="repo-table">
<thead><tr><th>Repository</th><th>Description</th><th>Analysis Type</th><th>Method</th><th>Language</th><th>Status</th></tr></thead>
<tbody>
</tbody></table>

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
</script>
