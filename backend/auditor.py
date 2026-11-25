from datetime import datetime, timezone

def check_inactivity(last_sign_in_date_time):
    if last_sign_in_date_time == None:
        return True, "Never Signed In"
    else:
        last_logged_in = datetime.fromisoformat(last_sign_in_date_time)
        current_ime = datetime.now(timezone.utc)
        inactivity = current_ime - last_logged_in
        if inactivity.days > 90:
            return True, last_sign_in_date_time[:10]
        else:
            return False, last_sign_in_date_time[:10]

def audit_user(user, roles, has_mfa, last_sign_in_date_time):
    is_inactive, last_sign_in = check_inactivity(last_sign_in_date_time)
    is_enabled = user.get("accountEnabled")

    if is_enabled == False and roles == []:
        status = "PASS"
        risk_level = "LOW"
        finding = "Account disabled (No active risk)"
        recommendation = "No action required"

    elif "Global Administrator" in roles and has_mfa == False:
        status = "FAIL"
        risk_level = "CRITICAL"
        finding = "Global Administrator without MFA"
        recommendation = "Revoke Global Administrator role or enforce MFA immediately"

    elif roles != [] and has_mfa == False:
        status = "FAIL"
        risk_level = "HIGH"
        finding = "Privileged role assigned without MFA"
        recommendation = "Revoke excessive administrative role (Least Privilege) and enforce MFA"

    elif is_inactive == True or has_mfa == False:
        status = "FAIL"
        risk_level = "MEDIUM"
        finding = "Inactive (zombie) account or missing MFA"
        recommendation = "Disable unused account or require MFA registration"
    else:
        status = "PASS"
        risk_level = "LOW"
        finding = "Compliant account (MFA enabled and active)"
        recommendation = "No action required"

    details_user = {
        "display_name": user["displayName"],
        "upn": user["userPrincipalName"],
        "account_enabled": is_enabled,
        "roles": roles if roles != [] else "None",
        "mfa_enabled": has_mfa,
        "last_sign_in": last_sign_in,
        "status": status,
        "risk_level": risk_level,
        "finding": finding,
        "recommendation": recommendation
    }

    return details_user

def audit_app_secrets(app):
    secret_result = []
    for secret in app.get("passwordCredentials"):
        start_date = datetime.fromisoformat(secret["startDateTime"])
        end_date = datetime.fromisoformat(secret["endDateTime"])
        current_time = datetime.now(timezone.utc)

        validity_days = (end_date - start_date).days
        days_remaining = (end_date - current_time).days

        if days_remaining <= 0:
            status = "FAIL"
            risk_level = "HIGH"
            finding = "Expired Client Secret"
            recommendation = "Remove expired secret immediately"
        elif validity_days > 93:
            status = "FAIL"
            risk_level = "HIGH"
            finding = "Client Secret validity exceeds 90-day policy"
            recommendation = "Revoke long-lived secret and rotate every 90 days"
        else:
            status = "PASS"
            risk_level = "LOW"
            finding = "Compliant Client Secret (<=90 days)"
            recommendation = "No action required"

        details_app = {
            "app_name": app["displayName"],
            "secret_name": secret["displayName"],
            "created_date": secret["startDateTime"][:10],
            "expiration_date": secret["endDateTime"][:10],
            "validity_days": validity_days,
            "status": status,
            "risk_level": risk_level,
            "finding": finding,
            "recommendation": recommendation
        }

        secret_result.append(details_app)
    return secret_result