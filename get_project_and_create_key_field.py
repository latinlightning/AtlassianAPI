import requests
import json

def get_jira_project_keys(url, username, password):
    api_url = url + '/rest/api/2/project'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers, auth=(username, password))
    if response.status_code == 200:
        projects = response.json()
        project_keys = [project['key'] for project in projects]
        return project_keys
    else:
        print('Failed to retrieve projects. Error:', response.status_code)
        return None

def create_jira_custom_field(url, username, password, field_name):
    api_url = url + '/rest/api/2/field'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'name': field_name,
        'description': 'Custom field created via API',
        'type': "com.atlassian.jira.plugin.system.customfieldtypes:select",
        'searcherKey': 'com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher'
    }
    response = requests.post(api_url, headers=headers, json=payload, auth=(username, password))
    if response.status_code == 201:
        custom_field = response.json()
        print('Custom field created successfully.')
        return custom_field['id']
    else:
        print('Failed to create custom field. Error:', response.status_code)
        return None

def get_custom_field_context(url, username, password, field_id):
    api_url = url + f'/rest/api/3/field/{field_id}/context'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers, auth=(username, password))
    if response.status_code == 200:
        custom_field_context = response.json()
        print('Custom field context retrieved successfully.')
        return custom_field_context
    else:
        print('Failed to retrieve custom field context. Error:', response.status_code)
        return None

def add_options_to_custom_field(url, username, password, field_id, context_id, options):
    api_url = url + f"/rest/api/3/field/{field_id}/context/{context_id}/option"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "options": options
    }
    payload_data = json.dumps(payload)
    response = requests.post(api_url, data=payload_data, headers=headers, auth=(username, password))
    if response.status_code == 200:
        response_data = response.json()
        print(json.dumps(response_data, sort_keys=True, indent=4, separators=(",", ": ")))
    else:
        print("Failed to add options to custom field. Error:", response.status_code)

# Auth
jira_url = 'https://jiraandshit.atlassian.net'
jira_username = 'carlosmaderajr1995@gmail.com'
jira_password = 



context_id = get_custom_field_context(jira_url, jira_username, jira_password)
context_id =['values'][0]['id']
