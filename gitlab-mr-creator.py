import json
import requests
from os import getenv

# Environment variables
GITLAB_TOKEN = getenv('GITLAB_TOKEN')
GITLAB_PROJECT_ID = getenv('CI_PROJECT_ID')
MR_IID = getenv('CI_MERGE_REQUEST_IID')  # The merge request IID (internal ID)

# File path to the findings JSON file
findings_file_path = f'endor_scan_for_{MR_IID}.json'

def post_mr_comment(project_id, mr_iid, message):
    """Post a comment on a Merge Request."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    headers = {'PRIVATE-TOKEN': GITLAB_TOKEN}
    data = {'body': message}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        print("Comment posted successfully.")
    else:
        print(f"Failed to post comment. Status code: {response.status_code}")

def extract_info(findings):
    """Extract required information from findings."""
    meta_desc = findings.get('meta', {}).get('description', '')
    spec_desc = findings.get('spec', {}).get('description', '')
    aliases = findings.get('spec', {}).get('finding_metadata', {}).get('vulnerability', {}).get('aliases', [])
    cvss_score = findings.get('spec', {}).get('finding_metadata', {}).get('vulnerability', {}).get('cvss_v3_severity', {}).get('score', '')
    remediation = findings.get('spec', {}).get('remediation', '')
    summary = findings.get('spec', {}).get('summary', '')
    errors = findings.get('errors', '')

    return meta_desc, spec_desc, aliases, cvss_score, remediation, summary, errors

def main():
    with open(findings_file_path, 'r') as file:
        data = json.load(file)
    
    blocking_findings = data.get('blocking_findings', [])
    if blocking_findings:
        for findings in blocking_findings:
            meta_desc, spec_desc, aliases, cvss_score, remediation, summary, errors = extract_info(findings)
            comment_title = f"Policy Violation: `{errors}`"
            comment_body = f"""
**Meta Description:** {meta_desc}
**Spec Description:** {spec_desc}
**Aliases:** {', '.join(aliases)}
**CVSS Score:** {cvss_score}
**Remediation:** {remediation}
**Summary:** {summary}
**Errors:** {errors}
"""
            comment = comment_title + comment_body
            post_mr_comment(GITLAB_PROJECT_ID, MR_IID, comment)

if __name__ == '__main__':
    main()
