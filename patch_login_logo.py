"""
로그인 화면: JF OS 로고 위에 + "Synapse Brain" 텍스트 아래에 추가
구조:
  [JF OS 로고 이미지]
  Synapse Brain (기존 그라디언트 텍스트 복원)
"""
import re

FILES = [
    '/home/ubuntu/braindump/galaxy.html',
    '/home/ubuntu/braindump/iphone.html',
    '/home/ubuntu/braindump/index.html',
]

# 새 login-logo 블록: 로고 이미지 + Synapse Brain 텍스트
NEW_LOGIN_LOGO = '''    <div class="login-logo">
      <img src="/images/jf_os_header_light_1x.png"
           srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"
           alt="JF OS" height="40" id="loginLogoImg" style="margin-bottom:10px;">
      <div class="login-brand-text">Synapse<br>Brain</div>
    </div>'''

# CSS 추가: login-brand-text 스타일
NEW_CSS = '''
.login-brand-text {
  font-size: 42px;
  font-weight: 900;
  line-height: 1.1;
  text-align: center;
  background: linear-gradient(135deg, #6c63ff 0%, #a855f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 4px;
  letter-spacing: -1px;
}
'''

for fpath in FILES:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    original = c

    # 1. login-logo CSS에 margin-bottom 조정 및 flex-direction: column 추가
    c = c.replace(
        '.login-logo {\n  display: flex; align-items: center; justify-content: center;\n  margin-bottom: 6px; text-align: center;\n}',
        '.login-logo {\n  display: flex; flex-direction: column; align-items: center; justify-content: center;\n  margin-bottom: 8px; text-align: center;\n}'
    )

    # 2. login-logo img height 조정 (56px → 40px) - CSS
    c = c.replace(
        '.login-logo img {\n  height: 56px;\n  width: auto;\n  display: block;\n}',
        '.login-logo img {\n  height: 40px;\n  width: auto;\n  display: block;\n  margin-bottom: 10px;\n}'
    )

    # 3. login-brand-text CSS 추가 (.login-sub 바로 앞)
    if '.login-brand-text' not in c:
        c = c.replace(
            '.login-sub {',
            NEW_CSS + '.login-sub {'
        )

    # 4. login-logo HTML 블록 교체 - 이미지만 있는 것 → 이미지 + Synapse Brain 텍스트
    # 패턴: <div class="login-logo">...(img 태그)...</div>
    pattern = re.compile(
        r'<div class="login-logo">\s*<img[^>]+id="loginLogoImg"[^>]*>\s*</div>',
        re.DOTALL
    )
    c = pattern.sub(NEW_LOGIN_LOGO, c)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

    changed = c != original
    print(f"{fpath.split('/')[-1]}: {'수정 완료' if changed else '변경 없음'}")

print("완료!")
