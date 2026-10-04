# Validación de la migración

2026-10-03, Mac local.

- Sintaxis correcta de .zshenv, .zprofile, .zshrc, .p10k.zsh, environment.zsh,
  integrations.zsh, aliases.zsh y bin/codex-switch.
- Configuraciones TOML de Herdr y Atuin parseadas correctamente.
- 12 enlaces activos apuntan a dotfiles; volver a planificar arroja 0 cambios.
- Dos pruebas del instalador: plan sin cambios, aplicación, repetición sin cambios,
  recuperación de archivo normal y enlace roto; restauración rechaza cambios
  posteriores del usuario antes de modificar cualquier destino.
- Shell interactiva real: Powerlevel10k 1.20.18, daemon Git activo, resaltado
  desde la instalación custom de Oh My Zsh, widget atuin-search y función wtp.
- EDITOR=hx porque nvim no está en el PATH; el respaldo de Neovim sigue separado.
- Disponibles Boot.dev, Bun, .NET, Cargo, Composio, Railway y Java del JDK 21.
- Prueba de variable SSH_AUTH_SOCK: la shell conserva el valor recibido del
  entorno. No se verificó autenticación SSH ni se enumeraron llaves.
- Ghostty +validate-config: exit 0 sin errores fuera del sandbox.
- Ghostty y codex-switch conservan el contenido exacto de sus fuentes anteriores.
  Herdr y p10k conservan sus ajustes; solo se normalizaron espacios finales.
  codex-switch se marcó ejecutable para que funcione desde ~/.local/bin.
- Escaneo de los archivos preparados: sin patrones de claves GitHub/OpenAI,
  llaves privadas o asignaciones literales de credenciales detectados.

Los errores de caché/p10k/Sentry dentro del sandbox no se reprodujeron fuera.
No se recargó Herdr, cambiaron cuentas, instalaron paquetes, importaron historiales
ni verificó sincronización remota de Atuin. No hubo revisión visual del prompt.
La MSI y otros equipos no fueron modificados.

Los tres repos anteriores no tenían issues, PRs o releases (incluidos los
cerrados) en el respaldo remoto previo a eliminarlos. Sus objetos Git, ramas,
worktrees y cambios locales se preservaron en un respaldo privado fuera de Git.

Los tres aliases de agentes añadidos durante la migración se revisaron como
texto y se conservaron; no se ejecutaron los agentes para validarlos.
