// ADA 1.0 — App.js
// Product-first UI with Mission support, Library-first experience, and Command Bar

let currentRun = null;
let currentMission = null;
let pollInterval = null;
let missionPollInterval = null;
const ACTIVE_MISSION_STATUSES = new Set(['CREATED', 'WAITING_FOR_GPU', 'RUNNING', 'PLANNING', 'GENERATING_CONCEPTS', 'PRODUCING', 'RECOVERING']);

// ==================== NAVIGATION ====================
document.querySelectorAll('.sidebar li').forEach(li => {
    li.addEventListener('click', () => {
        const tab = li.dataset.tab;
        if (tab !== 'library' && typeof clearLibrarySelection === 'function') clearLibrarySelection();
        document.querySelectorAll('.sidebar li').forEach(l => l.classList.remove('active'));
        li.classList.add('active');
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        const el = document.getElementById(tab);
        if (el) el.classList.add('active');
        
        if (tab === 'home') loadHome();
        if (tab === 'library') loadLibrary();
        if (tab === 'characters') loadCharacterCatalog();
        if (tab === 'create') loadCharacters();
        if (tab === 'model-lab') loadModelLab();
        if (tab === 'runs') loadRuns();
        if (tab === 'roadmap') loadRoadmap();
        if (tab === 'settings') loadSettings();
    });
});

function switchTab(tabName) {
    if (tabName !== 'library' && typeof clearLibrarySelection === 'function') clearLibrarySelection();
    document.querySelectorAll('.sidebar li').forEach(l => {
        l.classList.toggle('active', l.dataset.tab === tabName);
    });
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    const el = document.getElementById(tabName);
    if (el) el.classList.add('active');
}

// ==================== HOME ====================
async function loadHome() {
    loadActiveMissions();
    loadRecentAssets();
    loadCollectionsSummary();
}

async function loadActiveMissions() {
    const container = document.getElementById('active-missions-container');
    const details = document.getElementById('active-missions-details');
    const count = document.getElementById('active-missions-count');
    const expanded = localStorage.getItem('ada-active-missions-expanded');
    if (expanded !== null) details.open = expanded === '1';
    try {
        const resp = await fetch('/api/missions');
        const missions = await resp.json();
        
        if (!missions || missions.length === 0) {
            count.textContent = '0';
            container.innerHTML = '<p style="color:var(--text-secondary)">No missions yet. Use the command bar or Create tab to start.</p>';
            return;
        }
        const activeCount = missions.filter(m => ACTIVE_MISSION_STATUSES.has(m.status)).length;
        count.textContent = activeCount ? `${activeCount} in progress · ${missions.length} total` : `${missions.length} total`;
        
        container.innerHTML = '';
        missions.forEach(m => {
            const pct = Math.round((m.progress || 0) * 100);
            const isActive = ACTIVE_MISSION_STATUSES.has(m.status);
            const isRecoverable = m.status === 'PARTIAL' || m.status === 'FAILED';
            
            const card = document.createElement('div');
            card.className = 'mission-card';
            card.onclick = () => openMissionDetail(m.mission_id);
            
            card.innerHTML = `
                <div class="flex-between">
                    <h4>${m.character} — ${m.requested_assets} final images</h4>
                    <span class="badge ${isActive ? 'info' : m.status === 'COMPLETE' ? 'online' : 'warning'}">${m.status}</span>
                </div>
                <div class="mission-progress-bar">
                    <div class="mission-progress-fill ${m.status === 'COMPLETE' ? 'complete' : ''}" style="width:${pct}%"></div>
                </div>
                <div class="mission-status">
                    ${m.approved_assets} / ${m.requested_assets} approved
                    ${m.current_stage_detail ? ` · ${m.current_stage_detail}` : ''}
                    ${isRecoverable ? ' · <strong style="color:var(--warning)">Recoverable</strong>' : ''}
                </div>
            `;
            container.appendChild(card);
        });
    } catch (e) {
        count.textContent = '';
        container.innerHTML = '<p style="color:var(--text-secondary)">Could not load missions.</p>';
    }
}

document.getElementById('active-missions-details')?.addEventListener('toggle', event => {
    localStorage.setItem('ada-active-missions-expanded', event.currentTarget.open ? '1' : '0');
});

async function loadRecentAssets() {
    const grid = document.getElementById('recent-assets-grid');
    try {
        const resp = await fetch('/api/library/assets?visible_only=true');
        const assets = await resp.json();
        
        if (!assets || assets.length === 0) {
            grid.innerHTML = '<p style="color:var(--text-secondary)">No assets yet. Create a mission to generate images.</p>';
            return;
        }
        
        grid.innerHTML = '';
        const timestamp = asset => Date.parse(asset.generated_at || asset.created_at || '') || 0;
        assets.sort((a, b) => timestamp(b) - timestamp(a)).slice(0, 8).forEach(a => {
            grid.appendChild(createAssetCard(a));
        });
    } catch (e) {
        grid.innerHTML = '';
    }
}

async function loadCollectionsSummary() {
    const grid = document.getElementById('collections-grid');
    try {
        const resp = await fetch('/api/library/collections');
        const collections = await resp.json();
        
        grid.innerHTML = '';
        const summaries = Object.values(collections).sort((a, b) =>
            (a.display_name || a.collection_id || '').localeCompare(b.display_name || b.collection_id || '')
        );
        for (const summary of summaries) {
            const collectionId = summary.collection_id || '';
            const displayName = summary.display_name || collectionId;
            const characterCount = Number(summary.character_count || 0);
            const imageCount = Number(summary.total_images || 0);
            const card = document.createElement('div');
            card.className = 'collection-card';
            card.onclick = () => openLibraryCollection(collectionId);
            card.innerHTML = `
                <h4>${escapeHtml(displayName)}</h4>
                <div class="collection-card-meta">
                    <span>${characterCount} ${characterCount === 1 ? 'character' : 'characters'}</span>
                    <span>${imageCount} ${imageCount === 1 ? 'image' : 'images'}</span>
                </div>
            `;
            grid.appendChild(card);
        }
        
        if (Object.keys(collections).length === 0) {
            grid.innerHTML = '<p style="color:var(--text-secondary)">Collections will appear as you create assets.</p>';
        }
    } catch (e) {}
}

// ==================== CHARACTERS ====================
let characterCatalog = [];
let characterCatalogFilter = 'all';

function catalogDisplayLabel(value) {
    const raw = String(value || 'Unknown');
    if (!/^[a-z0-9_()\-]+$/.test(raw)) return raw;
    return raw.replaceAll('_', ' ').replaceAll('-', ' ').replace(/\b\w/g, letter => letter.toUpperCase()).replace(/\b(To|No|Of|The)\b/g, word => word.toLowerCase());
}

function renderCharacterCatalog() {
    const grid = document.getElementById('characters-catalog-grid');
    const query = (document.getElementById('character-catalog-search')?.value || '').trim().toLowerCase();
    const filtered = characterCatalog.filter(character => {
        if (characterCatalogFilter === 'registered' && !character.registered) return false;
        if (characterCatalogFilter === 'suggested' && character.registered) return false;
        if (characterCatalogFilter === 'needs-cover' && (!character.registered || character.has_cover)) return false;
        return !query || [character.display_name, character.name, character.franchise].some(value => String(value || '').toLowerCase().includes(query));
    });
    grid.innerHTML = '';
    for (const character of filtered) {
        const status = character.capability || {status:'unknown', label:'Not evaluated', reason:''};
        const card = document.createElement('article');
        card.className = `character-catalog-card ${character.registered ? 'is-registered' : 'is-suggested'}`;
        const displayName = character.display_name || character.name;
        const image = character.reference_image
            ? `<img src="/api/image?path=${encodeURIComponent(character.reference_image)}" alt="${escapeHtml(displayName)} cover" loading="lazy">`
            : `<div class="character-reference-placeholder">${escapeHtml(displayName.slice(0, 1).toUpperCase())}</div>`;
        const coverLabel = character.cover_source === 'stock_hero' || character.cover_source === 'stock'
            ? 'Stock cover'
            : character.has_cover ? 'Reference cover' : 'Needs Stock cover';
        const tags = (character.tags || []).slice(0, 12).map(tag => `<span class="character-tag">${escapeHtml(String(tag).replaceAll('_', ' '))}</span>`).join('');
        card.innerHTML = `
            <div class="character-reference">${image}<span class="catalog-state ${character.registered ? 'added' : 'suggested'}">${character.registered ? 'Added' : 'Suggested'}</span></div>
            <div class="character-catalog-body">
                <div class="character-card-heading"><div><h2>${escapeHtml(displayName)}</h2><p>${escapeHtml(catalogDisplayLabel(character.franchise))}</p></div>${character.registered ? `<span class="character-route ${escapeHtml(status.status)}">${escapeHtml(status.label)}</span>` : `<span class="recommendation-priority">${escapeHtml(character.priority || 'Suggested')}</span>`}</div>
                ${character.registered ? `
                    <div class="character-health-row"><span><strong>${character.image_count}</strong> visible image${character.image_count === 1 ? '' : 's'}</span><span class="cover-state ${character.has_cover ? 'ready' : 'missing'}">${escapeHtml(coverLabel)}</span></div>
                    <p class="character-stock-count">${character.stock_image_count || 0} Stock image${character.stock_image_count === 1 ? '' : 's'}${character.stale_hero ? ' · saved cover repaired' : ''}</p>
                    ${tags ? `<details><summary>Identity tags · ${character.tags?.length || 0}</summary><div class="character-tags">${tags}</div></details>` : ''}
                    <p class="character-capability-reason">${escapeHtml(status.reason)}</p>
                    <div class="character-card-actions"><button class="btn character-open-library" type="button">Open Library</button><button class="btn btn-primary character-generate-stock" type="button" ${status.status === 'red' ? 'disabled' : ''}>Generate Stock</button></div>
                ` : `
                    <p class="character-recommendation-reason">${escapeHtml(character.reason || 'Recommended identity for the catalog.')}</p>
                    <button class="btn btn-primary character-add-recommended" type="button">Add character</button>
                `}
            </div>`;
        if (character.registered) {
            card.querySelector('.character-open-library').addEventListener('click', () => openLibraryCharacter(character.name));
            card.querySelector('.character-generate-stock').addEventListener('click', () => openStockForCharacter(character.name));
        } else {
            card.querySelector('.character-add-recommended').addEventListener('click', () => openRecommendedCharacter(character.name));
        }
        grid.appendChild(card);
    }
    if (!filtered.length) grid.innerHTML = '<p class="catalog-empty">No characters match this view.</p>';
}

async function loadCharacterCatalog() {
    const grid = document.getElementById('characters-catalog-grid');
    if (!grid) return;
    grid.innerHTML = '<p style="color:var(--text-secondary)">Loading characters…</p>';
    try {
        const response = await fetch('/api/characters/catalog');
        characterCatalog = await response.json();
        if (!response.ok) throw new Error(characterCatalog.error || 'characters_unavailable');
        const registered = characterCatalog.filter(character => character.registered);
        const withStock = registered.filter(character => character.stock_image_count > 0);
        const withCover = registered.filter(character => character.has_cover);
        const suggested = characterCatalog.filter(character => !character.registered);
        document.getElementById('character-catalog-summary').innerHTML = `
            <div><strong>${registered.length}</strong><span>Added</span></div>
            <div><strong>${withCover.length}</strong><span>With cover</span></div>
            <div><strong>${withStock.length}</strong><span>Stock tested</span></div>
            <div><strong>${suggested.length}</strong><span>Suggested</span></div>`;
        renderCharacterCatalog();
    } catch (error) {
        grid.innerHTML = `<p class="error">Could not load Characters: ${escapeHtml(error.message)}</p>`;
    }
}

document.getElementById('character-catalog-search')?.addEventListener('input', renderCharacterCatalog);
document.querySelectorAll('[data-character-filter]').forEach(button => button.addEventListener('click', () => {
    characterCatalogFilter = button.dataset.characterFilter;
    document.querySelectorAll('[data-character-filter]').forEach(candidate => candidate.classList.toggle('active', candidate === button));
    renderCharacterCatalog();
}));

function openLibraryCharacter(character) {
    switchTab('library');
    currentLibraryView = 'characters';
    loadLibrary().then(() => openCharacterWorkspace(character));
}

async function openStockForCharacter(character) {
    switchTab('create');
    syncCreateMode('stock');
    await loadCharacters(character);
}

function openRecommendedCharacter(character) {
    switchTab('create');
    syncCreateMode('scene');
    const input = document.getElementById('add-character-name');
    input.value = character;
    input.focus();
    document.getElementById('add-character-status').textContent = 'Ready to add this recommended character.';
}

async function openCreateForCharacter(character) {
    switchTab('create');
    await loadCharacters(character);
    const miaomiao = document.getElementById('create-miaomiao-alternative');
    if (miaomiao) miaomiao.checked = false;
    syncCreateRendererControls();
}

// ==================== COMMAND BAR ====================
document.getElementById('btn-command').addEventListener('click', executeCommand);
document.getElementById('command-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') executeCommand();
});

async function executeCommand() {
    const input = document.getElementById('command-input');
    const feedback = document.getElementById('command-feedback');
    const text = input.value.trim();
    if (!text) return;
    
    feedback.textContent = 'Processing...';
    
    try {
        const resp = await fetch('/api/command', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text})
        });
        const result = await resp.json();
        
        if (result.intent === 'CREATE_IMAGES') {
            feedback.textContent = `Creating mission: ${result.count} images of ${result.character}...`;
            input.value = '';
            await createMission(result.character, result.count);
        } else if (result.intent === 'CHARACTER_NOT_REGISTERED') {
            feedback.textContent = result.message || 'Character is not registered. Add it in Create Images first.';
            feedback.style.color = 'var(--warning)';
        } else if (result.intent === 'OPEN_CHARACTER_LIBRARY') {
            input.value = '';
            feedback.textContent = '';
            switchTab('library');
            setTimeout(() => filterLibrary(result.character), 100);
        } else if (result.intent === 'OPEN_COLLECTION') {
            input.value = '';
            feedback.textContent = '';
            openLibraryCollection(result.franchise);
        } else if (result.intent === 'SHOW_ACTIVE_MISSIONS') {
            input.value = '';
            feedback.textContent = '';
            loadActiveMissions();
        } else {
            feedback.textContent = result.suggestion || 'Command not recognized.';
            feedback.style.color = 'var(--warning)';
            setTimeout(() => { feedback.style.color = ''; }, 3000);
        }
    } catch (e) {
        feedback.textContent = 'Error processing command.';
    }
}

// ==================== MISSION CREATE ====================
let characterLoadRequest = 0;
let characterRegistry = {};

function characterCapabilityFromEntry(entry) {
    const capabilities = entry?.renderer_capabilities || {};
    const lustify = capabilities.lustify || {};
    const miaomiao = capabilities.miaomiao || {};
    const confirmed = new Set(['confirmed','reliable','supported']);
    const failed = new Set(['unreliable','unsupported','not_recognized','failed']);
    const lustifyState = String(lustify.identity_recognition || 'unknown').toLowerCase();
    const miaomiaoState = String(miaomiao.identity_recognition || 'unknown').toLowerCase();
    if (confirmed.has(lustifyState)) return {status:'green', label:'Lustify direct', route:'lustify_direct', reason:lustify.note || 'Lustify identity recognition is confirmed.'};
    if (failed.has(lustifyState) && confirmed.has(miaomiaoState) && confirmed.has(String(lustify.img2img || '').toLowerCase()) && lustify.fallback_recipe) {
        return {status:'yellow', label:'Miaomiao → Lustify', route:'miaomiao_then_lustify_img2img', reason:lustify.note || 'Miaomiao supplies identity before Lustify Img2Img.'};
    }
    if (failed.has(lustifyState) && failed.has(miaomiaoState)) return {status:'red', label:'No recognized renderer', route:'blocked', reason:'Neither Lustify nor Miaomiao recognizes this character reliably.'};
    return {status:'unknown', label:'Not evaluated', route:'unverified', reason:'Renderer identity compatibility has not been evaluated yet.'};
}

let createMode = 'scene';
const createModeCounts = {scene: 6, stock: 1};

function syncCreateMode(nextMode) {
    if (!['scene', 'stock'].includes(nextMode) || nextMode === createMode) return;
    const countInput = document.getElementById('create-count');
    const currentCount = Number.parseInt(countInput?.value, 10);
    if (Number.isInteger(currentCount)) createModeCounts[createMode] = currentCount;
    createMode = nextMode;
    if (countInput) countInput.value = createModeCounts[createMode];
    const isStock = createMode === 'stock';
    document.getElementById('create-scene-fields').hidden = isStock;
    document.getElementById('create-stock-fields').hidden = !isStock;
    
    if (isStock) {
        document.getElementById('create-character-group').style.display = '';
        document.getElementById('create-count-label').textContent = 'Number of images';
    } else {
        const isDataset = document.querySelector('input[name="scene_submode"]:checked')?.value === 'dataset';
        document.getElementById('create-character-group').style.display = isDataset ? 'none' : '';
        document.getElementById('create-count-label').textContent = isDataset ? 'Images per character' : 'Number of images';
    }
    
    document.getElementById('create-character-onboarding').style.display = isStock ? 'none' : 'contents';
    document.getElementById('add-character-status').style.display = isStock ? 'none' : '';
    const button = document.getElementById('btn-create-mission');
    button.textContent = isStock ? 'Generate Stock' : 'Generate';
    document.getElementById('create-mode-scene').classList.toggle('active', !isStock);
    document.getElementById('create-mode-stock').classList.toggle('active', isStock);
    document.getElementById('create-mode-scene').setAttribute('aria-selected', String(!isStock));
    document.getElementById('create-mode-stock').setAttribute('aria-selected', String(isStock));
    document.getElementById('create-status').textContent = '';
    syncCreateRendererControls();
}

function syncCreateRendererControls() {
    const character = document.getElementById('create-character')?.value || '';
    const miaomiao = Boolean(document.getElementById('create-miaomiao-alternative')?.checked);
    const look = document.getElementById('create-render-intent');
    const capability = document.getElementById('create-renderer-capability');
    if (!look || !capability) return;
    if (createMode === 'stock') {
        const createButton = document.getElementById('btn-create-mission');
        if (createButton) createButton.disabled = false;
        return;
    }
    if (miaomiao) {
        if (!look.disabled) look.dataset.previousValue = look.value;
        look.value = 'anime';
        look.disabled = true;
    } else {
        look.disabled = false;
        if (look.value === 'anime' && look.dataset.previousValue) look.value = look.dataset.previousValue;
    }
    const entry = characterRegistry?.[character] || {};
    const route = characterCapabilityFromEntry(entry);
    const renderer = miaomiao ? 'miaomiao' : 'lustify';
    const rendererState = String(entry.renderer_capabilities?.[renderer]?.identity_recognition || 'unknown').toLowerCase();
    const rendererBlocked = ['unreliable','unsupported','not_recognized','failed'].includes(rendererState);
    const createButton = document.getElementById('btn-create-mission');
    if (miaomiao) {
        capability.textContent = rendererBlocked
            ? `Miaomiao is not reliable for ${character}. Generation is blocked.`
            : `Miaomiao only · Anime. Lustify will not run.`;
        capability.className = rendererBlocked ? 'mt-1 capability-message red' : 'mt-1 capability-message';
        if (createButton) createButton.disabled = rendererBlocked;
        return;
    }
    capability.textContent = route.status === 'yellow'
        ? `Identity route: Miaomiao first, then Lustify Img2Img. Lustify direct will not run.`
        : route.status === 'red' ? `${route.reason} Generation is blocked.`
        : route.status === 'green' ? `Identity route: Lustify direct.`
        : `Identity compatibility has not been evaluated; Lustify direct remains unverified.`;
    capability.className = `mt-1 capability-message ${route.status}`;
    if (createButton) createButton.disabled = route.status === 'red';
}

async function loadCharacters(selectedCharacter = null) {
    const select = document.getElementById('create-character');
    const previous = selectedCharacter || select.value;
    const requestId = ++characterLoadRequest;
    try {
        const resp = await fetch('/api/characters');
        if (!resp.ok) throw new Error('characters_unavailable');
        const characters = await resp.json();
        characterRegistry = characters || {};
        if (requestId !== characterLoadRequest) return select.value;
        const names = Object.keys(characters || {}).sort((a, b) => a.localeCompare(b));
        select.innerHTML = '';
        const datasetSelect = document.getElementById('create-dataset-characters');
        if (datasetSelect) datasetSelect.innerHTML = '<option value="ALL">-- All Characters --</option>';
        
        names.forEach(name => {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            select.appendChild(option);
            
            if (datasetSelect) {
                const opt2 = document.createElement('option');
                opt2.value = name;
                opt2.textContent = name;
                datasetSelect.appendChild(opt2);
            }
        });
        if (previous && names.includes(previous)) {
            select.value = previous;
        } else if (selectedCharacter) {
            select.value = '';
            throw new Error('bootstrapped_character_not_in_registry');
        }
        if (!names.length) select.innerHTML = '<option value="">No registered characters</option>';
        syncCreateRendererControls();
        return select.value;
    } catch (e) {
        if (requestId === characterLoadRequest && e.message !== 'bootstrapped_character_not_in_registry') {
            select.innerHTML = '<option value="">Could not load characters</option>';
        }
        if (selectedCharacter) throw e;
        return '';
    }
}

document.getElementById('btn-add-character').addEventListener('click', async () => {
    const input = document.getElementById('add-character-name');
    const button = document.getElementById('btn-add-character');
    const status = document.getElementById('add-character-status');
    const character = input.value.trim();
    if (!character) {
        status.textContent = 'Enter a character name.';
        return;
    }

    button.disabled = true;
    status.textContent = 'Resolving profile and references...';
    try {
        const resp = await fetch('/api/characters/bootstrap', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({character})
        });
        const result = await resp.json();
        if (!resp.ok) {
            status.textContent = result.message || result.error || 'Character could not be added.';
            return;
        }
        const selected = await loadCharacters(result.character);
        if (selected !== result.character) throw new Error('character_selection_failed');
        input.value = '';
        status.textContent = result.duplicate ? 'Character already registered.' : 'Character added.';
    } catch (e) {
        status.textContent = 'Character could not be added.';
    } finally {
        button.disabled = false;
    }
});

document.getElementById('create-character').addEventListener('change', syncCreateRendererControls);
document.getElementById('create-miaomiao-alternative').addEventListener('change', syncCreateRendererControls);
document.getElementById('create-mode-scene').addEventListener('click', () => syncCreateMode('scene'));
document.getElementById('create-mode-stock').addEventListener('click', () => syncCreateMode('stock'));
document.getElementById('create-stock-custom-outfit').addEventListener('change', event => {
    const input = document.getElementById('create-stock-outfit');
    input.disabled = !event.target.checked;
    if (event.target.checked) input.focus();
});

document.querySelectorAll('input[name="scene_submode"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        const isDataset = e.target.value === 'dataset';
        document.getElementById('dataset-character-group').style.display = isDataset ? '' : 'none';
        document.getElementById('create-character-group').style.display = isDataset ? 'none' : '';
        document.getElementById('directed-scene-fields').style.display = isDataset ? 'none' : '';
        document.getElementById('create-count-label').textContent = isDataset ? 'Images per character' : 'Number of images';
    });
});

document.getElementById('btn-create-mission').addEventListener('click', async () => {
    const isDataset = document.querySelector('input[name="scene_submode"]:checked')?.value === 'dataset' && createMode === 'scene';
    const count = Number.parseInt(document.getElementById('create-count').value, 10);
    const status = document.getElementById('create-status');

    if (!Number.isInteger(count) || count < 1 || count > 20) {
        status.textContent = 'Number of images must be between 1 and 20.';
        return;
    }

    if (createMode === 'stock' && document.getElementById('create-stock-custom-outfit').checked && !document.getElementById('create-stock-outfit').value.trim()) {
        status.textContent = 'Enter an outfit or disable Custom outfit.';
        return;
    }

    if (isDataset) {
        const select = document.getElementById('create-dataset-characters');
        const selectedOptions = Array.from(select.selectedOptions).map(opt => opt.value);
        if (selectedOptions.length === 0) {
            status.textContent = 'Select at least one character.';
            return;
        }

        let targetCharacters = selectedOptions;
        if (selectedOptions.includes('ALL')) {
            targetCharacters = Object.keys(characterRegistry || {});
        }
        
        const totalImages = targetCharacters.length * count;
        if (!confirm(`Confirm dataset batch?\n\nCharacters: ${targetCharacters.length}\nImages per character: ${count}\nTarget final images: ${totalImages}`)) {
            return;
        }

        document.getElementById('btn-create-mission').disabled = true;
        status.textContent = `Creating ${targetCharacters.length} missions...`;
        
        let successCount = 0;
        let lastId = null;
        for (const char of targetCharacters) {
            const payload = buildScenePayload(char, count);
            payload.what_happens = '';
            payload.where = '';
            payload.generation_mode = 'dataset_auto_concepts';
            
            try {
                const resp = await fetch('/api/missions/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const result = await resp.json();
                if (result.mission_id) {
                    successCount++;
                    lastId = result.mission_id;
                }
            } catch (e) {
                console.error(`Failed to create mission for ${char}`, e);
            }
        }
        
        document.getElementById('btn-create-mission').disabled = false;
        status.innerHTML = `<span style="color:var(--success)">Created ${successCount} missions!</span>`;
        if (successCount > 0) switchTab('queue');
        return;
    }

    const character = document.getElementById('create-character').value;
    if (!character) {
        status.textContent = 'Select a character.';
        return;
    }
    await createMission(character, count);
});

let creationSourceContext = null;

async function createMission(character, count) {
    const status = document.getElementById('create-status');
    status.textContent = 'Generating...';
    
    try {
        const payload = createMode === 'stock'
            ? buildStockPayload(character, count)
            : buildScenePayload(character, count);
        const resp = await fetch('/api/missions/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const result = await resp.json();
        
        if (result.mission_id) {
            status.innerHTML = `<span style="color:var(--success)">Mission created!</span>`;
            openMissionDetail(result.mission_id);
        } else {
            status.textContent = result.message || result.error || 'Mission could not be created.';
        }
    } catch (e) {
        status.textContent = 'Failed to create mission.';
    }
}

function buildScenePayload(character, count) {
    return {
            creation_mode: 'scene',
            character,
            requested_assets: count,
            what_happens: document.getElementById('create-intent-action')?.value || '',
            where: document.getElementById('create-intent-location')?.value || '',
            concept_multiplier: parseInt(document.getElementById('create-multiplier')?.value) || 3,
            production_buffer: parseInt(document.getElementById('create-buffer')?.value) || 2,
            max_rounds: parseInt(document.getElementById('create-rounds')?.value) || 2,
            renderer_choice: document.getElementById('create-miaomiao-alternative')?.checked ? 'miaomiao' : 'lustify',
            generate_miaomiao_alternative: false,
            render_intent: document.getElementById('create-render-intent')?.value || 'semi_realistic',
            source_asset_id: creationSourceContext?.asset_id || '',
            source_generation_id: creationSourceContext?.generation_id || '',
            generation_mode: creationSourceContext ? 'alternative' : 'direct',
            alternative_mode: creationSourceContext?.alternative_mode || '',
            alternative_instruction: creationSourceContext?.custom_instruction || '',
            source_context: creationSourceContext?.scene_context || {}
    };
}

function buildStockPayload(character, count) {
    const payload = {creation_mode: 'stock', character, requested_assets: count};
    if (document.getElementById('create-stock-custom-outfit').checked) {
        payload.outfit_override = document.getElementById('create-stock-outfit').value.trim();
    }
    return payload;
}

// ==================== MISSION DETAIL ====================
async function openMissionDetail(missionId) {
    currentMission = missionId;
    switchTab('mission-detail');
    
    if (missionPollInterval) clearInterval(missionPollInterval);
    await refreshMissionDetail();
    missionPollInterval = setInterval(refreshMissionDetail, 3000);
}

async function refreshMissionDetail() {
    if (!currentMission) return;
    
    try {
        const resp = await fetch(`/api/missions/${currentMission}`);
        const m = await resp.json();
        
        document.getElementById('mission-detail-title').textContent = `Mission: ${m.character}`;
        
        const cancelBtn = document.getElementById('btn-cancel-mission');
        const resumeBtn = document.getElementById('btn-resume-mission');
        const deleteBtn = document.getElementById('btn-delete-mission');
        const isActive = ACTIVE_MISSION_STATUSES.has(m.status);
        const isRecoverable = m.status === 'PARTIAL' || m.status === 'FAILED';
        const isDeletable = ['FAILED','COMPLETE','CANCELLED'].includes(m.status);
        
        cancelBtn.style.display = isActive ? '' : 'none';
        resumeBtn.style.display = isRecoverable ? '' : 'none';
        deleteBtn.style.display = isDeletable ? '' : 'none';
        
        const pct = Math.round((m.progress || 0) * 100);
        const dur = m.duration_seconds ? `${Math.round(m.duration_seconds / 60)}m ${Math.round(m.duration_seconds % 60)}s` : '—';
        const isComplete = m.status === 'COMPLETE' || m.status === 'PARTIAL';
        
        let html = '';
        
        if (isComplete) {
            html += `
            <div class="mission-summary ${m.status === 'PARTIAL' ? 'partial' : ''}">
                <h1>MISSION ${m.status}</h1>
                <p>${m.character}</p>
                <p>${m.approved_assets} / ${m.requested_assets} approved</p>
                <div class="stat-grid">
                    <div class="stat-item"><div class="stat-value">${m.generated_concepts}</div><div class="stat-label">Concepts</div></div>
                    <div class="stat-item"><div class="stat-value">${m.selected_candidates}</div><div class="stat-label">Candidates</div></div>
                    <div class="stat-item"><div class="stat-value">${m.approved_assets}</div><div class="stat-label">Approved</div></div>
                    <div class="stat-item"><div class="stat-value">${m.rejected_quality}</div><div class="stat-label">Rejected</div></div>
                    <div class="stat-item"><div class="stat-value">${m.retry_exhausted}</div><div class="stat-label">Retry Exhausted</div></div>
                    <div class="stat-item"><div class="stat-value">${m.failed_runtime}</div><div class="stat-label">Runtime Failures</div></div>
                </div>
                <p style="color:var(--text-secondary)">Duration: ${dur}</p>
                <div class="mt-1">
                    <button class="btn btn-primary" onclick="openMissionLibrary('${m.mission_id}')">View Assets in Library</button>
                </div>
            </div>`;
            if (missionPollInterval) { clearInterval(missionPollInterval); missionPollInterval = null; }
        } else {
            html += `
            <div class="card">
                <h3>Progress</h3>
                <div class="flex-between">
                    <span>${m.approved_assets} / ${m.requested_assets} approved</span>
                    <span class="badge ${isActive ? 'info' : 'warning'}">${m.status}</span>
                </div>
                <div class="mission-progress-bar mt-1">
                    <div class="mission-progress-fill" style="width:${pct}%"></div>
                </div>
                <p class="mission-status">${m.current_stage_detail || ''}</p>
                <p style="font-size:0.85em; color:var(--text-secondary)">
                    Round: ${m.current_round} / ${m.max_rounds} · 
                    Concepts: ${m.generated_concepts} · 
                    Candidates: ${m.selected_candidates} ·
                    Active: ${m.active_candidates}
                </p>
            </div>`;
        }
        
        // Stats card
        if (!isComplete) {
            html += `
            <div class="card mt-1">
                <h3>Results</h3>
                <div class="grid-2">
                    <div>
                        <p>Approved: <strong style="color:var(--success)">${m.approved_assets}</strong></p>
                        <p>Rejected Quality: <strong>${m.rejected_quality}</strong></p>
                    </div>
                    <div>
                        <p>Retry Exhausted: <strong>${m.retry_exhausted}</strong></p>
                        <p>Runtime Failures: <strong style="color:var(--error)">${m.failed_runtime}</strong></p>
                    </div>
                </div>
            </div>`;
        }
        
        if (m.error_message) {
            html += `<div class="card mt-1" style="border-color:var(--error)"><h3>Error</h3><p style="color:var(--error)">${m.error_message}</p></div>`;
        }
        
        document.getElementById('mission-detail-content').innerHTML = html;
        loadMissionFunnel(m.mission_id);
    } catch (e) {
        document.getElementById('mission-detail-content').innerHTML = '<p>Error loading mission details.</p>';
    }
}

document.getElementById('btn-cancel-mission').addEventListener('click', async () => {
    if (!currentMission) return;
    await fetch(`/api/missions/${currentMission}/cancel`, {method: 'POST'});
    refreshMissionDetail();
});

document.getElementById('btn-resume-mission').addEventListener('click', async () => {
    if (!currentMission) return;
    await fetch(`/api/missions/${currentMission}/resume`, {method: 'POST'});
    refreshMissionDetail();
});

document.getElementById('btn-delete-mission').addEventListener('click', async () => {
    if (!currentMission) return;
    const confirmed = window.confirm(
        'Delete this mission? This removes only its persisted mission state. Library assets and shared character references will remain.'
    );
    if (!confirmed) return;

    const resp = await fetch(`/api/missions/${currentMission}`, {method: 'DELETE'});
    const result = await resp.json();
    if (!resp.ok) {
        window.alert(result.message || result.error || 'Mission could not be deleted.');
        await refreshMissionDetail();
        return;
    }

    if (missionPollInterval) {
        clearInterval(missionPollInterval);
        missionPollInterval = null;
    }
    currentMission = null;
    switchTab('home');
    loadActiveMissions();
});

// ==================== LIBRARY ====================
let allAssets = [];
let libraryCollectionsSummary = {};
let libraryFilter = '';
let libraryMissionFilter = '';
let libraryCollectionFilter = '';
let librarySelectionMode = false;
let selectedLibraryAssetIds = new Set();
let currentWorkspaceGalleryFilter = 'all';

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
}

async function openMissionLibrary(missionId) {
    libraryMissionFilter = missionId;
    libraryFilter = '';
    libraryCollectionFilter = '';
    switchTab('library');
}

let currentLibraryView = 'characters'; // characters, all, favorites

function numericLibraryRating(value) {
    return typeof value === 'number' && value >= 1 && value <= 10 ? value : null;
}

function visibleLibraryAssets(assets) {
    return (Array.isArray(assets) ? assets : []).filter(asset => asset.is_visible_library_asset === true);
}

function applyLibraryControls(assets, {includeRejected = false, forcedFilter = null} = {}) {
    const renderer = document.getElementById('library-renderer-filter')?.value || '';
    const filter = forcedFilter || document.getElementById('library-rating-filter')?.value || 'all';
    const agentMin = Number(document.getElementById('library-agent-min')?.value || 0);
    const humanMin = Number(document.getElementById('library-human-min')?.value || 0);
    const explicitlyRejected = filter === 'rejected';
    const source = includeRejected || explicitlyRejected ? (Array.isArray(assets) ? assets : []) : visibleLibraryAssets(assets);
    let result = source.filter(asset => {
        const rejected = asset.library_status === 'REJECTED';
        const agent = numericLibraryRating(asset.agent_rating);
        const human = numericLibraryRating(asset.human_rating ?? asset.human_review?.rating);
        if (renderer && (asset.renderer || '').toLowerCase() !== renderer) return false;
        if (filter === 'rated' && human === null) return false;
        if (filter === 'unrated' && human !== null) return false;
        if (filter === 'approved' && asset.library_status !== 'APPROVED') return false;
        if (filter === 'rejected' && !rejected) return false;
        if (filter === 'favorites' && !asset.favorite) return false;
        if (agentMin && (agent === null || agent < agentMin)) return false;
        if (humanMin && (human === null || human < humanMin)) return false;
        return true;
    });
    const sort = document.getElementById('library-sort')?.value || 'newest';
    const dateValue = asset => Date.parse(asset.generated_at || asset.created_at || '') || 0;
    const ratingValue = value => numericLibraryRating(value) ?? -1;
    result = [...result].sort((a, b) => {
        if (sort === 'oldest') return dateValue(a) - dateValue(b);
        if (sort === 'agent_desc') return ratingValue(b.agent_rating) - ratingValue(a.agent_rating) || dateValue(b) - dateValue(a);
        if (sort === 'human_desc') return ratingValue(b.human_rating ?? b.human_review?.rating) - ratingValue(a.human_rating ?? a.human_review?.rating) || dateValue(b) - dateValue(a);
        return dateValue(b) - dateValue(a);
    });
    return result;
}

async function loadLibrary() {
    try {
        const query = libraryMissionFilter ? `?mission_id=${encodeURIComponent(libraryMissionFilter)}` : '';
        const [assetsResp, collectionsResp] = await Promise.all([
            fetch(`/api/library/assets${query}`),
            fetch('/api/library/collections'),
        ]);
        allAssets = await assetsResp.json() || [];
        libraryCollectionsSummary = await collectionsResp.json() || {};
        populateLibraryCollections();
        await loadCharacterHeroes();
        setLibraryView(currentLibraryView);
    } catch (e) {
        document.getElementById('library-characters-grid').innerHTML = '<p>Error loading library.</p>';
        document.getElementById('library-assets-grid').innerHTML = '<p>Error loading library.</p>';
    }
}

function populateLibraryCollections() {
    const select = document.getElementById('library-collection-filter');
    if (!select) return;
    const availableIds = new Set(visibleLibraryAssets(allAssets).map(asset => asset.collection_id || asset.franchise || 'Unknown'));
    const collections = Object.values(libraryCollectionsSummary)
        .filter(summary => summary.total_images > 0 && availableIds.has(summary.collection_id))
        .sort((a, b) => (a.display_name || a.collection_id).localeCompare(b.display_name || b.collection_id));
    select.innerHTML = `<option value="">All collections</option>${collections.map(summary => `<option value="${escapeHtml(summary.collection_id)}">${escapeHtml(summary.display_name || summary.collection_id)}</option>`).join('')}`;
    if (!collections.some(summary => summary.collection_id === libraryCollectionFilter)) libraryCollectionFilter = '';
    select.value = libraryCollectionFilter;
}

function openLibraryCollection(collectionId) {
    libraryMissionFilter = '';
    libraryCollectionFilter = typeof collectionId === 'string' ? collectionId : '';
    currentLibraryView = 'all';
    currentSearchQuery = '';
    const search = document.getElementById('library-search');
    if (search) search.value = '';
    switchTab('library');
    loadLibrary();
}

function setLibraryView(view) {
    currentLibraryView = view;
    document.querySelectorAll('#library-views-toggle .btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.toLowerCase().includes(view) || (view === 'all' && btn.textContent === 'All Images'));
    });
    
    document.getElementById('character-workspace').style.display = 'none';
    document.getElementById('library-main-view').style.display = 'block';

    const charGrid = document.getElementById('library-characters-grid');
    const allGrid = document.getElementById('library-assets-grid');
    document.querySelector('#library-main-view .library-selection-bar').hidden = (view === 'characters' || view === 'rejected');

    let filteredAssets = allAssets;
    if (libraryCollectionFilter) {
        filteredAssets = filteredAssets.filter(asset => (asset.collection_id || asset.franchise || 'Unknown') === libraryCollectionFilter);
    }
    if (currentSearchQuery) {
        filteredAssets = filteredAssets.filter(a =>
            (a.character || '').toLowerCase().includes(currentSearchQuery) ||
            (a.franchise || '').toLowerCase().includes(currentSearchQuery) ||
            (a.collection_display_name || '').toLowerCase().includes(currentSearchQuery) ||
            (a.concept_snapshot || '').toLowerCase().includes(currentSearchQuery)
        );
    }

    const includeRejected = view === 'rejected';
    filteredAssets = applyLibraryControls(filteredAssets, {includeRejected, forcedFilter:view === 'rejected' ? 'rejected' : view === 'favorites' ? 'favorites' : null});

    if (view === 'characters') {
        charGrid.style.display = 'grid';
        allGrid.style.display = 'none';
        renderLibraryCharacters(filteredAssets);
    } else {
        charGrid.style.display = 'none';
        allGrid.style.display = 'grid';
        const filtered = view === 'favorites' ? filteredAssets.filter(a => a.favorite) : filteredAssets;
        renderLibraryAssets(filtered, allGrid);
    }
}

let characterHeroes = {};
async function loadCharacterHeroes() {
    try {
        const res = await fetch('/api/characters/heroes');
        if (res.ok) {
            characterHeroes = await res.json();
        }
    } catch (e) {
        console.error('Error fetching heroes:', e);
    }
}

function renderLibraryCharacters(assets) {
    const grid = document.getElementById('library-characters-grid');
    grid.innerHTML = '';
    if (!assets || assets.length === 0) {
        grid.innerHTML = '<p style="color:var(--text-secondary)">No assets found.</p>';
        return;
    }

    const chars = {};
    for (const a of assets) {
        const name = a.character || 'Unknown';
        if (!chars[name]) chars[name] = { name, displayName: a.character_display_name || name, count: 0, favs: 0, latest: null, favAsset: null, heroAsset: null };
        chars[name].count++;
        if (a.favorite) {
            chars[name].favs++;
            if (!chars[name].favAsset) chars[name].favAsset = a;
        }
        if (!chars[name].latest || a.created_at > chars[name].latest.created_at) {
            chars[name].latest = a;
        }
        if (characterHeroes[name] && (a.asset_id === characterHeroes[name] || (a.generation_id === characterHeroes[name] && a.is_final_selection))) {
            chars[name].heroAsset = a;
        }
    }

    for (const charName in chars) {
        const data = chars[charName];
        const card = document.createElement('div');
        card.className = 'asset-card character-card';
        card.onclick = () => openCharacterWorkspace(charName);
        
        const bestAsset = data.heroAsset || data.favAsset || data.latest;
        const heroPath = bestAsset.full_image_path || bestAsset.thumbnail_path;
        const imageLabel = `${data.count} ${data.count === 1 ? 'image' : 'images'}`;
        const favoriteLabel = `${data.favs} ${data.favs === 1 ? 'favorite' : 'favorites'}`;
        card.innerHTML = `
            <img src="/api/image?path=${encodeURIComponent(heroPath)}" alt="${escapeHtml(data.displayName)}" loading="lazy">
            <div class="asset-label"><strong>${escapeHtml(data.displayName)}</strong><br><small>${imageLabel} · ${favoriteLabel}</small></div>
        `;
        grid.appendChild(card);
    }
}

function openCharacterWorkspace(charName) {
    clearLibrarySelection();
    document.getElementById('library-main-view').style.display = 'none';
    document.getElementById('character-workspace').style.display = 'block';
    document.getElementById('workspace-character-name').textContent = charName;
    
    const charAssets = visibleLibraryAssets(allAssets).filter(a => a.character === charName);
    document.getElementById('workspace-character-meta').textContent = `${charAssets.length} images`;
    
    filterWorkspaceGallery('all');
}

function filterWorkspaceGallery(filter) {
    currentWorkspaceGalleryFilter = filter;
    const buttons = document.querySelectorAll('#workspace-gallery-filters .filter-btn');
    buttons.forEach(b => b.classList.remove('active'));
    document.querySelector(`#workspace-gallery-filters .filter-btn[onclick="filterWorkspaceGallery('${filter}')"]`)?.classList.add('active');
    
    const selBar = document.querySelector('#workspace-gallery-container .library-selection-bar');
    if (selBar) {
        selBar.hidden = filter === 'rejected';
    }
    
    const charName = document.getElementById('workspace-character-name').textContent;
    let charAssets = allAssets.filter(a => a.character === charName);
    
    if (filter !== 'rejected') {
        charAssets = visibleLibraryAssets(charAssets);
    }

    if (filter === 'lustify') {
        charAssets = charAssets.filter(a => {
            const outputs = a.render_outputs || [];
            return outputs.some(o => o.renderer === 'lustify' || o.renderer === 'lustify_img2img' || o.preset === 'lustify_creative');
        });
    } else if (filter === 'miaomiao') {
        charAssets = charAssets.filter(a => {
            const outputs = a.render_outputs || [];
            return outputs.some(o => o.renderer === 'miaomiao' || o.preset === 'miaomiao_alternative');
        });
    } else if (filter === 'legacy') {
        charAssets = charAssets.filter(a => {
            const outputs = a.render_outputs || [];
            return outputs.some(o => o.renderer === 'klein' || o.renderer === 'illustrious');
        });
    }
    
    const grid = document.getElementById('workspace-gallery');
    renderLibraryAssets(applyLibraryControls(charAssets, {includeRejected:filter === 'rejected', forcedFilter:filter === 'rejected' ? 'rejected' : null}), grid);
}

function closeCharacterWorkspace() {
    setLibraryView('characters');
}

function workspaceCreateIntent() {
    switchTab('create');
    const charSelect = document.getElementById('create-character');
    const charName = document.getElementById('workspace-character-name').textContent;
    if (charSelect && Array.from(charSelect.options).some(o => o.value === charName)) {
        charSelect.value = charName;
    }
}

function prepareAlternativeFromAsset(asset) {
    syncCreateMode('scene');
    const spec = asset.resolved_render_spec || {};
    const hook = spec.hook_premise || spec.concept || {};
    creationSourceContext = {asset_id:asset.asset_id, generation_id:asset.generation_id, renderer:asset.renderer, character:asset.character, render_intent:asset.render_intent || spec.render_intent || '', scene_context:{snapshot:asset.concept_snapshot || hook.snapshot || '', core_action:hook.core_action || '', setting:hook.setting || hook.diversity_signature?.setting || '', visual_hook:hook.visual_hook || ''}, alternative_mode:'same_idea', custom_instruction:''};
    switchTab('create');
    const charSelect = document.getElementById('create-character');
    if (charSelect && Array.from(charSelect.options).some(option => option.value === asset.character)) charSelect.value = asset.character;
    const context = document.getElementById('create-source-context');
    context.style.display = 'block';
    context.innerHTML = `<strong>Generate alternative</strong><br><span>${asset.display_title || asset.character}</span><label>Variation <select id="create-alternative-mode" class="form-select"><option value="same_idea">Same idea, new variation</option><option value="change_action">Change action</option><option value="change_setting">Change setting</option><option value="change_look">Change look</option><option value="custom">Custom instruction</option></select></label><label id="create-alternative-custom-wrap" style="display:none">Instruction <input id="create-alternative-custom" type="text" maxlength="300" placeholder="Describe only the requested change"></label><button id="btn-clear-create-source" class="btn">Clear source</button>`;
    document.getElementById('create-alternative-mode').onchange = event => { creationSourceContext.alternative_mode = event.target.value; document.getElementById('create-alternative-custom-wrap').style.display = event.target.value === 'custom' ? 'block' : 'none'; };
    document.getElementById('create-alternative-custom').oninput = event => { creationSourceContext.custom_instruction = event.target.value; };
    document.getElementById('btn-clear-create-source').onclick = () => { creationSourceContext = null; context.style.display = 'none'; context.innerHTML = ''; };
}

function openAssetComparison(asset) {
    openAssetDetailGeneric(asset);
    const peers = comparisonItemsForAsset(asset);
    const section = document.getElementById('asset-stage-compare');
    const grid = document.getElementById('asset-render-output-grid');
    section.style.display = '';
    grid.innerHTML = peers.map(item => {
        const label = item.role === 'identity_reference' ? `${item.renderer || 'Miaomiao'} · identity source` : `${item.renderer || 'Unknown'}${item.is_final_selection ? ' · final result' : ''}`;
        const inspect = item.asset_id ? `<button class="btn" data-inspect-asset="${escapeHtml(item.asset_id)}">Inspect</button>` : '<span class="badge">Source reference</span>';
        return `<article class="stage-compare-card ${item.asset_id === asset.asset_id ? 'active' : ''}"><h4>${escapeHtml(label)}</h4><a href="/api/image?path=${encodeURIComponent(item.full_image_path)}" target="_blank"><img src="/api/image?path=${encodeURIComponent(item.full_image_path)}" alt="${escapeHtml(item.renderer || 'renderer')}"></a><p>Agent ${item.agent_rating ?? '—'} · You ${item.human_rating ?? '—'}</p>${inspect}</article>`;
    }).join('') || '<p>No comparable renderer siblings.</p>';
    grid.querySelectorAll('[data-inspect-asset]').forEach(button => button.addEventListener('click', () => openAssetDetailGeneric(allAssets.find(item => item.asset_id === button.dataset.inspectAsset))));
}

function comparisonItemsForAsset(asset) {
    const result = [];
    const seenPaths = new Set();
    const add = item => {
        const path = item.full_image_path || item.receipt?.output_asset || '';
        if (!path || seenPaths.has(path)) return;
        seenPaths.add(path);
        result.push({...item, full_image_path:path});
    };
    (asset.comparison_outputs || []).forEach(output => add({
        renderer:output.renderer, preset:output.preset || output.receipt?.preset,
        role:output.role || 'requested_output', full_image_path:output.receipt?.output_asset,
        agent_rating:numericLibraryRating(output.review?.agent_rating), human_rating:null,
        is_final_selection:output.role !== 'identity_reference',
    }));
    allAssets.filter(item => item.generation_id === asset.generation_id).forEach(add);
    return result;
}

function updateHardStats(assets) {
    const statsContainer = document.getElementById('library-hard-stats');
    if (!statsContainer) return;
    
    const hardReviewed = assets.filter(a => a.human_review?.hard_rating);
    if (hardReviewed.length === 0) {
        statsContainer.style.display = 'none';
        return;
    }
    
    let sumScore = 0;
    let sumDelta = 0;
    let over90 = 0, over80 = 0, over70 = 0, under70 = 0;
    
    hardReviewed.forEach(a => {
        const rating = a.human_review.hard_rating;
        const score = rating.final_score;
        sumScore += score;
        sumDelta += rating.delta;
        if (score >= 90) over90++;
        else if (score >= 80) over80++;
        else if (score >= 70) over70++;
        else under70++;
    });
    
    const count = hardReviewed.length;
    const avgScore = (sumScore / count).toFixed(1);
    const avgDelta = (sumDelta / count).toFixed(1);
    
    statsContainer.style.display = '';
    statsContainer.innerHTML = `
        <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:16px;">
            <div>
                <h4 style="margin-top:0;margin-bottom:8px;color:var(--accent);">Gallery Statistics</h4>
                <div style="font-family:monospace; line-height:1.5;">
                    Hard Reviewed &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${String(count).padStart(3, ' ')}<br>
                    Average Hard Score &nbsp;&nbsp;${String(avgScore).padStart(4, ' ')}<br>
                    Average Delta &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${(avgDelta > 0 ? '+' : '')}${String(avgDelta).padStart(3, ' ')}
                </div>
            </div>
            <div>
                <h4 style="margin-top:0;margin-bottom:8px;visibility:hidden;">Distribution</h4>
                <div style="font-family:monospace; line-height:1.5;">
                    90+ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${String(over90).padStart(3, ' ')}<br>
                    80-89 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${String(over80).padStart(3, ' ')}<br>
                    70-79 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${String(over70).padStart(3, ' ')}<br>
                    &lt;70 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${String(under70).padStart(3, ' ')}
                </div>
            </div>
        </div>
    `;
}

function renderLibraryAssets(assets, gridElement) {
    const grid = gridElement || document.getElementById('library-assets-grid');
    if (grid.id === 'library-assets-grid') updateHardStats(assets);
    
    if (!assets || assets.length === 0) {
        grid.innerHTML = '<p style="color:var(--text-secondary)">No assets found.</p>';
        return;
    }
    grid.innerHTML = '';
    assets.forEach(a => grid.appendChild(createAssetCard(a)));
    updateLibrarySelectionUI();
}

// Support search and filters
let currentSearchQuery = '';
function filterLibrary(query) {
    currentSearchQuery = query ? query.toLowerCase() : '';
    setLibraryView(currentLibraryView);
}
document.getElementById('library-search')?.addEventListener('input', e => {
    filterLibrary(e.target.value);
});
document.querySelectorAll('#library-filters .filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('#library-filters .filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterLibrary(libraryFilter);
    });
});

function createAssetCard(asset) {
    const card = document.createElement('div');
    const selected = selectedLibraryAssetIds.has(asset.asset_id);
    card.className = `asset-card${librarySelectionMode ? ' selection-mode' : ''}${selected ? ' selected' : ''}`;
    card.onclick = () => librarySelectionMode ? toggleLibraryAssetSelection(asset.asset_id, card) : openAssetDetailGeneric(asset);
    
    card.innerHTML = `
        ${asset.favorite ? '<span class="favorite-badge">♥</span>' : ''}
        ${librarySelectionMode ? `<button class="asset-selection-check" type="button" aria-label="${selected ? 'Deselect' : 'Select'} ${escapeHtml(asset.display_title || asset.character)}">${selected ? '✓' : ''}</button>` : ''}
        <img src="/api/image?path=${encodeURIComponent(asset.full_image_path || asset.thumbnail_path)}" alt="${asset.character}" loading="lazy">
        <div class="asset-label"><strong>${asset.display_title || asset.character}</strong><br><small>${asset.renderer || 'Unknown'} · ${asset.human_rating ? `★ Human ${asset.human_rating}` : 'Human —'} · Agent ${asset.agent_rating ?? '—'}</small>${asset.human_review?.hard_rating ? `<br><small style="color:var(--accent);font-weight:600;">Score ${asset.human_review.hard_rating.final_score} · Hard ✓</small>` : ''}</div>
    `;
    card.querySelector('.asset-selection-check')?.addEventListener('click', event => { event.stopPropagation(); toggleLibraryAssetSelection(asset.asset_id, card); });
    return card;
}

function updateLibrarySelectionUI() {
    const count = selectedLibraryAssetIds.size;
    document.querySelectorAll('.library-selection-bar').forEach(bar => {
        bar.classList.toggle('active', librarySelectionMode);
        const select = bar.querySelector('.btn-library-select');
        const actions = bar.querySelector('.library-selection-actions');
        if (select) select.hidden = librarySelectionMode;
        if (actions) actions.hidden = !librarySelectionMode;
        const label = bar.querySelector('.library-selection-count');
        if (label) label.textContent = `${count} selected`;
        const remove = bar.querySelector('.btn-library-remove-selected');
        if (remove) remove.disabled = count === 0;
    });
}

function rerenderLibrarySelectionSurface() {
    const workspace = document.getElementById('character-workspace');
    if (workspace && workspace.style.display !== 'none') filterWorkspaceGallery(currentWorkspaceGalleryFilter);
    else setLibraryView(currentLibraryView);
}

function setLibrarySelectionMode(enabled) {
    librarySelectionMode = Boolean(enabled);
    if (!librarySelectionMode) selectedLibraryAssetIds.clear();
    rerenderLibrarySelectionSurface();
    updateLibrarySelectionUI();
}

function clearLibrarySelection() {
    librarySelectionMode = false;
    selectedLibraryAssetIds.clear();
    updateLibrarySelectionUI();
}

function toggleLibraryAssetSelection(assetId, card) {
    if (selectedLibraryAssetIds.has(assetId)) selectedLibraryAssetIds.delete(assetId);
    else selectedLibraryAssetIds.add(assetId);
    card?.classList.toggle('selected', selectedLibraryAssetIds.has(assetId));
    const check = card?.querySelector('.asset-selection-check');
    if (check) check.textContent = selectedLibraryAssetIds.has(assetId) ? '✓' : '';
    updateLibrarySelectionUI();
}

async function removeSelectedLibraryImages() {
    const ids = [...selectedLibraryAssetIds];
    if (!ids.length) return;
    if (!window.confirm(`Remove ${ids.length} selected image${ids.length === 1 ? '' : 's'} from the normal galleries? Files and lineage will be kept in Rejected.`)) return;
    const workspace = document.getElementById('character-workspace');
    const returnCharacter = workspace && workspace.style.display !== 'none' ? document.getElementById('workspace-character-name').textContent : '';
    const response = await fetch('/api/library/remove-selected', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({asset_ids:ids})});
    const payload = await response.json();
    if (!response.ok) return window.alert(payload.error || 'Could not remove the selected images.');
    clearLibrarySelection();
    await loadLibrary();
    if (returnCharacter) openCharacterWorkspace(returnCharacter);
}

async function hardReevaluateSelectedLibraryImages() {
    const ids = [...selectedLibraryAssetIds];
    if (!ids.length) return;
    if (!window.confirm(`Run Hard Re-Evaluator on ${ids.length} selected image${ids.length === 1 ? '' : 's'}?`)) return;
    
    const btns = document.querySelectorAll('.btn-library-hard-reevaluate');
    btns.forEach(btn => btn.disabled = true);
    
    try {
        const workspace = document.getElementById('character-workspace');
        const returnCharacter = workspace && workspace.style.display !== 'none' ? document.getElementById('workspace-character-name').textContent : '';
        const response = await fetch('/api/library/hard-reevaluate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({asset_ids:ids})});
        const payload = await response.json();
        if (!response.ok) return window.alert(payload.error || 'Failed to hard re-evaluate the selected images.');
        clearLibrarySelection();
        await loadLibrary();
        if (returnCharacter) openCharacterWorkspace(returnCharacter);
    } finally {
        btns.forEach(btn => btn.disabled = false);
    }
}

document.querySelectorAll('.btn-library-select').forEach(button => button.addEventListener('click', () => setLibrarySelectionMode(true)));
document.querySelectorAll('.btn-library-cancel-selection').forEach(button => button.addEventListener('click', () => setLibrarySelectionMode(false)));
document.querySelectorAll('.btn-library-remove-selected').forEach(button => button.addEventListener('click', removeSelectedLibraryImages));
document.querySelectorAll('.btn-library-hard-reevaluate').forEach(button => button.addEventListener('click', hardReevaluateSelectedLibraryImages));

['library-sort','library-rating-filter','library-renderer-filter','library-agent-min','library-human-min'].forEach(id => {
    const element = document.getElementById(id);
    const eventName = element?.tagName === 'INPUT' ? 'input' : 'change';
    element?.addEventListener(eventName, () => setLibraryView(currentLibraryView));
});
document.getElementById('library-collection-filter')?.addEventListener('change', event => {
    libraryCollectionFilter = event.target.value;
    setLibraryView(currentLibraryView);
});

// ==================== ASSET DETAIL ====================
function openAssetDetail(asset) {
    const modal = document.getElementById('asset-detail-modal');
    modal.style.display = 'flex';
    const safe = (value) => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const imageUrl = (path) => `/api/image?path=${encodeURIComponent(path || '')}`;
    const stages = asset.stage_images || {};
    const automatic = asset.automatic_final_stage_decision || {};
    const effective = asset.effective_final_stage_decision || automatic;
    const comparison = asset.comparative_review || {};
    const human = asset.human_review || {};
    const humanStages = human.stages || {};
    document.getElementById('asset-stage-compare').style.display = stages.illustrious && stages.klein ? 'block' : 'none';

    const assetCharacterName = asset.character_display_name || asset.character;
    document.getElementById('asset-detail-title').textContent = `${assetCharacterName} — ${asset.concept_id || ''}`;
    document.getElementById('asset-detail-image').src = imageUrl(asset.full_image_path);
    document.getElementById('asset-detail-image-link').href = imageUrl(asset.full_image_path);
    for (const stage of ['illustrious', 'klein']) {
        const src = imageUrl(stages[stage]);
        document.getElementById(`compare-${stage}-image`).src = src;
        document.getElementById(`compare-${stage}-link`).href = src;
    }
    
    const meta = document.getElementById('asset-detail-meta');
    const series = [asset.franchise, asset.universe].filter((value, index, values) => value && values.indexOf(value) === index).join(' · ');
    meta.innerHTML = `
        <p><strong>${safe(assetCharacterName)}</strong></p>
        <p style="color:var(--text-secondary)">${safe(series)}</p>
        <p><strong>Final selection:</strong> <span class="badge online">${safe((effective.selected_stage || 'unknown').toUpperCase())}</span> · ${safe(effective.source || 'unknown')}</p>
        <p style="color:var(--text-secondary)">${safe(effective.reason || '')}</p>
        <p><strong>Automatic selection:</strong> ${safe((automatic.selected_stage || 'unknown').toUpperCase())}${automatic.requires_human_review ? ' · human review requested' : ''}</p>
        <p><strong>Comparative winner:</strong> <span class="badge">${safe(comparison.preferred_stage || 'LEGACY / NOT AVAILABLE')}</span>${comparison.confidence !== undefined ? ` · confidence ${safe(comparison.confidence)}` : ''}</p>
        ${comparison.comparison?.overall_preference ? `<p style="color:var(--text-secondary)">${safe(comparison.comparison.overall_preference.reason)}</p>` : ''}
        <p>${asset.favorite ? '<span style="color:var(--error)">♥ Favorite</span>' : ''}</p>
        <p style="margin-top:12px; font-size:0.9em; color:var(--text-secondary)">${safe(asset.concept_snapshot || '')}</p>
        ${asset.tags && asset.tags.length ? '<p style="margin-top:8px">' + asset.tags.map(t => `<span class="badge">${safe(t)}</span> `).join('') + '</p>' : ''}
    `;

    const machineReviews = {illustrious: asset.illustrious_review || {}, klein: asset.final_review || {}};
    for (const stage of ['illustrious', 'klein']) {
        const machine = machineReviews[stage];
        const stageHuman = humanStages[stage] || {status: 'UNREVIEWED', rating: null};
        document.getElementById(`compare-${stage}-summary`).innerHTML = `
            <div>Machine: <span class="badge ${machine.verdict === 'PASS' ? 'online' : 'warning'}">${safe(machine.verdict || 'UNKNOWN')}</span></div>
            <div>Human: <span class="badge">${safe(stageHuman.status || 'UNREVIEWED')}</span>${stageHuman.rating ? ` · ${safe(stageHuman.rating)}/5` : ''}</div>
        `;
    }
    
    // Favorite button
    const favBtn = document.getElementById('btn-asset-favorite');
    favBtn.textContent = asset.favorite ? '♥ Unfavorite' : '♥ Favorite';
    favBtn.onclick = async () => {
        await fetch(`/api/library/review/${asset.asset_id}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({favorite: !asset.favorite})
        });
        asset.favorite = !asset.favorite;
        favBtn.textContent = asset.favorite ? '♥ Unfavorite' : '♥ Favorite';
        loadLibrary();
    };

    // Asset Inspector Action Buttons
    document.getElementById('btn-asset-set-hero').onclick = async () => {
        try {
            await fetch(`/api/characters/${encodeURIComponent(asset.character)}/hero`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({asset_id: asset.asset_id})
            });
            await loadLibrary();
            document.getElementById('btn-close-asset').click();
        } catch (e) {
            console.error(e);
        }
    };
    
    document.getElementById('btn-asset-generate-alt').onclick = () => {
        document.getElementById('btn-close-asset').click();
        workspaceCreateIntent();
    };
    
    document.getElementById('btn-asset-reinterpret').onclick = () => {
        document.getElementById('btn-close-asset').click();
        workspaceCreateIntent();
    };
    
    document.getElementById('btn-asset-compare').onclick = () => {
        document.getElementById('btn-close-asset').click();
        openAssetComparison(asset);
    };
    const saveHumanReview = async (update) => {
        const response = await fetch(`/api/library/review/${asset.asset_id}`, {
            method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(update)
        });
        if (!response.ok) window.alert('Could not save the human review.');
        else {
            const result = await response.json();
            if (result.asset) Object.assign(asset, result.asset);
            else asset.human_review = result.review || asset.human_review;
            loadLibrary();
            openAssetDetail(asset);
        }
    };
    for (const stage of ['illustrious', 'klein']) {
        document.getElementById(`btn-${stage}-approve`).onclick = () => saveHumanReview({stage, human_status: 'APPROVED'});
        document.getElementById(`btn-${stage}-reject`).onclick = () => saveHumanReview({stage, human_status: 'REJECTED'});
        const rating = document.getElementById(`${stage}-rating`);
        rating.value = (humanStages[stage] || {}).rating || '';
        rating.onchange = () => rating.value && saveHumanReview({stage, rating: Number(rating.value)});
    }
    const preference = human.preference || 'NONE';
    for (const [button, value] of [['btn-prefer-illustrious', 'ILLUSTRIOUS'], ['btn-prefer-klein', 'KLEIN'], ['btn-prefer-none', 'NONE']]) {
        const element = document.getElementById(button);
        element.classList.toggle('active', preference === value);
        element.onclick = () => saveHumanReview({preference: value});
    }
    
    // Technical details
    const tech = document.getElementById('asset-detail-technical');
    const details = (label, value) => value ? `<p><strong>${label}:</strong></p><pre>${JSON.stringify(value, null, 2)}</pre>` : '';
    tech.innerHTML = `
        <p><strong>Asset ID:</strong> ${asset.asset_id}</p>
        <p><strong>Source Run:</strong> ${asset.source_run_id}</p>
        <p><strong>Source Mission:</strong> ${asset.source_mission_id || 'N/A'}</p>
        <p><strong>Creative Model:</strong> ${asset.creative_model}</p>
        <p><strong>Created:</strong> ${asset.created_at}</p>
        ${details('Semantic contract versions', asset.semantic_contract_versions)}
        ${details('Character Contract', asset.character_contract)}
        ${details('Resolved Render Spec', asset.resolved_render_spec)}
        ${details('Stage Render Plans', asset.stage_render_plans)}
        ${details('Prompt Artifacts', asset.prompt_artifacts)}
        ${details('Render Receipts', asset.render_receipts)}
        ${details('Review Observations', asset.review_observations)}
        ${details('Routing Decisions', asset.routing_decisions)}
        ${details('Comparative Review', asset.comparative_review)}
        ${details('Automatic Final Stage Decision', asset.automatic_final_stage_decision)}
        ${details('Effective Final Stage Decision', asset.effective_final_stage_decision)}
        ${details('Human Stage Overrides', asset.human_stage_overrides)}
        ${details('Human Stage Review History', human.stage_review_history)}
        ${details('Character profile', asset.character_profile)}
        ${details('Illustrious generation', asset.illustrious_generation)}
        ${details('Klein generation', asset.klein_generation)}
        ${details('Creative layer', asset.creative_layer)}
        ${details('Selection ranking', {rank: asset.selection_rank, reason: asset.selection_reason, scores: asset.m3_scores})}
        ${details('Illustrious Review', asset.illustrious_review)}
        ${details('Final Review', asset.final_review)}
    `;
}

async function loadMissionFunnel(missionId) {
    const content = document.getElementById('mission-detail-content');
    if (!content) return;
    document.getElementById('mission-funnel')?.remove();
    try {
        const response = await fetch(`/api/missions/${missionId}/funnel`);
        if (!response.ok) return;
        const data = await response.json();
        const rows = (data.concepts || []).map(item => `<tr><td>${item.concept_id}</td><td>${item.selected ? `#${item.selection_rank || '—'}` : 'Not selected'}</td><td>${item.pipeline_state}</td><td>${item.machine_review?.verdict || '—'}</td><td>${item.asset_id || '—'}</td><td>${item.snapshot || ''}</td></tr>`).join('');
        content.insertAdjacentHTML('beforeend', `<div id="mission-funnel" class="card mt-1"><h3>Concepts → Candidates → Assets</h3><p style="color:var(--text-secondary)">Not selected means it did not enter production; terminal candidate states show the actual machine outcome.</p><div style="overflow:auto"><table><thead><tr><th>Concept</th><th>Selection</th><th>Production</th><th>Machine review</th><th>Library asset</th><th>Hook</th></tr></thead><tbody>${rows || '<tr><td colspan="6">No persisted funnel data yet.</td></tr>'}</tbody></table></div></div>`);
    } catch (e) { /* Mission summary remains usable if old artifacts lack the funnel. */ }
}

document.getElementById('btn-close-asset').addEventListener('click', () => {
    document.getElementById('asset-detail-modal').style.display = 'none';
});

// ==================== MODEL LAB ====================
async function loadModelLab() {
    const modelsContainer = document.getElementById('model-lab-models');
    const runsContainer = document.getElementById('model-lab-runs');
    const safe = (value) => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    try {
        const response = await fetch('/api/model-lab');
        const data = await response.json();
        modelsContainer.innerHTML = (data.models || []).map(model => {
            const profile = model.capability_profile || {};
            const classification = model.classification || {};
            const recipe = profile.test_recipe || {};
            return `<article class="card model-lab-card">
                <div class="flex-between"><h3>${safe(model.file)}</h3><span class="badge ${model.status === 'production_baseline' ? 'online' : 'info'}">${safe(model.status)}</span></div>
                <p><strong>${safe(classification.type)}</strong> · ${safe(classification.family)} · ${safe(classification.architecture)}</p>
                <p>Loader: ${safe(classification.loader?.name || 'unknown')} <span class="badge">${safe(classification.loader?.status || 'unknown')}</span></p>
                <p>Size: ${model.size_gib == null ? 'configured' : safe(model.size_gib) + ' GiB'} · tensors: ${safe(model.tensor_summary?.count ?? '—')}</p>
                <p>Test: <span class="badge ${recipe.status === 'ready' ? 'online' : 'warning'}">${safe(recipe.status || 'unknown')}</span></p>
                <details><summary>Evidence and capabilities</summary><pre>${safe(JSON.stringify({evidence: classification.evidence, capabilities: profile.capabilities, metadata: model.metadata}, null, 2))}</pre></details>
            </article>`;
        }).join('') || '<p>No discovered models.</p>';

        const select = document.getElementById('model-lab-model');
        select.innerHTML = (data.models || []).map(model => {
            const recipe = model.capability_profile?.test_recipe || {};
            const ready = recipe.status === 'ready' && recipe.runner === 'klein_production_baseline_v1';
            return `<option value="${safe(model.id)}" ${ready ? '' : 'disabled'}>${safe(model.file)} — ${ready ? 'single runner ready' : (recipe.runner === 'direct_generator_benchmark_v1' ? 'use Direct Generator Benchmark' : 'recipe unavailable')}</option>`;
        }).join('');
        document.getElementById('model-lab-source').value = data.suggested_source || '';
        document.getElementById('model-lab-prompt').value = data.default_prompt || '';

        runsContainer.innerHTML = (data.runs || []).map(run => `<article class="card model-lab-card">
            <div class="flex-between"><h3>${safe(run.character)} · ${safe(run.model_id)}</h3><span class="badge ${run.status === 'COMPLETE' ? 'online' : 'warning'}">${safe(run.status)}</span></div>
            ${run.output_asset ? `<a href="/api/image?path=${encodeURIComponent(run.output_asset)}" target="_blank"><img src="/api/image?path=${encodeURIComponent(run.output_asset)}" alt="Model Lab output" loading="lazy"></a>` : ''}
            <p>${safe(run.duration_seconds ?? '—')} seconds · score ${safe(run.result?.score ?? '?')}</p>
            <details><summary>Model Test Receipt</summary><pre>${safe(JSON.stringify(run, null, 2))}</pre></details>
        </article>`).join('') || '<p style="color:var(--text-secondary)">No Model Lab tests yet.</p>';
        const missing = data.missing_files || [];
        document.getElementById('model-lab-scan-status').innerHTML = missing.length
            ? `<p class="badge warning">Missing: ${missing.map(safe).join(', ')}</p>`
            : `<p class="badge online">All requested files discovered</p>`;
        loadModelBenchmarks();
    } catch (error) {
        modelsContainer.innerHTML = `<p class="error">Could not load Model Lab: ${safe(error.message)}</p>`;
    }
}

document.getElementById('btn-model-scan').addEventListener('click', async () => {
    const status = document.getElementById('model-lab-scan-status');
    status.textContent = 'Scanning safetensors headers…';
    const response = await fetch('/api/model-lab/scan', {method: 'POST'});
    if (!response.ok) status.textContent = 'Model scan failed.';
    else loadModelLab();
});

async function loadModelBenchmarks() {
    const container = document.getElementById('model-benchmark-results');
    const safe = (value) => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const response = await fetch('/api/model-lab/benchmarks');
    const benchmarks = await response.json();
    if (!benchmarks.length) {
        container.innerHTML = '<p style="color:var(--text-secondary)">Initialize the official benchmark to create its first controlled test case.</p>';
        return;
    }
    container.innerHTML = benchmarks.map(benchmark => {
        const rankingRows = Object.entries(benchmark.rankings || {}).map(([role, rows]) => rows.length
            ? `<p><strong>${safe(role)}:</strong> ${rows.map((row, index) => `${index + 1}. ${safe(row.model_id)} ${safe(row.score)} (${safe(row.samples)} samples)`).join(' · ')}</p>`
            : '').join('');
        const recipeRanking = (benchmark.recipe_rankings || []).length
            ? `<p><strong>Recipe ranking:</strong> ${benchmark.recipe_rankings.map((row, index) => `${index + 1}. ${safe(row.recipe_id)} ${safe(row.score)} (${safe(row.samples)} samples)`).join(' · ')}</p>` : '';
        const speedQuality = (benchmark.speed_quality || []).length
            ? `<p><strong>Speed vs quality:</strong> ${benchmark.speed_quality.map(row => `${safe(row.recipe_id)} — ${safe(row.quality)}/10, ${safe(row.average_seconds ?? '—')}s`).join(' · ')}</p>` : '';
        const cases = (benchmark.cases || []).map(item => {
            const test = item.test_case;
            const dimensions = test.evaluation_dimensions || [];
            const eligibleRecipes = (benchmark.recipes || []).filter(recipe => (test.recipe_ids || []).includes(recipe.recipe_id) && recipe.availability?.ready);
            const recipeControl = eligibleRecipes.length ? `<div class="benchmark-run-controls">
                <label>Experimental model + recipe<select class="benchmark-recipe-select">${eligibleRecipes.map(recipe => `<option value="${safe(recipe.recipe_id)}" data-model="${safe(recipe.model_id)}">${safe(recipe.model_id)} — ${safe(recipe.recipe_id)}</option>`).join('')}</select></label>
                <button class="btn benchmark-run" data-benchmark="${safe(test.benchmark_id)}" data-test="${safe(test.test_id)}">Run exactly one image</button>
            </div>` : (test.status !== 'BLOCKED' && !(test.recipe_ids || []).length ? `<button class="btn benchmark-run" data-benchmark="${safe(test.benchmark_id)}" data-test="${safe(test.test_id)}" data-model="${safe(test.models[0])}">Run one controlled image</button>` : '');
            const executions = (item.executions || []).map(entry => {
                const run = entry.receipt;
                const latest = (entry.evaluations || []).slice(-1)[0];
                const scoreGrid = dimensions.map(dimension => `<label>${safe(dimension.replaceAll('_', ' '))}<input class="benchmark-score" data-dimension="${dimension}" type="number" min="1" max="10" value="${latest?.scores?.[dimension] || ''}"></label>`).join('');
                return `<article class="benchmark-result-card" data-run-id="${safe(run.run_id)}">
                    <div class="flex-between"><h4>${safe(run.character)} · ${safe(run.model_id)}</h4><span class="badge ${run.status === 'COMPLETE' ? 'online' : 'warning'}">${safe(run.status)}</span></div>
                    <div class="benchmark-images">
                        ${run.input_asset ? `<div><small>Input</small><a href="/api/image?path=${encodeURIComponent(run.input_asset)}" target="_blank"><img src="/api/image?path=${encodeURIComponent(run.input_asset)}" alt="Benchmark input"></a></div>` : ''}
                        ${run.output_asset ? `<div><small>Output</small><a href="/api/image?path=${encodeURIComponent(run.output_asset)}" target="_blank"><img src="/api/image?path=${encodeURIComponent(run.output_asset)}" alt="Benchmark output"></a></div>` : ''}
                    </div>
                    <p>Role: <strong>${safe(test.role)}</strong> · recipe ${safe(run.recipe_id || '—')} · total ${safe(run.duration_seconds)}s · inference ${safe(run.inference_seconds ?? '—')}s · ${safe(run.configuration?.resolution?.width ?? '—')}×${safe(run.configuration?.resolution?.height ?? '—')} · ${safe(run.configuration?.sampling?.steps ?? run.configuration?.sampling?.first_pass?.steps ?? '—')} steps · job size ${safe(run.job_size ?? 1)}</p>
                    <div class="benchmark-score-grid">${scoreGrid}</div>
                    <label>Human notes<textarea class="benchmark-notes" rows="2">${safe(latest?.notes || '')}</textarea></label>
                    <button class="btn btn-primary benchmark-save" data-benchmark="${safe(test.benchmark_id)}" data-test="${safe(test.test_id)}" data-run="${safe(run.run_id)}">Save human evaluation</button>
                    <details><summary>Technical receipt</summary><pre>${safe(JSON.stringify(run, null, 2))}</pre></details>
                </article>`;
            }).join('') || `<p>No execution yet. Status: ${safe(test.status)}</p>`;
            return `<section class="card"><h3>${safe(test.test_id)}</h3><p>${safe(test.scene_intent || '')}</p>${recipeControl}${executions}</section>`;
        }).join('');
        return `<div><h3>${safe(benchmark.manifest.title)}</h3><p>${safe(benchmark.manifest.decision_question)}</p>${rankingRows}${recipeRanking}${speedQuality}${cases}</div>`;
    }).join('');
    document.querySelectorAll('.benchmark-save').forEach(button => {
        button.onclick = async () => {
            const card = button.closest('.benchmark-result-card');
            const scores = {};
            card.querySelectorAll('.benchmark-score').forEach(input => scores[input.dataset.dimension] = Number(input.value));
            const response = await fetch(`/api/model-lab/benchmarks/${button.dataset.benchmark}/tests/${button.dataset.test}/evaluate`, {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({run_id: button.dataset.run, scores, notes: card.querySelector('.benchmark-notes').value}),
            });
            const result = await response.json();
            if (!response.ok) window.alert(result.error || 'Could not save evaluation.');
            else loadModelBenchmarks();
        };
    });
    document.querySelectorAll('.benchmark-run').forEach(button => {
        button.onclick = async () => {
            const section = button.closest('section');
            const recipeSelect = section?.querySelector('.benchmark-recipe-select');
            const selectedOption = recipeSelect?.selectedOptions?.[0];
            const modelId = selectedOption?.dataset?.model || button.dataset.model;
            const recipeId = selectedOption?.value || '';
            button.disabled = true;
            button.textContent = 'Running one image…';
            const response = await fetch(`/api/model-lab/benchmarks/${button.dataset.benchmark}/tests/${button.dataset.test}/run`, {
                method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({model_id: modelId, recipe_id: recipeId}),
            });
            const result = await response.json();
            if (!response.ok) window.alert(result.error || 'Benchmark execution failed.');
            loadModelBenchmarks();
        };
    });
}

document.getElementById('btn-benchmark-initialize').addEventListener('click', async () => {
    await fetch('/api/model-lab/benchmarks/initialize', {method: 'POST'});
    loadModelBenchmarks();
});

document.getElementById('btn-direct-benchmark-initialize').addEventListener('click', async () => {
    await fetch('/api/model-lab/benchmarks/initialize-direct', {method: 'POST'});
    loadModelBenchmarks();
});

document.getElementById('btn-model-lab-run').addEventListener('click', async () => {
    const status = document.getElementById('model-lab-run-status');
    status.textContent = 'Running one isolated Model Lab image…';
    const response = await fetch('/api/model-lab/run', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            model_id: document.getElementById('model-lab-model').value,
            character: document.getElementById('model-lab-character').value,
            source_image: document.getElementById('model-lab-source').value,
            prompt: document.getElementById('model-lab-prompt').value,
            seed: Number(document.getElementById('model-lab-seed').value),
        }),
    });
    const result = await response.json();
    status.textContent = response.ok ? `${result.status}: ${result.output_asset || result.error || ''}` : (result.error || 'Model Lab run failed.');
    loadModelLab();
});

// ==================== RUNS (ADVANCED) ====================
function runStatusLabel(status) {
    return ({
        COMPLETE_TEXT_ONLY: 'Concepts ready',
        COMPLETE: 'Complete',
        FAILED: 'Failed',
        RUNNING: 'Running',
    })[status] || String(status || '—').replaceAll('_', ' ').toLowerCase().replace(/^./, char => char.toUpperCase());
}

async function loadRuns() {
    try {
        const resp = await fetch('/api/runs');
        const runs = await resp.json();
        const tbody = document.querySelector('#runs-table tbody');
        tbody.innerHTML = '';
        
        runs.forEach(r => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="run-cell-id" title="${escapeHtml(r.run_id)}">${escapeHtml(r.run_id)}</td>
                <td>${escapeHtml(r.run_type || '—')}</td>
                <td>${escapeHtml(r.character || '—')}</td>
                <td class="run-cell-model" title="${escapeHtml(r.source_model || '—')}">${escapeHtml(r.source_model || '—')}</td>
                <td title="${escapeHtml(r.status || '—')}">${escapeHtml(runStatusLabel(r.status))}</td>
                <td>${escapeHtml(r.created_at ? new Date(r.created_at).toLocaleString() : '—')}</td>
                <td><button class="btn run-view-button" type="button">View</button></td>
            `;
            tr.querySelector('.run-view-button').addEventListener('click', () => openRunDetail(r.run_id));
            tbody.appendChild(tr);
        });
    } catch (e) {}
}

async function openRunDetail(runId) {
    try {
        const resp = await fetch(`/api/runs/${runId}`);
        currentRun = await resp.json();
        currentRun.run_id = runId;
        
        document.getElementById('run-detail').style.display = 'block';
        document.getElementById('detail-title').textContent = `Run: ${runId}`;
        
        const overview = document.getElementById('detail-overview');
        overview.innerHTML = `
            <p>Valid: ${currentRun.valid_count} / Requested: ${currentRun.requested_count}</p>
            <p>Rejected: ${currentRun.rejected_count}</p>
        `;
        
        document.getElementById('telemetry-pre').textContent = JSON.stringify(currentRun.telemetry, null, 2);
        
        renderConcepts(currentRun.concepts || [], 'detail-concepts');
    } catch (e) {}
}

document.getElementById('btn-close-detail')?.addEventListener('click', () => {
    document.getElementById('run-detail').style.display = 'none';
});

// ==================== CREATIVE LAB ====================
document.getElementById('btn-generate-concepts')?.addEventListener('click', async () => {
    const status = document.getElementById('generate-status');
    status.textContent = 'Generating concepts...';
    try {
        await fetch('/api/creative_expansion', {method: 'POST'});
        status.textContent = 'Creative expansion started in background.';
    } catch (e) {
        status.textContent = 'Error starting creative expansion.';
    }
});

document.getElementById('btn-generate-pilot')?.addEventListener('click', async () => {
    const count = parseInt(document.getElementById('lab-concept-count').value) || 12;
    const pilotCount = parseInt(document.getElementById('lab-pilot-count').value) || 3;
    const status = document.getElementById('generate-status');
    status.textContent = 'Generating pilot...';
    
    try {
        const resp = await fetch('/api/pilot/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({conceptCount: count, pilotCount: pilotCount})
        });
        const result = await resp.json();
        status.textContent = `Pilot started: ${result.run_id}`;
        currentRun = {run_id: result.run_id};
        
        document.getElementById('pilot-status-card').style.display = 'block';
        if (pollInterval) clearInterval(pollInterval);
        pollInterval = setInterval(() => pollPilot(result.run_id), 3000);
    } catch (e) {
        status.textContent = 'Error starting pilot.';
    }
});

async function pollPilot(runId) {
    try {
        const resp = await fetch(`/api/runs/${runId}/pilot`);
        const candidates = await resp.json();
        
        const container = document.getElementById('pilot-status-container');
        container.innerHTML = '';
        
        candidates.forEach(c => {
            const card = document.createElement('div');
            card.className = 'card';
            card.style.marginBottom = '8px';
            
            let imgHtml = '';
            if (c.klein_image) {
                imgHtml = `<img src="/api/image?path=${encodeURIComponent(c.klein_image)}" style="width:100%; max-width:200px; border-radius:4px;">`;
            } else if (c.illustrious_image) {
                imgHtml = `<img src="/api/image?path=${encodeURIComponent(c.illustrious_image)}" style="width:100%; max-width:200px; border-radius:4px; opacity:0.7;">`;
            }
            
            card.innerHTML = `
                <div style="display:flex; gap:12px; align-items:start;">
                    ${imgHtml}
                    <div>
                        <h4>${c.concept_id}</h4>
                        <p>Status: <strong>${c.pipeline_state}</strong></p>
                        ${c.quality_retries > 0 ? `<span class="badge warning">Retries: ${c.quality_retries}/${c.max_retries || 2}</span>` : ''}
                        ${c.retry_reason ? `<p style="font-size:0.85em; color:var(--error)">${c.retry_reason}</p>` : ''}
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
        
        const terminals = ['APPROVED', 'REJECTED_QUALITY', 'RETRY_EXHAUSTED', 'FAILED_RUNTIME'];
        if (candidates.length > 0 && candidates.every(c => terminals.includes(c.pipeline_state))) {
            clearInterval(pollInterval);
        }
    } catch (e) {}
}

// ==================== CONCEPTS RENDERER ====================
function renderConcepts(concepts, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    concepts.forEach(c => {
        const card = document.createElement('div');
        card.className = `concept-card ${c.status === 'PASS' ? 'pass' : 'fail'}`;
        
        card.innerHTML = `
            <div class="concept-header">
                <span>${c.concept_id}</span>
                <span class="badge ${c.status === 'PASS' ? 'online' : 'offline'}">${c.status}</span>
            </div>
            <div class="concept-body">
                <p><strong>Hook:</strong> ${c.hook || ''}</p>
                <p><strong>Composition:</strong> ${c.composition || ''}</p>
            </div>
            ${c.human_decision ? `<div class="decision-badge ${c.human_decision}">${c.human_decision}</div>` : ''}
        `;
        container.appendChild(card);
    });
}

// ==================== ROADMAP ====================
async function loadRoadmap() {
    try {
        const resp = await fetch('/api/roadmap');
        const data = await resp.json();
        const container = document.getElementById('roadmap-container');
        container.innerHTML = '';
        
        if (data.milestones) {
            const msContainer = document.createElement('div');
            msContainer.className = 'roadmap-category';
            msContainer.innerHTML = '<h2>Milestones</h2>';
            data.milestones.forEach(m => {
                const div = document.createElement('div');
                div.className = `roadmap-item ${m.status === 'Complete' ? 'complete' : 'planned'}`;
                const icon = m.status === 'Complete' ? '✓' : m.status === 'In Progress' ? '◐' : '○';
                div.innerHTML = `<span class="status-icon">${icon}</span><div><strong>${m.name}</strong><br><small style="color:var(--text-secondary)">${m.status}</small></div>`;
                msContainer.appendChild(div);
            });
            container.appendChild(msContainer);
        }

        if (data.categories) {
            data.categories.forEach(cat => {
                const catContainer = document.createElement('div');
                catContainer.className = 'roadmap-category';
                catContainer.innerHTML = `<h2>${cat.category}</h2>`;
                cat.items.forEach(m => {
                    const div = document.createElement('div');
                    div.className = `roadmap-item ${m.status === 'Complete' ? 'complete' : 'planned'}`;
                    const icon = m.status === 'Complete' ? '✓' : m.status === 'In Progress' ? '◐' : '○';
                    div.innerHTML = `<span class="status-icon">${icon}</span><div><strong>${m.name}</strong><br><small style="color:var(--text-secondary)">${m.status}</small>${m.description ? `<p class="roadmap-description">${m.description}</p>` : ''}</div>`;
                    catContainer.appendChild(div);
                });
                container.appendChild(catContainer);
            });
        }
    } catch (e) {}
}

// ==================== SETTINGS ====================
async function loadSettings() {
    try {
        const resp = await fetch('/api/system');
        const data = await resp.json();
        
        const lm = document.getElementById('status-lm');
        lm.textContent = data.lm_studio;
        lm.className = `badge ${data.lm_studio === 'Online' ? 'online' : 'offline'}`;
        
        const comfy = document.getElementById('status-comfy');
        comfy.textContent = data.comfyui;
        comfy.className = `badge ${data.comfyui === 'Online' ? 'online' : 'offline'}`;
    } catch (e) {}
}

// ==================== TAB BTN HANDLERS ====================
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const parent = btn.closest('.tabs') || btn.parentElement;
        parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        const target = btn.dataset.target;
        if (target) {
            const container = btn.closest('.card') || btn.closest('.tab-content');
            if (container) {
                container.querySelectorAll('.detail-pane').forEach(p => p.classList.remove('active'));
                const pane = document.getElementById(target);
                if (pane) pane.classList.add('active');
            }
        }
    });
});

// ==================== INIT ====================
loadHome();
loadSettings();
loadCharacters();

// Hide ADVANCED section if empty
document.addEventListener('DOMContentLoaded', () => {
    const advancedDetails = document.querySelector('.nav-section details');
    if (advancedDetails) {
        const lis = advancedDetails.querySelectorAll('li');
        const anyVisible = Array.from(lis).some(li => window.getComputedStyle(li).display !== 'none');
        if (!anyVisible) advancedDetails.style.display = 'none';
    }
});
