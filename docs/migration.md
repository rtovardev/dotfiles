# Consolidación

Dotfiles reúne los ajustes antes separados en `cli-config`, `ghostty-config`
y `herdr-config`.

Conserva las preferencias de Ghostty, Herdr, Atuin, Lazygit y Lazydocker,
el prompt p10k y el wrapper de cuentas vigente. Zsh se adaptó a Oh My Zsh y
Powerlevel10k con una sola carga del resaltado, Atuin, WTP, rutas de herramientas
y selección de un editor disponible.

La migración corrigió enlaces a un workspace anterior, retiró la sobrescritura
del socket SSH y dejó de inicializar Oh My Posh. Los paquetes instalados se
administran aparte del repo.

Los historiales Git, worktrees y cambios locales de los repos retirados se
preservan en respaldos privados fuera del repo. Las notas específicas de la
intervención tampoco forman parte de la documentación pública actual.

Los repos de configuración de Neovim y del inventario Pi se retiran por separado;
sus contenidos no se incorporan a dotfiles. Esta configuración de terminal no
instala ni desinstala esos programas.

Se comprobó la instalación en la Mac original: sintaxis, doce enlaces,
idempotencia, restauración y arranque real con p10k, estado Git, resaltado,
Atuin y WTP. Ghostty validó su archivo con `+validate-config`. Linux y otros
equipos requieren su propia comprobación.
