
The source_code table is designed to store information about source code files and their associated comments extracted from repositories. The structure facilitates the storage, retrieval, and analysis of comments tied to specific files in a structured and efficient manner.

Table Structure:
Columns:

1.serial_id:
  Data Type: SERIAL
  Description: Auto-incrementing unique identifier for each record in the table.
  Constraints:
    Primary Key: Ensures each record has a unique identifier.

2.file_name:
 Data Type: TEXT
 Description: The name of the source code file.
 Constraints:
  Unique: Prevents duplicate entries for the same file.

3.comments:
 Data Type: JSONB
 Description: JSON-formatted array containing comments extracted from the source code file.
