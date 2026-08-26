import re
with open('ada_app/static/app.js', 'r', encoding='utf-8') as f: js = f.read()

rep = '''
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
'''

rep2 = '''
        let reasonHtml = "";
        if (c.retry_reason) {
            reasonHtml = `<p style="font-size:0.85em; color:#ff6b6b; margin-top:5px;"><strong>Reason:</strong> ${c.retry_reason}</p>`;
        }
        
        let resumeHtml = "";
        if (c.pipeline_state === "FAILED_RUNTIME") {
            resumeHtml = `<button class="btn btn-sm" style="background:#007bff; color:white; margin-top:5px;" onclick="resumeRun('${currentRun.run_id}')">Resume</button>`;
        }
        
        card.innerHTML = `
            ${imgHtml}
            <h4>${c.concept_id}</h4>
            <p><strong>Status:</strong> ${c.pipeline_state} ${retryHtml}</p>
            ${reasonHtml}
            ${resumeHtml}
            <p style="font-size:0.85em; color:#ddd;"><strong>Illustrious Review:</strong> ${c.illustrious_review ? c.illustrious_review.verdict : 'N/A'}</p>
            <p style="font-size:0.85em; color:#ddd;"><strong>Final Review:</strong> ${c.final_review ? c.final_review.verdict : 'N/A'}</p>
        `;
'''

js = js.replace(rep.strip(), rep2.strip())

resume_fn = '''
async function resumeRun(run_id) {
    await fetch(`/api/pilot/resume/${run_id}`, {method: 'POST'});
    pollPilot(); // refresh
}
'''
js += resume_fn

with open('ada_app/static/app.js', 'w', encoding='utf-8') as f: f.write(js)
