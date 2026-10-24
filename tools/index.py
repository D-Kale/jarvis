TOOLS = [
    {
        "type": "function",
        
        "function": {
            "name": "found_file",
            "description": "Busca un archivo en el sistema de archivos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_path": {"type": "string", "description": "Ruta del archivo a buscar."},
                    "file_name": {"type": "string", "description": "Nombre del archivo a buscar."}
                },
                "required": ["file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lista los archivos de una ruta especifica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {"type": "string", "description": "Ruta del directorio a explorar."},
                },
                "required": ["directory_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lee el contenido de un archivo especifico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Ruta del archivo a leer."},
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_txt_file",
            "description": "Escribe un archivo con contenido especificado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Ruta del archivo a escribir."},
                    "content": {"type": "string", "description": "contenido del archivo a escribir."},
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Elimina un archivo que sea solicitado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Ruta del archivo a eliminar."}
                },
                "required": ["file_path"]
            }
        }
    },
]
