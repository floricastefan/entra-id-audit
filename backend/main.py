import graph_client
import auditor
import report_generator

token = graph_client.get_access_token()
users = graph_client.get_users(token)

user_results = []
for user in users:
    roles = graph_client.get_user_roles(token, user["id"])
    has_mfa = graph_client.get_user_mfa(token, user["id"])
    last_sign_in = graph_client.get_last_sign_in(token, user["id"])
    user_results.append(auditor.audit_user(user, roles, has_mfa, last_sign_in))

applications = graph_client.get_applications(token)

secret_results = []
for app in applications:
    secret_results.extend(auditor.audit_app_secrets(app))

report_generator.generate_report(user_results, secret_results)
print("Generated report!")