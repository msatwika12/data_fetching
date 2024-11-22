CREATE TABLE source_code (
    serial_id SERIAL PRIMARY KEY,   -- Auto-incrementing unique identifier
    file_name TEXT UNIQUE,          -- Unique file name
    comments JSONB                  -- Comments stored as JSONB array
);