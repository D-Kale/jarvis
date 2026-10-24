from pathlib import Path
import os

def found_file(file_name, search_path=None):
    """
    Permite al agente buscar un archivo pidiendo el nombre (file_name obligatorio) y permitiendole
    acercarse a la ruta por medio de una search_path (opcional). Si no se encuentra el archivo, devuelve un
    mensaje de error (Para que el agente sepa que no se encontró el archivo). Si se encuentra, devuelve la ruta
    completa del archivo, el tipo de archivo y el tamaño del archivo en bytes.
    """
    if not file_name:
        return "Nombre de archivo obligatorio."

    if not search_path:
        search_path = Path.home()

    for root, _, files in os.walk(search_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            file_type = os.path.splitext(file_name)[1]
            file_size = os.path.getsize(file_path)
            return f"Archivo encontrado: '{file_path}', Tipo: {file_type}, Tamaño: {file_size} bytes"
    return f"Archivo '{file_name}' no encontrado."

def list_files(directory_path):
    """
    Permite al agente listar todos los archivos en un directorio dado su ruta completa (directory_path obligatorio).
    Si el directorio no existe, devuelve un mensaje de error. Si el directorio existe, devuelve una lista de archivos
    en el directorio.
    """
    if not os.path.isdir(directory_path):
        return f"Directorio '{directory_path}' no encontrado."
    
    files = os.listdir(directory_path)
    if not files:
        return f"No hay archivos en el directorio '{directory_path}'."
    
    return f"Archivos en '{directory_path}': {', '.join(files)}"

def read_file(file_path):
    """
    Permite al agente leer un archivo dado su ruta completa (file_path obligatorio). Si el archivo no existe,
    devuelve un mensaje de error. Si el archivo existe, devuelve el contenido del archivo.
    """
    if not os.path.isfile(file_path):
        return f"Archivo '{file_path}' no encontrado."

    file_size = os.path.getsize(file_path)

    if file_size > 100 * 1024 * 1024:  # 100 MB
        return f"Archivo '{file_path}' demasiado grande para leer (más de 100 MB)."
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        return f"Error: '{file_path}' es un archivo binario o no usa codificación UTF-8."
    except PermissionError:
        return f"Error: Permiso denegado para leer '{file_path}'."
    except Exception as e:
        return f"Error inesperado al leer el archivo: {str(e)}"

def write_txt_file(file_path=None, content=None):
    """
    Permite al agente escribir en un archivo dado su ruta completa (file_path obligatorio) y el contenido a escribir
    (content obligatorio). Si el archivo no existe, lo crea y escribe el contenido. Si el archivo existe, sobrescribe
    el contenido existente con el nuevo contenido.
    """
    if not file_path:
        file_path = os.path.join(os.getcwd(), "jarvis_output.txt")

    if not content:
        return "Contenido obligatorio."

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return f"Contenido escrito en '{file_path}' exitosamente."

def delete_file(file_path):
    """
    Permite al agente eliminar un archivo dado su ruta completa (file_path obligatorio). Si el archivo no existe,
    devuelve un mensaje de error. Si el archivo existe, lo elimina y devuelve un mensaje de confirmación.
    """
    if not os.path.isfile(file_path):
        return f"Archivo '{file_path}' no encontrado."
    
    os.remove(file_path)
    return f"Archivo '{file_path}' eliminado exitosamente."