#!/usr/bin/env python3
"""Plan por defecto; aplicación con respaldo privado, sin instalar dependencias."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
from manifest import links


def install(home: Path, apply=False):
    pairs = links(home)
    for source, target in pairs:
        if not source.is_file():
            raise RuntimeError(f'Falta fuente: {source}')
        if target.exists() and target.is_dir() and not target.is_symlink():
            raise RuntimeError(f'No se reemplaza un directorio: {target}')
    pending = [(s, t) for s, t in pairs if not (t.is_symlink() and t.resolve() == s.resolve())]
    for source, target in pending:
        print(f'ENLAZAR {target} -> {source}')
    if not apply:
        print(f'Plan: {len(pending)} enlaces. Aplicar: python3 scripts/install.py --apply')
        return None
    if not pending:
        print('Sin cambios: los enlaces ya son correctos.')
        return None
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = home / '.local/state/dotfiles/backups' / stamp
    backup.mkdir(parents=True, mode=0o700)
    records = []
    for index, (source, target) in enumerate(pending):
        record = {'target': str(target), 'source': str(source), 'existed': target.exists() or target.is_symlink()}
        if record['existed']:
            original = backup / str(index)
            shutil.copy2(target, original, follow_symlinks=False)
            record['backup'] = str(original)
        records.append(record)
    # Guardar antes de aplicar: permite restaurar incluso si hay un fallo intermedio.
    receipt = backup / 'manifest.json'
    receipt.write_text(json.dumps(records, indent=2) + '\n')
    receipt.chmod(0o600)
    for source, target in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + '.dotfiles-new')
        if temporary.exists() or temporary.is_symlink():
            raise RuntimeError(f'Existe un temporal ajeno: {temporary}')
        temporary.symlink_to(source)
        os.replace(temporary, target)
    print(f'Respaldo: {backup}')
    print('No se instalaron paquetes, cambiaron cuentas ni recargaron servicios.')
    return backup


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--home', type=Path, default=Path.home())
    args = parser.parse_args()
    install(args.home.resolve(), args.apply)
