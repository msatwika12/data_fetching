# SCtoDbjson

This Python script automates the process of extracting comments from source code files in a GitHub repository. It utilizes the GitHub REST API to fetch repository contents, parses comments from source files based on their programming language, and stores the extracted data in both a JSON file and a PostgreSQL database for further analysis.

Features:
1.Repository Parsing: Identifies and fetches the repository details using a GitHub URL.
2.File Filtering: Selects files based on predefined valid extensions and README files.
3.Comment Extraction: Extracts comments from source code using regular expressions tailored for specific languages.
4.Data Storage:
  Saves comments in a JSON file for portability.
  Stores comments in a PostgreSQL database for querying and analysis.
5.Error Handling: Handles API errors, invalid inputs, and database connection issues gracefully.

Prerequisites:
1.Python Libraries: Install the following libraries using pip install requests psycopg2.
2.GitHub Token: Generate a GitHub Personal Access Token with appropriate repository access.
3.PostgreSQL: Set up a PostgreSQL database with proper credentials.

Configuration:
1.GITHUB_API_URL: Template for the GitHub API URL.
2.VALID_EXTENSIONS: A set of valid file extensions for filtering source files.
3.README_FILE_NAME: Specifies the README file to be included in processing.

Functions:
1. parse_repo_details(repo_url)
Extracts repository details (owner and repository name) from a given GitHub URL.
Input:
  repo_url: GitHub repository URL (e.g., https://github.com/user/repo).
Output: Tuple of (owner, repo).

2. get_repo_contents(owner, repo, path="", headers=None)
Fetches the contents of a GitHub repository directory using the API.
Input:
  owner: Repository owner.
  repo: Repository name.
  path: (Optional) Path to a subdirectory.
  headers: HTTP headers containing the GitHub token.
Output: List of files and directories from the repository.

3. get_filtered_file_names(owner, repo, headers, path="")
Filters repository files based on valid extensions and the README file.
Input: Same as get_repo_contents.
Output: List of files that match the criteria.

4. extract_comments(file_content, file_name)
Extracts comments from a source file based on its programming language.
Input:
  file_content: Content of the file as a string.
  file_name: Name of the file (used to identify language by extension).
Output: List of extracted comments.

5. get_file_content(owner, repo, file_path, headers)
Fetches the content of a specific file from the repository.
Input:
  owner: Repository owner.
  repo: Repository name.
  file_path: Path of the file within the repository.
  headers: HTTP headers containing the GitHub token.
Output: Base64-encoded file content (decoded by the calling function).

6. save_comments_to_json(comments_data, filename="source_code_comments.json")
Saves the extracted comments into a JSON file for further analysis or portability.
Input:
  comments_data: List of dictionaries containing file names and comments.
  filename: Name of the output JSON file (default: source_code_comments.json).

7. get_comments_for_files(repo_url, token)
Main function to fetch comments from all valid files in the repository.
Input:
  repo_url: GitHub repository URL.
  token: GitHub Personal Access Token.
Output: List of dictionaries containing file names and their comments.

8. load_data_to_postgresql(json_file, db_config)
Loads comment data from a JSON file into a PostgreSQL database.
Input:
  json_file: Path to the JSON file containing comment data.
  db_config: Dictionary with PostgreSQL database configuration:
  dbname: Database name.
  user: Database username.
  password: Database password.
  host: Database host (e.g., localhost).
  port: Database port (default: 5432).

Data Flow:
Input:
  GitHub Repository URL.
  GitHub Personal Access Token.
  PostgreSQL database configuration.
  
Process:
  Parses repository details.
  Fetches repository contents and filters files.
  Extracts comments from files.
  Saves comments to a JSON file.
  Loads comments into the PostgreSQL database.
  
Output:
  JSON file (source_code_comments.json) with extracted comments.
  PostgreSQL database table (source_code) with file names and comments.
  
Database Schema:
  Table: source_code
  serial_id (Primary Key): Auto-incremented unique ID for each entry.
  file_name (Text): Name of the file.
  comments (JSONB): Extracted comments stored in JSON format.
  
Usage:
Execution Steps
Run the script: python script_name.py
Provide the following inputs:
  GitHub Repository URL: GitHub Personal Access Token.
  Configure the PostgreSQL database credentials in the script.
  
Error Handling:
Invalid GitHub URL: Throws a ValueError with a descriptive message.
API Errors: Logs HTTP status codes and error messages for debugging.
Database Errors: Catches exceptions during PostgreSQL connection or data insertion.

Example:
Input:
  Enter the GitHub repository URL: https://github.com/user/repo
  Enter your GitHub token: your_token
Output:
  JSON File: source_code_comments.json
[
    {
        "file_name": "example.py",
        "comments": [
            "# This is a sample comment",
            "# Another comment"
        ]
    }
]

Database Table: source_code
| serial_id	| file_name	|             comments              |
|	    1     | example.py|  [{"# This is a sample comment"}] |
