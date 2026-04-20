import re

with open("original_index.html", "r") as f:
    orig = f.read()

def get_section(text, tag_start):
    pattern = tag_start + r'(.*?)<\/section>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return ""

about = get_section(orig, '<section id="about">')
work = get_section(orig, '<section id="work">')

apps = re.search(r'(<div class="works-grid">.*?<\/div>)\s*<div class="reveal"[^>]*>\s*<h3[^>]*>.*?03 \·', work, re.DOTALL)
apps_html = apps.group(1) if apps else ""

design1 = re.search(r'(<div class="works-grid">.*?<\/div>)\s*<div class="reveal"[^>]*>\s*<h3[^>]*>.*?04 \·', work[apps.end():] if apps else work, re.DOTALL)
design1_html = design1.group(1) if design1 else ""

design2 = re.search(r'(<div class="works-grid">.*?<\/div>)\s*<div class="reveal"[^>]*>\s*<h3[^>]*>.*?05 \·', work, re.DOTALL)
design2_html = design2.group(1) if design2 else ""

videos = re.search(r'(<div class="works-grid">.*?<\/div>)\s*$', work, re.DOTALL)
videos_html = videos.group(1) if videos else ""

# Extract only the work-cards from these blocks
def get_cards(html):
    cards = re.findall(r'(<div class="work-card[^>]*>.*?<\/div>\s*<\/div>|<a class="work-card[^>]*>.*?<\/a>)', html, re.DOTALL)
    if not cards:
        # Fallback to simple matching if nested divs break regex
        # Just return the content inside works-grid div (safely strip outer div)
        return re.sub(r'^<div class="works-grid">|<\/div>$', '', html.strip(), flags=re.DOTALL)
    return "\n".join(cards)

scene_1 = f'<section class="scene" id="scene-1">\n{about}\n</section>'
scene_2 = f'<section class="scene" id="scene-2">\n{get_cards(apps_html)}\n</section>'
scene_4 = f'<section class="scene" id="scene-4">\n{get_cards(design1_html)}\n{get_cards(design2_html)}\n</section>'

# The user explicitly created a styled ig-card for scene-3 in their paste. Let's use their ig-card or the one from original?
# The original was: <a class="work-card span-12 reveal" href="https://www.instagram.com/7_leaders_corp/" target="_blank" rel="noopener">...</a>
# User's: <div class="work-card ig-card"> ... </div>
# I'll use the user's ig-card for scene-3 because they specifically redesigned it for CSS3D!
scene_3 = """<section class="scene" id="scene-3">
  <div class="work-card ig-card">
    <div class="ig-card-inner">
      <div class="ig-badge"><svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="18" cy="6" r="1" fill="#fff"/></svg></div>
      <h3>@7_leaders_corp</h3>
      <p style="margin-top:10px; font-size:13px; color:#a5a5c0;"><span data-zh>所有影片都發佈於七駿 Instagram。點擊前往查看。</span><span data-en>Click to view all reels.</span></p>
    </div>
  </div>
</section>"""

with open("user_code.txt", "r") as f:
    user_code = f.read()

# Replace the placeholders in user_code with our complete scenes
new_html = re.sub(r'<!-- SCENE 1 \(Station 1: Personal\) -->.*?<!-- SCENE 2', f'<!-- SCENE 1 (Station 1: Personal) -->\n{scene_1}\n\n<!-- SCENE 2', user_code, flags=re.DOTALL)
new_html = re.sub(r'<!-- SCENE 2 \(Station 2: Apps\) -->.*?<!-- SCENE 3', f'<!-- SCENE 2 (Station 2: Apps) -->\n{scene_2}\n\n<!-- SCENE 3', new_html, flags=re.DOTALL)
new_html = re.sub(r'<!-- SCENE 3 \(Station 3: Videos\) -->.*?<!-- SCENE 4', f'<!-- SCENE 3 (Station 3: Videos) -->\n{scene_3}\n\n<!-- SCENE 4', new_html, flags=re.DOTALL)
new_html = re.sub(r'<!-- SCENE 4 \(Station 4: Design\) -->.*?<!-- SCENE 5', f'<!-- SCENE 4 (Station 4: Design) -->\n{scene_4}\n\n<!-- SCENE 5', new_html, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(new_html)
print("done")
