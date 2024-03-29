import requests
import json

def get_jira_project_keys(url, username, password):
    api_url = url + '/rest/api/2/project'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers, auth=(username, password), verify=False)
    if response.status_code == 200:
        projects = response.json()
        project_keys = []
        for project in projects:
            project = f"{project['name']} : {project['key']}"
            project_keys.append(project)
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
        'description': 'Custom field that automatically updates through webhooks and automations',
        'type': "com.atlassian.jira.plugin.system.customfieldtypes:select",
        'searcherKey': 'com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher'
    }
    response = requests.post(api_url, headers=headers, json=payload, auth=(username, password), verify=False)
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
    response = requests.get(api_url, headers=headers, auth=(username, password), verify=False)
    if response.status_code == 200:
        custom_field_context = response.json()
        print('Custom field context retrieved successfully.')
        return custom_field_context
    else:
        print('Failed to retrieve custom field context. Error:', response.status_code)
        return None

def add_options_to_custom_field(url, username, password, field_id, context_id, project_keys):
    api_url = url + f"/rest/api/3/field/{field_id}/context/{context_id}/option"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    options = []
    for key in project_keys:
        option = {
            "disabled": False,
            "value": key
        }
        options.append(option)
    payload = {
        "options": options
    }
    response = requests.post(api_url, json=payload, headers=headers, auth=(username, password), verify=False)
    response_data = response.json()  # Parse the response data
    if response.status_code == 201:
        print("Options added successfully.")
        print(json.dumps(response_data, sort_keys=True, indent=4, separators=(",", ": ")))
    else:
        print("Failed to add options to custom field. Error:", response.status_code)
        print(json.dumps(response_data, sort_keys=True, indent=4, separators=(",", ": ")))


# Auth
jira_url = 'https://xxxxxxx.atlassian.net'
jira_username = 'an email'
jira_password = 'an api key'

# Retrieve project keys
project_keys = get_jira_project_keys(jira_url, jira_username, jira_password)
print(project_keys)


if project_keys:
    # Create custom field
    custom_field_id = create_jira_custom_field(jira_url, jira_username, jira_password, "Project Name : Key")
    
    if custom_field_id:
        # Get custom field context
        custom_field_context = get_custom_field_context(jira_url, jira_username, jira_password, custom_field_id)
        
        if custom_field_context:
            context_id = custom_field_context['values'][0]['id']  # Assuming the first context is used
            # Add project keys as options to the custom field
            add_options_to_custom_field(jira_url, jira_username, jira_password, custom_field_id, context_id, project_keys)
