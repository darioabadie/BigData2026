# Guía paso a paso — Git y GitHub desde cero

Esta guía explica los conceptos básicos con dos ejercicios conectados. En la **Parte 1** trabajás desde la interfaz web de GitHub, sin instalar programas. En la **Parte 2** clonás ese mismo repositorio en tu computadora y practicás comandos de Git. Actualizada el **23 de septiembre de 2026**. Los nombres o posiciones de algunas opciones pueden variar según la interfaz.

## Objetivo

Al terminar deberías tener:

- Una cuenta personal de GitHub.
- Un repositorio propio con un archivo de presentación.
- Dos cambios guardados como commits.
- Una primera experiencia consultando el historial de un archivo.
- Una copia del repositorio en tu computadora.
- Un archivo nuevo publicado con `git add`, `git commit` y `git push`.

Tiempo estimado: 10–15 minutos para la Parte 1 y 15–20 minutos para la Parte 2, más la instalación de Git si hace falta.

## Parte 1 — Trabajar desde la interfaz web de GitHub

### 1. Entender qué es Git y qué es GitHub

**Git** es una herramienta de control de versiones: registra los cambios de los archivos de un proyecto. Permite consultar versiones anteriores, comparar modificaciones y trabajar con otras personas.

Por ejemplo, en lugar de tener `trabajo_final`, `trabajo_final_2` y `trabajo_final_ahora_si`, podés mantener un archivo y guardar su evolución con Git.

**GitHub** es una plataforma web donde podés alojar proyectos que usan Git, compartirlos y colaborar. Git también puede usarse en tu computadora sin GitHub.

En este ejercicio, GitHub permite hacer los cambios y guardarlos en Git directamente desde su página web.

Documentación oficial: [acerca de Git](https://docs.github.com/es/get-started/using-git/about-git).

### 2. Reconocer las palabras básicas

| Término | Qué significa |
|---|---|
| **Repositorio** | Un proyecto con sus archivos y su historial de cambios. |
| **Commit** | Un punto de guardado en el historial, acompañado de un mensaje que explica el cambio. |
| **README.md** | Un archivo de texto que presenta el proyecto. GitHub lo muestra en la página principal del repositorio. |
| **Markdown** | El formato usado en archivos `.md` para escribir títulos, listas y otros elementos con texto sencillo. |
| **Rama / branch** | Una línea de trabajo dentro del repositorio. En este ejercicio usaremos la rama principal, llamada `main`. |

El recorrido que vas a practicar es: **editar un archivo → guardar un commit → consultar el historial**.

### 3. Crear la cuenta y el repositorio

1. Entrá a [GitHub](https://github.com) y creá una cuenta con **Sign up**, o ingresá con **Sign in** si ya tenés una.
2. Completá la verificación de la cuenta si se solicita.
3. En el menú **+**, seleccioná **New repository**.
4. En **Repository name**, escribí `mi-primer-proyecto`.
5. Elegí **Public** para que el repositorio sea público. Antes de continuar, leé [qué implica que sea público](#qué-implica-que-el-repositorio-sea-público).
6. Activá la opción **Add a README file** o **Add README**.
7. Dejá las demás opciones con sus valores predeterminados y seleccioná **Create repository**.

Deberías ver la página de tu proyecto y un archivo llamado `README.md`.

#### Qué implica que el repositorio sea público

Usamos repositorios públicos porque las entregas de las prácticas se hacen en este mismo repositorio, y así el docente puede verlas sin que tengas que darle permisos. Eso tiene consecuencias que conviene conocer desde el principio:

- **Cualquier persona puede verlo.** No hace falta tener cuenta de GitHub ni conocerte: basta con la URL. Los buscadores también pueden indexarlo.
- **El historial también es público.** Se puede ver cada commit, no solo la versión actual de los archivos. Borrar un archivo en un commit nuevo no lo elimina de los commits anteriores.
- **Público no significa editable.** Solo vos (y las personas que invites como colaboradoras) pueden hacer commits. Los demás pueden leer, descargar o copiar el contenido.
- **Tus datos de autor quedan visibles.** Cada commit muestra el nombre y el correo configurados en Git. Por eso en la Parte 2 recomendamos usar la dirección `noreply` de GitHub.
- **Tus compañeros pueden ver tus resoluciones.** Cada entrega tiene que ser trabajo propio.

Nunca subas a este repositorio:

- Tokens, contraseñas ni claves, incluidos los tokens de acceso de Databricks.
- Datos personales tuyos o de otras personas: documento, teléfono, dirección.
- Datasets o archivos generados por las prácticas.

Si subiste una credencial por error, considerala comprometida aunque la borres enseguida: revocala o cambiala desde el servicio que la emitió y avisale al docente.

Podés cambiar la visibilidad más adelante desde **Settings → General → Danger Zone → Change repository visibility**, pero el repositorio tiene que seguir siendo público mientras se corrijan las entregas.

### 4. Ejercicio — escribir una presentación

1. Abrí `README.md`.
2. Seleccioná el ícono del lápiz para editarlo.
3. Reemplazá su contenido por el siguiente ejemplo, usando tu nombre o un alias:

   ```markdown
   # Mi primer proyecto

   Soy Ana y estoy aprendiendo a usar GitHub.

   ## Mi objetivo

   Quiero organizar mis trabajos de Big Data.
   ```

4. Si aparece la pestaña **Preview**, usala para ver el resultado. El símbolo `#` crea un título y `##` un subtítulo.
5. Seleccioná **Commit changes**.
6. En el mensaje del commit, escribí `Agrego mi presentación`.
7. Si aparece la elección de rama, seleccioná guardar directamente en `main`.
8. Confirmá con **Commit changes**.

Acabás de guardar tu primer cambio. El mensaje del commit ayuda a entender qué hiciste sin tener que abrir el archivo.

### 5. Hacer un segundo cambio

1. Volvé a abrir `README.md` y seleccioná el lápiz.
2. Agregá al final:

   ```markdown
   ## Mi primer avance

   Hoy creé un repositorio y guardé mi primer commit.
   ```

3. Guardá el cambio con **Commit changes**, directamente en `main`.
4. Usá el mensaje `Agrego mi primer avance` y confirmá.

Ahora el archivo contiene tu presentación y tu avance. Ambos cambios quedaron registrados por separado.

### 6. Consultar el historial

1. Abrí `README.md` desde la pestaña **Code** del repositorio.
2. Buscá la opción **History** en la vista del archivo.
3. Identificá los mensajes `Agrego mi presentación` y `Agrego mi primer avance`.
4. Abrí el commit `Agrego mi primer avance` para ver las líneas agregadas.

También vas a encontrar un commit inicial, creado al generar el repositorio con el README. Es normal: deberías tener ese commit más los dos que hiciste durante el ejercicio.

**Desafío breve:** cambiá el objetivo de tu presentación, guardá otro commit con un mensaje descriptivo y encontrá esa modificación en el historial.

Documentación oficial para ampliar la práctica: [Hola mundo en GitHub](https://docs.github.com/es/get-started/using-github/hello-world).

### 7. Relación con las prácticas de Databricks

El repositorio de la materia contiene las guías y los notebooks que vamos a usar. Tu repositorio `mi-primer-proyecto` es un espacio independiente para practicar.

Cuando la guía de Databricks te pida **clonar** el repositorio de la materia, significa crear una copia de ese proyecto y su historial dentro de tu workspace. Seguí la URL indicada allí; para ese paso no uses el repositorio personal de este ejercicio.

La [guía paso a paso de Databricks Free Edition](GUIA_SETUP_DATABRICKS_FREE.md) explica esa conexión. Antes, completá la Parte 2 para practicar Git en tu computadora.

### 8. Solución de problemas

#### No aparece el lápiz para editar

Confirmá que iniciaste sesión y estás en tu propio repositorio. En un repositorio ajeno puede que no tengas permiso para editar directamente.

#### No encuentro el README

Si no lo agregaste al crear el repositorio, usá la opción para crear un archivo nuevo —puede aparecer como **creating a new file** o **Add file → Create new file**— y llamalo `README.md`.

#### Escribí el texto, pero no aparece en el proyecto

Completá el diálogo de **Commit changes**. Escribir en el editor o mirar la vista previa no guarda un commit por sí solo.

### Checklist de la Parte 1

- [ ] Puedo explicar la diferencia entre Git y GitHub.
- [ ] Creé mi repositorio público `mi-primer-proyecto`.
- [ ] Sé qué información no debo subir a un repositorio público.
- [ ] El README muestra mi presentación y mi objetivo.
- [ ] Guardé los dos commits del ejercicio con mensajes descriptivos.
- [ ] Encontré ambos cambios en el historial.
- [ ] Entiendo que el repositorio de la materia es distinto de mi repositorio de práctica.

## Parte 2 — Trabajar desde tu computadora con Git

Vas a usar **el mismo repositorio `mi-primer-proyecto` que creaste en la Parte 1**. El objetivo es agregar un archivo llamado `aprendizajes.md` desde tu computadora y publicarlo en GitHub.

### 1. Preparar Git y la terminal

1. Instalá Git desde la [página oficial de descargas](https://git-scm.com/downloads), siguiendo las instrucciones para tu sistema operativo.
2. En Windows, usá Git for Windows y conservá la opción **Git Credential Manager** durante la instalación: permite iniciar sesión en GitHub desde el navegador cuando Git lo solicita.
3. Abrí **Git Bash** en Windows o **Terminal** en macOS/Linux.
4. Comprobá que Git esté disponible:

   ```bash
   git --version
   ```

Deberías ver una respuesta como `git version 2.x.x`. La versión exacta puede ser distinta.

> Ejecutá los comandos de esta parte de a uno. Los ejemplos usan Git Bash o Terminal.

### 2. Clonar tu repositorio

**Clonar** significa descargar una copia del proyecto junto con su historial. Git también recuerda de qué repositorio de GitHub proviene esa copia.

En GitHub, abrí tu repositorio y copiá su dirección desde **Code → HTTPS**. Debería ser similar a `https://github.com/TU-USUARIO/mi-primer-proyecto.git`.

En la terminal, creá una carpeta para esta práctica fuera de otros repositorios:

```bash
cd ~
mkdir practica-git
cd practica-git
```

Si `practica-git` ya existe, omití `mkdir` y entrá con `cd practica-git`.

Ahora ejecutá lo siguiente, reemplazando `TU-USUARIO` por tu usuario real de GitHub o usando la URL que copiaste:

```bash
git clone https://github.com/TU-USUARIO/mi-primer-proyecto.git
cd mi-primer-proyecto
git status
```

Como el repositorio es público, el clonado no pide credenciales. Git te va a pedir iniciar sesión recién al publicar cambios con `git push` (paso 7). Si se abre el navegador mediante Git Credential Manager, ingresá con la cuenta que creó el repositorio y completá la autorización.

En macOS/Linux, si todavía no tenés un método de autenticación configurado, hacelo ahora siguiendo la [guía oficial de Git Credential Manager](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git). GitHub no acepta la contraseña de tu cuenta como contraseña de Git por HTTPS; si aparece ese pedido en la terminal, configurá el gestor de credenciales antes de continuar.

Deberías estar en la rama `main`, con un estado similar a `nothing to commit, working tree clean`: todavía no hiciste cambios locales. Tu copia ya contiene el README de la Parte 1.

### 3. Configurar el autor de tus commits

Dentro de `mi-primer-proyecto`, ejecutá estos comandos reemplazando los datos del ejemplo:

```bash
git config user.name "Ana Perez"
git config user.email "tu-correo@example.com"
```

Como tu repositorio es público, este correo va a quedar visible en cada commit. Recomendamos usar tu dirección privada `noreply`, que figura en **Settings → Emails** de GitHub; también podés usar otro correo asociado a tu cuenta. Esta configuración identifica al autor de los commits en este repositorio; no inicia sesión en GitHub.

### 4. Crear un archivo Markdown

Desde la misma terminal, creá el archivo:

```bash
echo "# Mis aprendizajes de Git" > aprendizajes.md
echo "" >> aprendizajes.md
echo "Aprendi a clonar un repositorio en mi computadora." >> aprendizajes.md
```

El primer comando crea el archivo con un título; los siguientes agregan una línea vacía y una frase. Usá un nombre nuevo: `>` reemplaza el contenido si el archivo ya existe.

Revisá su contenido y el estado del repositorio:

```bash
cat aprendizajes.md
git status
```

Deberías ver `aprendizajes.md` bajo **Untracked files**: el archivo existe, pero Git todavía no lo incorporó a un commit.

### 5. Preparar el archivo con `git add`

```bash
git add aprendizajes.md
git status
```

Ahora debería aparecer bajo **Changes to be committed**, como un archivo nuevo (`new file`).

**`git add` prepara el contenido que querés incluir en el próximo commit.** Todavía no lo guarda en el historial ni lo sube a GitHub. Si modificás el archivo después de prepararlo, ejecutá `git add` nuevamente para incluir la nueva versión.

### 6. Guardar el cambio con `git commit`

```bash
git commit -m "Agrego mis aprendizajes de Git"
```

**`git commit` guarda lo preparado en el historial de tu copia local.** La opción `-m` permite escribir el mensaje del commit.

Comprobá el resultado:

```bash
git log -1 --oneline
git status
```

El primer comando muestra tu último commit. El segundo debería indicar que no hay cambios pendientes y que tu rama está un commit por delante de `origin/main`. Eso significa que el cambio está guardado en tu computadora y falta enviarlo a GitHub.

### 7. Publicar el cambio con `git push`

```bash
git push origin main
```

**`git push` envía tus commits locales a GitHub.** En este comando, `origin` es el nombre que Git asignó al repositorio remoto al clonarlo y `main` es la rama que estás publicando.

Si Git pide autenticación, usá la cuenta que creó el repositorio. Esperá a que el comando termine sin errores.

Para comprobar el resultado, actualizá la página del repositorio en GitHub: debería aparecer `aprendizajes.md` con su contenido y el mensaje `Agrego mis aprendizajes de Git`.

### 8. Repetir el ciclo con un cambio pequeño

Agregá una frase más y repetí los tres comandos principales:

```bash
echo "Ya practique add, commit y push." >> aprendizajes.md
git add aprendizajes.md
git commit -m "Registro mi primera practica de comandos"
git push origin main
```

Actualizá GitHub para comprobar que la frase nueva está publicada.

| Comando | Qué hace | Dónde ocurre |
|---|---|---|
| `git clone URL` | Obtiene una copia del repositorio y su historial. | De GitHub a tu computadora. |
| `git status` | Muestra el estado de tus cambios. | En tu computadora. |
| `git add aprendizajes.md` | Prepara el contenido del archivo para el próximo commit. | En tu computadora. |
| `git commit -m "Mensaje"` | Guarda los cambios preparados en el historial. | En tu computadora. |
| `git push origin main` | Envía los commits al repositorio remoto. | De tu computadora a GitHub. |

### 9. Solución de problemas

#### Git no se reconoce como comando

Comprobá la instalación y cerrá y volvé a abrir la terminal. En Windows, abrí **Git Bash**.

#### Aparece `not a git repository`

La terminal no está dentro del repositorio. Entrá con `cd ~/practica-git/mi-primer-proyecto` y volvé a ejecutar `git status`.

#### El commit pide nombre y correo

Completá la configuración del paso 3 y repetí `git commit`.

#### Aparece `nothing to commit`

Revisá `git status`: puede que el cambio ya esté guardado o que todavía no hayas preparado el archivo con `git add`. Si ya hiciste el commit, continuá con `git push origin main`.

#### El clonado o el push falla por permisos

Verificá que la URL sea la de tu repositorio personal y que estés autenticado con la cuenta que lo creó. Revisá el método de autenticación del paso 2.

#### El push se rechaza porque hay cambios nuevos en GitHub

Puede ocurrir si editaste el repositorio desde la web después de clonarlo. Con tus cambios locales ya guardados en un commit y sin archivos pendientes en `git status`, ejecutá:

```bash
git pull --rebase origin main
git push origin main
```

El primer comando trae los cambios remotos y vuelve a aplicar tus commits encima. Si informa un conflicto, detenete y pedí ayuda al docente antes de seguir con el push.

### Checklist de la Parte 2

- [ ] Cloné mi repositorio personal en la computadora.
- [ ] Configuré el nombre y el correo para mis commits.
- [ ] Creé `aprendizajes.md` dentro del repositorio.
- [ ] Preparé el archivo con `git add`.
- [ ] Guardé un commit local con `git commit`.
- [ ] Publiqué el commit con `git push` y vi el archivo en GitHub.
- [ ] Repetí el ciclo agregando una frase.
- [ ] Puedo explicar la diferencia entre preparar, guardar y publicar un cambio.
