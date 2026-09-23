# Guía paso a paso — Git y GitHub desde cero

Esta guía explica los conceptos básicos y termina con un ejercicio en GitHub. Todo se hace desde el navegador: no necesitás instalar programas ni usar la terminal. Preparada el **22 de septiembre de 2026**. Los nombres o posiciones de algunas opciones pueden variar según la interfaz.

## Objetivo

Al terminar deberías tener:

- Una cuenta personal de GitHub.
- Un repositorio propio con un archivo de presentación.
- Dos cambios guardados como commits.
- Una primera experiencia consultando el historial de un archivo.

Tiempo estimado: 10–15 minutos.

## 1. Entender qué es Git y qué es GitHub

**Git** es una herramienta de control de versiones: registra los cambios de los archivos de un proyecto. Permite consultar versiones anteriores, comparar modificaciones y trabajar con otras personas.

Por ejemplo, en lugar de tener `trabajo_final`, `trabajo_final_2` y `trabajo_final_ahora_si`, podés mantener un archivo y guardar su evolución con Git.

**GitHub** es una plataforma web donde podés alojar proyectos que usan Git, compartirlos y colaborar. Git también puede usarse en tu computadora sin GitHub.

En este ejercicio, GitHub permite hacer los cambios y guardarlos en Git directamente desde su página web.

Documentación oficial: [acerca de Git](https://docs.github.com/es/get-started/using-git/about-git).

## 2. Reconocer las palabras básicas

| Término | Qué significa |
|---|---|
| **Repositorio** | Un proyecto con sus archivos y su historial de cambios. |
| **Commit** | Un punto de guardado en el historial, acompañado de un mensaje que explica el cambio. |
| **README.md** | Un archivo de texto que presenta el proyecto. GitHub lo muestra en la página principal del repositorio. |
| **Markdown** | El formato usado en archivos `.md` para escribir títulos, listas y otros elementos con texto sencillo. |
| **Rama / branch** | Una línea de trabajo dentro del repositorio. En este ejercicio usaremos la rama principal, llamada `main`. |

El recorrido que vas a practicar es: **editar un archivo → guardar un commit → consultar el historial**.

## 3. Crear la cuenta y el repositorio

1. Entrá a [GitHub](https://github.com) y creá una cuenta con **Sign up**, o ingresá con **Sign in** si ya tenés una.
2. Completá la verificación de la cuenta si se solicita.
3. En el menú **+**, seleccioná **New repository**.
4. En **Repository name**, escribí `mi-primer-proyecto`.
5. Elegí **Private** para que el repositorio sea privado.
6. Activá la opción **Add a README file** o **Add README**.
7. Dejá las demás opciones con sus valores predeterminados y seleccioná **Create repository**.

Deberías ver la página de tu proyecto y un archivo llamado `README.md`.

## 4. Ejercicio — escribir una presentación

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

## 5. Hacer un segundo cambio

1. Volvé a abrir `README.md` y seleccioná el lápiz.
2. Agregá al final:

   ```markdown
   ## Mi primer avance

   Hoy creé un repositorio y guardé mi primer commit.
   ```

3. Guardá el cambio con **Commit changes**, directamente en `main`.
4. Usá el mensaje `Agrego mi primer avance` y confirmá.

Ahora el archivo contiene tu presentación y tu avance. Ambos cambios quedaron registrados por separado.

## 6. Consultar el historial

1. Abrí `README.md` desde la pestaña **Code** del repositorio.
2. Buscá la opción **History** en la vista del archivo.
3. Identificá los mensajes `Agrego mi presentación` y `Agrego mi primer avance`.
4. Abrí el commit `Agrego mi primer avance` para ver las líneas agregadas.

También vas a encontrar un commit inicial, creado al generar el repositorio con el README. Es normal: deberías tener ese commit más los dos que hiciste durante el ejercicio.

**Desafío breve:** cambiá el objetivo de tu presentación, guardá otro commit con un mensaje descriptivo y encontrá esa modificación en el historial.

Documentación oficial para ampliar la práctica: [Hola mundo en GitHub](https://docs.github.com/es/get-started/using-github/hello-world).

## 7. Relación con las prácticas de Databricks

El repositorio de la materia contiene las guías y los notebooks que vamos a usar. Tu repositorio `mi-primer-proyecto` es un espacio independiente para practicar.

Cuando la guía de Databricks te pida **clonar** el repositorio de la materia, significa crear una copia de ese proyecto y su historial dentro de tu workspace. Seguí la URL indicada allí; para ese paso no uses el repositorio personal de este ejercicio.

Continuá con la [guía paso a paso de Databricks Free Edition](GUIA_SETUP_DATABRICKS_FREE.md).

## 8. Solución de problemas

### No aparece el lápiz para editar

Confirmá que iniciaste sesión y estás en tu propio repositorio. En un repositorio ajeno puede que no tengas permiso para editar directamente.

### No encuentro el README

Si no lo agregaste al crear el repositorio, usá la opción para crear un archivo nuevo —puede aparecer como **creating a new file** o **Add file → Create new file**— y llamalo `README.md`.

### Escribí el texto, pero no aparece en el proyecto

Completá el diálogo de **Commit changes**. Escribir en el editor o mirar la vista previa no guarda un commit por sí solo.

## Checklist final

- [ ] Puedo explicar la diferencia entre Git y GitHub.
- [ ] Creé mi repositorio `mi-primer-proyecto`.
- [ ] El README muestra mi presentación y mi objetivo.
- [ ] Guardé los dos commits del ejercicio con mensajes descriptivos.
- [ ] Encontré ambos cambios en el historial.
- [ ] Entiendo que el repositorio de la materia es distinto de mi repositorio de práctica.
