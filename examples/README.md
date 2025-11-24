# Peargent Examples

Welcome to the Peargent examples directory! This collection demonstrates all major features of the Peargent framework through practical, runnable code examples.

## 📋 Table of Contents

1. [Getting Started](#1-getting-started)
2. [Tools](#2-tools)
3. [Agent Pools](#3-agent-pools)
4. [History Management](#4-history-management)
5. [Tracing & Observability](#5-tracing--observability)
6. [Streaming](#6-streaming)
7. [Structured Output](#7-structured-output)
8. [Advanced Patterns](#8-advanced-patterns)
9. [Routing](#9-routing)

## Prerequisites

```bash
# Install Peargent
pip install peargent

# Set up API keys (choose your provider)
export GROQ_API_KEY="your-groq-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## 1. Getting Started

**Location:** `01-getting-started/`

Learn the basics of creating and running agents.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `quickstart.py` | Complete introduction to all major features | Agents, tools, history, tracing, streaming, pools |
| `basic_agent.py` | Simplest possible agent | Agent creation, basic usage |
| `anthropic_example.py` | Using Anthropic Claude models | Anthropic integration |

**Quick Start:**
```bash
cd 01-getting-started
python quickstart.py
```

## 2. Tools

**Location:** `02-tools/`

Learn how to equip agents with tools for real-world tasks.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `basic_tools.py` | Creating and using tools | Tool creation, parallel execution |
| `tool_timeout.py` | Prevent tools from hanging | Timeout configuration, override |
| `tool_retry.py` | Handle flaky operations | Retry logic, exponential backoff |
| `tool_error_handling.py` | Graceful error handling | `on_error` strategies (raise/return_error/return_none) |
| `tool_validation.py` | Output validation with Pydantic | `output_schema`, type safety |
| `parallel_tools.py` | Execute multiple tools simultaneously | Parallel execution, performance |

**Example:**
```python
from peargent import create_tool, create_agent

weather_tool = create_tool(
    name="get_weather",
    description="Get weather for a city",
    input_parameters={"city": str},
    call_function=get_weather_function,
    timeout=5.0,              # Timeout after 5s
    max_retries=3,            # Retry 3 times
    retry_backoff=True,       # Exponential backoff
    on_error="return_error"   # Return error message
)
```

## 3. Agent Pools

**Location:** `03-agent-pools/`

Learn how to orchestrate multiple specialized agents.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `basic_pool.py` | Multi-agent collaboration | Pool creation, routing, collaboration |

**Example:**
```python
from peargent import create_pool

pool = create_pool(
    agents=[researcher, analyst, writer],
    router=intelligent_router,
    max_iter=10
)
```

## 4. History Management

**Location:** `04-history/`

Learn how to maintain conversation context across requests.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `basic_history.py` | In-memory conversation history | `InMemory` store, basic usage |
| `sqlite_history.py` | SQLite-backed persistence | `Sqlite` store, local persistence |
| `postgresql_history.py` | PostgreSQL for production | `Postgresql` store, production-ready |
| `redis_history.py` | Redis for distributed systems | `Redis` store, high-performance |
| `history_all_methods.py` | Comprehensive comparison | All storage backends, unified API |

**Storage Options:**

| Store | Use Case | Persistence | Performance |
|-------|----------|-------------|-------------|
| `InMemory` | Testing, temporary | None | ⚡ Fastest |
| `File` | Local development | Local files | ⚡ Fast |
| `Sqlite` | Single-server apps | SQLite database | ⚡ Fast |
| `Postgresql` | Production apps | PostgreSQL | ⚙️ Medium |
| `Redis` | Distributed systems | Redis cache | ⚡⚡ Very Fast |

**Example:**
```python
from peargent import create_agent, HistoryConfig
from peargent.storage import Sqlite

agent = create_agent(
    name="Assistant",
    history=HistoryConfig(
        store=Sqlite(connection_string="sqlite:///./chat.db"),
        auto_manage_context=True,
        max_context_messages=20,
        strategy="trim_last"
    )
)
```

## 5. Tracing & Observability

**Location:** `05-tracing/`

Learn how to monitor, debug, and optimize your agents.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `sqlite_tracing.py` | Basic tracing with SQLite | Trace storage, retrieval |
| `postgres_tracing.py` | Production tracing with PostgreSQL | Production storage, scalability |
| `cost_tracking.py` | Track token usage and costs | Cost monitoring, budgets |
| `metrics.py` | Performance metrics | Duration, tokens, success rate |
| `custom_tables.py` | Custom trace storage | Custom schema, advanced queries |
| `advanced_tracing.py` | Comprehensive tracing patterns | Sessions, users, filtering |

**Example:**
```python
from peargent.observability import enable_tracing, get_tracer

# Enable tracing
tracer = enable_tracing(
    store_type="sqlite",
    connection_string="sqlite:///./traces.db"
)

# Use agents...
agent.run("Hello", tracing=True)

# Analyze
stats = tracer.get_aggregate_stats()
print(f"Total cost: ${stats['total_cost']:.6f}")
print(f"Total tokens: {stats['total_tokens']:,}")
```

## 6. Streaming

**Location:** `06-streaming/`

Learn how to stream agent responses in real-time.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `basic_streaming.py` | Stream text responses | `agent.stream()`, real-time output |
| `streaming_with_tracing.py` | Stream with metadata | `agent.stream_observe()`, costs, tokens |
| `async_streaming.py` | Async streaming for concurrency | `agent.astream_observe()`, FastAPI, SSE |

**Example:**
```python
# Simple streaming
for chunk in agent.stream("Explain quantum computing"):
    print(chunk, end="", flush=True)

# Rich streaming with metadata
for update in agent.stream_observe("What is AI?"):
    if update.is_token:
        print(update.content, end="", flush=True)
    elif update.is_agent_end:
        print(f"\nCost: ${update.cost:.6f}")
        print(f"Tokens: {update.tokens}")
```

## 7. Structured Output

**Location:** `07-structured-output/`

Learn how to get structured, validated outputs from agents.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `basic_structured.py` | Simple Pydantic schemas | `output_schema`, type safety |
| `nested_structured.py` | Complex nested structures | Nested models, validation |
| `advanced_structured.py` | Advanced validation patterns | Constraints, custom validators |
| `comparison.py` | Structured vs unstructured | Performance, reliability comparison |

**Example:**
```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    name: str
    age: int = Field(ge=0, le=150)
    email: str
    premium: bool

agent = create_agent(
    name="ProfileExtractor",
    persona="Extract user information from text.",
    output_schema=UserProfile  # Guaranteed structure!
)

result = agent.run("John Doe, 30 years old, john@example.com, premium user")
print(result.name)   # Type-safe access
print(result.age)    # Validated: 0-150
```

## 8. Advanced Patterns

**Location:** `08-advanced/`

Advanced multi-agent workflows and specialized use cases.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `research_expert.py` | Multi-agent research pipeline | Researcher → Analyzer → Reporter |
| `story_generator.py` | Creative content generation | Story Writer → Prompt Designer → Synthesizer |
| `routing_agent.py` | Intelligent task routing | Routing agent, conditional flows |

**Example:**
```python
# Multi-agent pipeline
pool = create_pool(
    agents=[researcher, analyzer, reporter],
    router=workflow_router,
    max_iter=5
)

result = pool.run("Analyze Q3 sales data and create a report")
```

## 9. Routing

**Location:** `09-routing/`

Learn how to build custom routing logic for agent pools.

| Example | Description | Key Features |
|---------|-------------|--------------|
| `custom_router_basic.py` | Basic custom router | RouterResult, simple routing |
| `custom_router_conditional.py` | Conditional routing logic | State-based decisions |
| `custom_router_statebased.py` | Stateful routing | History-aware routing |
| `router_comparison.py` | Compare routing strategies | Performance, accuracy |
| `router_with_agent_access.py` | Access agent metadata in router | Agent descriptions, dynamic routing |

**Example:**
```python
from peargent.core.router import RouterResult

def my_router(state):
    """Custom routing logic"""
    if "research" in state.user_input.lower():
        return RouterResult(
            agent="Researcher",
            instructions="Search for relevant information"
        )
    elif "analyze" in state.user_input.lower():
        return RouterResult(
            agent="Analyst",
            instructions="Analyze the data"
        )
    else:
        return RouterResult(
            agent=None,  # No more routing needed
            instructions="Task complete"
        )
```

## Running Examples

### Run Individual Examples
```bash
# Navigate to specific folder
cd examples/02-tools

# Run example
python basic_tools.py
```

### Run All Examples in a Category
```bash
# Run all tool examples
cd examples/02-tools
for file in *.py; do
    echo "Running $file..."
    python "$file"
done
```

## Common Patterns

### Pattern 1: Simple Agent
```python
from peargent import create_agent
from peargent.models import groq

agent = create_agent(
    name="Assistant",
    description="A helpful assistant",
    persona="You are helpful and concise.",
    model=groq("llama-3.3-70b-versatile")
)

response = agent.run("Hello!")
```

### Pattern 2: Agent with Tools
```python
agent = create_agent(
    name="ToolAgent",
    persona="You use tools to answer questions.",
    model=groq("llama-3.3-70b-versatile"),
    tools=[search_tool, calculator_tool]
)
```

### Pattern 3: Agent with History
```python
from peargent import HistoryConfig
from peargent.storage import InMemory

agent = create_agent(
    name="MemoryAgent",
    persona="You remember past conversations.",
    model=groq("llama-3.3-70b-versatile"),
    history=HistoryConfig(
        store=InMemory(),
        auto_manage_context=True,
        max_context_messages=10
    )
)
```

### Pattern 4: Agent with Tracing
```python
from peargent.observability import enable_tracing

tracer = enable_tracing(
    store_type="sqlite",
    connection_string="sqlite:///./traces.db"
)

agent = create_agent(
    name="TracedAgent",
    persona="You are helpful.",
    model=groq("llama-3.3-70b-versatile"),
    tracing=True  # Enable tracing
)
```

## Best Practices

### 1. Start Simple
Begin with `01-getting-started/basic_agent.py` before exploring advanced features.

### 2. Use Appropriate Storage
- **Development**: `InMemory` or `File`
- **Production**: `Postgresql` or `Redis`
- **Local Apps**: `Sqlite`

### 3. Enable Tracing in Production
Always enable tracing to monitor costs and performance:
```python
tracer = enable_tracing(store_type="postgresql")
agent = create_agent(..., tracing=True)
```

### 4. Handle Errors Gracefully
Use appropriate error handling for tools:
```python
critical_tool = create_tool(..., on_error="raise")
optional_tool = create_tool(..., on_error="return_error")
analytics_tool = create_tool(..., on_error="return_none")
```

### 5. Manage Context
Use history management to control token usage:
```python
history=HistoryConfig(
    auto_manage_context=True,
    max_context_messages=10,
    strategy="trim_last"
)
```

## Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $GROQ_API_KEY

# Set API key
export GROQ_API_KEY="your-key-here"
```

### Import Errors
```bash
# Reinstall Peargent
pip uninstall peargent
pip install peargent
```

### Database Connection Issues
```bash
# SQLite: Check file permissions
ls -la *.db

# PostgreSQL: Test connection
psql -h localhost -U user -d database

# Redis: Test connection
redis-cli ping
```

## Contributing

Found a bug or have an improvement? Please:
1. Check existing examples first
2. Create a minimal reproduction
3. Submit an issue or PR

## License

All examples are provided under the MIT License. Feel free to use them as starting points for your own projects!