#!/usr/bin/env python3
"""
iphone.html, index.html 스플래시 패치 (실제 패턴 기반)
"""
import re

# iphone.html: jf_os_header_light_2x.png 사용
# index.html: jf_os_header_light_2x.png 사용

PATCHES = {
    'iphone.html': {
        'old_splash': '''<div id="bootSplash" style="
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
                background-clip:text;"><img src="/images/jf_os_header_light_2x.png" alt="JF OS" height="32" style="display:block; margin:0 auto;"></div>
    <div style="margin-top:6px; font-size:13px; color:rgba(255,255,255,0.4);">로딩 중…</div>
  </div>
</div>''',
        'new_splash': '''<div id="bootSplash" style="
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
</div>''',
        'old_logo': '''      <img src="/images/jf_os_header_light_1x.png"
           srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
           alt="JF OS" height="40" id="loginLogoImg" style="margin-bottom:10px;">
      <div class="login-brand-text">Synapse<br>Brain</div>''',
        'new_logo': '''      <img src="/images/jf_os_header_light_master.png"
           srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
           alt="JF OS" id="loginLogoImg"
           style="width:180px; height:auto; display:block; margin:0 auto 16px; transition:opacity 0.3s;"
           onerror="this.src='/images/jf_os_header_light_2x.png'">''',
        'old_logo_css': '''.login-logo {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  margin-bottom: 8px; text-align: center;
}
.login-logo img {
  height: 40px;
  width: auto;
  display: block;
  margin-bottom: 10px;
}''',
        'new_logo_css': '''.login-logo {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  margin-bottom: 20px; text-align: center;
}
.login-logo img {
  width: 180px;
  height: auto;
  display: block;
  margin: 0 auto 0;
}''',
        'old_hdr': '''        <img src="/images/jf_os_header_light_1x.png"
             srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
             alt="JF OS" height="28" data-logo="header" id="hdrLogoImg">''',
        'new_hdr': '''        <img src="/images/jf_os_header_light_1x.png"
             srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
             alt="JF OS" height="36" data-logo="header" id="hdrLogoImg">''',
    }
}

# index.html은 iphone.html과 동일한 패턴
PATCHES['index.html'] = PATCHES['iphone.html'].copy()

for fname, p in PATCHES.items():
    fpath = f'/home/ubuntu/braindump/{fname}'
    with open(fpath, encoding='utf-8') as f:
        content = f.read()
    
    applied = []
    skipped = []
    
    for key in ['old_splash', 'old_logo', 'old_logo_css', 'old_hdr']:
        new_key = key.replace('old_', 'new_')
        old = p[key]
        new = p[new_key]
        if old in content:
            content = content.replace(old, new, 1)
            applied.append(key)
        else:
            skipped.append(key)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ {fname}")
    for a in applied:
        print(f"   적용: {a}")
    for s in skipped:
        print(f"   스킵: {s}")

print("\n패치 완료!")
