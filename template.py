import sys

user_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Pei-Hsun Peng — Lunar Portfolio</title>
<meta name="description" content="Portfolio of Pei-Hsun Peng (彭培勛) — A lunar journey through product development, UI/UX design, and multimedia work. Based in Taichung, Taiwan." />
<meta name="author" content="Pei-Hsun Peng" />
<meta property="og:title" content="Pei-Hsun Peng — Lunar Portfolio" />
<meta property="og:description" content="A scroll-driven 3D journey through apps, videos, and design — orbiting four pedestals on the moon." />
<meta property="og:type" content="website" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Noto+Sans+TC:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
<style>
/* ============= RESET & BASE ============= */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{overflow-x:hidden;max-width:100vw}
html{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
body{
  font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:#020010;
  color:#e8e8f5;
  line-height:1.6;
  position:relative;
}
:lang(zh) body, body.lang-zh{font-family:'Noto Sans TC','Inter',sans-serif}
img,video{max-width:100%;display:block}
a{color:inherit;text-decoration:none;transition:color .2s ease}
button{font:inherit;cursor:pointer;border:none;background:none;color:inherit}

/* ============= COSMIC BACKGROUND ============= */
.cosmos{
  position:fixed;inset:0;z-index:-10;pointer-events:none;
  background:
    radial-gradient(ellipse at 20% 10%,rgba(76,29,149,.45),transparent 55%),
    radial-gradient(ellipse at 85% 20%,rgba(30,64,175,.32),transparent 55%),
    radial-gradient(ellipse at 50% 80%,rgba(15,23,42,.6),transparent 70%),
    linear-gradient(180deg,#020010 0%,#050118 50%,#070225 100%);
}
.three-canvas{
  position:fixed;inset:0;z-index:-8;pointer-events:none;
  width:100%;height:100%;display:block;
}

/* ============= CSS3D RENDERER CONTAINER ============= */
#css-container {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none; /* 讓整體容器不阻擋 WebGL 滾動 */
  z-index: 5; /* 確保全息投影在 WebGL 之上，但在 Header 之下 */
}

/* ============= HOLOGRAPHIC CARDS ============= */
.holo-card {
  width: 320px;
  height: 480px;
  background: linear-gradient(180deg, rgba(15,10,35,0.7), rgba(6,4,22,0.9));
  border: 1px solid rgba(192, 132, 252, 0.4);
  box-shadow: 0 0 25px rgba(192, 132, 252, 0.15), inset 0 0 15px rgba(192, 132, 252, 0.1);
  border-radius: 16px;
  padding: 24px;
  overflow-y: auto;
  pointer-events: auto; /* 讓卡片本體可以被點擊與滑動 */
  cursor: pointer;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: #e8e8f5;
  transition: border-color 0.3s, box-shadow 0.3s;
  position: relative;
}
.holo-card::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(34, 211, 238, 0.04) 3px, rgba(34, 211, 238, 0.04) 4px);
  border-radius: 16px;
}
.holo-card:hover {
  border-color: rgba(34, 211, 238, 0.8);
  box-shadow: 0 0 40px rgba(34, 211, 238, 0.3), inset 0 0 20px rgba(34, 211, 238, 0.2);
}
.holo-card::-webkit-scrollbar { width: 4px; }
.holo-card::-webkit-scrollbar-track { background: transparent; }
.holo-card::-webkit-scrollbar-thumb { background: rgba(34, 211, 238, 0.4); border-radius: 4px; }

/* 讓提取進全息卡牌的元素適應尺寸 */
.holo-card .work-card { width: 100%; transform: none !important; margin-bottom: 20px; border:none; box-shadow:none; pointer-events: none; background: transparent; padding: 0; }
.holo-card .work-card .media { pointer-events: auto; cursor: pointer; border-radius: 12px; }
.holo-card .work-card:hover { transform: none !important; }
.holo-card .work-card h3 { font-size: 16px; }
.holo-card .personal-text p { font-size: 13.5px; line-height: 1.6; }
.holo-card .hero-meta { grid-template-columns: 1fr; gap: 12px; margin-top: 16px; padding-top: 16px; }
.holo-card .skills-grid { grid-template-columns: 1fr; gap: 10px; }
.holo-card .timeline-item { grid-template-columns: 1fr; gap: 8px; padding: 16px 0; }
.holo-card .timeline-head { font-size: 18px; margin-bottom: 16px; }
.holo-card .sub-head { margin: 0 0 20px 0; }
.holo-card .ig-card { height: auto; aspect-ratio: unset; padding: 20px 0; background: transparent; }

/* ============= HIDING ORIGINAL SCROLL CONTENT ============= */
/* 我們保留它們在 DOM 裡撐開網頁高度，但在視覺上隱藏，因為現在內容全都在 3D 全息投影裡了 */
#scene-1, #scene-2, #scene-3, #scene-4, #scene-5 {
  opacity: 0;
  pointer-events: none;
}
.scene-intro { opacity: 1; pointer-events: auto; }

/* ============= BACKGROUNDS / ETC (Retained from original) ============= */
.bg-grid{
  position:fixed;inset:0;z-index:-3;pointer-events:none;opacity:.12;
  background-image:
    linear-gradient(rgba(139,92,246,.06) 1px,transparent 1px),
    linear-gradient(90deg,rgba(139,92,246,.06) 1px,transparent 1px);
  background-size:88px 88px;
  mask-image:radial-gradient(ellipse at center,black 10%,transparent 65%);
  -webkit-mask-image:radial-gradient(ellipse at center,black 10%,transparent 65%);
}
.vignette{
  position:fixed;inset:0;z-index:-2;pointer-events:none;
  background:radial-gradient(ellipse at center,transparent 35%,rgba(2,0,16,.55) 85%,rgba(2,0,16,.92) 100%);
}
.loading-screen{ position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:28px;background:#020010;transition:opacity .9s ease, visibility .9s ease;}
.loading-screen.hidden{opacity:0;visibility:hidden;pointer-events:none}
.loading-ring{ position:relative;width:96px;height:96px;}
.loading-ring::before,.loading-ring::after{ content:'';position:absolute;inset:0;border-radius:50%;border:2px solid transparent;}
.loading-ring::before{ border-top-color:#c084fc;border-right-color:#c084fc;animation:loadingSpin 1.1s cubic-bezier(.4,0,.2,1) infinite;}
.loading-ring::after{ inset:10px;border-top-color:#22d3ee;border-left-color:#22d3ee;animation:loadingSpin 1.8s cubic-bezier(.4,0,.2,1) infinite reverse;}
.loading-ring .moon{ position:absolute;inset:24px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#e2e8f0,#94a3b8 55%,#475569 100%);box-shadow:0 0 24px rgba(226,232,240,.4),inset -6px -6px 16px rgba(0,0,0,.4);}
@keyframes loadingSpin{to{transform:rotate(360deg)}}
.loading-pct{ font-family:'Space Grotesk',sans-serif;font-size:42px;font-weight:700;letter-spacing:-.02em;background:linear-gradient(120deg,#c084fc,#ec4899,#22d3ee);-webkit-background-clip:text;background-clip:text;color:transparent;}
.loading-text{ font-family:'Space Grotesk',sans-serif;font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:rgba(192,132,252,.6);}

/* HEADER / NAV */
header{ position:fixed;top:0;left:0;right:0;z-index:100;padding:18px 0;transition:all .3s ease;backdrop-filter:blur(0px);}
header.scrolled{ background:rgba(5,2,20,.72);backdrop-filter:blur(20px) saturate(180%);border-bottom:1px solid rgba(255,255,255,.06);padding:14px 0;}
.nav{display:flex;align-items:center;justify-content:space-between}
.logo{ font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:18px;letter-spacing:-.01em;display:flex;align-items:center;gap:10px;}
.logo-mark{ width:28px;height:28px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#e2e8f0,#94a3b8 55%,#334155 100%);box-shadow:0 0 16px rgba(192,132,252,.5),inset -3px -3px 8px rgba(0,0,0,.3);}
.nav-links{display:flex;align-items:center;gap:28px;font-size:13px;font-weight:500}
.nav-links a{color:#b4b4c7;position:relative}
.nav-links a:hover{color:#fff}
.nav-links a::after{ content:'';position:absolute;bottom:-6px;left:0;right:0;height:1px;background:linear-gradient(90deg,#c084fc,#22d3ee);transform:scaleX(0);transform-origin:left;transition:transform .3s ease;}
.nav-links a:hover::after{transform:scaleX(1)}
.lang-toggle{ display:flex;align-items:center;gap:0;border:1px solid rgba(255,255,255,.12);border-radius:999px;padding:3px;font-size:13px;font-weight:600;}
.lang-toggle button{ padding:6px 14px;border-radius:999px;color:#8b8ba5;transition:all .2s ease;}
.lang-toggle button.active{ background:linear-gradient(135deg,#c084fc,#22d3ee);color:#050509;box-shadow:0 4px 12px -4px rgba(192,132,252,.6);}
@media(max-width:760px){.nav-links{display:none}}

/* SIDE NAV */
.side-nav{ position:fixed;left:24px;top:50%;transform:translateY(-50%);z-index:90;display:flex;flex-direction:column;gap:22px;padding:20px 12px;border-radius:999px;background:rgba(8,4,24,.55);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.06);}
.side-nav-item{ position:relative;display:flex;align-items:center;width:10px;height:10px;}
.side-nav-item .dot{ width:10px;height:10px;border-radius:50%;background:rgba(192,132,252,.28);transition:all .3s cubic-bezier(.4,0,.2,1);}
.side-nav-item:hover .dot{background:rgba(192,132,252,.7);transform:scale(1.35)}
.side-nav-item.active .dot{ background:#c084fc;box-shadow:0 0 14px rgba(192,132,252,.9);transform:scale(1.5);}
.side-nav-item .label{ position:absolute;left:26px;top:50%;transform:translateY(-50%) translateX(-6px);font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#c084fc;white-space:nowrap;opacity:0;pointer-events:none;transition:all .25s ease;padding:5px 10px;border-radius:6px;background:rgba(8,4,24,.88);backdrop-filter:blur(8px);border:1px solid rgba(192,132,252,.2);}
.side-nav-item:hover .label, .side-nav-item.active .label{opacity:1;transform:translateY(-50%) translateX(0)}
@media(max-width:840px){.side-nav{display:none}}

.scroll-cue{ position:fixed;bottom:30px;left:50%;transform:translateX(-50%);z-index:50;pointer-events:none;display:flex;flex-direction:column;align-items:center;gap:10px;font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:600;letter-spacing:.32em;text-transform:uppercase;color:rgba(192,132,252,.72);transition:opacity .5s ease;}
.scroll-cue.hide{opacity:0}
.scroll-cue .cue-line{ position:relative;width:1px;height:42px;overflow:hidden;background:rgba(192,132,252,.2);}
.scroll-cue .cue-line::after{ content:'';position:absolute;top:-42px;left:0;width:100%;height:42px;background:linear-gradient(180deg,transparent,#c084fc);animation:cueSlide 2s cubic-bezier(.4,0,.2,1) infinite;}
@keyframes cueSlide{ 0%{top:-42px;opacity:0} 20%{opacity:1} 80%{opacity:1} 100%{top:42px;opacity:0} }

.journey{position:relative;z-index:1}
.scene{ position:relative;padding:140px 0 120px;min-height:100vh;}
.scene-intro{ min-height:100vh;padding:120px 0;display:flex;align-items:center;justify-content:center;text-align:center;}
.intro-wrap{display:flex;flex-direction:column;align-items:center;gap:26px}
.intro-chip{ display:inline-flex;align-items:center;gap:10px;padding:8px 18px;border-radius:999px;border:1px solid rgba(192,132,252,.3);background:rgba(192,132,252,.08);font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:700;letter-spacing:.26em;text-transform:uppercase;color:#c084fc;}
.intro-chip .dot{ width:6px;height:6px;border-radius:50%;background:#22c55e;box-shadow:0 0 12px #22c55e;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.intro-title{ font-family:'Space Grotesk','Noto Sans TC',sans-serif;font-size:clamp(54px,10vw,132px);font-weight:700;letter-spacing:-.035em;line-height:.98;}
.intro-title .gradient{ background:linear-gradient(120deg,#c084fc 0%,#ec4899 45%,#22d3ee 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 30px rgba(192,132,252,.5));}
.intro-sub{ font-size:clamp(15px,1.7vw,19px);color:#b4b4c7;max-width:600px;line-height:1.65;}
.intro-cta{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-top:14px}
.btn{ display:inline-flex;align-items:center;gap:10px;padding:14px 24px;border-radius:12px;font-weight:600;font-size:14px;transition:all .25s ease;cursor:pointer;font-family:'Space Grotesk','Noto Sans TC',sans-serif;}
.btn-primary{background:#ffffff;color:#050509}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 12px 32px -8px rgba(255,255,255,.3)}
.btn-ghost{ background:rgba(255,255,255,.05);color:#fff;border:1px solid rgba(255,255,255,.14);backdrop-filter:blur(8px);}
.btn-ghost:hover{background:rgba(255,255,255,.1);border-color:rgba(192,132,252,.4)}
.btn svg{width:15px;height:15px}

/* MODALS */
.modal{ position:fixed;inset:0;z-index:200;background:rgba(2,0,16,.9);backdrop-filter:blur(16px);display:none;align-items:center;justify-content:center;padding:40px 20px;animation:fadeIn .25s ease;}
.modal.open{display:flex}
.modal-body{ position:relative;max-width:1200px;width:100%;max-height:90vh;border-radius:16px;overflow:hidden;background:#000;box-shadow:0 40px 80px -20px rgba(0,0,0,.8);}
.modal-body video{width:100%;height:auto;max-height:90vh;display:block}
.modal-close{ position:absolute;top:-48px;right:0;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.1);color:#fff;display:grid;place-items:center;transition:background .2s ease;}
.modal-close:hover{background:rgba(255,255,255,.2)}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}

[data-en],[data-zh]{display:none}
body.lang-en [data-en]{display:revert}
body.lang-zh [data-zh]{display:revert}
body.lang-en span[data-en]{display:inline}
body.lang-zh span[data-zh]{display:inline}

/* NEW CSS TO ENSURE OLD WORK-CARDS DISPLAY CORRECTLY WHEN CLONED INTO CSS3D */
.holo-card .info { padding: 16px 0 0 0; }
.holo-card .tag { display: inline-block; padding: 4px 10px; border-radius: 6px; background: rgba(192,132,252,0.15); color: #c084fc; font-size: 11px; margin-bottom: 8px; border: 1px solid rgba(192,132,252,0.3); }
.holo-card .desc { font-size: 13px; color: #a5a5c0; margin-top: 6px; }
.holo-card .skills-grid .skill-card { background: rgba(255,255,255,0.03); padding: 16px; border-radius: 12px; margin-bottom: 12px; }
.holo-card .skills-grid h4 { font-size: 15px; margin-bottom: 6px; color: #fff; }
.holo-card .play-badge { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); width: 44px; height: 44px; background: rgba(0,0,0,0.6); border-radius: 50%; display: grid; place-items: center; opacity: 0; transition: opacity 0.3s; }
.holo-card .media:hover .play-badge { opacity: 1; }
.holo-card .play-badge svg { width: 22px; height: 22px; color: #fff; }
.holo-card .ig-badge { width: 48px; height: 48px; background: linear-gradient(135deg,#f58529,#dd2a7b,#8134af,#515bd4); border-radius: 50%; display: grid; place-items: center; margin-bottom: 16px; }
.holo-card .ig-card-inner { display: flex; flex-direction: column; align-items: center; text-align: center; justify-content: center; height: 100%; border: 1px dashed rgba(192,132,252,0.4); border-radius: 12px; padding: 32px 16px; }

</style>
</head>
<body class="lang-en">

<!-- Loading screen -->
<div class="loading-screen" id="loadingScreen">
  <div class="loading-ring"><div class="moon"></div></div>
  <div class="loading-pct" id="loadingPct">0%</div>
  <div class="loading-text"><span data-en>Entering Lunar Orbit</span><span data-zh>進入月球軌道</span></div>
</div>

<!-- Background layers & WebGL Canvas -->
<div class="cosmos" aria-hidden="true"></div>
<canvas class="three-canvas" id="threeCanvas" aria-hidden="true"></canvas>

<!-- 全息投影 UI 容器 (CSS3DRenderer) -->
<div id="css-container"></div>

<div class="bg-grid" aria-hidden="true"></div>
<div class="vignette" aria-hidden="true"></div>

<!-- Scroll cue -->
<div class="scroll-cue" id="scrollCue">
  <span data-en>Scroll</span><span data-zh>向下滾動</span>
  <div class="cue-line"></div>
</div>

<!-- Side nav -->
<nav class="side-nav" id="sideNav" aria-label="Scene navigation">
  <a href="#scene-0" class="side-nav-item active" data-idx="0">
    <span class="dot"></span>
    <span class="label"><span data-en>Intro</span><span data-zh>序章</span></span>
  </a>
  <a href="#scene-1" class="side-nav-item" data-idx="1">
    <span class="dot"></span>
    <span class="label"><span data-en>About</span><span data-zh>個人資料</span></span>
  </a>
  <a href="#scene-2" class="side-nav-item" data-idx="2">
    <span class="dot"></span>
    <span class="label"><span data-en>Apps</span><span data-zh>App 設計</span></span>
  </a>
  <a href="#scene-3" class="side-nav-item" data-idx="3">
    <span class="dot"></span>
    <span class="label"><span data-en>Videos</span><span data-zh>影片展示</span></span>
  </a>
  <a href="#scene-4" class="side-nav-item" data-idx="4">
    <span class="dot"></span>
    <span class="label"><span data-en>Design</span><span data-zh>圖像設計</span></span>
  </a>
  <a href="#scene-5" class="side-nav-item" data-idx="5">
    <span class="dot"></span>
    <span class="label"><span data-en>Contact</span><span data-zh>聯絡</span></span>
  </a>
</nav>

<!-- Header -->
<header id="header">
  <div class="container nav">
    <a href="#scene-0" class="logo">
      <div class="logo-mark"></div>
      <span>Pei-Hsun Peng</span>
    </a>
    <nav class="nav-links">
      <a href="#scene-1"><span data-en>About</span><span data-zh>關於</span></a>
      <a href="#scene-2"><span data-en>Apps</span><span data-zh>App</span></a>
      <a href="#scene-3"><span data-en>Videos</span><span data-zh>影片</span></a>
      <a href="#scene-4"><span data-en>Design</span><span data-zh>設計</span></a>
      <a href="#scene-5"><span data-en>Contact</span><span data-zh>聯絡</span></a>
    </nav>
    <div class="lang-toggle" role="group" aria-label="Language toggle">
      <button class="active" data-lang="en">EN</button>
      <button data-lang="zh">中</button>
    </div>
  </div>
</header>

<main class="journey">
<!-- ============ SCENE 0 · INTRO (STAYS VISIBLE) ============ -->
<section class="scene scene-intro" id="scene-0">
  <div class="container">
    <div class="intro-wrap">
      <div class="intro-chip reveal">
        <span class="dot"></span>
        <span data-en>Portfolio · 2026 Edition</span><span data-zh>作品集 · 2026 版</span>
      </div>
      <h1 class="intro-title reveal">
        <span data-en>Pei-Hsun <span class="gradient">Peng</span></span>
        <span data-zh>彭<span class="gradient">培勛</span></span>
      </h1>
      <p class="intro-sub reveal">
        <span data-en>A lunar journey across product, design, and multimedia work. Scroll down to enter the lunar base — explore the holographic pedestals.</span>
        <span data-zh>一趟橫跨產品、設計與影音的月球旅程。向下滾動，進入月表基地內部空間——點擊並展開全息投影卡牌。</span>
      </p>
      <div class="intro-cta reveal">
        <a href="#scene-1" class="btn btn-primary">
          <span data-en>Enter Base</span><span data-zh>進入基地</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
        </a>
      </div>
    </div>
  </div>
</section>

<!-- SCENE 1 (Station 1: Personal) -->
__SCENE_1__

<!-- SCENE 2 (Station 2: Apps) -->
__SCENE_2__

<!-- SCENE 3 (Station 3: Videos) -->
__SCENE_3__

<!-- SCENE 4 (Station 4: Design) -->
__SCENE_4__

<!-- SCENE 5 -->
<section class="scene" id="scene-5"></section>
</main>

__REST_OF_HTML__
"""

# Extract the pieces we need from original_index.html
def get_section(text, tag_start):
    import re
    # We want to extract <section id="..."> to </section>
    pattern = tag_start + r'(.*?)<\/section>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return tag_start + match.group(1) + "</section>"
    return ""

with open("original_index.html", "r") as f:
    orig = f.read()

# Original sections based on ids
scene_1 = get_section(orig, '<section id="about">').replace('id="about"', 'class="scene" id="scene-1"')
scene_2 = ""
scene_3 = ""
scene_4 = ""

# Work section has everything else
work_sec = get_section(orig, '<section id="work">')
if work_sec:
    # 01/02 Apps
    import re
    app_pattern = r'<h3.*?01 \· .*?<div class="reveal".*?<h3.*?03 \·'
    apps_match = re.search(r'(<h3.*?01 \· .*?)(?=<div class="reveal"[^>]*>\s*<h3[^>]*>\s*<span[^>]*>(03 \·))', work_sec, re.DOTALL)
    if apps_match:
        # Wrap the apps in section
        scene_2 = f'<section class="scene" id="scene-2">\n{apps_match.group(1)}\n</section>'
    
    # 05 Videos
    videos_match = re.search(r'(<div class="reveal"[^>]*>\s*<h3[^>]*>\s*<span[^>]*>(05 \·).*?)(?=$|<\/section>)', work_sec, re.DOTALL)
    if videos_match:
        scene_3 = f'<section class="scene" id="scene-3">\n{videos_match.group(1)}\n</section>'
        
    # 03/04 Design
    design_match = re.search(r'(<div class="reveal"[^>]*>\s*<h3[^>]*>\s*<span[^>]*>(03 \·).*?)(?=<div class="reveal"[^>]*>\s*<h3[^>]*>\s*<span[^>]*>(05 \·))', work_sec, re.DOTALL)
    if design_match:
        scene_4 = f'<section class="scene" id="scene-4">\n{design_match.group(1)}\n</section>'


# If we couldn't parse correctly due to regex missing, just rely on hardcoded class="work-card" extraction
# But wait, we want the literal HTML, including titles!
# Let's clean it up slightly to just wrap all the `.work-card` correctly.
# The user's provided code already has some nice structure for scene-1, scene-2, etc.
# Actually I'd rather use the user's provided scene-1, scene-2, scene-3 structure if it's cleaner, BUT inject the missing 03/04 cards into scene-4, and the missing arduino app into scene-2. 

# Let's extract the user's exact rest_of_html
user_code = """__USER_PROVIDED_HTML__"""
with open("user_code.txt", "r") as f:
    user_code = f.read()

rest_of_html = user_code.split('</main>')[1]

# Rebuild scenes using original_index.html cards

final_html = user_html.replace('__SCENE_1__', scene_1)
final_html = final_html.replace('__SCENE_2__', scene_2)
final_html = final_html.replace('__SCENE_3__', scene_3)
final_html = final_html.replace('__SCENE_4__', scene_4)
final_html = final_html.replace('__REST_OF_HTML__', rest_of_html)

with open("index.html", "w") as f:
    f.write(final_html)

