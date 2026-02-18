from pathlib import Path

logo = Path('branding/logo.png')
icons_dir = Path('branding/icons')
icons_dir.mkdir(parents=True, exist_ok=True)

if not logo.exists():
    print('branding/logo.png not found. Place your logo there and generate icons with your preferred tool.')
else:
    print('Logo found. Generate favicon/icon_192/icon_512/maskable/splash assets from branding/logo.png.')
