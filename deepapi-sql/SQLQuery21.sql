USE deep;

DROP TABLE IF EXISTS ConversationnewHistory;

CREATE TABLE ConversationnewHistory ( 
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id NVARCHAR(100),
    task_name NVARCHAR(100),       -- ✅ Must exist
    prompt NVARCHAR(MAX),
    message NVARCHAR(MAX),
    code NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);

