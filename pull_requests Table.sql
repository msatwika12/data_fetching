CREATE TABLE pull_requests (
    pr_number INT PRIMARY KEY,               -- The PR number, which is unique
    owner TEXT,                              -- The owner of the PR
    title TEXT,                              -- The title of the PR
    description TEXT,                        -- The description of the PR
    conversation JSONB,                      -- The conversation as a JSONB array
    files_modified JSONB                     -- The modified files as a JSONB array (only file_name values)
);