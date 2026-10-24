import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

# Importamos la función de conversación desde tu archivo jarvis.py
from jarvis import jarvis

console = Console()

def main():
    console.clear()
    
    # Encabezado principal
    console.print(
        Panel.fit(
            "[bold cyan]🤖 JARVIS AI - Asistente Virtual Local[/bold cyan]\n"
            "[dim]Escribe '[bold red]salir[/bold red]' para terminar la sesión.[/dim]",
            border_style="cyan",
            padding=(1, 4)
        )
    )

    historial = None

    while True:
        try:
            # Captura de entrada del usuario
            usuario = Prompt.ask("\n[bold green]Tú[/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold cyan]Jarvis:[/bold cyan] Hasta luego, señor.")
            sys.exit(0)

        if not usuario:
            continue

        if usuario.lower() in ["salir", "exit", "quit"]:
            console.print("[bold cyan]Jarvis:[/bold cyan] Desconectando sistemas. Hasta luego.")
            break

        # Indicador visual de procesamiento mientras ejecuta tools o genera respuesta
        with console.status("[bold yellow]Procesando solicitud...[/bold yellow]", spinner="dots"):
            respuesta, historial = jarvis(usuario, historial=historial, verbose=True)

        # Mostrar respuesta formateada con Markdown
        console.print("\n[bold cyan]Jarvis:[/bold cyan]")
        console.print(
            Panel(
                Markdown(respuesta),
                border_style="bright_blue",
                expand=False
            )
        )

if __name__ == "__main__":
    main()