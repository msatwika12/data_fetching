import requests
import json
import re
import base64
import psycopg2
from urllib.parse import urlparse

# Parse repository details from the GitHub URL
def parse_repo_details(repo_url):
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) >= 2:
        return path_parts[0], path_parts[1]
    else:
        raise ValueError("Invalid GitHub repository URL. Ensure it is in the format: https://github.com/owner/repo")

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
VALID_EXTENSIONS = {'.java', '.cpp', '.html', '.js', '.scala', '.sh', '.clj', '.cs', '.go', '.php', '.hpp', '.py', '.json', '.rb', 'README'}
README_FILE_NAME = "README.md"

# Fetch repository contents
def get_repo_contents(owner, repo, path="", headers=None):
    url = GITHUB_API_URL.format(owner=owner, repo=repo, path=path)
    all_files = []
    
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
        
        files = response.json()
        all_files.extend(files)

        next_url = None
        if 'Link' in response.headers:
            links = response.headers['Link']
            for link in links.split(','):
                if 'rel="next"' in link:
                    next_url = link.split(';')[0][1:-1]  
        url = next_url  

    return all_files

# Filter file names by valid extensions
def get_filtered_file_names(owner, repo, headers, path=""):
    file_names = []
    contents = get_repo_contents(owner, repo, path, headers)

    for file in contents:
        if file['type'] == 'dir':
            file_names.extend(get_filtered_file_names(owner, repo, headers, file['path']))
        else:
            file_name = file['name']
            if file_name == README_FILE_NAME or any(file_name.endswith(ext) for ext in VALID_EXTENSIONS):
                file_names.append(file)

    return file_names

# Extract comments from source code
def extract_comments(file_content, file_name):
    comments = []
    if file_name.endswith(('.java', '.cpp', '.js', '.go', '.cs', '.rb', '.scala', '.sh', '.clj', '.hpp')):
        comments = re.findall(r'//.*?$|/\*.*?\*/', file_content, re.DOTALL | re.MULTILINE)
    elif file_name.endswith(('.html', '.php')):
        comments = re.findall(r'<!--.*?-->', file_content, re.DOTALL | re.MULTILINE)
    elif file_name.endswith('.py'):
        comments = re.findall(r'#.*$', file_content, re.MULTILINE)
    elif file_name.endswith('.json'):
        comments = re.findall(r'//.*?$|/\*.*?\*/', file_content, re.DOTALL | re.MULTILINE)
    if file_name == README_FILE_NAME or file_name == "README":
        comments = re.findall(r'<!--.*?-->', file_content, re.DOTALL | re.MULTILINE)
    return comments

# Fetch file content from GitHub
def get_file_content(owner, repo, file_path, headers):
    url = GITHUB_API_URL.format(owner=owner, repo=repo, path=file_path)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_content = response.json()
        return file_content.get('content')
    return None

# Save comments to a JSON file
def save_comments_to_json(comments_data, filename="source_code_comments.json"):
    with open(filename, 'w') as json_file:
        json.dump(comments_data, json_file, indent=4)

# Fetch comments from files in a repository
def get_comments_for_files(repo_url, token):
    owner, repo = parse_repo_details(repo_url)
    headers = {"Authorization": f"token {token}"}
    comments_data = []

    filtered_files = get_filtered_file_names(owner, repo, headers)
    for file in filtered_files:
        file_content_base64 = get_file_content(owner, repo, file['path'], headers)
        if file_content_base64:
            file_content = base64.b64decode(file_content_base64).decode('utf-8', errors='ignore')
            comments = extract_comments(file_content, file['name'])
            if comments:
                comments_data.append({"file_name": file['name'], "comments": comments})

    save_comments_to_json(comments_data)
    return comments_data

# Load data into PostgreSQL
def load_data_to_postgresql(json_file, db_config):
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Create table with serial_id
        cur.execute("""
            CREATE TABLE IF NOT EXISTS source_code (
                serial_id SERIAL PRIMARY KEY,
                file_name TEXT NOT NULL,
                comments JSONB
            );
        """)

        with open(json_file, 'r') as file:
            data = json.load(file)

        for entry in data:
            file_name = entry.get('file_name', None)
            comments = json.dumps(entry.get('comments', []))
            
            cur.execute("""
                INSERT INTO source_code (file_name, comments)
                VALUES (%s, %s::jsonb)
                ON CONFLICT (file_name) DO NOTHING;
            """, (file_name, comments))

        conn.commit()
        print("Data inserted into PostgreSQL successfully")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        conn.close()

# Main script execution
if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    token = input("Enter your GitHub token: ")
    db_config = {
        'dbname': 'PullRequestDatabase',  # Database name
        'user': 'postgres',              # PostgreSQL username
        'password': 'Srikala@76',        # PostgreSQL password
        'host': 'localhost',             # Host (localhost or other)
        'port': '5432'                   # Port number
    }
    
    comments_data = get_comments_for_files(repo_url, token)
    json_file = "source_code_comments.json"
    load_data_to_postgresql(json_file, db_config)
