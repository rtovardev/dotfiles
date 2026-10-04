# Mantenimiento y restauración

## Comprobar cambios

Los destinos instalados enlazan al checkout. Editar el repo cambia los ajustes
disponibles en la próxima recarga de cada aplicación.

Desde el checkout que administra los enlaces activos:

```sh
python3 scripts/check.py --installed
python3 -m unittest discover -s tests -v
git diff --check
git diff
```

En un worktree de desarrollo utiliza `check.py` sin `--installed`: los enlaces
pueden apuntar al checkout principal.

El verificador revisa sintaxis Zsh/shell, TOML de Herdr/Atuin y los enlaces
cuando se solicita. Las pruebas comprueban plan sin modificaciones, aplicación,
idempotencia, restauración de archivos/enlaces rotos y protección de cambios
posteriores. No certifican glifos, plugins, cuentas o sincronización remota.

## Actualizar

Revisa `git status`, ejecuta `git fetch origin` y revisa tu diff antes de
actualizar la rama. Conserva cualquier trabajo local y vuelve a verificar después
de integrar cambios. Si mueves el checkout, vuelve a planificar y aplicar enlaces.

Oh My Zsh, p10k y sus plugins se actualizan en sus instalaciones respectivas.

## Respaldos

Cada aplicación del instalador que requiere cambios guarda un respaldo en:

```text
~/.local/state/dotfiles/backups/<fecha-UTC>/
  manifest.json
  0
  1
  ...
```

El manifiesto relaciona los archivos numerados con sus destinos originales.
Los enlaces anteriores se guardan como enlaces, incluidos los rotos. Los
respaldos viven en un directorio privado fuera de Git.

## Restaurar

Primero revisa el plan y después aplica el mismo respaldo:

```sh
python3 scripts/restore.py "$HOME/.local/state/dotfiles/backups/<fecha-UTC>"
python3 scripts/restore.py "$HOME/.local/state/dotfiles/backups/<fecha-UTC>" --apply
```

La restauración revisa todos los destinos antes de actuar. Si alguno cambió
desde la instalación, se detiene; revisa y recupera manualmente lo necesario.

Restaurar un enlace no recupera el repo al que apuntaba. Si ese checkout fue
retirado, recupera también su archivo de consolidación o enlaza a una fuente
disponible.

## Publicar

Mantén fuera de Git credenciales, claves SSH, OAuth, sesiones, historiales,
bases de datos, cachés, respaldos privados y `.env`. Revisa siempre el diff:
el `.gitignore` excluye patrones comunes, pero no sustituye esa revisión.
