# pull_requests Table
The pull_requests table is designed to store metadata and relevant details about pull requests (PRs) from a GitHub repository. This schema enables structured storage of PR-related information, including metadata, comments, and modified file details, to facilitate querying and analysis.

Table Structure:
Columns:
1.pr_number:
 Data Type: INT
 Description: Unique identifier for the pull request.
 Constraints:
    Primary Key: Ensures uniqueness and prevents duplicate entries for a PR.

2.owner:
 Data Type: TEXT
 Description: The GitHub username of the pull request's creator.

3.title:
 Data Type: TEXT
 Description: The title of the pull request, summarizing its purpose.
 
4.description:
 Data Type: TEXT
 Description: A detailed description of the pull request, outlining changes, goals, and any additional information provided by the creator.

5.conversation:
 Data Type: JSONB
 Description: JSON-formatted array containing the comments exchanged in the pull request conversation. This includes both the review comments and general discussion.

6.files_modified:
  Data Type: JSONB
  Description: JSON-formatted array of filenames that were modified in the pull request.
