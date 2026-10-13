#!/usr/bin/env python3
import argparse
import json
import subprocess
import tomllib
from pathlib import Path

from manifest import ROOT, links


def check_auto_title(path: Path):
    """Valida el formato público que consume Auto Title, sin ejecutar el plugin."""
    booleans = {
        'POSITION', 'PANES', 'WORKSPACES', 'AGENT_NAME', 'PREFER_AGENT',
        'PANE_ID', 'TRANSCRIPT', 'DEBUG',
    }
    integers = {'POLL_MS', 'MAX_LENGTH', 'BRANCH_MAX'}
    values = {}
    for number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        key, separator, value = line.partition('=')
        prefix = 'HERDR_AUTO_TITLE_'
        setting = key.removeprefix(prefix)
        if not separator or not key.startswith(prefix) or key in values:
            raise ValueError(f'{path.name}:{number}: ajuste inválido o duplicado')
        if setting in booleans:
            valid = value in {'true', 'false'}
        elif setting in integers:
            try:
                valid = value.isascii() and value.isdigit() and int(value) > 0
            except ValueError:
                valid = False
        else:
            valid = False
        if not valid:
            raise ValueError(f'{path.name}:{number}: valor no admitido para {key}')
        values[key] = value
    if not values:
        raise ValueError(f'{path.name}: configuración vacía')
    return values


def check(home: Path, installed=False):
    failed = False
    candidates = {ROOT / 'zsh' / name for name in ['.zshenv', '.zprofile', '.zshrc']}
    candidates.update((ROOT / 'zsh').glob('*.zsh'))
    candidates.add(ROOT / 'zsh/.p10k.zsh')
    for p in sorted(candidates):
        if p.is_file():
            result = subprocess.run(['zsh', '-n', str(p)], check=False, capture_output=True)
            print(f'ZSH {p.name}: {"OK" if result.returncode == 0 else "ERROR"}')
            failed |= result.returncode != 0
    for relative in ['atuin/config.toml', 'herdr/config.toml']:
        tomllib.loads((ROOT / relative).read_text())
        print(f'TOML {relative}: OK')
    try:
        bar = json.loads((ROOT / 'herdr/bar.json').read_text())
    except (OSError, json.JSONDecodeError) as error:
        print(f'JSON herdr/bar.json: ERROR ({error})')
        return 1
    if not isinstance(bar, dict):
        print('JSON herdr/bar.json: ERROR (se requiere un objeto JSON)')
        return 1
    print('JSON herdr/bar.json: OK')
    check_auto_title(ROOT / 'herdr/auto-title.env')
    print('ENV herdr/auto-title.env: OK')
    if installed:
        for source, target in links(home):
            good = target.is_symlink() and target.exists() and target.resolve() == source.resolve()
            print(f'LINK {target.relative_to(home)}: {"OK" if good else "ERROR"}')
            failed |= not good
    return 1 if failed else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--installed', action='store_true')
    parser.add_argument('--home', type=Path, default=Path.home())
    args = parser.parse_args()
    raise SystemExit(check(args.home.resolve(), args.installed))
