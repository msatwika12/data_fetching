import requests
import re
import psycopg2
import json
import os

# File extensions to filter
VALID_EXTENSIONS = {'.java', '.cpp', '.html', '.js', '.scala', '.sh', '.clj', '.cs', '.go', '.php', '.hpp', '.py', '.json', '.rb'}
README_FILE_NAME = "README.md"

# Regular expressions for extracting comments based on file type
COMMENT_PATTERNS = {
    'single_line': re.compile(r'//.*|#.*'),
    'multi_line': re.compile(r'/\*.*?\*/', re.DOTALL),
    'html': re.compile(r'<!--.*?-->', re.DOTALL)
}

# Function to extract comments from text
def extract_comments_from_text(text, file_extension):
    """Extract comments from text based on file extension."""
    comments = []
    if file_extension in {'.java', '.cpp', '.js', '.scala', '.sh', '.py', '.rb', '.cs', '.go', '.php', '.hpp'}:
        comments += COMMENT_PATTERNS['single_line'].findall(text)
    if file_extension in {'.java', '.cpp', '.js', '.scala', '.cs', '.php', '.hpp'}:
        comments += COMMENT_PATTERNS['multi_line'].findall(text)
    if file_extension == '.html':
        comments += COMMENT_PATTERNS['html'].findall(text)
    return [comment.strip() for comment in comments if comment.strip()]

# Function to get pull request details
def get_pull_request_details(repo_owner, repo_name, pr_number, headers):
    """Fetch PR details (title, description, owner) and retrieve comments from modified files of specific types."""
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    pr_response = requests.get(pr_url, headers=headers)
    pr_response.raise_for_status()
    pr_data = pr_response.json()

    comments_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
    comments_response = requests.get(comments_url, headers=headers)
    comments_response.raise_for_status()
    comments = [comment["body"] for comment in comments_response.json()]

    files_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
    files_response = requests.get(files_url, headers=headers)
    files_response.raise_for_status()
    modified_files_data = files_response.json()

    modified_files = []
    for file in modified_files_data:
        filename = file["filename"]
        file_extension = f".{filename.split('.')[-1]}"
        if (file_extension in VALID_EXTENSIONS or filename == README_FILE_NAME) and "patch" in file:
            file_comments = extract_comments_from_text(file["patch"], file_extension)
            modified_files.append({"file_name": filename, "comments": file_comments})

    return {
        "pr_number": pr_number,
        "owner": pr_data["user"]["login"],
        "title": pr_data["title"],
        "description": pr_data["body"],
        "conversation": comments,
        "modified_files": modified_files
    }

# Function to load data into PostgreSQL
def load_data_to_postgresql(pr_details_list, db_config):
    """Insert PR details into the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        for pr in pr_details_list:
            pr_number = pr['pr_number']
            owner = pr['owner']
            title = pr['title']
            description = pr['description']
            conversation = json.dumps(pr['conversation'])
            files_modified = json.dumps([file['file_name'] for file in pr['modified_files']])

            cur.execute("""
                INSERT INTO pull_requests (pr_number, owner, title, description, conversation, files_modified)
                VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb)
                ON CONFLICT (pr_number) DO NOTHING;
            """, (pr_number, owner, title, description, conversation, files_modified))

        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

# Function to parse repository details from URL
def parse_repo_details(repo_url):
    """Parse repository owner and name from the URL."""
    match = re.match(r"https://github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        raise ValueError("Invalid GitHub repository URL. Make sure it is in the format: https://github.com/owner/repo")
    return match.group(1), match.group(2)

# Main function
def main():
    # Input GitHub details
    access_token = input("Enter your GitHub access token: ").strip()
    repo_url = input("Enter the GitHub repository URL: ").strip()

    # Parse repository details
    repo_owner, repo_name = parse_repo_details(repo_url)

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch all closed PRs
    pull_requests = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
        params = {"state": "closed", "per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        prs = response.json()
        if not prs:
            break
        pull_requests.extend(prs)
        page += 1

    # Process each PR
    pr_details_list = []
    for pr in pull_requests:
        pr_number = pr["number"]
        print(f"Fetching details for PR #{pr_number}...")
        pr_details = get_pull_request_details(repo_owner, repo_name, pr_number, headers)
        pr_details_list.append(pr_details)

    # Save data to a JSON file
    json_filename = f"{repo_name}_pr_details.json"
    with open(json_filename, "w") as json_file:
        json.dump(pr_details_list, json_file, indent=4)
    print(f"Data saved to {json_filename}")

    # Database configuration
    db_config = {
        'dbname': 'PullRequestDatabase', #DataBase Name
        'user': 'postgres', #mention the username
        'password': 'Srikala@76', # provide the password for postgresql
        'host': 'localhost',  #localhost or some other
        'port': '5432' #mention the port number
    }

    # Load data into PostgreSQL
    load_data_to_postgresql(pr_details_list, db_config)

if __name__ == "__main__":
    main()
