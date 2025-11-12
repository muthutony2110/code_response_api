USE deep;

CREATE TABLE ConversationHistory1 (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id NVARCHAR(100),
    task_name NVARCHAR(100),
    prompt NVARCHAR(MAX),
    message NVARCHAR(MAX),
    code NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);
