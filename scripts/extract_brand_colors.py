from collections import Counter
from pathlib import Path

FALLBACK = {
    "primary": "#0E3A53",
    "secondary": "#2DB3E8",
    "accent": "#F59C2D",
    "background": "#E6ECEF",
    "accent_yellow": "#F6C33B",
}

logo = Path('branding/logo.png')
palette = FALLBACK.copy()
status = "fallback"
reason = "Plik branding/logo.png nie istnieje."

if logo.exists():
    try:
        from PIL import Image

        img = Image.open(logo).convert('RGB').resize((180, 180))
        colors = Counter(img.getdata()).most_common(12)
        hexes = ['#%02X%02X%02X' % c for c, _ in colors]
        if len(hexes) >= 4:
            palette.update({
                'primary': hexes[0],
                'secondary': hexes[1],
                'accent': hexes[2],
                'background': hexes[-1],
            })
            status = 'extracted'
            reason = 'Kolory pobrane automatycznie z logo.'
        else:
            reason = 'Za mało kolorów w logo, użyto fallback.'
    except Exception as exc:
        reason = f'Ekstrakcja nieudana ({exc}), użyto fallback.'

md = f"""# BRAND_COLORS

Status: **{status}**  
Powód: {reason}

## Paleta marki
- Primary: `{palette['primary']}`
- Secondary: `{palette['secondary']}`
- Accent: `{palette['accent']}`
- Background: `{palette['background']}`
- Accent yellow (fallback): `{palette['accent_yellow']}`

## Źródło logo
Umieść logo w ścieżce `branding/logo.png` (repo root), aby automatyczna ekstrakcja kolorów działała.
"""
Path('BRAND_COLORS.md').write_text(md)
print(status, reason)
