
from tools.files import found_file, list_files, read_file, write_txt_file, delete_file

TOOL_DISPATCH = {
    "found_file": found_file,
    "list_files": list_files,
    "read_file": read_file,
    "write_txt_file": write_txt_file,
    "delete_file": delete_file,
}


def ejecutar_tool(nombre_tool, argumentos):
    """Ejecuta una tool por nombre y devuelve su resultado."""
    if nombre_tool not in TOOL_DISPATCH:
        return {"ok": False, "error": f"Tool no encontrada: {nombre_tool}"}

    try:
        return TOOL_DISPATCH[nombre_tool](**argumentos)
    except Exception as e:
        return {"ok": False, "error": str(e), "tool": nombre_tool, "argumentos": argumentos}