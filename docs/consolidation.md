# Procedencia de la consolidación

2026-10-03. Ricardo autorizó consolidar Zsh, Ghostty, Herdr y las herramientas
CLI en dotfiles y eliminar cli-config, ghostty-config y herdr-config tanto
localmente como en GitHub. Neovim y my-pi-setup quedan fuera.

Los archivos de Ghostty y Herdr se copiaron de los árboles locales, incluidos
sus cambios sin commit. Atuin, Lazygit y Lazydocker se copiaron de cli-config.
codex-switch se copió del worktree native-codex-account-switch, que era el
destino efectivo de ~/.local/bin/codex-switch. El archivo coincide byte a byte
con la versión activa anterior; no se cambió el backend de cuentas. Se marcó
ejecutable el wrapper y se normalizó whitespace de Herdr y p10k.

El p10k procede del ~/.p10k.zsh vigente. Zsh se reconstruyó a partir de la
configuración Oh My Zsh nueva y de las integraciones pertinentes del respaldo
pre-oh-my-zsh. No se copiaron credenciales ni .env al repo.

Se conserva fuera de Git un respaldo de los tres repos anteriores, sus
worktrees e información remota antes de eliminarlos. Su ubicación concreta
se informa a Ricardo al finalizar; no forma parte de la instalación portable.

El diagnóstico audit-2026-10-03.md describe el estado ANTERIOR a la adaptación;
sus enlaces rotos y defectos enumerados no describen el resultado final.

Durante la revisión final aparecieron nuevos aliases codex, agy y opencode en
el .zshrc enlazado. Se preservaron como trabajo local concurrente.
