# Dotfiles de Ricardo

Configuración de Zsh, Ghostty, Herdr y herramientas CLI en un solo repositorio.
Sustituye cli-config, ghostty-config y herdr-config. Neovim y my-pi-setup conservan
sus repositorios independientes.

## Contenido

| Carpeta | Responsabilidad |
|---|---|
| zsh/ | Entorno, Oh My Zsh, Powerlevel10k, integraciones y atajos propios |
| ghostty/ | Tema, fuentes, teclado e iconos de Herdr |
| herdr/ | Configuración del multiplexor y sus atajos |
| atuin/ | Preferencias de historial; datos y cuenta fuera del repo |
| lazygit/, lazydocker/ | Preferencias de las herramientas TUI |
| bin/ | Wrapper vigente de codex-switch |
| scripts/ | Plan, instalación con respaldo, restauración y verificación |
| docs/ | Diagnóstico inicial y procedencia de la consolidación |

Ghostty dibuja la terminal; Herdr organiza paneles; Zsh ejecuta comandos;
Oh My Zsh proporciona funciones de shell; p10k dibuja el prompt;
zsh-syntax-highlighting colorea la línea de comandos; Atuin busca el historial.

## Instalar

Dependencias del instalador: Python 3.11+ y Zsh. Las herramientas se instalan aparte.

```sh
git clone git@github.com:rtovardev/dotfiles.git ~/workspace/developer/personal/dotfiles
cd ~/workspace/developer/personal/dotfiles
python3 scripts/install.py
python3 scripts/install.py --apply
python3 scripts/check.py --installed
```

El primer comando muestra el plan. --apply respalda cada archivo o enlace existente
en ~/.local/state/dotfiles/backups/ y enlaza la configuración con el repo clonado.
Repetirlo no genera respaldos si los enlaces ya son correctos. No instala paquetes,
cambia cuentas de agentes, activa watchers ni recarga Herdr.

En macOS se enlazan las ubicaciones de Library/Application Support para Ghostty,
Lazygit y Lazydocker; en Linux se usan ~/.config. Si ~/.config/ghostty ya apunta
al directorio nativo de macOS, se conserva ese enlace de directorio.

Las preferencias de Herdr preservan el stack actual de Ricardo, incluidos sus
plugins. En Linux los enlaces y Zsh son portables, pero la compatibilidad de cada
plugin de Herdr debe verificarse en ese equipo. Esta migración solo se probó en Mac.

Abre una nueva shell con exec zsh. Ghostty permite recargar con Cmd+Shift+,.
No se reinicia el servidor de Herdr automáticamente.

## Framework y prompt

Oh My Zsh se instala según https://ohmyz.sh/. Para p10k:

```sh
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"
git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"
```

No ejecutes esos clones si las carpetas ya existen. El plugin git se mantiene.
El resaltado se carga una sola vez al final, desde la instalación custom de
Oh My Zsh, con Homebrew como alternativa. Esto permite cargar Atuin y WTP antes
del resaltado. Oh My Zsh ejecuta compinit; no se duplica en las integraciones.

El p10k configurado por Ricardo se conserva en zsh/.p10k.zsh. Puedes ejecutar
p10k configure cuando quieras cambiarlo; si el asistente reemplaza el enlace,
revisa el archivo generado y reincorpóralo al repo antes de reaplicar el instalador.

## Entorno y preferencias locales

PATH incluye solamente directorios presentes y elimina duplicados. Conserva
las toolchains previamente instaladas de Ricardo (Go, Bun, .NET, Rust, Java,
Railway y Composio), sin instalarlas. El editor es Vim por SSH; localmente usa
Neovim si existe, luego Helix y finalmente Vim. No se sobrescribe SSH_AUTH_SOCK.

Las preferencias de historial actuales desactivan share_history e
inc_append_history; Atuin se inicializa si está disponible.

Atajos propios: lg, ld, t, tb, cs, codex-mart, codex-personal y perfiles OpenCode.
Se conservaron además los aliases codex, agy y opencode añadidos localmente
a .zshrc durante la migración, incluidos sus flags personalizados. Las pruebas
y el instalador no ejecutan estos comandos.
El hook lean-ctx permanece fuera de la configuración común porque reescribe
muchos comandos; si lo quieres, cárgalo explícitamente desde el archivo local.

- ~/.config/zsh/env.local.zsh: variables privadas indispensables en todas las shells.
- ~/.config/zsh/local.zsh: ajustes interactivos personales, antes del resaltado.

Esos archivos son locales y quedan fuera del repo. No hay carga automática de
.env del cerebro. No se versionan claves, credenciales, historial, bases de datos,
cachés, sesiones, plugins instalados ni respaldos privados.

codex-switch conserva el wrapper de la instalación vigente: las acciones de
cambio de cuenta pueden detener procesos de Codex; el instalador y las pruebas
no ejecutan esas acciones. El wrapper requiere el plugin de Herdr Account Switch
y codex-reload externo para su subcomando update.

## Paquetes y pruebas

El Brewfile declara el stack CLI anterior, sin Oh My Posh. Ejecutar brew bundle
es una acción aparte: puede instalar o actualizar paquetes. Los paquetes ya
instalados de Oh My Posh no se desinstalan incidentalmente.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check.py
git diff --check
```

Para restaurar los enlaces y archivos de una instalación:

```sh
python3 scripts/restore.py /ruta/al/respaldo
python3 scripts/restore.py /ruta/al/respaldo --apply
```

La restauración comprueba todos los destinos antes de actuar y se niega a pisar
cambios posteriores del usuario. Si un destino cambió, revisa y restaura el archivo
que corresponda manualmente desde el respaldo.
