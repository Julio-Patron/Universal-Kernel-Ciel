from rich.console import Console
from rich.prompt import Confirm

console = Console()

def request_approval(action_description: str) -> bool:
    """Requests explicit human approval before executing a potentially destructive action."""
    console.print(f"\n[bold yellow]⚠️ Action Required:[/bold yellow] {action_description}")
    
    # In a real CLI context, this pauses for user input
    return Confirm.ask("Do you approve this execution?", default=False)
