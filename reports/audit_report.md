# Microsoft Entra ID - Identity Security Audit Report

## 1. User Identities Audit

| Display Name | UPN | Enabled | Roles | MFA | Last Sign-In |Status | Risk | Finding | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| Florica Admin | flo.admin@flostefan13gmail.onmicrosoft.com | True | ['Global Administrator'] | True | 2026-11-25 | PASS | LOW | Compliant account (MFA enabled and active) | No action required |
| Legacy Admin | legacy.admin@flostefan13gmail.onmicrosoft.com | False | None | False | Never Signed In | PASS | LOW | Account disabled (No active risk) | No action required |
| Mike Helpdesk | mike.helpdesk@flostefan13gmail.onmicrosoft.com | True | None | True | 2026-11-25 | PASS | LOW | Compliant account (MFA enabled and active) | No action required |
| Stale Employee | stale.employee@flostefan13gmail.onmicrosoft.com | False | None | False | Never Signed In | PASS | LOW | Account disabled (No active risk) | No action required |

## 2. Application Client Secrets Audit

| App Name | Secret Name | Created | Expires | Validity Days | Status | Risk | Finding | Recommendation |
|---|---|---|---|---|---|---|---|---|
| Entra ID Security Auditor | Auditor Script Key | 2026-11-14 | 2027-02-12 | 90 | PASS | LOW | Compliant Client Secret (<=90 days) | No action required |
