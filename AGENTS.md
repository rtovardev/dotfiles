# Dotfiles de Ricardo

Este repositorio contiene ajustes de Zsh, Ghostty, Atuin, Herdr y herramientas CLI.
Herdr organiza el trabajo de código con Pi como harness principal; Warp y Ghostty son terminales.
Las instalaciones de frameworks/plugins y los datos de los agentes viven fuera.

- Leer README.md. Preservar cambios locales y revisar las rutas antes de enlazar.
- No versionar credenciales, historiales, sesiones, cachés ni respaldos privados.
- install.py sin argumentos solo muestra el plan. --apply crea respaldos y enlaces.
- No instalar paquetes, activar watchers, cambiar cuentas, abrir terminales ni publicar
  como efecto incidental de aplicar configuraciones.
- macOS y Linux tienen rutas distintas. No sobrescribir SSH_AUTH_SOCK.
- Ejecutar unittest, check.py y git diff --check antes de entregar cambios.
- Merge, push y eliminación de repos remotos requieren autorización vigente.
