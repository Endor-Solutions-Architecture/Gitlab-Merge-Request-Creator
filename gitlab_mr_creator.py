import json
import requests
from os import getenv

# env variables
GITLAB_TOKEN = getenv('ENDOR_POLICY_CHECK') # name PAT something endor-y to recognize it, it's a user
GITLAB_PROJECT_ID = getenv('CI_PROJECT_ID')
MR_IID = getenv('CI_MERGE_REQUEST_IID')  # merge request IID (internal ID)

# file path to the json output of endorctl scan
findings_file_path = f'endor_scan_for_{MR_IID}.json'

def post_mr_comment(project_id, mr_iid, message):
    """function to post a comment on a MR"""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    headers = {'PRIVATE-TOKEN': GITLAB_TOKEN}
    data = {'body': message}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        print("Comment posted successfully.")
    else:
        print(f"Failed to post comment. Status code: {response.status_code}")

def extract_info(findings):
    """function to extract required info from blocking_findings"""
    meta_desc = findings.get('meta', {}).get('description', '')
    spec_desc = findings.get('spec', {}).get('explanation', '')
    aliases = [f"**CVE or Known Vulnerability ID:** {alias}" for alias in findings.get('spec', {}).get('finding_metadata', {}).get('vulnerability', {}).get('spec', {}).get('aliases', [])]
    cvss_score = findings.get('spec', {}).get('finding_metadata', {}).get('vulnerability', {}).get('spec', {}).get('cvss_v3_severity', {}).get('score')
    remediation = findings.get('spec', {}).get('remediation', '')
    summary = findings.get('spec', {}).get('summary', '')

    return meta_desc, spec_desc, aliases, cvss_score, remediation, summary

def main():
    with open(findings_file_path, 'r') as file:
        data = json.load(file)
    
    blocking_findings = data.get('blocking_findings', [])
    if blocking_findings:
        for findings in blocking_findings:
            comment_body_parts = []  # initialize inside the loop
            meta_desc, spec_desc, aliases, cvss_score, remediation, summary = extract_info(findings)

            if meta_desc:
                comment_body_parts.append(f"\n**Finding:** {meta_desc}")
            if spec_desc:
                comment_body_parts.append(f"**Description:** {spec_desc}")
            if aliases:
                comment_body_parts.append(f"{', '.join(aliases)} ")
            if cvss_score is not None:  # checking for none as `0` is a valid score but returns false
                comment_body_parts.append(f"**CVSS Score:** {cvss_score}")
            if remediation:
                comment_body_parts.append(f"**How Can I Fix It?:** {remediation}")
            if summary:
                comment_body_parts.append(f"**Summary:** {summary}")

            # join only if there are parts to join
            if comment_body_parts:
                comment_body = "\n\n".join(comment_body_parts)
                post_mr_comment(GITLAB_PROJECT_ID, MR_IID, comment_body)

if __name__ == '__main__':
    main()
