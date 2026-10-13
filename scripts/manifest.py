from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent


def links(home: Path):
    targets = {
        'zsh/.zshenv': '.zshenv',
        'zsh/.zprofile': '.zprofile',
        'zsh/.zshrc': '.zshrc',
        'zsh/.p10k.zsh': '.p10k.zsh',
        'atuin/config.toml': '.config/atuin/config.toml',
        'herdr/config.toml': '.config/herdr/config.toml',
        'herdr/bar.json': '.config/herdr/plugins/config/herdr-bar/config.json',
        'herdr/auto-title.env': '.config/herdr-auto-title/config.env',
        'lazygit/config.yml': '.config/lazygit/config.yml',
    }
    if sys.platform == 'darwin':
        targets['ghostty/config'] = 'Library/Application Support/com.mitchellh.ghostty/config'
    else:
        targets['ghostty/config'] = '.config/ghostty/config'
    result = [(ROOT / source, home / target) for source, target in targets.items()]
    if sys.platform == 'darwin':
        result.extend([
            (ROOT / 'lazygit/config.yml', home / 'Library/Application Support/lazygit/config.yml'),
        ])
        # Si XDG ya apunta al directorio nativo, ambos nombres leen el mismo archivo.
        ghostty_xdg = home / '.config/ghostty/config'
        native = home / 'Library/Application Support/com.mitchellh.ghostty/config'
        if ghostty_xdg.parent.resolve() != native.parent.resolve():
            result.append((ROOT / 'ghostty/config', ghostty_xdg))
    return result
