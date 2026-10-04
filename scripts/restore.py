#!/usr/bin/env python3
"""Restaurar un respaldo de enlaces; plan por defecto."""
import argparse
import json
from pathlib import Path
import os
import shutil


def restore(backup: Path, apply=False):
    records = json.loads((backup / 'manifest.json').read_text())
    if apply:
        for record in records:
            target = Path(record['target'])
            if not target.is_symlink() or str(target.readlink()) != record['source']:
                raise RuntimeError(f'El destino cambió después de la instalación: {target}')
            temporary = target.with_name(target.name + '.dotfiles-restore')
            if temporary.exists() or temporary.is_symlink():
                raise RuntimeError(f'Existe un temporal ajeno: {temporary}')
            if record['existed']:
                original = Path(record['backup'])
                if not original.exists() and not original.is_symlink():
                    raise RuntimeError(f'Falta respaldo: {original}')
    for record in records:
        target = Path(record['target'])
        print(f'RESTAURAR {target}')
        if not apply:
            continue
        if record['existed']:
            original = Path(record['backup'])
            temporary = target.with_name(target.name + '.dotfiles-restore')
            shutil.copy2(original, temporary, follow_symlinks=False)
            os.replace(temporary, target)
        else:
            target.unlink()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('backup', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    restore(args.backup.resolve(), args.apply)
