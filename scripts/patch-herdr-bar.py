#!/usr/bin/env python3
"""Parche explícito y versionado; no descarga plugins ni inicia watchers."""
import argparse
from pathlib import Path
import subprocess

UPSTREAM_COMMIT = 'e22455068e26340b6be02cec8a07707fc1f11ae1'
PATCH = Path(__file__).resolve().parent.parent / 'herdr/patches/pi-session-titles.patch'


def git(root: Path, *args):
    return subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)


def apply_patch(root: Path, apply=False, patch_path=PATCH, commit=UPSTREAM_COMMIT):
    root = root.expanduser().resolve()
    patch_path = patch_path.resolve()
    location = git(root, 'rev-parse', '--show-toplevel')
    if location.returncode or Path(location.stdout.strip()).resolve() != root:
        raise RuntimeError('La ruta debe ser la raíz Git del plugin instalado.')
    revision = git(root, 'rev-parse', 'HEAD')
    if revision.returncode or revision.stdout.strip() != commit:
        raise RuntimeError(f'Parche limitado a herdr-bar {commit}; revisa la nueva versión antes de aplicarlo.')
    if not patch_path.is_file():
        raise RuntimeError(f'Falta el parche: {patch_path}')
    if git(root, 'apply', '--reverse', '--check', str(patch_path)).returncode == 0:
        print(f'Parche de Pi ya aplicado: {root}')
        return False
    check = git(root, 'apply', '--check', str(patch_path))
    if check.returncode:
        raise RuntimeError(f'El parche no aplica limpiamente; se conservan los cambios locales:\n{check.stderr.strip()}')
    if not apply:
        print(f'Plan: aplicar {patch_path.name} en {root}')
        print('Sin cambios. Repite el comando con --apply para aplicar.')
        return False
    result = git(root, 'apply', str(patch_path))
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    print(f'Parche de títulos de Pi aplicado: {root}')
    print('No se instalaron paquetes ni se iniciaron watchers.')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plugin-root', type=Path, required=True,
                        help='plugin_root de herdr plugin list --json')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        apply_patch(args.plugin_root, args.apply)
    except RuntimeError as error:
        parser.exit(1, f'{error}\n')
