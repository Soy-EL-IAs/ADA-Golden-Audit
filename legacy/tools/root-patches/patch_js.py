import re

with open('ada_app/static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update initTabs to handle data-target for a tags instead of li
tabs_init = r'''function initTabs() {
    const tabs = document.querySelectorAll(".sidebar .nav-link");
    tabs.forEach(tab => {
        tab.addEventListener("click", (e) => {
            e.preventDefault();
            document.querySelectorAll(".sidebar .nav-link").forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".view-section").forEach(c => c.classList.add("d-none"));
            tab.classList.add("active");
            document.getElementById(tab.dataset.target).classList.remove("d-none");
            
            if (tab.dataset.target === "library") {
                loadLibrary();
            }
        });
    });
}
'''
js = re.sub(r'function initTabs\(\) \{.*?\n\}\n', tabs_init, js, flags=re.DOTALL)

# Update loadRuns to match RunInfo schema
load_runs = r'''async function loadRuns() {
    try {
        const res = await fetch("/api/runs");
        const runs = await res.json();
        const tbody = document.querySelector("#runs-table tbody");
        if (!tbody) return;
        tbody.innerHTML = "";

        runs.forEach(run => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${run.run_id}</td>
                <td><span class="badge bg-secondary">${run.run_type}</span></td>
                <td>${run.character || 'Unknown'}</td>
                <td>${run.source_model || 'Unknown'}</td>
                <td>${run.pipeline_stage || run.status}</td>
                <td>${run.created_at}</td>
                <td><button class="btn btn-sm btn-outline-light btn-open" data-id="${run.run_id}">View</button></td>
            `;
            tbody.appendChild(tr);
        });

        document.querySelectorAll(".btn-open").forEach(btn => {
            btn.addEventListener("click", (e) => {
                openRun(e.target.dataset.id);
            });
        });

        if (runs.length > 0) {
            const last = runs[0];
            const detailsEl = document.getElementById("last-run-details");
            if (detailsEl) {
                detailsEl.innerHTML = `
                    <p class="mb-1"><strong>ID:</strong> ${last.run_id}</p>
                    <p class="mb-1"><strong>Model:</strong> ${last.source_model}</p>
                    <p class="mb-0"><strong>Status:</strong> ${last.status}</p>
                `;
            }
            const btnOpen = document.getElementById("btn-open-last-run");
            if(btnOpen) btnOpen.dataset.id = last.run_id;
            loadCreativeLabRun(last.run_id);
        } else {
            const detailsEl = document.getElementById("last-run-details");
            if(detailsEl) detailsEl.innerHTML = "<p>No runs found.</p>";
        }
    } catch (e) {
        console.error("Failed to load runs", e);
    }
}'''
js = re.sub(r'async function loadRuns\(\) \{.*?\n\}\n(?=\nlet creativeLabConcepts)', load_runs, js, flags=re.DOTALL)

# Add loadLibrary and asset functions
library_js = r'''
let allAssets = [];
let currentAssetDetail = null;

async function loadLibrary() {
    try {
        const res = await fetch("/api/library/assets");
        allAssets = await res.json();
        
        // Update Dashboard Stats if we are loading library
        document.getElementById("dash-lib-assets").textContent = allAssets.length;
        const chars = new Set(allAssets.map(a => a.character));
        document.getElementById("dash-lib-chars").textContent = chars.size;
        
        renderLibraryCharacters(chars);
        filterLibrary('all');
    } catch (e) {
        console.error("Failed to load library", e);
    }
}

async function rebuildLibraryIndex() {
    try {
        await fetch("/api/library/build_index", { method: "POST" });
        await loadLibrary();
    } catch (e) {
        console.error("Failed to rebuild library", e);
    }
}

function renderLibraryCharacters(chars) {
    const cont = document.getElementById("library-characters");
    if (!cont) return;
    cont.innerHTML = `<button class="btn btn-sm btn-primary char-filter active" data-char="all" onclick="filterLibraryChar('all')">All Characters</button>`;
    chars.forEach(c => {
        if (!c || c === "Unknown") return;
        cont.innerHTML += `<button class="btn btn-sm btn-outline-primary char-filter" data-char="${c}" onclick="filterLibraryChar('${c}')">${c}</button>`;
    });
}

let activeLibFilter = 'all';
let activeCharFilter = 'all';

function filterLibrary(filter) {
    activeLibFilter = filter;
    document.querySelectorAll("[data-lib-filter]").forEach(b => b.classList.remove("active"));
    document.querySelector(`[data-lib-filter="${filter}"]`).classList.add("active");
    renderLibraryGrid();
}

function filterLibraryChar(char) {
    activeCharFilter = char;
    document.querySelectorAll(".char-filter").forEach(b => b.classList.remove("active", "btn-primary"));
    document.querySelectorAll(".char-filter").forEach(b => b.classList.add("btn-outline-primary"));
    const btn = document.querySelector(`.char-filter[data-char="${char}"]`);
    if(btn) {
        btn.classList.remove("btn-outline-primary");
        btn.classList.add("active", "btn-primary");
    }
    renderLibraryGrid();
}

function renderLibraryGrid() {
    const grid = document.getElementById("library-grid");
    if (!grid) return;
    grid.innerHTML = "";
    
    let filtered = allAssets.filter(a => {
        if (activeCharFilter !== 'all' && a.character !== activeCharFilter) return false;
        if (activeLibFilter === 'favorites' && !a.favorite) return false;
        if (activeLibFilter === 'rejected' && a.favorite) return false; // Simple logic: not fav
        return true;
    });
    
    filtered.forEach(a => {
        const col = document.createElement("div");
        col.className = "col-md-3";
        col.innerHTML = `
            <div class="card bg-dark border-secondary h-100 asset-card">
                <img src="/api/image?path=${encodeURIComponent(a.thumbnail_path)}" class="card-img-top" style="height: 200px; object-fit: cover; cursor: pointer;" onclick="openAssetDetail('${a.asset_id}')">
                <div class="card-body p-2">
                    <div class="d-flex justify-content-between align-items-start">
                        <h6 class="card-title text-truncate mb-1" title="${a.character}">${a.character}</h6>
                        ${a.favorite ? '<i class="fas fa-star text-warning"></i>' : ''}
                    </div>
                    <p class="card-text text-muted small text-truncate" style="max-height: 40px; overflow: hidden;" title="${a.concept_snapshot}">${a.concept_snapshot}</p>
                </div>
                <div class="card-footer p-2 border-secondary d-flex justify-content-between">
                    <span class="badge bg-${a.final_review_verdict === 'PASS' ? 'success' : 'secondary'}">${a.final_review_verdict || 'UNKNOWN'}</span>
                    <button class="btn btn-xs btn-outline-light" onclick="openAssetDetail('${a.asset_id}')">Open</button>
                </div>
            </div>
        `;
        grid.appendChild(col);
    });
}

function openAssetDetail(asset_id) {
    const asset = allAssets.find(a => a.asset_id === asset_id);
    if (!asset) return;
    currentAssetDetail = asset;
    
    document.getElementById("assetDetailTitle").textContent = `${asset.character} - ${asset.asset_id}`;
    
    // Setup modal buttons
    const favBtn = document.getElementById("btn-fav-asset");
    const rejBtn = document.getElementById("btn-rej-asset");
    if (asset.favorite) {
        favBtn.classList.replace("btn-outline-warning", "btn-warning");
        favBtn.innerHTML = '<i class="fas fa-star"></i> Favorited';
    } else {
        favBtn.classList.replace("btn-warning", "btn-outline-warning");
        favBtn.innerHTML = '<i class="fas fa-star"></i> Favorite';
    }
    
    let compareHtml = '';
    if (asset.illustrious_image && asset.full_image_path) {
        compareHtml = `
            <h5 class="mt-4 mb-3">Compare</h5>
            <div class="row">
                <div class="col-md-6">
                    <h6>Illustrious (Base)</h6>
                    <img src="/api/image?path=${encodeURIComponent(asset.illustrious_image)}" class="img-fluid rounded">
                </div>
                <div class="col-md-6">
                    <h6>Klein (Refined)</h6>
                    <img src="/api/image?path=${encodeURIComponent(asset.full_image_path)}" class="img-fluid rounded">
                </div>
            </div>
        `;
    }
    
    const body = document.getElementById("assetDetailBody");
    body.innerHTML = `
        <div class="row">
            <div class="col-md-8">
                <img src="/api/image?path=${encodeURIComponent(asset.full_image_path)}" class="img-fluid rounded mb-3 w-100">
                ${compareHtml}
            </div>
            <div class="col-md-4">
                <h5>Concept</h5>
                <p class="text-muted small">${asset.concept_snapshot}</p>
                
                <h5 class="mt-4">Provenance</h5>
                <ul class="list-unstyled text-muted small">
                    <li><strong>Source Run:</strong> ${asset.source_run_id}</li>
                    <li><strong>Creative Model:</strong> ${asset.creative_model}</li>
                    <li><strong>Concept ID:</strong> ${asset.concept_id}</li>
                    <li><strong>Created At:</strong> ${asset.created_at}</li>
                </ul>
                
                <h5 class="mt-4">Pipeline Status</h5>
                <div class="d-flex align-items-center mb-3">
                    <span class="badge bg-success">IDEA</span> <i class="fas fa-arrow-right mx-1 text-muted"></i>
                    <span class="badge bg-success">ILLUSTRIOUS</span> <i class="fas fa-arrow-right mx-1 text-muted"></i>
                    <span class="badge bg-success">KLEIN</span> <i class="fas fa-arrow-right mx-1 text-muted"></i>
                    <span class="badge bg-success">FINAL</span>
                </div>
                
                <h5 class="mt-4">Final Review</h5>
                <div class="alert alert-${asset.final_review_verdict === 'PASS' ? 'success' : 'warning'} p-2 small">
                    <strong>Verdict:</strong> ${asset.final_review_verdict || 'UNKNOWN'}<br>
                    ${asset.final_review && asset.final_review.summary ? asset.final_review.summary : 'No review details available.'}
                </div>
            </div>
        </div>
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('assetDetailModal'));
    modal.show();
}

async function toggleFavAsset() {
    if (!currentAssetDetail) return;
    const isFav = !currentAssetDetail.favorite;
    
    await fetch(`/api/library/review/${currentAssetDetail.asset_id}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({status: isFav ? "Favorite" : "None"})
    });
    
    currentAssetDetail.favorite = isFav;
    openAssetDetail(currentAssetDetail.asset_id);
    renderLibraryGrid();
}

async function toggleRejAsset() {
    if (!currentAssetDetail) return;
    await fetch(`/api/library/review/${currentAssetDetail.asset_id}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({status: "Reject"})
    });
    currentAssetDetail.favorite = false;
    openAssetDetail(currentAssetDetail.asset_id);
    renderLibraryGrid();
}
'''
js = js + "\n" + library_js

with open('ada_app/static/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
