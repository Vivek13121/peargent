-- PostgreSQL Migration: Initial Schema for Tracing
-- Table names are customizable using placeholders: {{traces_table}} and {{spans_table}}

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Traces table: Stores high-level trace information
CREATE TABLE IF NOT EXISTS {{traces_table}} (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_name VARCHAR(255) NOT NULL,
    input_data TEXT,
    output TEXT,
    error TEXT,
    session_id VARCHAR(255),
    user_id VARCHAR(255),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_ms INTEGER,
    total_tokens INTEGER DEFAULT 0,
    total_cost DECIMAL(10, 6) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_agent_name ON {{traces_table}}(agent_name);
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_session_id ON {{traces_table}}(session_id);
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_user_id ON {{traces_table}}(user_id);
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_start_time ON {{traces_table}}(start_time);
CREATE INDEX IF NOT EXISTS idx_{{traces_table}}_created_at ON {{traces_table}}(created_at);

-- Spans table: Stores detailed span information (LLM calls, tool executions, etc.)
CREATE TABLE IF NOT EXISTS {{spans_table}} (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trace_id UUID NOT NULL,
    parent_span_id UUID,
    span_type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_ms INTEGER,

    -- LLM-specific fields
    llm_prompt TEXT,
    llm_response TEXT,
    llm_model VARCHAR(100),
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    cost DECIMAL(10, 6),

    -- Tool-specific fields
    tool_name VARCHAR(255),
    tool_args TEXT,
    tool_output TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraint
    FOREIGN KEY (trace_id) REFERENCES {{traces_table}}(id) ON DELETE CASCADE
);

-- Indexes for spans
CREATE INDEX IF NOT EXISTS idx_{{spans_table}}_trace_id ON {{spans_table}}(trace_id);
CREATE INDEX IF NOT EXISTS idx_{{spans_table}}_span_type ON {{spans_table}}(span_type);
CREATE INDEX IF NOT EXISTS idx_{{spans_table}}_created_at ON {{spans_table}}(created_at);
