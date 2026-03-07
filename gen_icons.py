"""
PWA 아이콘 생성 스크립트
jasoneye.com (Synapse Brain) - JF 브랜드 컬러 적용
배경: #0B1220 (다크 네이비), 그라디언트: #6C63FF → #00D4FF
"""
from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('/home/ubuntu/braindump/icons', exist_ok=True)

def create_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 라운드 배경 (다크 네이비 #0B1220)
    radius = size // 5
    bg_color = (11, 18, 32, 255)

    # 라운드 사각형 배경
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=bg_color)

    # 그라디언트 효과를 위한 오버레이 (보라 → 파랑)
    for i in range(size):
        t = i / size
        r = int(108 * (1-t) + 0 * t)
        g = int(99 * (1-t) + 212 * t)
        b = int(255 * (1-t) + 255 * t)
        a = int(60 * (1 - abs(t - 0.5) * 2))  # 중앙이 가장 밝게
        draw.line([(0, i), (size, i)], fill=(r, g, b, a))

    # 다시 라운드 마스크 적용 (모서리 투명 처리)
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=255)
    img.putalpha(mask)

    # 배경 재적용 (그라디언트 오버레이 후 배경 복원)
    final = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    bg = Image.new('RGBA', (size, size), bg_color)
    bg_mask = Image.new('L', (size, size), 0)
    bg_mask_draw = ImageDraw.Draw(bg_mask)
    bg_mask_draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=255)
    bg.putalpha(bg_mask)
    final = Image.alpha_composite(final, bg)

    # 그라디언트 오버레이
    overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for i in range(size):
        t = i / size
        r = int(108 * (1-t) + 0 * t)
        g = int(99 * (1-t) + 180 * t)
        b = int(255)
        a = 30
        overlay_draw.line([(0, i), (size, i)], fill=(r, g, b, a))
    overlay.putalpha(bg_mask)
    final = Image.alpha_composite(final, overlay)

    # "JF" 텍스트 렌더링
    draw_final = ImageDraw.Draw(final)
    text = "JF"
    font_size = int(size * 0.42)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

    # 텍스트 크기 계산 및 중앙 정렬
    bbox = draw_final.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) // 2 - bbox[0]
    y = (size - text_h) // 2 - bbox[1]

    # 텍스트 그림자 (깊이감)
    shadow_offset = max(1, size // 64)
    draw_final.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 120))

    # 메인 텍스트 - 밝은 화이트/라이트 블루
    draw_final.text((x, y), text, font=font, fill=(220, 230, 255, 255))

    # 하단 작은 점 장식 (브랜드 포인트)
    dot_r = max(2, size // 40)
    dot_y = int(size * 0.78)
    dot_x = size // 2
    draw_final.ellipse([dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r],
                       fill=(108, 99, 255, 200))

    return final

for sz in [192, 512]:
    icon = create_icon(sz)
    # PNG로 저장 (RGBA → RGB 변환 with white background for compatibility)
    bg = Image.new('RGB', (sz, sz), (11, 18, 32))
    bg.paste(icon, mask=icon.split()[3])
    bg.save(f'/home/ubuntu/braindump/icons/icon-{sz}.png', 'PNG', optimize=True)
    print(f"icon-{sz}.png 생성 완료")

print("아이콘 생성 완료!")
