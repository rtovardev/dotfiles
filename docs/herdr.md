# Herdr + Pi

Herdr es el gestor de workspaces y paneles persistentes para el trabajo de código.
Pi es el harness principal. Warp y Ghostty siguen disponibles como terminales.
Las versiones y el estado observado están en el [README](../README.md).

## Configuración versionada

[herdr/config.toml](../herdr/config.toml) conserva el ajuste vigente
`onboarding = false`; el resto usa los valores por defecto de Herdr. El instalador
enlaza **solo ese archivo** a `~/.config/herdr/config.toml`, con respaldo del
archivo anterior. No enlaza todo el directorio ni restaura el perfil antiguo.

`HERDR_CONFIG_PATH` permite usar otro archivo de configuración: si lo defines,
comprueba esa ruta antes de asumir que Herdr lee el archivo enlazado.

Quedan fuera de Git `plugins.json` (registro con rutas locales), código de
plugins, configuraciones privadas de plugins, cuentas, tokens, dispositivos
emparejados, sesiones, snapshots, sockets, logs y backups. Los datos y paquetes
de Pi también permanecen fuera de dotfiles.

## Flujo principal

```sh
cd /ruta/al/proyecto
herdr
# Dentro del panel del proyecto:
pi
```

Herdr y Pi se instalan por separado; el instalador de dotfiles no los instala,
no activa watchers ni modifica integraciones. La integración Pi existente se
comprobó con `herdr integration status`, y la API del servidor detectó Pi.
Esa integración de agente es distinta del plugin de workflow Heeler y se conserva.

## Comprobar el estado sin cambiarlo

```sh
herdr --version
herdr status
herdr plugin list
herdr plugin action list
herdr plugin log list --limit 30
herdr integration status
```

`plugin list` muestra instalación y habilitación; `action list` comprueba las
acciones que carga el servidor. Los logs permiten verificar arranques y eventos:
`status: succeeded` con `exit_code: 0` acredita ese comando, no todas las funciones
del plugin. Las consultas de estado no cambian cuentas ni abren paneles.

## Fuentes de los plugins registrados

| ID | Fuente instalada | Ref/commit registrado |
|---|---|---|
| `heeler` | `ZingerLittleBee/Heeler/plugin` | `749d11cc4011ff1a921eb83339a4f8b2bbe7f7a7` (instalado desde `main`) |

Para una instalación nueva, revisa primero la fuente y sus dependencias. La forma
explícita de instalar un plugin de GitHub es:

```sh
herdr plugin install OWNER/REPO[/SUBDIR] --ref COMMIT
```

Esto descarga código y puede ejecutar pasos de build; no se ejecuta como parte
de instalar dotfiles. El inventario es una fotografía, no un lockfile automático.

## Plugins retirados

El 2026-10-13 se desvinculó `herdr-tsk` (su fuente local ya no existía) y se
desinstalaron `ttt.editor`, `rcosteira.account-switch` y `herdr-agent-usage`.
También se borraron sus directorios de configuración y se detuvo el watcher
residual de Agent Usage. El registro y las acciones del servidor conservan solo
Heeler. No se borraron las CLI independientes `ttt`/`tsk`, cuentas, credenciales
ni la integración de Pi. El inventario publicado de dotfiles refleja este estado;
publicarlo no desinstala plugins automáticamente en otras máquinas.
