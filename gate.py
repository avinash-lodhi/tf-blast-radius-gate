import json
import os
import sys

STATEFUL_TYPES = {
    "aws_db_instance",
    "aws_rds_cluster",
    "aws_s3_bucket",
    "aws_dynamodb_table",
    "aws_opensearch_domain",
    "google_sql_database_instance",
}

def evaluate_plan(plan_path: str) -> int:
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    blocked = []
    for rc in plan.get("resource_changes", []):
        actions = rc.get("change", {}).get("actions", [])
        if "delete" in actions and rc.get("type") in STATEFUL_TYPES:
            blocked.append((rc["address"], actions))

    if not blocked:
        print("PASS: No destructive stateful changes detected.")
        return 0

    print("HIGH BLAST RADIUS DETECTED:")
    for addr, actions in blocked:
        print(f"  - {addr} -> actions={actions}")

    # governed break-glass escape hatch for planned migrations
    if os.getenv("BREAK_GLASS_APPROVAL") == "true":
        print("OVERRIDE: BREAK_GLASS_APPROVAL=true set. Allowing with audit warning.")
        return 0

    print("\nBLOCKED: Merge halted. Add PR label 'break-glass-db' or set BREAK_GLASS_APPROVAL=true.")
    return 1

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "tfplan-example.json"
    sys.exit(evaluate_plan(target))
