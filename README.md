# Dotfiles · Ricardo Tovar

Mi flujo principal de código: **Herdr + Pi**, sobre **Zsh + Oh My Zsh + Powerlevel10k**.
**Ghostty** es la única terminal; **Atuin** gestiona el historial y **Lazygit**
es una herramienta auxiliar. Un repositorio para los ajustes; cada herramienta
conserva sus propios datos, paquetes y sesiones.

Probado en **macOS con Apple Silicon**. El instalador reconoce las rutas XDG de
Linux, pero ese entorno todavía no está verificado.

## El stack

```mermaid
flowchart LR
  Ghostty[Ghostty · terminal, ventana y fuentes] --> Zsh[Zsh + Oh My Zsh · shell]
  Zsh --> P10k[Powerlevel10k · prompt]
  Zsh --> Highlight[Syntax highlighting · colores al escribir]
  Zsh --> Atuin[Atuin · historial]
  Zsh --> Herdr[Herdr · workspaces y paneles persistentes]
  Herdr --> Pi[Pi · harness principal de código]
  Zsh --> Tools[Lazygit · herramientas CLI]
```

| Componente | Configuración | Qué aporta |
|---|---|---|
| Herdr | [herdr/config.toml](herdr/config.toml) | Workspaces, paneles y sesiones de código persistentes |
| Pi | Instalación y datos externos al repo | Harness principal de código dentro de Herdr |
| Zsh / Oh My Zsh | [zsh/](zsh/) | Entorno, completions, plugin `git` y atajos |
| Powerlevel10k | [zsh/.p10k.zsh](zsh/.p10k.zsh) | Prompt personal e inicio rápido |
| Ghostty | [ghostty/config](ghostty/config) | Catppuccin Mocha, Meslo Nerd Font y teclado |
| Atuin | [atuin/config.toml](atuin/config.toml) | Búsqueda del historial de comandos |
| Lazygit | [lazygit/config.yml](lazygit/config.yml) | Interfaz Git con tema Catppuccin |

Ghostty es la única terminal del flujo. Herdr usa la configuración vigente y
atajos de Bar, no el antiguo perfil de `herdr-config`.

## Herdr y plugins actuales

Inventario comprobado el **2026-10-13**: **Herdr 0.9.3** y **Pi 1.2.0**.
El servidor está activo, su API detecta `pi` en el panel y la integración Pi de
Herdr está instalada y vigente (`v9`). Pi es el harness principal elegido;
los aliases de otros agentes se conservan como alternativas.

| Plugin habilitado | Versión | Estado observado |
|---|---|---|
| `heeler` | 0.5.0 | Arranque y hooks de actividad/notificaciones exitosos; emparejamiento móvil no comprobado |
| `herdr-bar` | 0.7.3 + parche Pi conservado | Popup, navegación e iconos; watcher de títulos/prefijos detenido |
| `herdr.auto-title` | 0.13.2 | Único renombrador de pestañas/paneles; topic en sidebar; nombres manuales retenidos tras restart |
| `mirror` | 0.4.3 | Registrado y habilitado; sincronización remota no comprobada en esta revisión |

**Heeler, Bar, Auto Title y Mirror están instalados y habilitados**. Bar se abre
con **Cmd+K** en Ghostty o **Ctrl+B, K** en Herdr. **Recarga primero la ventana
abierta de Ghostty con Cmd+Shift+,**: Ricardo confirmó la apertura real tras esa
recarga. Auto Title nombra pestañas/paneles desde contexto terminal, agente y Git;
publica `$topic` en sidebar sin renombrar workspaces. Sus ajustes públicos están en
[herdr/auto-title.env](herdr/auto-title.env); **Ctrl+B, Shift+R** reinicia el daemon.

Bar conserva navegación/iconos, con sus escritores de etiquetas desactivados en
[herdr/bar.json](herdr/bar.json). El parche de nombres de Pi se conserva inactivo:
Auto Title **no refleja `/name` ni genera nombres de sesiones Pi**. Se retiró
`pi-rename-session` por incompatibilidad comprobada con `pi-topping`. Consulta
[el setup y sus límites](docs/herdr.md#auto-title-etiquetas-y-topic). El instalador
enlaza configuraciones: no instala plugins, aplica parches ni activa watchers.

Se retiraron los plugins
`herdr-tsk`, `ttt.editor`, `rcosteira.account-switch` y `herdr-agent-usage`, junto
con sus configuraciones locales; el watcher de Agent Usage también se detuvo.
Las CLI independientes `ttt` y `tsk` se conservan, al igual que las cuentas y
credenciales. Las carpetas residuales de otros plugins no equivalen a plugins
instalados. Consulta [Herdr, Pi y plugins](docs/herdr.md) para comprobar el estado
y la fuente de instalación.

Para trabajar, ejecuta `herdr` en tu terminal y después `pi` dentro del panel
del proyecto. El instalador no abre agentes, instala plugins ni cambia cuentas.

## Empezar

Necesitas **Git, Zsh y Python 3.11+**. Instala Oh My Zsh, Powerlevel10k y el
resaltado siguiendo la [guía de instalación](docs/setup.md).

```sh
git clone https://github.com/rtovardev/dotfiles.git ~/workspace/developer/personal/dotfiles
cd ~/workspace/developer/personal/dotfiles

# Revisar qué archivos se enlazarán.
python3 scripts/install.py

# Crear respaldos y aplicar los enlaces.
python3 scripts/install.py --apply

# Comprobar sintaxis y enlaces.
python3 scripts/check.py --installed
```

Puedes clonar en otra carpeta: el instalador resuelve las rutas desde el propio
repo. Mantén esa carpeta disponible mientras sus archivos estén enlazados.

Después, abre una nueva shell con `exec zsh`. En Ghostty, recarga la configuración
con **Cmd + Shift + ,**.

## Cómo funciona

- El instalador muestra un plan antes de aplicar. Repetir una instalación correcta
  no modifica los enlaces ni genera otro respaldo.
- Los archivos anteriores se guardan en `~/.local/state/dotfiles/backups/`.
- Oh My Zsh gestiona las completions. Atuin y WTP se inicializan antes de cargar
  el resaltado una sola vez al final.
- El entorno conserva las toolchains instaladas y elimina duplicados de `PATH`.
  El editor usa Vim por SSH y, localmente, Neovim, Helix o Vim según disponibilidad.
- `SSH_AUTH_SOCK` se hereda del entorno, respetando el agente SSH del sistema.

Los paquetes del [Brewfile](Brewfile) se instalan **por separado**:

```sh
brew bundle --file=Brewfile
```

Ese comando puede instalar o actualizar herramientas. El instalador de enlaces
no ejecuta Homebrew ni instala frameworks o plugins.

## Personalizar

Edita los archivos del repo y revisa el diff antes de guardar los cambios. Para
configurar el prompt, usa `p10k configure`; la guía explica cómo conservar el
enlace si el asistente reemplaza `~/.p10k.zsh`.

Los ajustes de una sola máquina pueden vivir fuera de Git:

| Archivo local | Se carga en |
|---|---|
| `~/.config/zsh/env.local.zsh` | Todas las shells Zsh |
| `~/.config/zsh/local.zsh` | Shells interactivas, antes del resaltado |

Los [atajos de agentes](docs/shell.md#atajos-de-agentes) reflejan mis preferencias;
revísalos si vas a reutilizar esta configuración.

## Documentación

- [Instalación y dependencias](docs/setup.md)
- [Zsh, integraciones y atajos](docs/shell.md)
- [Herdr, Pi y plugins](docs/herdr.md)
- [Mantenimiento, comprobaciones y restauración](docs/maintenance.md)
- [Consolidación de los repos anteriores](docs/migration.md)

Las cuentas, credenciales, historiales, bases de datos, sesiones, cachés y backups
privados se conservan fuera de este repositorio. Los frameworks y plugins también
se instalan aparte.
