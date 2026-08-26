// Library Image v2 inspector. Technical provenance stays available but collapsed.
function libraryEsc(value) {
    return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function libraryImageUrl(path) {
    return `/api/image?path=${encodeURIComponent(path || '')}`;
}

function libraryRating(value) {
    return typeof value === 'number' && value >= 1 && value <= 10 ? value : null;
}

async function saveLibraryImageReview(asset, update) {
    const response = await fetch(`/api/library/review/${encodeURIComponent(asset.asset_id)}`, {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(update),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'Could not save Library metadata.');
    await loadLibrary();
    return allAssets.find(item => item.asset_id === asset.asset_id) || payload.asset || asset;
}

function renderTechnicalDetails(asset, output) {
    const receipt = output?.receipt || {};
    const generation = receipt.generation || {};
    const review = output?.review || {};
    const prompt = generation.positive_prompt || generation.prompt || asset.prompt_artifacts?.[asset.renderer]?.prompt || '';
    const size = generation.width && generation.height ? `${generation.width}×${generation.height}` : '—';
    const source = asset.source_asset_id ? `<p><strong>Source asset:</strong> ${libraryEsc(asset.source_asset_id)}</p>` : '';
    return `
        <details><summary>Prompt</summary><textarea class="technical-prompt" readonly>${libraryEsc(prompt || 'Not available for this historical image.')}</textarea></details>
        <details><summary>Render settings</summary><div class="technical-summary">
            <p><strong>Renderer:</strong> ${libraryEsc(asset.renderer || '—')}</p><p><strong>Preset:</strong> ${libraryEsc(asset.preset || receipt.preset || '—')}</p>
            <p><strong>Resolution:</strong> ${libraryEsc(size)}</p><p><strong>Steps:</strong> ${libraryEsc(generation.steps ?? '—')} &nbsp; <strong>CFG:</strong> ${libraryEsc(generation.cfg ?? '—')}</p>
            <p><strong>Sampler:</strong> ${libraryEsc(generation.sampler || '—')} &nbsp; <strong>Seed:</strong> ${libraryEsc(generation.seed ?? '—')}</p>
        </div></details>
        <details><summary>Machine review</summary><div class="technical-summary"><p><strong>${libraryEsc(review.verdict || 'UNKNOWN')}</strong> &nbsp; Agent rating: ${libraryRating(asset.agent_rating) ?? '—'}</p><p>${libraryEsc(review.summary || 'No summary available.')}</p></div><pre>${libraryEsc(JSON.stringify(asset.review_observations?.[asset.renderer] || {}, null, 2))}</pre></details>
        <details><summary>Lineage</summary><div class="technical-summary"><p><strong>Character:</strong> ${libraryEsc(asset.character)}</p><p><strong>Generation:</strong> ${libraryEsc(asset.generation_id)}</p>${source}<p><strong>Sibling images:</strong> ${libraryEsc((asset.lineage?.sibling_image_ids || []).join(', ') || '—')}</p><p><strong>Run:</strong> ${libraryEsc(asset.source_run_id || '—')}</p></div></details>
        <details><summary>Raw JSON</summary><pre>${libraryEsc(JSON.stringify(asset, null, 2))}</pre></details>`;
}

function openAssetDetailGeneric(asset) {
    if (!asset) return;
    const modal = document.getElementById('asset-detail-modal');
    modal.style.display = 'flex';
    document.getElementById('reinterpret-panel')?.remove();
    const peers = comparisonItemsForAsset(asset);
    const output = (asset.render_outputs || []).find(item => item?.renderer === asset.renderer) || {};
    const humanRating = libraryRating(asset.human_rating ?? asset.human_review?.rating);
    const agentRating = libraryRating(asset.agent_rating);
    const status = asset.library_status || 'UNREVIEWED';
    const displayStatus = status === 'UNREVIEWED' ? 'Awaiting human review' : status;

    document.getElementById('asset-detail-title').textContent = asset.display_title || asset.character || 'Library image';
    document.getElementById('asset-detail-image').src = libraryImageUrl(asset.full_image_path);
    document.getElementById('asset-detail-image-link').href = libraryImageUrl(asset.full_image_path);
    document.getElementById('asset-detail-meta').innerHTML = `
        <p class="asset-short-description">${libraryEsc(asset.short_description || '')}</p>
        <p class="asset-renderer-name">${libraryEsc((asset.renderer || 'Unknown').replace(/^./, c => c.toUpperCase()))}</p>
        <p><span class="badge ${status === 'APPROVED' ? 'online' : status === 'REJECTED' ? 'warning' : ''}">${libraryEsc(displayStatus)}</span></p>
        
        <hr style="border:none;border-top:1px solid var(--border-color);margin:16px 0 8px 0;">
        <div style="color:var(--text-secondary);font-size:0.75em;text-transform:uppercase;margin-bottom:8px;letter-spacing:1px;">Machine Evaluation</div>
        <div class="rating-row"><span>Agent rating (Visual Review)</span><strong>${agentRating === null ? '—' : `${agentRating} / 10`}</strong></div>
        
        <hr style="border:none;border-top:1px solid var(--border-color);margin:16px 0 8px 0;">
        <div style="color:var(--text-secondary);font-size:0.75em;text-transform:uppercase;margin-bottom:8px;letter-spacing:1px;">Latest Hard Re-Evaluation</div>
        
        <div style="margin: 8px 0;">
            <button id="btn-modal-hard-reevaluate" class="btn btn-warning" style="width: 100%;">
                ${asset.human_review?.hard_rating && !asset.human_review.hard_rating.evaluation_failed ? 'Re-Evaluate Again' : 'Hard Re-Evaluate'}
            </button>
            <div id="hard-reeval-error" style="color:var(--danger);font-size:0.85em;margin-top:8px;display:none;"></div>
        </div>
        
        ${asset.human_review?.hard_rating && asset.human_review.hard_rating.evaluation_failed ? `
        <div style="color:var(--danger); font-size:0.85em; padding:8px; background:var(--bg-panel); border-left: 2px solid var(--danger); margin-bottom: 8px;">
            Evaluation failed. See backend logs.
        </div>
        ` : asset.human_review?.hard_rating ? `
        <div class="rating-row" style="color:var(--accent);"><span>Hard rating</span><strong>${asset.human_review.hard_rating.final_score} / 100 &nbsp; Hard ✓</strong></div>
        <div class="rating-row" style="color:var(--text-secondary);"><span>Delta</span><strong>${asset.human_review.hard_rating.delta > 0 ? '+' : ''}${asset.human_review.hard_rating.delta}</strong></div>
        
        <div style="margin: 12px 0; padding-left: 8px; border-left: 2px solid var(--border-color);">
            <div style="display:flex; justify-content:space-between; margin-bottom: 4px;"><span>Quality</span><strong>${asset.human_review.hard_rating.basic_quality}</strong></div>
            <div style="display:flex; justify-content:space-between; margin-bottom: 4px;"><span>Primary Hook</span><strong>${asset.human_review.hard_rating.primary_attraction_hook}</strong></div>
            <div style="display:flex; justify-content:space-between;"><span>Context Hook</span><strong>${asset.human_review.hard_rating.contextual_hook}</strong></div>
        </div>
        
        ${asset.human_review.hard_rating.primary_hook_targets?.length ? `
        <div style="margin: 12px 0 4px 0;">
            <div style="color:var(--text-secondary); font-size:0.9em; margin-bottom:2px;">Primary hooks</div>
            <strong>${libraryEsc(asset.human_review.hard_rating.primary_hook_targets.join(' · '))}</strong>
        </div>` : ''}

        ${asset.human_review.hard_rating.context_hook_types?.length ? `
        <div style="margin: 12px 0 4px 0;">
            <div style="color:var(--text-secondary); font-size:0.9em; margin-bottom:2px;">Context hooks</div>
            <strong>${libraryEsc(asset.human_review.hard_rating.context_hook_types.join(' · '))}</strong>
        </div>` : ''}

        <p style="font-size:0.85em;color:var(--text-secondary);margin: 12px 0;font-style:italic;">
            ${libraryEsc(asset.human_review.hard_rating.hook_reason)}<br>
            ${libraryEsc(asset.human_review.hard_rating.context_reason)}
        </p>
        ` : ''}
        
        <hr style="border:none;border-top:1px solid var(--border-color);margin:16px 0 8px 0;">
        <div style="color:var(--text-secondary);font-size:0.75em;text-transform:uppercase;margin-bottom:8px;letter-spacing:1px;">Human Judgment</div>
        <label class="rating-row" for="asset-human-rating"><span>Your rating</span><select id="asset-human-rating" class="form-select rating-select"><option value="">Not rated</option>${Array.from({length:10}, (_, i) => `<option value="${i + 1}" ${humanRating === i + 1 ? 'selected' : ''}>${i + 1} / 10</option>`).join('')}</select></label>`;

    document.getElementById('asset-stage-compare').style.display = 'none';
    const compareButton = document.getElementById('btn-asset-compare');
    compareButton.style.display = peers.length > 1 ? '' : 'none';
    compareButton.onclick = () => { document.getElementById('btn-close-asset').click(); openAssetComparison(asset); };

    document.getElementById('asset-human-rating').onchange = async event => {
        if (!event.target.value) return;
        try { openAssetDetailGeneric(await saveLibraryImageReview(asset, {human_rating:Number(event.target.value)})); }
        catch (error) { window.alert(error.message); }
    };
    document.getElementById('btn-modal-hard-reevaluate')?.addEventListener('click', async (event) => {
        const btn = event.target;
        btn.disabled = true;
        btn.textContent = 'Evaluating...';
        document.getElementById('hard-reeval-error').style.display = 'none';
        try {
            const response = await fetch('/api/library/hard-reevaluate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({asset_ids: [asset.asset_id]})
            });
            if (!response.ok) throw new Error('Failed to run hard re-evaluate');
            const data = await response.json();
            if (data.results && data.results[asset.asset_id]) {
                const resData = data.results[asset.asset_id];
                if (resData.evaluation_failed) {
                    const errDiv = document.getElementById('hard-reeval-error');
                    errDiv.textContent = "Evaluation failed: " + resData.error;
                    errDiv.style.display = 'block';
                    btn.disabled = false;
                    btn.textContent = 'Hard Re-Evaluate';
                    return;
                }
                if (!asset.human_review) asset.human_review = {};
                asset.human_review.hard_rating = resData;
                // Reload modal in place
                openAssetDetailGeneric(asset);
                // Also silent reload main grid if possible, to update card badges
                if (typeof loadLibrary === 'function') {
                    loadLibrary(); 
                }
            } else {
                throw new Error('Evaluation did not return results');
            }
        } catch (e) {
            btn.disabled = false;
            btn.textContent = asset.human_review?.hard_rating ? 'Re-Evaluate Again' : 'Hard Re-Evaluate';
            let errDiv = document.getElementById('hard-reevaluate-error');
            if (!errDiv) {
                errDiv = document.createElement('div');
                errDiv.id = 'hard-reevaluate-error';
                errDiv.style.color = 'var(--error)';
                errDiv.style.marginTop = '8px';
                errDiv.style.fontSize = '0.9em';
                btn.parentNode.appendChild(errDiv);
            }
            errDiv.textContent = e.message || 'Evaluation failed. Please try again.';
        }
    });

    const favorite = document.getElementById('btn-asset-favorite');
    favorite.textContent = asset.favorite ? '♥ Unfavorite' : '♥ Favorite';
    favorite.onclick = async () => {
        try { openAssetDetailGeneric(await saveLibraryImageReview(asset, {favorite:!asset.favorite})); }
        catch (error) { window.alert(error.message); }
    };
    document.getElementById('btn-asset-set-hero').onclick = async () => {
        const response = await fetch(`/api/characters/${encodeURIComponent(asset.character)}/hero`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({asset_id:asset.asset_id})});
        if (!response.ok) return window.alert('Could not set this image as hero.');
        await loadCharacterHeroes();
        await loadCharacterCatalog();
        document.getElementById('btn-asset-set-hero').textContent = 'Hero image';
    };
    const remove = document.getElementById('btn-asset-remove');
    remove.textContent = status === 'REJECTED' ? 'Restore to Library' : 'Remove from Library';
    remove.onclick = async () => {
        const rejecting = status !== 'REJECTED';
        if (rejecting && !window.confirm('Remove this image from the default Library gallery? The file and its history will be kept.')) return;
        try { openAssetDetailGeneric(await saveLibraryImageReview(asset, {human_status:rejecting ? 'REJECTED' : 'UNREVIEWED'})); }
        catch (error) { window.alert(error.message); }
    };
    document.getElementById('btn-asset-generate-alt').onclick = () => { document.getElementById('btn-close-asset').click(); prepareAlternativeFromAsset(asset); };
    document.getElementById('btn-asset-reinterpret').onclick = async () => {
        let panel = document.getElementById('reinterpret-panel');
        if (panel) { panel.remove(); return; }
        const response = await fetch('/api/characters');
        const characters = await response.json();
        panel = document.createElement('div'); panel.id = 'reinterpret-panel'; panel.className = 'card mt-1 reinterpret-panel';
        panel.innerHTML = `<h3>Reinterpret</h3><label>Target character <select id="reinterpret-character" class="form-select">${Object.keys(characters || {}).map(name => `<option value="${libraryEsc(name)}">${libraryEsc(name)}</option>`).join('')}</select></label><label>Renderer <select id="reinterpret-renderer" class="form-select"><option value="lustify">Lustify</option><option value="miaomiao">Miaomiao</option></select></label><label>Render intent <select id="reinterpret-intent" class="form-select"><option value="semi_realistic">Semi-realistic</option><option value="anime">Anime</option><option value="photorealistic">Photorealistic</option></select></label><label>Template mode <select id="reinterpret-template-mode" class="form-select"><option value="strict_composition">Strict composition</option><option value="balanced" selected>Balanced</option><option value="loose_inspiration">Loose inspiration</option></select></label><button id="btn-submit-reinterpret" class="btn btn-primary">Start reinterpretation</button><div id="reinterpret-status" class="action-feedback"></div>`;
        document.querySelector('#asset-detail-modal .modal-body').appendChild(panel);
        panel.querySelector('#btn-submit-reinterpret').onclick = async () => {
            const submitButton = panel.querySelector('#btn-submit-reinterpret');
            const statusBox = panel.querySelector('#reinterpret-status');
            submitButton.disabled = true;
            statusBox.innerHTML = '<strong>Queuing reinterpretation…</strong>';
            const body = {target_character:panel.querySelector('#reinterpret-character').value, renderer:panel.querySelector('#reinterpret-renderer').value, render_intent:panel.querySelector('#reinterpret-intent').value, template_mode:panel.querySelector('#reinterpret-template-mode').value};
            let result;
            let payload;
            try {
                result = await fetch(`/api/library/reinterpret/${encodeURIComponent(asset.asset_id)}`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
                payload = await result.json();
            } catch (error) {
                submitButton.disabled = false;
                statusBox.textContent = `Could not reach ADA: ${error.message}`;
                return;
            }
            if (!result.ok) {
                submitButton.disabled = false;
                statusBox.textContent = payload.error || 'Could not start reinterpretation.';
                return;
            }
            const requestId = payload.request.request_id;
            const poll = async () => {
                if (!panel.isConnected) return;
                let response;
                let state;
                try {
                    response = await fetch(`/api/library/reinterpretation/${encodeURIComponent(requestId)}`);
                    state = await response.json();
                } catch (error) {
                    statusBox.textContent = `Status unavailable: ${error.message}. Retrying…`;
                    window.setTimeout(poll, 2000);
                    return;
                }
                if (!response.ok) {
                    submitButton.disabled = false;
                    statusBox.textContent = state.error || 'Could not read reinterpretation status.';
                    return;
                }
                const labels = {QUEUED:'Queued', PREPARING_RENDER:'Preparing renderer', RENDERING:'Rendering in ComfyUI', REGISTERING:'Adding result to Library', RELEASING_RESOURCES:'Releasing GPU resources'};
                if (state.status === 'COMPLETE') {
                    await loadLibrary();
                    const created = allAssets.find(item => item.asset_id === state.library_asset_id);
                    statusBox.innerHTML = `<strong>Reinterpretation complete</strong><br><span class="badge online">COMPLETE</span>${state.output_asset ? `<a class="reinterpret-result" href="${libraryImageUrl(state.output_asset)}" target="_blank"><img src="${libraryImageUrl(state.output_asset)}" alt="Reinterpretation result"></a>` : ''}${created ? '<button id="btn-inspect-reinterpret-result" class="btn btn-primary">Inspect result</button>' : ''}`;
                    statusBox.querySelector('#btn-inspect-reinterpret-result')?.addEventListener('click', () => openAssetDetailGeneric(created));
                    return;
                }
                if (state.status === 'FAILED') {
                    submitButton.disabled = false;
                    statusBox.innerHTML = `<strong>Reinterpretation failed</strong><br>${libraryEsc(state.error?.message || 'Unknown renderer error.')}`;
                    return;
                }
                statusBox.innerHTML = `<strong>${libraryEsc(labels[state.status] || state.status)}</strong><br><small>${libraryEsc(requestId)}</small>`;
                window.setTimeout(poll, 1500);
            };
            poll();
        };
    };
    document.getElementById('asset-detail-technical').innerHTML = renderTechnicalDetails(asset, output);
}
