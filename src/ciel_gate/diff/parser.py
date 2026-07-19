from ciel_gate.diff.facts import DiffFacts

def parse_diff(diff_text: str) -> DiffFacts:
    """Parses a unified diff and extracts facts."""
    # Stub implementation
    facts = DiffFacts()
    
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            facts.files_modified.append(line[6:])
        elif line.startswith("--- a/"):
            pass
        elif line.startswith("+") and not line.startswith("+++"):
            facts.total_additions += 1
        elif line.startswith("-") and not line.startswith("---"):
            facts.total_deletions += 1
            
    return facts
