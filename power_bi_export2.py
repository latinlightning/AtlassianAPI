import csv
import json

def format_for_power_bi(filepath):
    def has_parent_field(issue_dict):
        if 'fields' in issue_dict:
            fields = issue_dict['fields']
            if 'parent' in fields:
                return True
        return False

    #Store formatted entry in results array
    results = []

    #Set Colors
    theme_color = '#008000' #Green
    initiative_color = '#FFFF00' #Yellow
    epic_color = '#800080' #Purple
    story_color = '#90EE90' #Green
    subtask_color = '#0000FF' #Blue
    edge_color = '#000000' #Black
    test_case_color = '#FF0000' #Red
    test_plan_color = '#301934' #Dark Purple

    # Open results csv, iterate over, and format based on issue type
    with open(filepath, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # Skip headers
        next(reader)
        # Iterate over the rows
        for row in reader:        
            issue = eval(row[0])
            issue_type = issue['fields']['issuetype']['name']
            entry = {
                "Source Node": issue['key'],
                "Target Node": '',
                "Target Node Color": '',
                "Target Node Weight": '',
                "Edge Weight": 1, 
                "Color Edge": edge_color,
                "Source Node Color": '',
                "Source Node Weight": ''
                }

            if issue_type == 'Theme':
                entry['Source Node Color'] = theme_color
                entry['Source Node Weight'] = 5

            elif issue_type == 'Initiative':
                entry['Source Node Color'] = initiative_color
                entry['Source Node Weight'] = 4
                if has_parent_field(issue) == True:
                    entry['Target Node'] = issue['fields']['parent']['key']
                    entry['Target Node Color'] = theme_color
                    entry['Target Node Weight'] = 5

            elif issue_type == 'Epic':
                entry['Source Node Color'] = epic_color
                entry['Source Node Weight'] = 3
                if has_parent_field(issue) == True:
                    entry['Target Node'] = issue['fields']['parent']['key']
                    entry['Target Node Color'] = initiative_color
                    entry['Target Node Weight'] = 5

            elif issue_type == 'Story':
                entry['Source Node Color'] = story_color
                entry['Source Node Weight'] = 2
                if has_parent_field(issue) == True:
                    entry['Target Node'] = issue['fields']['parent']['key']
                    entry['Target Node Color'] = epic_color
                    entry['Target Node Weight'] = 3

            elif issue_type == 'Sub-Task':
                entry['Source Node Color'] = subtask_color
                entry['Source Node Weight'] = 1
                if has_parent_field(issue) == True:
                    entry['Target Node'] = issue['fields']['parent']['key']
                    entry['Target Node Color'] = story_color
                    entry['Target Node Weight'] = 2

            elif issue_type == 'Test Case':
                entry['Source Node Color'] = test_case_color
                entry['Source Node Weight'] = 1
                if has_parent_field(issue) == True:
                    entry['Target Node'] = issue['fields']['parent']['key']
                    entry['Target Node Weight'] = 2
                    entry['Target Node Color'] = epic_color

            elif issue_type == 'Test Plan':
                entry['Source Node Color'] = test_plan_color
                entry['Source Node Weight'] = 2
                if has_parent_field(issue) == True:
                    entry['Target Node'] = issue['fields']['parent']['key']
                    entry['Target Node Color'] = epic_color
                    entry['Target Node Weight'] = 2
            results.append(entry)
    
    #Write to CSV
    columns = ["Source Node", "Target Node", "Target Node Color", "Target Node Weight", "Edge Weight", "Color Edge", "Source Node Color", "Source Node Weight"]
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader() 
        for result in results:
            writer.writerow(result)
    return "Made CSV!"

filepath = r'C:\Users\carlos.madera\Desktop\Repos and Code\dwn-jira-automation\carlosScripts\jira_scripts\SAMSUNGRAN_issues.csv'

format_for_power_bi(filepath)