# Zsh e integraciones

## Orden de carga

1. `.zshenv` carga variables privadas opcionales desde `env.local.zsh`.
2. `.zprofile` prepara el entorno de login.
3. `.zshrc` carga el inicio rápido de p10k y el entorno compartido.
4. Oh My Zsh carga el plugin `git` e inicializa las completions.
5. Se cargan WTP, Atuin, completions de Bun y atajos propios.
6. Se elige el editor, se ajusta el historial y se carga `.p10k.zsh`.
7. Se cargan ajustes locales opcionales y el resaltado de sintaxis al final.

El resaltado usa la instalación custom de Oh My Zsh, con Homebrew como
alternativa. Se carga una sola copia. El plugin `git` conserva sus aliases
y funciones. Oh My Zsh realiza `compinit`; las integraciones no lo duplican.

## Entorno e historial

`environment.zsh` añade solamente directorios presentes y elimina duplicados
de `PATH`. Reconoce Homebrew, Go, Bun, .NET, Rust/rustup, Java 21, Railway,
Composio y ejecutables personales. Preparar las rutas no instala programas.

`EDITOR` y `VISUAL` usan Vim por SSH. Localmente prefieren Neovim si está
instalado, después Helix y finalmente Vim. La configuración de Neovim no está
incluida. `SSH_AUTH_SOCK` conserva el valor recibido del entorno.

Atuin se inicializa si está disponible. Sus preferencias viven en el repo;
historial, claves y cuentas permanecen fuera. Zsh mantiene desactivadas las
opciones `share_history` e `inc_append_history`. El instalador no importa ni
sincroniza el historial.

## Atajos

| Atajo | Comando |
|---|---|
| `lg` | Lazygit |
| `t` / `tb` | TTT / terminal-browser |
| `opencode-personal` / `opencode-trabajo` | OpenCode con directorios de datos separados |

## Atajos de agentes

La configuración personal conserva estos aliases en `.zshrc`:

```zsh
alias codex="codex --yolo"
alias agy="agy --dangerously-skip-permissions"
alias opencode="opencode --yolo"
```

Incluyen flags personalizados de cada CLI. Puedes retirarlos o ajustarlos a tu
flujo. La compatibilidad del flag de OpenCode no se ha certificado; el instalador
y las pruebas no ejecutan agentes.

## Ajustes locales

Usa `~/.config/zsh/env.local.zsh` para variables de todas las shells y
`~/.config/zsh/local.zsh` para ajustes interactivos. Son opcionales y quedan
fuera de Git. El segundo se carga antes del resaltado.

Hooks que reescriben comandos, como lean-ctx, pueden cargarse explícitamente
desde ese archivo local; no se cargan por defecto desde dotfiles.
