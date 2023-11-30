import os
import requests
import json

INPUT_COMMITS_URL = os.environ['INPUT_COMMITS_URL']
INPUT_ISSUE_URL = os.environ['INPUT_ISSUE_URL']
INPUT_COMMENTS_URL = os.environ['INPUT_COMMENTS_URL']
INPUT_LABEL = os.environ.get('INPUT_LABEL', 'dco')
INPUT_TOKEN = os.environ['INPUT_TOKEN']

def find_signed_off_by(msg):
    """ find signed-off-by
    """
    if msg.find("Signed-off-by:") == -1:
        return False
    return True

def add_label(url, label):
    """ add label to issue
    """
    label_url = url + "/labels"
    headers = {"Authorization": "Bearer " + INPUT_TOKEN}
    response = requests.post(label_url, headers=headers, data=json.dumps({"labels": [label]}))
    if response.status_code != 200:
        raise Exception(f"Failed to add label to issue: {response.status_code}")

def add_comment(url):
    """ If DCO failed, add comments to issue
    """
    comment = """
    # Deverloper Certificate of Origin (DCO)

    You must sign-off that you wrote the patch or have the right to pass it on as an open-source patch. The rules are pretty simple, and were created to insure that the community is free to use your contributions.

    The command is 

    ~~~
    git commit --signoff
    # or
    git commit -s
    ~~~

    # References
    - [DCO](https://developercertificate.org/)
    """
    headers = {"Authorization": "Bearer " + INPUT_TOKEN}
    data = {
            'body': comment
            }
    response = requests.post(label_url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to add comment to issue: {response.status_code}")


def parse_commit_msg(url):
    """ parse url
    find commit message
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to get commit message")
    parsed = json.loads(response.text)
    passed = False
    for commit in parsed:
        msg = commit['commit']['message']
        if find_signed_off_by(msg):
            print("Signed-off-by found")
            add_label(INPUT_ISSUE_URL, INPUT_LABEL + ": yes")
            passed = True
        else:
            print("Signed-off-by not found")
            add_label(INPUT_ISSUE_URL, INPUT_LABEL + ": no")
            passed = False
    if passed == False:
        add_comment(INPUT_COMMENTS_URL)
    return passed

if __name__ == "__main__":
    parse_commit_msg(INPUT_COMMITS_URL)
