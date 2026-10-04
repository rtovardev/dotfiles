# Instalación

## Requisitos

Git, Zsh y Python 3.11+. El stack está probado en macOS Apple Silicon. En Linux
el instalador usa rutas XDG, pero hay que revisar las opciones específicas de
macOS de Ghostty y la compatibilidad de los plugins de Herdr.

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
| Herdr | `~/.config/herdr/config.toml` | Igual |
| Atuin | `~/.config/atuin/config.toml` | Igual |
| Lazygit | Ruta XDG y `~/Library/Application Support/lazygit/config.yml` | `~/.config/lazygit/config.yml` |
| Lazydocker | Ruta XDG y `~/Library/Application Support/lazydocker/config.yml` | `~/.config/lazydocker/config.yml` |
| codex-switch | `~/.local/bin/codex-switch` | Igual |

Si `~/.config/ghostty` ya apunta al directorio nativo de macOS, se conserva ese
enlace de directorio; ambas rutas leen el mismo archivo instalado.

## Fuentes y herramientas

Ghostty usa `MesloLGS Nerd Font Mono`. Sus mapas de iconos requieren la fuente
`Herdr Agent Icons Max`; instálala o retira los dos `font-codepoint-map` si no
usas esos iconos.

El Brewfile declara Atuin, Lazygit, Lazydocker, TTT, GitHub CLI y terminal-browser.
Ghostty, Herdr, fuentes, plugins y toolchains se instalan aparte. Lazygit utiliza
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

El instalador no recarga Herdr, abre agentes o cambia sus cuentas.
