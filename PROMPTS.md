# Peargent Prompts Documentation

This document catalogs all prompts used throughout the peargent framework. **All prompts are now organized as Jinja2 templates** in the `peargent/templates/` directory for easy customization and maintenance.

---

## Table of Contents
1. [Template Files Overview](#1-template-files-overview)
2. [Tool Usage Prompt Template](#2-tool-usage-prompt-template)
3. [No-Tools Prompt Template](#3-no-tools-prompt-template)
4. [Follow-up Prompt Template](#4-follow-up-prompt-template)
5. [Routing Prompt Template](#5-routing-prompt-template)
6. [Summarization Prompt Template](#6-summarization-prompt-template)
7. [Model System Prompts](#7-model-system-prompts)
8. [Quick Reference](#8-quick-reference)

---

## 1. Template Files Overview

All prompt templates are stored in: `peargent/templates/`

| Template File | Purpose | Used By |
|--------------|---------|---------|
| `tools_prompt.j2` | Tool calling instructions | `agent.py` |
| `no_tools_prompt.j2` | No-tools agent instruction | `agent.py` |
| `follow_up_prompt.j2` | Post-tool execution prompt | `agent.py` |
| `routing_prompt.j2` | Agent routing logic | `router.py` |
| `summarization_prompt.j2` | Context summarization | `history/base.py` |

**Benefits of Template-Based Approach:**
- ✅ Easy to customize prompts without touching code
- ✅ Version control friendly (track prompt changes)
- ✅ Consistent formatting with Jinja2
- ✅ Reusable across different parts of the framework
- ✅ No hardcoded strings scattered in code

---

## 2. Tool Usage Prompt Template

**File:** `peargent/templates/tools_prompt.j2`
**Used By:** `agent.py` → `_render_tools_prompt()` method
**Purpose:** Instructs agents how to call tools using JSON format

### Template Content:
```jinja2
You have access to the following tools:
{% for tool in tools %}
{{ loop.index }}. {{ tool.name }}: {{ tool.description }}. Parameters: {{ tool.parameters }}
{% endfor %}

IMPORTANT TOOL USAGE RULES:

1. When you need to use a tool, respond with ONLY the JSON below - NO additional text before or after:
{
  "tool": "<tool_name>",
  "args": { ... }
}

2. After the tool executes and returns a result, you will see the output. Then provide a natural, conversational response.
3. DO NOT mix JSON tool calls with explanatory text in the same response.
4. DO NOT explain what you're about to do with a tool - just call it.
5. Each response should be EITHER a tool call (pure JSON) OR natural language (no JSON).

If no tool is required, reply normally in plain text.
```

### Template Variables:
- `tools`: List of tool schemas with `name`, `description`, `parameters`

### How to Customize:
Edit `peargent/templates/tools_prompt.j2` to change JSON format, rules, or instructions.

---

## 3. No-Tools Prompt Template

**File:** `peargent/templates/no_tools_prompt.j2`
**Used By:** `agent.py` → `_render_no_tools_prompt()` method
**Purpose:** Tells agents without tools to respond in natural language only

### Template Content:
```jinja2
IMPORTANT: You do not have access to any tools. Respond directly in natural language only. Do NOT output JSON.
```

### Template Variables:
- None (static template)

### When Used:
- When `create_agent(..., tools=[])` (no tools provided)
- Prevents agents from trying to output tool-call JSON

### How to Customize:
Edit `peargent/templates/no_tools_prompt.j2` to change the instruction text.

---

## 4. Follow-up Prompt Template

**File:** `peargent/templates/follow_up_prompt.j2`
**Used By:** `agent.py` → `_render_follow_up_prompt()` method
**Purpose:** Prompt sent after a tool has executed, instructing agent on next steps

### Template Content:
```jinja2
{{ persona }}

{{ tools_prompt }}

Conversation History:
{{ conversation_history }}

{% if has_tools %}
Assistant: The tool has executed successfully. Based on the tool output above:
1. If you need to use another tool, respond with the tool JSON.
2. Otherwise, provide your final response that INCLUDES the actual tool results/data.
3. Do NOT just describe what you did - show the actual results. Unless mentioned otherwise.
DO NOT output JSON unless calling a tool.
{% else %}
Assistant: Based on the information above, provide your response in natural language.
{% endif %}
```

### Template Variables:
- `persona`: Agent's system prompt
- `tools_prompt`: Rendered tools instructions (if agent has tools)
- `conversation_history`: Formatted conversation with tool results
- `has_tools`: Boolean indicating if agent has tools

### How to Customize:
Edit `peargent/templates/follow_up_prompt.j2` to change post-tool instructions or formatting.

---

## 5. Routing Prompt Template

**File:** `peargent/templates/routing_prompt.j2`
**Used By:** `router.py` → `RoutingAgent.route()` method
**Purpose:** Instructs routing agent how to select next agent in a pool

### Template Content:
```jinja2
{{ persona }}

=== AVAILABLE AGENTS ===
{% for agent_info in agent_details %}
Agent: {{ agent_info.name }}
Role: {{ agent_info.description }}
Tools: {{ agent_info.tools|join(', ') if agent_info.tools else 'None' }}
---
{% endfor %}

=== CONVERSATION HISTORY ===
{% for message in history %}
{% if message.agent %}[{{ message.agent }}] {% endif %}{{ message.role|capitalize }}: {{ message.content }}
{% endfor %}

=== ROUTING DECISION ===
{% if last_agent %}
Last agent that executed: {{ last_agent }}
{% endif %}

Your task is to analyze the conversation and determine which agent should act next.

Decision Guidelines:
1. CRITICAL: Look at which tools have been used - if an agent already completed their task (used their tool successfully), move to the NEXT agent in the workflow
2. Identify what still needs to be done to complete the user's request
3. Match the required next step to the agent with the most relevant tools and expertise
4. NEVER route to the same agent twice in a row - each agent should act exactly once unless there's an error
5. Follow the natural workflow progression - don't go backwards unless something failed
6. Choose 'STOP' only when all required steps are complete and the user has a final formatted result

Workflow Analysis:
- What was the user's original goal?
- Which agents have already completed their work? (check tool usage markers)
- What is the NEXT logical step in the pipeline?
- Has the final formatting/reporting been done?

Common Workflow Pattern:
Data Collection → Analysis → Formatting/Reporting → STOP

Respond with ONLY the agent name ({{ agents|join(', ') }}) or 'STOP'.
Do not include any explanation or additional text.
```

### Template Variables:
- `persona`: Routing agent's system prompt
- `agent_details`: List of available agents with their info
- `history`: Conversation history with agent attributions
- `last_agent`: Name of last agent that executed
- `agents`: List of agent names for output format

### How to Customize:
Edit `peargent/templates/routing_prompt.j2` to change routing logic, decision guidelines, or workflow patterns.

---

## 6. Summarization Prompt Template

**File:** `peargent/templates/summarization_prompt.j2`
**Used By:** `history/base.py` → `Thread.summarize_messages()` method
**Purpose:** Instructs LLM to summarize old conversation messages

### Template Content:
```jinja2
Summarize the following conversation concisely, preserving key information, decisions, and context:

{{ conversation_text }}

Provide a clear, factual summary in 2-4 paragraphs.
```

### Template Variables:
- `conversation_text`: Formatted messages to summarize (e.g., "[User] message\n[Assistant] response")

### When Used:
- By `ConversationHistory.manage_context_window()` when strategy is "summarize" or "smart"
- Automatically triggered when context window exceeds `max_context_messages`

### How to Customize:
Edit `peargent/templates/summarization_prompt.j2` to:
- Change summary length (2-4 paragraphs → bullet points, single paragraph, etc.)
- Add specific instructions (e.g., "focus on decisions", "highlight action items")
- Change tone or style of summary

---

## 7. Model System Prompts

These are optional system-level prompts that can be set when creating model instances.

### 7.1 Groq Model
**Location:** `models/groq.py:33`

```python
model = groq("llama-3.3-70b-versatile", system_prompt="Custom system instructions")
```

### 7.2 OpenAI Model
**Location:** `models/openai.py:32-33`

```python
model = openai("gpt-4", system_prompt="Custom system instructions")
```

### 7.3 Gemini Model
**Location:** `models/gemini.py:36-44`

```python
model = gemini("gemini-pro", system_prompt="Custom system instructions")
```

**Note:** Gemini doesn't have a separate system role, so system_prompt is prepended as the first user message.

---

## 8. Quick Reference

### All Template Files

| Template | Location | Rendered By | Customization Level |
|----------|----------|-------------|---------------------|
| `tools_prompt.j2` | `peargent/templates/` | `agent.py` | High - Tool format/rules |
| `no_tools_prompt.j2` | `peargent/templates/` | `agent.py` | Low - Simple instruction |
| `follow_up_prompt.j2` | `peargent/templates/` | `agent.py` | Medium - Post-tool logic |
| `routing_prompt.j2` | `peargent/templates/` | `router.py` | High - Routing strategy |
| `summarization_prompt.j2` | `peargent/templates/` | `history/base.py` | Medium - Summary format |

### How to Customize Any Prompt

1. **Locate the template file** in `peargent/templates/`
2. **Edit the Jinja2 template** with your changes
3. **Restart your application** (templates are loaded at runtime)
4. **Test the changes** with your agents

**Example: Change tool JSON format**
```jinja2
<!-- Original in tools_prompt.j2 -->
{
  "tool": "<tool_name>",
  "args": { ... }
}

<!-- Change to -->
{
  "action": "<tool_name>",
  "parameters": { ... }
}
```

Then update the JSON parsing in `agent.py` accordingly.

### Prompt Composition Flow

```
Model System Prompt (optional)
        ↓
Agent Persona (create_agent)
        ↓
Template Rendered (tools/no-tools/follow-up)
        ↓
Conversation Memory
        ↓
Final Prompt → LLM
```

### Template Best Practices

1. **Use clear variable names** in templates
2. **Add comments** explaining complex logic
3. **Test changes** with different agent configurations
4. **Version control** template changes separately
5. **Document customizations** for your team

### Template Variables Reference

**agent.py templates:**
- `tools`: Tool schemas (name, description, parameters)
- `persona`: Agent system prompt
- `conversation_history`: Formatted conversation
- `has_tools`: Boolean for conditional rendering

**router.py template:**
- `persona`: Router system prompt
- `agent_details`: Agent metadata
- `history`: Conversation history
- `last_agent`: Previous agent name
- `agents`: Available agent names

**history/base.py template:**
- `conversation_text`: Messages to summarize

---

## Notes

- **All prompts are now template-based** - no hardcoded strings in code
- **Easy to experiment** - change templates without touching Python
- **Version controlled** - track prompt evolution in git
- **Consistent formatting** - Jinja2 handles whitespace/indentation
- **Reusable** - templates can be shared across components

**Pro Tip:** Create custom template directories for different use cases:
```python
# In your code
custom_templates = "/path/to/my/templates"
jinja_env = Environment(loader=FileSystemLoader(custom_templates))
```
