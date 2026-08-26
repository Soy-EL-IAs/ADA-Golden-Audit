import re

with open('ada_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Library to sidebar
sidebar_runs = r'(<a href="#" class="nav-link" data-target="runs"><i class="fas fa-history"></i> Runs</a>)'
library_link = r'\1\n                <a href="#" class="nav-link" data-target="library"><i class="fas fa-images"></i> Library</a>'
html = re.sub(sidebar_runs, library_link, html)

# Modify Dashboard to include Library stats
# I'll just append it to the dashboard-overview row
dashboard_row = r'(<div class="row mb-4" id="dashboard-overview">.*?</div>)'
lib_stats = '''
<div class="col-md-3">
    <div class="card bg-dark text-white mb-3">
        <div class="card-body">
            <h5 class="card-title text-muted text-uppercase text-sm">Library</h5>
            <h2 class="card-text mb-0" id="dash-lib-assets">0</h2>
            <p class="text-muted text-sm mb-0">Assets across <span id="dash-lib-chars">0</span> characters</p>
        </div>
    </div>
</div>
'''
html = re.sub(r'(<div class="row mb-4" id="dashboard-overview">.*?)</div>\s*<div class="card', r'\1' + lib_stats + r'</div>\n        <div class="card', html, flags=re.DOTALL)

# Add Library Tab Content
runs_tab = r'(<div id="runs" class="view-section d-none">.*?</div>\s*<!-- RUN DETAIL -->)'
library_tab = '''
<div id="library" class="view-section d-none">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Asset Library</h2>
        <div>
            <button class="btn btn-outline-light btn-sm me-2" onclick="loadLibrary()"><i class="fas fa-sync"></i> Refresh</button>
            <button class="btn btn-primary btn-sm" onclick="rebuildLibraryIndex()"><i class="fas fa-cogs"></i> Rebuild Index</button>
        </div>
    </div>
    
    <!-- Character Collections -->
    <div class="mb-4">
        <h4>Character Collections</h4>
        <div class="d-flex gap-2 flex-wrap" id="library-characters">
            <!-- Badges -->
        </div>
    </div>
    
    <!-- Filters -->
    <div class="d-flex gap-2 mb-3">
        <button class="btn btn-sm btn-outline-light active" data-lib-filter="all" onclick="filterLibrary('all')">All</button>
        <button class="btn btn-sm btn-outline-light" data-lib-filter="favorites" onclick="filterLibrary('favorites')">Favorites <i class="fas fa-star text-warning"></i></button>
        <button class="btn btn-sm btn-outline-light" data-lib-filter="rejected" onclick="filterLibrary('rejected')">Rejected</button>
    </div>
    
    <!-- Asset Grid -->
    <div class="row g-3" id="library-grid">
        <!-- Cards -->
    </div>
</div>

<!-- ASSET DETAIL MODAL -->
<div class="modal fade" id="assetDetailModal" tabindex="-1">
  <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
    <div class="modal-content bg-dark text-light">
      <div class="modal-header border-secondary">
        <h5 class="modal-title" id="assetDetailTitle">Asset Detail</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body" id="assetDetailBody">
        <!-- Injected via JS -->
      </div>
      <div class="modal-footer border-secondary">
        <button type="button" class="btn btn-outline-warning" id="btn-fav-asset" onclick="toggleFavAsset()"><i class="fas fa-star"></i> Favorite</button>
        <button type="button" class="btn btn-outline-danger" id="btn-rej-asset" onclick="toggleRejAsset()"><i class="fas fa-times"></i> Reject</button>
      </div>
    </div>
  </div>
</div>
'''
html = re.sub(runs_tab, library_tab + r'\n\1', html, flags=re.DOTALL)

with open('ada_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
