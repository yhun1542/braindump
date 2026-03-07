#!/usr/bin/env python3
"""
스플래시 화면 수정 + PC 멈춤 수정 패치
1. bootSplash: icon-192.png 제거, JF OS 로고 크게 표시
2. loginScreen: JF OS 로고 크게 표시 (height 40→80)
3. 앱 헤더: JF OS 로고 크게 (height 28→36)
4. PC 멈춤: __hideSplash 타임아웃 안전장치 추가 (8초 후 강제 제거)
"""

import re

files = [
    '/home/ubuntu/braindump/galaxy.html',
    '/home/ubuntu/braindump/iphone.html',
    '/home/ubuntu/braindump/index.html',
]

# ── 1. bootSplash HTML 교체 ──
OLD_SPLASH = '''<div id="bootSplash" style="
  position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
  background:#0B1220; z-index:99999;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  transition: opacity 0.18s ease;
">
  <div style="text-align:center;">
    <img src="/icons/icon-192.png" width="80" height="80"
         style="border-radius:20px; box-shadow:0 8px 32px rgba(108,99,255,0.4);"
         alt="Synapse Brain">
    <div style="margin-top:14px; font-size:20px; font-weight:700;
                background:linear-gradient(135deg,#6c63ff,#00d4ff);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                background-clip:text;"><img src="/images/jf_os_header_dark_2x.png" alt="JF OS" height="32" style="display:block;"></div>
    <div style="margin-top:6px; font-size:13px; color:rgba(255,255,255,0.4);">로딩 중…</div>
  </div>
</div>'''

NEW_SPLASH = '''<div id="bootSplash" style="
  position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
  background:#0B1220; z-index:99999;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  transition: opacity 0.4s ease;
">
  <div style="text-align:center;">
    <img src="/images/jf_os_header_dark_master.png" alt="JF OS"
         style="width:200px; height:auto; display:block; margin:0 auto;"
         onerror="this.src='/images/jf_os_header_dark_2x.png'">
    <div style="margin-top:16px; font-size:13px; color:rgba(255,255,255,0.35); letter-spacing:0.05em;">로딩 중…</div>
  </div>
</div>'''

# ── 2. __hideSplash 타임아웃 안전장치 추가 ──
OLD_HIDE_SPLASH = '''window.__hideSplash = function () {
  var el = document.getElementById('bootSplash');
  if (!el) return;
  el.style.opacity = '0';
  setTimeout(function() { if (el.parentNode) el.parentNode.removeChild(el); }, 200);
};'''

NEW_HIDE_SPLASH = '''window.__hideSplash = function () {
  var el = document.getElementById('bootSplash');
  if (!el) return;
  el.style.opacity = '0';
  setTimeout(function() { if (el && el.parentNode) el.parentNode.removeChild(el); }, 400);
};
// 안전장치: 8초 후 강제 제거 (Firebase 응답 지연/오류 시 멈춤 방지)
setTimeout(function() { window.__hideSplash && window.__hideSplash(); }, 8000);'''

# ── 3. 로그인 화면 로고 크게 ──
OLD_LOGIN_LOGO = '''      <img src="/images/jf_os_header_light_1x.png"
           srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
           alt="JF OS" height="40" id="loginLogoImg" style="margin-bottom:10px;">
      <div class="login-brand-text">Synapse<br>Brain</div>'''

NEW_LOGIN_LOGO = '''      <img src="/images/jf_os_header_light_master.png"
           srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
           alt="JF OS" id="loginLogoImg"
           style="width:180px; height:auto; display:block; margin:0 auto 16px; transition:opacity 0.3s;"
           onerror="this.src='/images/jf_os_header_light_2x.png'">'''

# ── 4. login-logo CSS 개선 ──
OLD_LOGIN_LOGO_CSS = '''.login-logo {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  margin-bottom: 8px; text-align: center;
}
.login-logo img {
  height: 40px;
  width: auto;
  display: block;
  margin-bottom: 10px;
}'''

NEW_LOGIN_LOGO_CSS = '''.login-logo {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  margin-bottom: 20px; text-align: center;
}
.login-logo img {
  width: 180px;
  height: auto;
  display: block;
  margin: 0 auto 0;
}'''

# ── 5. 앱 헤더 로고 크기 조정 ──
OLD_HDR_LOGO = '''        <img src="/images/jf_os_header_light_1x.png"
             srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
             alt="JF OS" height="28" data-logo="header" id="hdrLogoImg">'''

NEW_HDR_LOGO = '''        <img src="/images/jf_os_header_light_1x.png"
             srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
             alt="JF OS" height="36" data-logo="header" id="hdrLogoImg">'''

patches = [
    ('bootSplash HTML', OLD_SPLASH, NEW_SPLASH),
    ('__hideSplash 타임아웃', OLD_HIDE_SPLASH, NEW_HIDE_SPLASH),
    ('로그인 로고 크게', OLD_LOGIN_LOGO, NEW_LOGIN_LOGO),
    ('login-logo CSS', OLD_LOGIN_LOGO_CSS, NEW_LOGIN_LOGO_CSS),
    ('앱 헤더 로고 크기', OLD_HDR_LOGO, NEW_HDR_LOGO),
]

for fpath in files:
    with open(fpath, encoding='utf-8') as f:
        content = f.read()
    
    fname = fpath.split('/')[-1]
    applied = []
    skipped = []
    
    for name, old, new in patches:
        if old in content:
            content = content.replace(old, new, 1)
            applied.append(name)
        else:
            skipped.append(name)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ {fname}")
    for a in applied:
        print(f"   적용: {a}")
    for s in skipped:
        print(f"   스킵: {s}")

print("\n패치 완료!")
