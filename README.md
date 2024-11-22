# PrtoDbjson
This Python script retrieves details from closed pull requests (PRs) of a GitHub repository using the GitHub REST API. It extracts metadata such as PR titles, descriptions, comments, and changes to source code files, saving this data in both a JSON file and a PostgreSQL database. The code also parses and extracts comments from modified files based on their type.

Features:
Pull Request Data Extraction: Retrieves metadata, comments, and changes from closed PRs.
File Comment Parsing: Extracts comments from modified files using regular expressions.
Data Storage:
        Saves PR data in a JSON file for offline analysis.
        Stores PR details and file changes in a PostgreSQL database.
Pagination Support: Handles API pagination for large repositories with multiple PRs.
Error Handling: Includes detailed error reporting for API requests and database operations.

Prerequisites:
1. Python Libraries:
      Install required libraries using:
        pip install requests psycopg2
2. GitHub Access Token: Generate a Personal Access Token with permissions to access repository and PR data.
3. PostgreSQL: Configure a PostgreSQL database with a valid schema.
   
Configuration:
Constants:
        VALID_EXTENSIONS: File extensions for filtering valid source files.
        README_FILE_NAME: Name of the README file to include in the analysis.
Regular Expressions:
        Single-line Comments: Matches single-line comments (e.g., // or #).
        Multi-line Comments: Matches block comments (e.g., /* ... */).
        HTML Comments: Matches HTML comments (e.g., <!-- ... -->).
        
Functions:
1. extract_comments_from_text(text, file_extension)
Extracts comments from text based on file type.
Input:
        text: The content of a file.
        file_extension: File extension to determine the comment pattern.
Output: A list of extracted comments.
2. get_pull_request_details(repo_owner, repo_name, pr_number, headers)
Fetches metadata, comments, and modified file details for a specific pull request.
Input:
        repo_owner: GitHub repository owner.
        repo_name: GitHub repository name.
        pr_number: Pull request number.
        headers: HTTP headers, including the GitHub token.
Output: A dictionary containing PR metadata, conversation comments, and modified file details.

3. load_data_to_postgresql(pr_details_list, db_config)
Loads pull request details into a PostgreSQL database.
Input:
        pr_details_list: List of dictionaries containing PR details.
        db_config: PostgreSQL database connection details.
   
Database Table:
Table Name: pull_requests
Columns:
        pr_number: Pull request number (Primary Key).
        owner: Owner of the PR.
        title: Title of the PR.
        description: Description of the PR.
        conversation: PR comments in JSON format.
        files_modified: List of modified files in JSON format.
        
5. parse_repo_details(repo_url)
Parses the owner and repository name from a GitHub URL.
Input:
        repo_url: GitHub repository URL (e.g., https://github.com/user/repo).
Output: Tuple containing (repo_owner, repo_name).

5. main()
Orchestrates the script execution:
1.Prompts the user for a GitHub token and repository URL.
2.Parses repository details.
3.Retrieves closed pull requests using pagination.
4.Processes each PR to extract metadata, comments, and modified file details.
5.Saves the extracted data to a JSON file.
6.Inserts the PR details into a PostgreSQL database.
Data Flow
Input:
        GitHub repository URL.
        GitHub Personal Access Token.
Process:
1.Parses the repository owner and name.
2.Fetches closed pull requests using the GitHub REST API.
3.Extracts metadata, comments, and modified file details for each PR.
4.Saves the extracted data into a JSON file.
5.Inserts the data into a PostgreSQL database.

Output:
        JSON File: Contains PR details, comments, and modified file data.
        PostgreSQL Table: Stores PR metadata and modified file details.
Usage:
Run the script:python script_name.py

Input:
1.GitHub Personal Access Token:
        Enter your GitHub access token: your_token
2.GitHub Repository URL:
        Enter the GitHub repository URL: https://github.com/owner/repo
        
Output:
1.JSON File: Saved as repo_name_pr_details.json.
2.PostgreSQL Database: Data inserted into the pull_requests table.

Example: 
Input:
        Enter your GitHub access token: your_token
        Enter the GitHub repository URL: https://github.com/user/repo
JSON File Output:
[
  {
    "pr_number": 1,
    "owner": "username",
    "title": "Fix Bug #123",
    "description": "This PR fixes bug #123.",
    "conversation": ["Looks good to me!", "Please add more tests."],
    "modified_files": [
      {
        "file_name": "example.py",
        "comments": ["# TODO: Add unit tests"]
      }
    ]
  }
]

PostgreSQL Table:
| pr_number | owner   | title        | description | conversation | files_modified |
| 1         |username |	Fix Bug #123 |	This PR fixes bug #123 | ["Looks good to me!", "Please add more tests."] | ["example.py"] |

Extensibility:
        Support for additional file types can be added by extending the COMMENT_PATTERNS.
        Additional database fields can be incorporated for enhanced PR metadata storage.
        Integration with visualization tools or reporting frameworks for data analysis.
Error Handling:
        Invalid GitHub URL: Raises a ValueError for incorrect URLs.
        API Errors: Logs HTTP response codes and error messages for debugging.
        Database Errors: Catches exceptions during connection and data insertion.
