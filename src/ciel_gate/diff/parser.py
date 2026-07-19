from ciel_gate.contracts import DiffFacts

def parse_diff(diff_text: str) -> DiffFacts:
    """Parses a unified git diff and extracts facts."""
    files_added = set()
    files_modified = set()
    files_deleted = set()
    total_additions = 0
    total_deletions = 0
    sensitive_paths = set()

    current_file_a = None
    current_file_b = None
    is_new = False
    is_deleted = False
    is_rename = False

    lines = diff_text.splitlines()
    for line in lines:
        if line.startswith("diff --git "):
            parts = line.split(" ", 3)
            if len(parts) >= 4:
                # Format: diff --git a/file b/file
                a_path = parts[2]
                b_path = parts[3]
                if a_path.startswith("a/"): a_path = a_path[2:]
                if b_path.startswith("b/"): b_path = b_path[2:]
                current_file_a = a_path
                current_file_b = b_path
            is_new = False
            is_deleted = False
            is_rename = False
        elif line.startswith("new file"):
            is_new = True
        elif line.startswith("deleted file"):
            is_deleted = True
        elif line.startswith("rename from"):
            is_deleted = True # The old file is deleted conceptually
        elif line.startswith("rename to"):
            is_rename = True
        elif line.startswith("+++ "):
            path = line[4:].strip()
            if path == "/dev/null" and current_file_a:
                files_deleted.add(current_file_a)
            elif path.startswith("b/"):
                path = path[2:]
                if is_new:
                    files_added.add(path)
                elif not is_deleted:
                    files_modified.add(path)
                if "../" in path or path.startswith("/"):
                    sensitive_paths.add(path)
        elif line.startswith("--- "):
            path = line[4:].strip()
            if path.startswith("a/"):
                path = path[2:]
                if "../" in path or path.startswith("/"):
                    sensitive_paths.add(path)
        elif line.startswith("+") and not line.startswith("+++"):
            total_additions += 1
        elif line.startswith("-") and not line.startswith("---"):
            total_deletions += 1

    # Catch renames if they don't have +++ / ---
    for f in list(files_added) + list(files_modified) + list(files_deleted):
        if "../" in f or f.startswith("/"):
            sensitive_paths.add(f)
            
    return DiffFacts(
        files_added=list(files_added),
        files_modified=list(files_modified),
        files_deleted=list(files_deleted),
        total_additions=total_additions,
        total_deletions=total_deletions,
        sensitive_paths=list(sensitive_paths)
    )
