import re

with open('ada_app/static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

rep = '''function updateGallery(candidates) {
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
                       <div style="color:red; font-size:0.8em;">Klein pending/failed. Showing Illustrious fallback.</div>`;
        }
        
        let retryHtml = "";
        if (c.quality_retries !== undefined && c.quality_retries > 0) {
            retryHtml = `<span class="badge" style="background:#ffc107; color:black;">Retries: ${c.quality_retries} / ${c.max_retries || 2}</span>`;
        }
        
        let reasonHtml = "";
        if (c.retry_reason) {
            reasonHtml = `<p style="font-size:0.85em; color:#ff6b6b; margin-top:5px;"><strong>Reason:</strong> ${c.retry_reason}</p>`;
        }
        
        card.innerHTML = `
            ${imgHtml}
            <h4>${c.concept_id}</h4>
            <p><strong>Status:</strong> ${c.pipeline_state} ${retryHtml}</p>
            ${reasonHtml}
            <p style="font-size:0.85em; color:#ddd;"><strong>Illustrious Review:</strong> ${c.illustrious_review ? c.illustrious_review.verdict : 'N/A'}</p>
            <p style="font-size:0.85em; color:#ddd;"><strong>Final Review:</strong> ${c.final_review ? c.final_review.verdict : 'N/A'}</p>
        `;
        container.appendChild(card);
    });
}'''

js = re.sub(r'function updateGallery\(candidates\) \{.*?container\.appendChild\(card\);\n    \}\);\n\}', rep, js, flags=re.DOTALL)

with open('ada_app/static/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
