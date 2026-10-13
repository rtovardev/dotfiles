# Instalación

## Requisitos

Git, Zsh y Python 3.11+. El stack está probado en macOS Apple Silicon. En Linux
el instalador usa rutas XDG, pero hay que revisar las opciones específicas de
macOS de Ghostty. Comprueba `python3 --version`: el Python del sistema de
macOS puede ser 3.9 y no incluye `tomllib`. En esta Mac se validó con
`/opt/homebrew/bin/python3` (3.14); usa Python 3.11+ para los comandos del repo.

Instala [Oh My Zsh](https://ohmyz.sh/) según sus instrucciones oficiales.
Después instala [Powerlevel10k](https://github.com/romkatv/powerlevel10k#oh-my-zsh)
y [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md)
si sus carpetas todavía no existen:

```sh
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"

git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"
```

Las instalaciones existentes se actualizan en sus propios checkouts; no se
copian dentro de dotfiles. Powerlevel10k declara soporte limitado en su repo.

## Aplicar los enlaces

Desde el checkout de dotfiles:

```sh
python3 scripts/install.py
python3 scripts/install.py --apply
python3 scripts/check.py --installed
```

El primer comando muestra los destinos exactos. `--apply` respalda los archivos
anteriores y crea los enlaces. Si encuentra un directorio donde esperaba un
archivo, se detiene para que revises el destino.

| Aplicación | macOS | Linux |
|---|---|---|
| Zsh | `.zshenv`, `.zprofile`, `.zshrc` y `.p10k.zsh` del home | Igual |
| Ghostty | `~/Library/Application Support/com.mitchellh.ghostty/config` y ruta XDG cuando corresponde | `~/.config/ghostty/config` |
| Atuin | `~/.config/atuin/config.toml` | Igual |
| Herdr | `~/.config/herdr/config.toml` | Igual |
| Lazygit | Ruta XDG y `~/Library/Application Support/lazygit/config.yml` | `~/.config/lazygit/config.yml` |

Si `~/.config/ghostty` ya apunta al directorio nativo de macOS, se conserva ese
enlace de directorio; ambas rutas leen el mismo archivo instalado.

## Fuentes y herramientas

Ghostty usa `MesloLGS Nerd Font Mono`.

Ghostty es la única terminal del flujo y utiliza los archivos de Zsh enlazados.

El Brewfile declara Atuin, Lazygit, TTT, GitHub CLI y terminal-browser.
Ghostty, Herdr, Pi, fuentes, plugins y toolchains se instalan aparte. Lazygit utiliza
`delta` como pager; WTP se inicializa solo si está disponible.

## Configurar y recargar

```sh
exec zsh
p10k configure
```

El prompt incluido vive en `zsh/.p10k.zsh`. Si el asistente reemplaza el enlace
por un archivo normal, guarda ese resultado y revisa sus cambios antes de
incorporarlos al repo y reaplicar enlaces. Reaplicar directamente podría
reemplazar el archivo nuevo por la versión guardada en el checkout.

En Ghostty usa Cmd + Shift + , para recargar. Para validar su archivo en macOS:

```sh
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
```

El instalador no abre agentes ni cambia sus cuentas. Herdr organiza el flujo
principal de código con Pi; consulta [su configuración y plugins](herdr.md).
Aplicar enlaces tampoco recarga el servidor de Herdr.
