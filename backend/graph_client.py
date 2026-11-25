import os
from dotenv import load_dotenv
import msal
import requests

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

auth_url = "https://login.microsoftonline.com/" + TENANT_ID
scopes = ["https://graph.microsoft.com/.default"]

def get_access_token():
    ConfidentialClient = msal.ConfidentialClientApplication(CLIENT_ID, authority=auth_url, client_credential=CLIENT_SECRET)
    token = ConfidentialClient.acquire_token_for_client(scopes=scopes)

    if "access_token" in token:
        return token["access_token"]
    else:
        print(token["error_description"])
        return None

def get_users(token):
    headers = {"Authorization": "Bearer " + token}
    url = "https://graph.microsoft.com/v1.0/users?$select=id,displayName,userPrincipalName,accountEnabled,userType,createdDateTime,signInActivity"

    response = requests.request(method='GET', url=url, headers=headers)

    users = []
    for user in response.json()["value"]:
        if "#EXT#" not in user["userPrincipalName"]:
            users.append(user)

    return users

def get_user_roles(token, user_id):
    headers = {"Authorization": "Bearer " + token}
    url = "https://graph.microsoft.com/v1.0/users/" + user_id + "/memberOf"

    response = requests.request(method='GET', url=url, headers=headers)

    roles = []
    for role in response.json()["value"]:
        if role["@odata.type"] == "#microsoft.graph.directoryRole":
            roles.append(role["displayName"])

    return roles

def get_user_mfa(token, user_id):
    headers = {"Authorization": "Bearer " + token}
    url = "https://graph.microsoft.com/v1.0/users/" + user_id + "/authentication/methods"

    response = requests.request(method='GET', url=url, headers=headers)

    for method in response.json()["value"]:
        if method["@odata.type"] != "#microsoft.graph.passwordAuthenticationMethod":
            return True

    return False

def get_applications(token):
    headers = {"Authorization": "Bearer " + token}
    url = "https://graph.microsoft.com/v1.0/applications?$select=id,appId,displayName,passwordCredentials"

    response = requests.request(method='GET', url=url, headers=headers)

    return response.json()["value"]

def get_last_sign_in(token, user_id):
    headers = {"Authorization": "Bearer " + token}
    url = "https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=userId eq '" + user_id + "'&$top=1"

    response = requests.request(method='GET', url=url, headers=headers)

    logs = response.json()["value"]
    if logs != []:
        return logs[0]["createdDateTime"]
    else:
        return None