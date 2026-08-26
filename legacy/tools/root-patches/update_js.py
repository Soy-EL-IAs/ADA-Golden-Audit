with open("ada_app/static/app.js", "a", encoding="utf-8") as f:
    f.write("""
let pilotPollInterval = null;
let currentPilotRunId = null;

document.addEventListener("DOMContentLoaded", () => {
    const btnGeneratePilot = document.getElementById("btn-generate-pilot");
    if (btnGeneratePilot) {
        btnGeneratePilot.addEventListener("click", generatePilot);
    }
});

async function generatePilot() {
    const btn = document.getElementById("btn-generate-pilot");
    const status = document.getElementById("generate-status");
    const cCount = document.getElementById("lab-concept-count").value;
    const pCount = document.getElementById("lab-pilot-count").value;
    
    btn.disabled = true;
    status.textContent = "Starting Pilot Generation... This will take a few minutes.";
    document.getElementById("pilot-status-card").style.display = "block";
    document.getElementById("pilot-status-container").innerHTML = "Initializing...";
    
    try {
        const res = await fetch("/api/pilot/generate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                conceptCount: parseInt(cCount),
                pilotCount: parseInt(pCount)
            })
        });
        const data = await res.json();
        currentPilotRunId = data.run_id;
        
        status.textContent = "Pilot workflow started. Monitoring progress...";
        startPilotPolling();
        
    } catch (e) {
        status.textContent = "Failed to start pilot.";
        btn.disabled = false;
    }
}

function startPilotPolling() {
    if (pilotPollInterval) clearInterval(pilotPollInterval);
    pilotPollInterval = setInterval(pollPilotStatus, 3000);
    pollPilotStatus();
}

async function pollPilotStatus() {
    if (!currentPilotRunId) return;
    
    try {
        const res = await fetch(`/api/runs/${currentPilotRunId}/pilot`);
        const candidates = await res.json();
        
        const container = document.getElementById("pilot-status-container");
        container.innerHTML = "";
        
        let allDone = true;
        
        candidates.forEach(c => {
            const card = document.createElement("div");
            card.style.border = "1px solid #444";
            card.style.padding = "10px";
            card.style.marginBottom = "10px";
            card.style.borderRadius = "4px";
            
            const state = c.pipeline_state || "SELECT";
            if (state !== "COMPLETE" && !state.startsWith("ERROR")) {
                allDone = false;
            }
            
            card.innerHTML = `
                <div style="display:flex; justify-content:space-between;">
                    <strong>${c.concept_id} - Rank ${c.selection_rank}</strong>
                    <span>State: <span style="color:${state.startsWith('ERROR') ? 'red' : '#00ff00'}">${state}</span></span>
                </div>
                <div class="pipeline-indicator mt-1" style="font-size:0.8em;">
                    <span class="pipe-step ${state === 'SELECT' ? 'active' : (['ILLUSTRIOUS','REVIEW','KLEIN','FINAL','COMPLETE'].includes(state) ? 'done' : '')}">SELECT</span> &rarr;
                    <span class="pipe-step ${state === 'ILLUSTRIOUS' ? 'active' : (['REVIEW','KLEIN','FINAL','COMPLETE'].includes(state) ? 'done' : '')}">ILLUSTRIOUS</span> &rarr;
                    <span class="pipe-step ${state === 'REVIEW' ? 'active' : (['KLEIN','FINAL','COMPLETE'].includes(state) ? 'done' : '')}">REVIEW</span> &rarr;
                    <span class="pipe-step ${state === 'KLEIN' ? 'active' : (['FINAL','COMPLETE'].includes(state) ? 'done' : '')}">KLEIN</span> &rarr;
                    <span class="pipe-step ${state === 'FINAL' ? 'active' : (['COMPLETE'].includes(state) ? 'done' : '')}">FINAL</span>
                </div>
                <div style="font-size:0.85em; margin-top:5px; color:#aaa;">
                    ${c.original_proposal ? c.original_proposal.snapshot : ''}
                </div>
            `;
            container.appendChild(card);
        });
        
        if (allDone && candidates.length > 0) {
            clearInterval(pilotPollInterval);
            document.getElementById("generate-status").textContent = "Pilot completed! Check Pilot Gallery.";
            document.getElementById("btn-generate-pilot").disabled = false;
            updateGallery(candidates);
        }
    } catch (e) {
        console.error("Polling error", e);
    }
}

function updateGallery(candidates) {
    const container = document.getElementById("gallery-container");
    container.innerHTML = "";
    
    candidates.forEach(c => {
        const card = document.createElement("div");
        card.className = "card";
        
        let imgHtml = "";
        if (c.klein_image) {
            imgHtml = `<img src="/api/image?path=${encodeURIComponent(c.klein_image)}" style="width:100%; border-radius:4px; margin-bottom:10px;" />`;
        } else if (c.illustrious_image) {
            imgHtml = `<img src="/api/image?path=${encodeURIComponent(c.illustrious_image)}" style="width:100%; border-radius:4px; margin-bottom:10px; opacity:0.7;" />
                       <div style="color:red; font-size:0.8em;">Klein failed. Showing Illustrious fallback.</div>`;
        }
        
        card.innerHTML = `
            ${imgHtml}
            <h4>Rank ${c.selection_rank} - ${c.concept_id}</h4>
            <p><strong>Status:</strong> ${c.pipeline_state}</p>
            <p style="font-size:0.85em; color:#ddd;"><strong>Illustrious Review:</strong> ${c.illustrious_review ? c.illustrious_review.verdict : 'N/A'}</p>
            <p style="font-size:0.85em; color:#ddd;"><strong>Final Review:</strong> ${c.final_review ? c.final_review.verdict : 'N/A'}</p>
            <hr style="border-color:#444; margin:10px 0;"/>
            <p style="font-size:0.8em; color:#bbb;">${c.original_proposal.snapshot}</p>
        `;
        container.appendChild(card);
    });
}
""")
