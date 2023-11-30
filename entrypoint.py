import os
import requests
import json

print("==== Commit URL ====")
print(os.environ['INPUT_COMMITS_URL'])
print(os.environ['INPUT_ISSUE_URL'])

def find_signed_off_by(msg):
    """ find signed-off-by
    """
    if msg.find("Signed-off-by:") == -1:
        return False
    return True

def add_label(url, label="Signed-off-by"):
    """ add label to issue
    """
    label_url = url + "/labels"
    headers = {"Authorization": "Bearer " + os.environ['INPUT_TOKEN']}
    response = requests.post(label_url, headers=headers, data=json.dumps({"labels": [label]}))
    if response.status_code != 200:
        print(response.status_code)
        raise Exception("Failed to add label to issue")

def parse_commit_msg(url):
    """ parse url
    find commit message
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to get commit message")
    parsed = json.loads(response.text)
    for commit in parsed:
        msg = commit['commit']['message']
        print(msg)
        if find_signed_off_by(msg):
            print("Signed-off-by found")
            add_label(os.environ['INPUT_ISSUE_URL'])
            return True
        else:
            print("Signed-off-by not found")
            add_label(os.environ['INPUT_ISSUE_URL'], "No Signed-off-by")
            return False


if __name__ == "__main__":
    parse_commit_msg(os.environ['INPUT_COMMITS_URL'])
