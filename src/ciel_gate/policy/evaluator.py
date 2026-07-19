import fnmatch
from ciel_gate.contracts import ChangeProposal, GateDecision, PolicyViolation, DiffFacts
from ciel_gate.policy.schema import Ruleset

def evaluate_proposal(proposal: ChangeProposal, policy: Ruleset, facts: DiffFacts, diff_hash: str, policy_hash: str) -> GateDecision:
    """Evaluates a change proposal against a policy."""
    violations = []
    
    all_files = set(facts.files_added + facts.files_modified + facts.files_deleted)
    
    # 1. Directory traversal / absolute paths
    for path in all_files:
        if "../" in path or path.startswith("/") or ".." in path.split("/"):
            violations.append(PolicyViolation(
                rule_id="path-traversal", severity="critical", path=path, reason="Path traversal or absolute path detected."
            ))

    # 2. Deny file patterns
    for path in all_files:
        for pattern in policy.deny.file_patterns:
            # We match the pattern or a glob if it's not a pure basename
            # fnmatch is sufficient for simple globs like **/.env if we simplify or just use normal match
            # Python's fnmatch doesn't do ** properly across dirs, but we can do a naive check:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path.split("/")[-1], pattern.replace("**", "*").strip("/")):
                violations.append(PolicyViolation(
                    rule_id="deny-file-pattern", severity="high", path=path, reason=f"Matches denied pattern: {pattern}"
                ))
            elif pattern.startswith("**/") and fnmatch.fnmatch(path, pattern.replace("**/", "*/")):
                 violations.append(PolicyViolation(
                    rule_id="deny-file-pattern", severity="high", path=path, reason=f"Matches denied pattern: {pattern}"
                ))
            elif pattern.startswith("**/") and fnmatch.fnmatch(path, pattern.replace("**/", "")):
                 violations.append(PolicyViolation(
                    rule_id="deny-file-pattern", severity="high", path=path, reason=f"Matches denied pattern: {pattern}"
                ))


    # 3. Protected paths
    for path in all_files:
        for pp in policy.protected_paths:
            # Support ** wildcard roughly
            patt = pp.pattern
            if patt.endswith("/**"):
                if path.startswith(patt[:-3]):
                    violations.append(PolicyViolation(
                        rule_id="protected-path", severity="medium", path=path, reason=f"Protected path modified, action: {pp.action}"
                    ))
            elif fnmatch.fnmatch(path, patt):
                violations.append(PolicyViolation(
                    rule_id="protected-path", severity="medium", path=path, reason=f"Protected path modified, action: {pp.action}"
                ))

    # 4. Deny commands
    for cmd in proposal.requested_commands:
        cmd_lower = cmd.lower()
        for deny_cmd in policy.deny.commands:
            if deny_cmd in cmd_lower.split():
                violations.append(PolicyViolation(
                    rule_id="deny-command", severity="high", path=None, reason=f"Command contains denied token: {deny_cmd}"
                ))

    # 5. Limits
    total_files = len(all_files)
    if total_files > policy.limits.changed_files:
        violations.append(PolicyViolation(
            rule_id="limit-files", severity="medium", path=None, reason=f"Too many changed files: {total_files} > {policy.limits.changed_files}"
        ))
        
    total_lines = facts.total_additions + facts.total_deletions
    if total_lines > policy.limits.total_changed_lines:
        violations.append(PolicyViolation(
            rule_id="limit-lines", severity="medium", path=None, reason=f"Too many changed lines: {total_lines} > {policy.limits.total_changed_lines}"
        ))

    # Determine verdict
    verdict = "allow"
    risk = "low"
    
    if violations:
        has_deny = False
        has_approval = False
        for v in violations:
            if v.severity in ["high", "critical"] or "deny" in v.reason.lower() or "limit" in v.rule_id:
                has_deny = True
            if "require_approval" in v.reason.lower() or "action: require_approval" in v.reason.lower():
                has_approval = True
                
        if has_deny:
            verdict = "deny"
            risk = "high"
        elif has_approval:
            verdict = "require_approval"
            risk = "medium"
        else:
            verdict = "deny"
            risk = "high"
            
    return GateDecision(
        verdict=verdict,
        risk=risk,
        violations=violations,
        diff_hash=diff_hash,
        policy_hash=policy_hash
    )
