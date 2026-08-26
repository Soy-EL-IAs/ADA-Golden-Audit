import re

# Fix app.js initTabs
with open('ada_app/static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

tabs_init = '''function initTabs() {
    const tabs = document.querySelectorAll(".sidebar li");
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".sidebar li").forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            tab.classList.add("active");
            const targetId = tab.dataset.tab;
            const targetEl = document.getElementById(targetId);
            if(targetEl) targetEl.classList.add("active");
            
            if (targetId === "library" && typeof loadLibrary === "function") {
                loadLibrary();
            }
        });
    });
}
'''
js = re.sub(r'function initTabs\(\) \{.*?\n\}\n', tabs_init, js, flags=re.DOTALL)
with open('ada_app/static/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Fix index.html Library link and tab classes
with open('ada_app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the injected Library sidebar link with a native li element
html = re.sub(r'<a href="#" class="nav-link" data-target="library">.*?Library</a>', r'<li data-tab="library">Library</li>', html)

# In case I didn't replace it before properly, let's also remove the previous run's injected code
html = html.replace('<div id="library" class="view-section d-none">', '<div id="library" class="tab-content">')
html = html.replace('<div id="library" class="view-section">', '<div id="library" class="tab-content">')

with open('ada_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
