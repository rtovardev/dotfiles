#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess
import tomllib
from manifest import ROOT, links


def check(home: Path, installed=False):
    failed = False
    candidates = {ROOT / 'zsh' / name for name in ['.zshenv', '.zprofile', '.zshrc']}
    candidates.update((ROOT / 'zsh').glob('*.zsh'))
    candidates.add(ROOT / 'zsh/.p10k.zsh')
    for p in sorted(candidates):
        if p.is_file():
            result = subprocess.run(['zsh', '-n', str(p)], capture_output=True)
            print(f'ZSH {p.name}: {"OK" if result.returncode == 0 else "ERROR"}')
            failed |= result.returncode != 0
    for relative in ['atuin/config.toml']:
        tomllib.loads((ROOT / relative).read_text())
        print(f'TOML {relative}: OK')
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
