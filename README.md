# Jarvis: un laboratorio para aprender cómo funciona un agente de IA

Jarvis es un asistente experimental de terminal, escrito en Python, para aprender construyendo. Conecta un modelo de Gemini con herramientas que buscan, listan, leen, escriben y eliminan archivos. El proyecto está creciendo paso a paso: hoy explora especialmente el *tool calling* y el ciclo que permite a un modelo pedir una acción y continuar la conversación con su resultado.

> **Importante:** Jarvis se ejecuta en tu equipo, pero el modelo se consulta a través de la API de Google. No es un modelo de IA ejecutándose localmente.

## Qué hace hoy

- Mantiene una conversación en la terminal y conserva el historial durante la sesión.
- Envía cada solicitud a Gemini con una instrucción de sistema y definiciones de herramientas.
- Cuando Gemini solicita una herramienta, Jarvis despacha la llamada en Python, devuelve el resultado al modelo y continúa el ciclo.
- Limita el ciclo a cinco pasos por solicitud y reintenta errores de API hasta tres veces, con esperas crecientes.
- Muestra la conversación con formato Markdown y usa Rich para la interfaz de terminal.

### Flujo de una solicitud

```text
Usuario
  → main.py: captura el mensaje y conserva el historial
  → jarvis.py: envía mensaje, historial y herramientas a Gemini
  → Gemini: responde o solicita una herramienta
  → tools/tools.py: despacha la función local
  → tools/files.py: opera sobre archivos y devuelve el resultado
  → jarvis.py: comparte el resultado con Gemini y obtiene la respuesta final
  → main.py: muestra la respuesta
```

## Requisitos

- Python 3.14 o superior, según `pyproject.toml`.
- Una clave de API de Google AI Studio con acceso al modelo configurado.
- [uv](https://docs.astral.sh/uv/) para instalar las dependencias declaradas en `uv.lock`.

## Empezar

1. Clona el repositorio y entra en su directorio:

   ```bash
   git clone https://github.com/D-Kale/jarvis.git
   cd Jarvis
   ```

2. Instala las dependencias:

   ```bash
   uv sync
   ```

3. Crea un archivo `.env` en la raíz y agrega tu clave:

   ```dotenv
   API_KEY=tu_clave_de_google
   ```

   El proyecto carga esta variable con `python-dotenv`. `.env` está excluido de Git; no compartas ni publiques tu clave.

4. Inicia Jarvis:

   ```bash
   uv run python main.py
   ```

   Escribe `salir`, `exit` o `quit` para terminar. También puedes interrumpir con `Ctrl+C`.

## Herramientas disponibles

| Herramienta | Qué permite hacer |
|---|---|
| `found_file` | Buscar un nombre de archivo; si no se indica ruta, comienza en el directorio personal. |
| `list_files` | Listar las entradas de un directorio. |
| `read_file` | Leer texto UTF-8 de un archivo de hasta 100 MB. |
| `write_txt_file` | Crear o sobrescribir un archivo de texto. Si no se indica ruta, usa `jarvis_output.txt` en el directorio actual. |
| `delete_file` | Eliminar un archivo existente. |

Las descripciones y parámetros que el modelo ve están en `tools/index.py`; la correspondencia entre nombres y funciones está en `tools/tools.py`; las operaciones de archivos están en `tools/files.py`.

## Arquitectura del proyecto

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Interfaz de terminal, captura de entrada, historial y presentación de respuestas. |
| `jarvis.py` | Configuración del cliente de Gemini, instrucciones del sistema, conversación, llamadas a herramientas y reintentos. |
| `tools/index.py` | Declaraciones de herramientas que se envían al modelo. |
| `tools/tools.py` | Despachador que resuelve el nombre de la herramienta y ejecuta la función correspondiente. |
| `tools/files.py` | Búsqueda, listado, lectura, escritura y borrado de archivos. |
| `tools/system.py` | Recopila información del sistema para el contexto del asistente. |
| `pyproject.toml` y `uv.lock` | Dependencias y configuración del proyecto. |

## Seguridad y privacidad

Jarvis es un proyecto de aprendizaje, no una herramienta segura para operar sobre datos importantes:

- Las herramientas de archivos actúan con los permisos del usuario que ejecuta el programa. No hay una carpeta raíz restringida ni confirmación humana antes de escribir o borrar.
- El modelo puede proponer llamadas a herramientas. Revisa con cuidado lo que le pides y no lo uses en directorios con datos valiosos.
- El contenido leído y los resultados de herramientas pueden enviarse a Gemini para continuar la conversación. Evita archivos con credenciales, información personal o datos confidenciales.
- El contexto inicial incluye el nombre de usuario y detalles del sistema operativo. `tools/system.py` también recopila otra información del equipo.
- La aplicación depende de `API_KEY`; mantenla solo en tu `.env` local y rótala si alguna vez se expone.

## Lo que estoy aprendiendo

Soy desarrollador backend y estoy usando Jarvis para entender mejor cómo se construyen los sistemas con IA. Hasta ahora he aprendido sobre *tooling* y sigo aprendiendo y mejorando el proyecto poco a poco. La idea es que cada avance convierta un concepto en una pieza observable del sistema:

1. **Interfaz y configuración:** recibir mensajes, cargar dependencias y manejar la clave de API.
2. **Contexto conversacional:** conservar el historial entre turnos y definir instrucciones para el modelo.
3. **Tool calling:** describir herramientas, interpretar una solicitud del modelo y conectar sus argumentos con funciones Python.
4. **Ciclo del agente:** devolver los resultados de las herramientas al modelo, limitar pasos y manejar errores transitorios.
5. **Próximos pasos de aprendizaje:** agregar pruebas, validar argumentos y permisos, pedir confirmación para acciones destructivas, mejorar los errores y registrar el flujo para poder observarlo.

La última lista es una ruta posible de mejora, no una afirmación de que esas protecciones o pruebas ya estén implementadas.

## Limitaciones actuales

- El modelo configurado en `jarvis.py` es `gemini-3.5-flash-lite`; puedes cambiarlo allí según los modelos disponibles para tu cuenta y API.
- Las operaciones de archivos son locales y no tienen un límite de directorio permitido.
- No hay confirmación antes de sobrescribir o eliminar un archivo.
- No se incluyen pruebas automatizadas todavía.
- `groq` aparece como dependencia, pero no se utiliza en el flujo actual.

## Para seguir explorando

Un buen siguiente ejercicio es agregar una prueba unitaria al despachador y luego diseñar una política que impida que las herramientas salgan de una carpeta de trabajo elegida. Así puedes experimentar con el ciclo de herramientas sin perder de vista que cada llamada del modelo puede producir efectos reales en el equipo.
