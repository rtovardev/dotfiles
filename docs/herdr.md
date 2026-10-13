# Herdr + Pi

Herdr organiza los workspaces y paneles persistentes para el trabajo de código.
Pi es el harness principal y Ghostty es la única terminal del flujo.
Las versiones y el estado observado están en el [README](../README.md).

## Configuración versionada

El instalador enlaza archivos concretos, con respaldo del archivo anterior:

| Fuente | Destino |
|---|---|
| [herdr/config.toml](../herdr/config.toml) | `~/.config/herdr/config.toml` |
| [herdr/bar.json](../herdr/bar.json) | `~/.config/herdr/plugins/config/herdr-bar/config.json` |
| [herdr/auto-title.env](../herdr/auto-title.env) | `~/.config/herdr-auto-title/config.env` |

Herdr conserva `onboarding = false`, los atajos de Bar y una segunda fila `$topic`
en la sidebar. **Auto Title es el único escritor de etiquetas**; Bar conserva la
vista previa e iconos automáticos con `auto_titles = false` y `tab_status = false`.
No se enlaza todo el directorio ni se restaura el perfil antiguo.

`HERDR_CONFIG_PATH` permite usar otro archivo: si lo defines, comprueba esa ruta
antes de asumir que Herdr lee el archivo enlazado.

Quedan fuera de Git el registro `plugins.json`, checkouts de plugins, configuraciones
privadas, cuentas, tokens, dispositivos emparejados, sesiones, snapshots, sockets,
logs y backups. Las excepciones públicas son los ajustes de Bar, Auto Title y el
parche de Bar conservado con pruebas. `manual-names.json` es estado local privado.
Los datos y paquetes de Pi también permanecen fuera de dotfiles.

## Flujo principal

```sh
cd /ruta/al/proyecto
herdr
# Dentro del panel del proyecto:
pi
```

Herdr y Pi se instalan por separado. El instalador de dotfiles no instala plugins,
aplica parches, activa watchers ni modifica integraciones. La integración Pi
existente de Herdr se conserva: detecta el agente, su estado y su sesión activa.
Esa integración es distinta de los plugins Heeler y Bar.

## Bar: navegación, iconos y estados

[herdr-bar](https://github.com/jeffarese/herdr-bar) 0.7.3 requiere Herdr 0.9+ y
Python 3.9+, sin dependencias Python adicionales. Se comprobó con Herdr 0.9.3,
Python 3.9 y 3.14 en macOS. Linux no se verificó.

- **Cmd+K** en Ghostty envía Ctrl+Alt+K a Herdr; reemplaza limpiar scrollback.
- **Ctrl+B, K** también abre Bar con el prefijo por defecto de Herdr.
- El popup permite buscar y saltar entre pestañas, paneles y agentes; Enter
  selecciona y Esc cierra. Ctrl+O alterna la vista previa.
- Bar conserva navegación, vista previa, logos y los estados de agentes en el
  popup. Su watcher de títulos y prefijos de estado está detenido para no competir
  con Auto Title. El estado nativo sigue visible en Herdr/sidebar.
- Los logos requieren la fuente **Herdr Agent Icons Max**, instalada aparte.
  Ghostty la usa como fallback de `U+E1A0–U+E1B7`; se conserva Meslo como fuente
  principal. La fuente está instalada localmente, pero dotfiles no la instala.

Recarga Ghostty con **Cmd+Shift+,** para aplicar el atajo y el fallback de fuente.
**Es necesario recargar la ventana ya abierta:** cambiar el archivo o validar su
sintaxis no carga el nuevo binding en esa ventana. Después, pulsa **Cmd+K** dentro
de Herdr y comprueba que aparece Bar. El 2026-10-13 Ricardo confirmó esa apertura
tras la recarga; antes, Cmd+K no hacía nada. No fue necesario cambiar la secuencia
ni reiniciar Herdr o Pi.

Después de aplicar los enlaces, la recarga explícita de Herdr es:

```sh
herdr server reload-config
```

## Auto Title: etiquetas y topic

[herdr-auto-title](https://github.com/kryptamine/herdr-auto-title) **0.13.2** se
instaló y verificó el 2026-10-13, fijado al commit
`8b2504514bb2aaa79ecbba6cb0e6c426652f4419`. Requiere Herdr 0.9.2+ y Go para
compilar; el proceso instalado es un binario Go sin llamadas a modelos.

- Nombra **pestañas y paneles** desde agente, título terminal, proceso, cwd y Git.
- Publica **`$topic` en la sidebar** del workspace activo; **no renombra workspaces**.
- No cambia nombres de sesiones de Pi, no lee sus JSONL ni genera resúmenes de tareas.
  El lector de transcripciones Claude está desactivado en este setup.
- Configuración: posición visible, agente habilitado, paneles y topic activos,
  máximo 50 caracteres, rama máximo 12 y sondeo de 500 ms. Se lee al arrancar.

### Instalación reproducible

Aplica primero los enlaces de dotfiles. Después instala el plugin explícitamente:

```sh
herdr plugin action invoke herdr-bar.stop-titles
herdr plugin install kryptamine/herdr-auto-title --ref 8b2504514bb2aaa79ecbba6cb0e6c426652f4419
herdr server reload-config
herdr plugin action invoke herdr.auto-title.restart
```

La instalación ejecuta el build del plugin y lo habilita; no es un efecto del
instalador de dotfiles. Para aplicar futuros cambios en `config.env`, ejecuta
la acción `herdr.auto-title.restart` o **Ctrl+B, Shift+R** (prefijo por defecto).
Actualiza solo tras revisar una versión/commit nuevo y reinicia el daemon después.
Bar 0.7.3 también tiene una protección nativa que cede a Auto Title; aquí además
se desactivaron sus dos escritores y se detuvo el watcher deliberadamente.

### Nombres manuales y límites

Renombrar una pestaña o panel **con Auto Title ya activo** lo protege de siguientes
sondeos y reinicios. Borrar su nombre devuelve el control al plugin:

```sh
herdr tab rename <TAB_ID> ""
herdr pane rename <PANE_ID> --clear
```

**El primer sondeo no protege nombres previos**: respalda las etiquetas antes de
la primera instalación y vuelve a aplicar las manuales cuando el daemon ya esté
activo. En esta Mac se restauraron y verificaron tres etiquetas manuales, incluidas
las de MSI, y permanecieron tras reiniciar Auto Title. Los IDs y etiquetas concretas
quedan en el respaldo privado, no en este repo.

Los bloqueos viven en `~/Library/Application Support/herdr-auto-title/manual-names.json`
en esta Mac; en Linux usa la ruta XDG. No edites ese archivo mientras corre el
plugin. Un renombrado realizado con el daemon parado puede no conservarse.

Verificación real: mismo número e IDs de workspaces/pestañas/paneles, workspaces sin
renombrar, etiquetas automáticas actualizadas, `$topic` publicado y nombres manuales
retenidos tras restart. `go test ./...` pasó en el checkout instalado. La sidebar
está configurada y su token confirmado por API; eso no certifica su apariencia en
una ventana que todavía no haya recargado.

## Títulos de Pi

**En el setup vigente Auto Title no refleja `/name` ni resume conversaciones de Pi**:
sus etiquetas muestran contexto terminal/proceso/proyecto, no el tema semántico de
la sesión. `/name Mi tarea` y `pi --name "Mi tarea"` siguen siendo comandos de Pi,
pero no fuerzan el nombre de una pestaña con Auto Title.

### Parche de Bar conservado, inactivo

Antes de Auto Title, se utilizaba Bar para reflejar nombres manuales de Pi. El
parche se conserva como alternativa, no como segundo renombrador. La versión
upstream 0.7.3 no incluye Pi en sus candidatos de renombrado. El
[parche local](../herdr/patches/pi-session-titles.patch) añade ese soporte:

1. Lee la ruta JSONL exacta que Herdr publica como `agent_session` de Pi.
2. Reutiliza el último `session_info.name`, sin leer prompts como títulos ni
   ejecutar llamadas al modelo desde Bar.
3. Conserva las protecciones de nombres manuales, conflictos y cambios de sesión;
   funciona con el mismo watcher de estados. No modifica la integración oficial.

**En esa alternativa**, los nombres de Pi se definen manualmente con su comando nativo:

```text
/name Mi tarea
```

También puedes iniciar Pi con `pi --name "Mi tarea"`. El parche de Bar recoge
el nombre guardado en `session_info.name`; no necesita un plugin generador.
`auto_titles = true` permitiría ese reflejo y los títulos upstream de otros agentes,
pero no significa que se generen nombres de Pi. **Hoy ambas opciones están en false**.
No actives este watcher mientras Auto Title esté habilitado. Las 415 pruebas de Bar
validan el lector y la convivencia con estados del setup anterior.

El **2026-10-13**, por decisión de Ricardo, se desinstaló
`npm:@zhushanwen/pi-rename-session` 0.11.1 y se eliminó su configuración externa
`~/.pi/agent/config/rename-session-ext-config.json`. No se intentó repararlo ni
se instaló otro renombrador. Las sesiones y sus nombres existentes se conservan.
Reinicia Pi o ejecuta `/reload` en las sesiones ya abiertas para descargar la
extensión que todavía puedan tener en memoria; las sesiones nuevas no la cargan.

La decisión sigue a una prueba real en una sesión nueva mediante Herdr CLI,
sin `/name`: Pi respondió correctamente, pero no escribió `session_info.name`
y Bar conservó el título numérico. El diagnóstico mostró
`[rename-session] ... skip: no user prompt`: `pi-topping` guarda la pregunta como
`custom_message` de tipo `pi-topping-prompt`, mientras el renombrador solo lee
`message` con `role: "user"`. Se prefirió retirar esta dependencia incompatible
a mantenerla habilitada sin funcionar.

### Conservar y reaplicar el parche

El parche se limita al commit upstream registrado, no es una función oficial ni
se aplica automáticamente al instalar dotfiles. Obtén `plugin_root` de:

```sh
herdr plugin list --json
```

Desde dotfiles, revisa primero y aplica después usando la ruta de ese registro:

```sh
python3 scripts/patch-herdr-bar.py --plugin-root /ruta/al/plugin
python3 scripts/patch-herdr-bar.py --plugin-root /ruta/al/plugin --apply
```

El script exige el commit correcto y un parche limpio, conserva cambios
incompatibles y es idempotente. No descarga código ni inicia watchers. El watcher
de Bar, cuando está activo, detecta cambios de código y se reemplaza automáticamente.
Para detenerlo, o iniciarlo solo tras deshabilitar Auto Title y habilitar las
opciones correspondientes de Bar:

```sh
herdr plugin action invoke herdr-bar.start-titles
herdr plugin action invoke herdr-bar.stop-titles
```

**Al actualizar/reinstalar Bar puede perderse el parche.** Si el upstream cambia,
revisa si ya admite Pi y adapta/prueba el parche antes de aplicarlo; el script
rechaza otros commits. Para deshacerlo, desde dotfiles y con el plugin correcto:

```sh
git -C /ruta/al/plugin apply --reverse --check "$PWD/herdr/patches/pi-session-titles.patch"
git -C /ruta/al/plugin apply --reverse "$PWD/herdr/patches/pi-session-titles.patch"
```

Pruebas del checkout del plugin (415 pruebas, incluidas 15 específicas de Pi):

```sh
cd /ruta/al/plugin
PYTHONPATH=src python3 -m unittest discover -s tests -t . -q
```

## Comprobar el estado sin cambiarlo

```sh
herdr --version
herdr status
herdr plugin list
herdr plugin action list
herdr plugin log list --limit 30
herdr integration status
```

`plugin list` muestra instalación y habilitación; `action list` muestra las
acciones del servidor. Un log `status: succeeded` con `exit_code: 0` acredita
ese comando, no todas las funciones del plugin. Estas consultas no cambian
cuentas ni abren paneles.

## Fuentes de los plugins registrados

| ID | Fuente instalada | Ref/commit registrado |
|---|---|---|
| `heeler` | `ZingerLittleBee/Heeler/plugin` | `749d11cc4011ff1a921eb83339a4f8b2bbe7f7a7` (desde `main`) |
| `herdr-bar` | `jeffarese/herdr-bar` | `e22455068e26340b6be02cec8a07707fc1f11ae1` (0.7.3 + parche Pi inactivo) |
| `herdr.auto-title` | `kryptamine/herdr-auto-title` | `8b2504514bb2aaa79ecbba6cb0e6c426652f4419` (0.13.2) |
| `mirror` | `nikok6/herdr-mirror` | `195398c1275f9f3d18ddff70282149005a2bec01` (0.4.3) |

Mirror apareció registrado y habilitado al comprobar este inventario; no se instaló,
modificó ni se probó su sincronización remota durante la retirada del renombrador.

Para instalar Bar de nuevo, revisa la fuente y aplica el parche por separado:

```sh
herdr plugin install jeffarese/herdr-bar --ref e22455068e26340b6be02cec8a07707fc1f11ae1
```

Descargar un plugin puede ejecutar pasos de build; no forma parte de instalar
dotfiles. El inventario es una fotografía, no un lockfile automático.

## Plugins retirados

El 2026-10-13 se desvinculó `herdr-tsk` y se desinstalaron `ttt.editor`,
`rcosteira.account-switch` y `herdr-agent-usage`, con sus configuraciones. Se
detuvo el watcher residual de Agent Usage. No se borraron las CLI independientes
`ttt`/`tsk`, cuentas, credenciales ni la integración de Pi. El inventario vigente
conserva **Heeler, Bar, Auto Title y Mirror**. El renombrador retirado `pi-rename-session`
era una extensión de Pi, no un plugin de Herdr. Publicar este inventario no
desinstala plugins automáticamente en otras máquinas.
