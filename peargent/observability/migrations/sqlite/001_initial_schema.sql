-- SQLite Migration: Initial Schema for Tracing
-- Table names are customizable using placeholders: {{traces_table}} and {{spans_table}}

-- Traces table: Stores high-level trace information
CREATE TABLE IF NOT EXISTS {{traces_table}} (
    id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    input_data TEXT,
    output TEXT,
    error TEXT,
    session_id TEXT,
    user_id TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT,
    duration_ms INTEGER,
    total_tokens INTEGER DEFAULT 0,
    total_cost REAL DEFAULT 0.0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_agent_name ON {{traces_table}}(agent_name);
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_session_id ON {{traces_table}}(session_id);
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_user_id ON {{traces_table}}(user_id);
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_start_time ON {{traces_table}}(start_time);
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_created_at ON {{traces_table}}(created_at);

-- Spans table: Stores detailed span information (LLM calls, tool executions, etc.)
CREATE TABLE IF NOT EXISTS {{spans_table}} (
    id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    parent_span_id TEXT,
    span_type TEXT NOT NULL,
    name TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    duration_ms INTEGER,

    -- LLM-specific fields
    llm_prompt TEXT,
    llm_response TEXT,
    llm_model TEXT,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    cost REAL,

    -- Tool-specific fields
    tool_name TEXT,
    tool_args TEXT,
    tool_output TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraint
    FOREIGN KEY (trace_id) REFERENCES {{traces_table}}(id) ON DELETE CASCADE
);

-- Indexes for spans
CREATE INDEX IF NOT EXISTS idx_{{spans_table}}_trace_id ON {{spans_table}}(trace_id);
CREATE INDEX IF NOT EXISTS idx_{{spans_table}}_span_type ON {{spans_table}}(span_type);
CREATE INDEX IF NOT EXISTS idx_{{spans_table}}_created_at ON {{spans_table}}(created_at);
