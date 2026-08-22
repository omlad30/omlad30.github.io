import re
import difflib

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

original_html = html

# 1. TYPO FIXES
html = html.replace("Finised", "Finished")
html = html.replace("amoung", "among")
html = html.replace("Demmed tobe University", "Deemed to be University")

# 2. RESUME LINK BUG
html = html.replace("images/OM LAD.pdf", "images/OM_LAD_Resume.pdf")

# 3. PROJECT CARD "00" BUG
# Find all <div class="proj-meta">...</div> and remove them
html = re.sub(r'<div class="proj-meta">.*?</div>\s*', '', html, flags=re.DOTALL)

# 4. CERTIFICATE MODAL
# Replace the broken data-src="images/" with data-src="images/prabal.pdf"
html = html.replace('data-src="images/"', 'data-src="images/prabal.pdf"')

# 5 & 6. TRIM FEATURED PROJECTS & PROJECT DESCRIPTIONS
proj_grid_start = html.find('<div class="proj-grid" id="projGrid">')
proj_grid_end = html.find('<div class="more-cta reveal">')
if proj_grid_start != -1 and proj_grid_end != -1:
    before_grid = html[:proj_grid_start + len('<div class="proj-grid" id="projGrid">')]
    after_grid = html[proj_grid_end:]
    
    grid_content = html[proj_grid_start + len('<div class="proj-grid" id="projGrid">'):proj_grid_end]
    
    # Extract each article
    articles = re.findall(r'<article.*?</article>', grid_content, flags=re.DOTALL)
    
    kept_articles = []
    for article in articles:
        if "AssignmentGuard" in article:
            # Update description
            article = re.sub(
                r'(<p class="proj-desc">).*?(</p>)',
                r'\1A JavaScript web app that ensures assignment integrity by employing plagiarism-aware submission handling and robust client-side validation logic.\2',
                article, flags=re.DOTALL
            )
            kept_articles.append(article)
        elif "Sports Chatbot" in article or "Sports_Chatboat" in article:
            kept_articles.append(article)
        elif "Quiz App" in article:
            # Update description
            article = re.sub(
                r'(<p class="proj-desc">).*?(</p>)',
                r'\1An interactive quiz application featuring dynamic question flow, real-time scoring logic, and effective DOM-based state management.\2',
                article, flags=re.DOTALL
            )
            kept_articles.append(article)
        elif "Image Processing" in article:
            kept_articles.append(article)
        elif "Sortable Table" in article:
            kept_articles.append(article)
            
    new_grid_content = "\n\n" + "\n\n".join(kept_articles) + "\n\n      </div>\n\n      "
    html = before_grid + new_grid_content + after_grid

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

diff = difflib.unified_diff(
    original_html.splitlines(keepends=True), 
    html.splitlines(keepends=True), 
    fromfile='index.html (before)', 
    tofile='index.html (after)'
)
with open("diff_summary.txt", "w", encoding="utf-8") as f:
    f.writelines(diff)
print("Done")
