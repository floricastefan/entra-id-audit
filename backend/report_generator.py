from pathlib import Path

parent = Path(__file__).parent.parent
reports = parent / "reports" / "audit_report.md"

def generate_report(user_results, secret_results):
    with open(reports, "w") as f:
        f.write("# Microsoft Entra ID - Identity Security Audit Report\n\n")
        f.write("## 1. User Identities Audit\n\n")
        f.write("| Display Name | UPN | Enabled | Roles | MFA | Last Sign-In |Status | Risk | Finding | Recommendation |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")

        for user in user_results:
            f.write(f"| {user["display_name"]} | {user["upn"]} | {user["account_enabled"]} "
                    f"| {user["roles"]} | {user["mfa_enabled"]} | {user["last_sign_in"]} "
                    f"| {user["status"]} | {user["risk_level"]} | {user["finding"]} | {user["recommendation"]} |\n")

        f.write("\n## 2. Application Client Secrets Audit\n\n")
        f.write("| App Name | Secret Name | Created | Expires | Validity Days | Status | Risk | Finding | Recommendation |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")

        for secret in secret_results:
            f.write(f"| {secret["app_name"]} | {secret["secret_name"]} | {secret["created_date"]} "
                    f"| {secret["expiration_date"]} | {secret["validity_days"]} | {secret["status"]} "
                    f"| {secret["risk_level"]} | {secret["finding"]} | {secret["recommendation"]} |\n")