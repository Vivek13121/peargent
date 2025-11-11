"""
Example demonstrating context window management in peargent.

This example shows how to:
1. Trim messages to manage context size
2. Delete specific messages
3. Summarize old messages to preserve context
4. Use automatic context management
5. NEW: Use HistoryConfig DSL for streamlined history configuration
"""

from peargent import create_agent, create_history, File, Memory, HistoryConfig
from peargent.models import groq


def example_1_trim_messages():
    """Example 1: Trim messages to manage context window."""
    print("\n" + "="*60)
    print("Example 1: Trim Messages")
    print("="*60)

    history = create_history(store_type=File(storage_dir="./context_examples"))
    thread_id = history.create_thread(metadata={"example": "trim"})

    # Add many messages
    for i in range(15):
        history.add_user_message(f"Message {i}")
        history.add_assistant_message(f"Response {i}")

    print(f"Total messages before trim: {history.get_message_count()}")

    # Strategy 1: Keep only last 10 messages
    removed = history.trim_messages(strategy="last", count=10)
    print(f"\nAfter 'last' strategy: {history.get_message_count()} messages (removed {removed})")

    # Add more messages
    for i in range(10):
        history.add_user_message(f"New message {i}")
        history.add_assistant_message(f"New response {i}")

    print(f"\nAfter adding more: {history.get_message_count()} messages")

    # Strategy 2: Keep first 15 messages
    removed = history.trim_messages(strategy="first", count=15)
    print(f"After 'first' strategy: {history.get_message_count()} messages (removed {removed})")


def example_2_delete_messages():
    """Example 2: Delete specific messages."""
    print("\n" + "="*60)
    print("Example 2: Delete Specific Messages")
    print("="*60)

    history = create_history(store_type=SessionBuffer())
    thread_id = history.create_thread()

    # Add messages
    msg1 = history.add_user_message("Keep this message")
    msg2 = history.add_assistant_message("Delete this one")
    msg3 = history.add_user_message("Keep this too")
    msg4 = history.add_assistant_message("Delete this too")

    print(f"Messages before deletion: {history.get_message_count()}")

    # Delete specific messages by ID
    deleted = history.delete_messages([msg2.id, msg4.id])
    print(f"Deleted {deleted} messages")
    print(f"Messages after deletion: {history.get_message_count()}")

    # View remaining messages
    print("\nRemaining messages:")
    for msg in history.get_messages():
        print(f"  [{msg.role}] {msg.content}")


def example_3_summarize_messages():
    """Example 3: Summarize old messages."""
    print("\n" + "="*60)
    print("Example 3: Summarize Old Messages")
    print("="*60)

    history = create_history(store_type=File(storage_dir="./context_examples"))
    thread_id = history.create_thread(metadata={"example": "summarize"})

    # Simulate a long conversation
    history.add_user_message("Hi, I need help with Python programming")
    history.add_assistant_message("I'd be happy to help! What do you need?")
    history.add_user_message("How do I read a file?")
    history.add_assistant_message("You can use open() function with a file path")
    history.add_user_message("Can you show me an example?")
    history.add_assistant_message("Sure: with open('file.txt', 'r') as f: content = f.read()")
    history.add_user_message("Thanks! Now how do I write to a file?")
    history.add_assistant_message("Use open() with 'w' mode: with open('file.txt', 'w') as f: f.write(content)")
    history.add_user_message("Great! What about appending?")
    history.add_assistant_message("Use 'a' mode: with open('file.txt', 'a') as f: f.write(content)")

    print(f"Messages before summarization: {history.get_message_count()}")

    # Summarize old messages, keeping only the last 4
    model = groq("llama-3.3-70b-versatile")
    summary = history.summarize_messages(model, keep_recent=4)

    print(f"Messages after summarization: {history.get_message_count()}")
    print(f"\nSummary created:")
    print(summary.content[:200] + "...")


def example_4_auto_context_management():
    """Example 4: Automatic context management with agents."""
    print("\n" + "="*60)
    print("Example 4: Auto Context Management (Legacy)")
    print("="*60)

    # Create history
    history = create_history(store_type="file", storage_dir="./context_examples")
    thread_id = history.create_thread(metadata={"example": "auto_manage"})

    # Create agent with automatic context management
    # When messages exceed 10, it will automatically summarize
    agent = create_agent(
        name="Assistant",
        description="A helpful assistant",
        persona="You are a helpful AI assistant.",
        model=groq("llama-3.3-70b-versatile"),
        tools=[],
        history=history,
        auto_manage_context=True,  # Enable automatic management
        max_context_messages=10     # Trigger when > 10 messages
    )

    # Have a long conversation
    print("\nHaving a conversation...")
    for i in range(7):
        response = agent.run(f"Tell me fact #{i+1} about space")
        print(f"Turn {i+1}: {response[:80]}...")

    print(f"\nFinal message count: {history.get_message_count()}")
    print("(Context was automatically managed to stay under limit)")


def example_5_manual_context_management():
    """Example 5: Manual context window management."""
    print("\n" + "="*60)
    print("Example 5: Manual Context Window Management")
    print("="*60)

    history = create_history(store_type="session_buffer")
    thread_id = history.create_thread()
    model = groq("llama-3.3-70b-versatile")

    # Add many messages
    for i in range(25):
        history.add_user_message(f"Question {i}")
        history.add_assistant_message(f"Answer {i}")

    print(f"Messages before management: {history.get_message_count()}")

    # Option 1: Trim to keep only recent messages
    print("\nOption 1: Trim to last 20 messages")
    history.manage_context_window(model, max_messages=20, strategy="trim_last")
    print(f"Messages after trim: {history.get_message_count()}")

    # Add more messages
    for i in range(15):
        history.add_user_message(f"New question {i}")
        history.add_assistant_message(f"New answer {i}")

    print(f"\nMessages after adding more: {history.get_message_count()}")

    # Option 2: Summarize old messages
    print("Option 2: Summarize with max 15 messages")
    history.manage_context_window(model, max_messages=15, strategy="summarize")
    print(f"Messages after summarization: {history.get_message_count()}")


def example_6_history_config_dsl():
    """Example 6: NEW HistoryConfig DSL for streamlined configuration."""
    print("\n" + "="*60)
    print("Example 6: HistoryConfig DSL (NEW)")
    print("="*60)

    # Example 1: Basic HistoryConfig with smart strategy
    print("\n--- HistoryConfig with Smart Strategy ---")
    agent1 = create_agent(
        name="SmartAgent",
        description="An agent with smart context management",
        persona="You are a helpful AI assistant.",
        model=groq("llama-3.3-70b-versatile"),
        tools=[],
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=8,
            strategy="smart",  # Default smart strategy
            summarize_model=groq("llama-3.3-70b-versatile"),  # Use same model for summarization
            store=File(storage_dir="./context_examples")
        )
    )

    print("Created agent with HistoryConfig:")
    print(f"  - Auto manage: {agent1.auto_manage_context}")
    print(f"  - Max messages: {agent1.max_context_messages}")
    print(f"  - Strategy: {agent1.context_strategy}")
    print(f"  - Has summarize model: {agent1.summarize_model is not None}")

    # Example 2: HistoryConfig with explicit trim strategy
    print("\n--- HistoryConfig with Trim Strategy ---")
    agent2 = create_agent(
        name="TrimAgent",
        description="An agent that trims old messages",
        persona="You are concise and efficient.",
        model=groq("llama-3.3-70b-versatile"),
        tools=[],
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=5,
            strategy="trim_last",  # Always trim, no summarization
            store=SessionBuffer()  # In-memory storage
        )
    )

    print("Created agent with trim strategy:")
    print(f"  - Strategy: {agent2.context_strategy}")
    print(f"  - Summarize model: {agent2.summarize_model}")

    # Example 3: HistoryConfig with dedicated summarization model
    print("\n--- HistoryConfig with Dedicated Summary Model ---")
    agent3 = create_agent(
        name="SummaryAgent", 
        description="An agent with dedicated summary model",
        persona="You are thoughtful and preserve context well.",
        model=groq("llama-3.3-70b-versatile"),  # Main model
        tools=[],
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=6,
            strategy="summarize",  # Always summarize
            summarize_model=groq("llama-3.1-8b-instant"),  # Faster model for summaries
            store=File(storage_dir="./context_examples")
        )
    )

    print("Created agent with dedicated summary model:")
    print(f"  - Main model: {type(agent3.model).__name__}")
    print(f"  - Summary model: {type(agent3.summarize_model).__name__}")
    print(f"  - Strategy: {agent3.context_strategy}")

    # Demonstrate the agents with a short conversation
    print("\n--- Testing Smart Agent ---")
    for i in range(3):
        response = agent1.run(f"What's interesting fact #{i+1} about AI?")
        print(f"Response {i+1}: {response[:60]}...")

    print(f"Final message count: {agent1.history.get_message_count()}")

def example_7_smart_strategy_selection():
    """Example 7: Smart strategy selection."""
    print("\n" + "="*60)
    print("Example 7: Smart Strategy Selection")
    print("="*60)

    model = groq("llama-3.3-70b-versatile")

    # Scenario 1: Small overflow - should trim
    print("\n--- Scenario 1: Small Overflow (should trim) ---")
    history1 = create_history(store_type="session_buffer")
    history1.create_thread()

    for i in range(22):  # Just 2 over limit of 20
        history1.add_user_message(f"Message {i}")
        history1.add_assistant_message(f"Response {i}")

    print(f"Before: {history1.get_message_count()} messages")
    history1.manage_context_window(model, max_messages=20, strategy="smart")
    print(f"After smart management: {history1.get_message_count()} messages")
    print("Strategy used: trim_last (small overflow, no LLM needed)")

    # Scenario 2: Medium overflow - should summarize
    print("\n--- Scenario 2: Medium Overflow (should summarize) ---")
    history2 = create_history(store_type="session_buffer")
    history2.create_thread()

    for i in range(30):  # 10 over limit
        history2.add_user_message(f"Message {i}")
        history2.add_assistant_message(f"Response {i}")

    print(f"Before: {history2.get_message_count()} messages")
    history2.manage_context_window(model, max_messages=20, strategy="smart")
    print(f"After smart management: {history2.get_message_count()} messages")
    print("Strategy used: summarize (medium overflow, preserve context)")

    # Scenario 3: Has tool calls - should summarize to preserve context
    print("\n--- Scenario 3: Has Tool Calls (should summarize) ---")
    history3 = create_history(store_type="session_buffer")
    history3.create_thread()

    for i in range(15):
        history3.add_user_message(f"Message {i}")
        history3.add_assistant_message(f"Response {i}")

    # Add tool message (important context)
    history3.add_assistant_message("Let me calculate that")
    history3.add_tool_message({
        "name": "calculator",
        "args": {"x": 5, "y": 10},
        "output": "15"
    })

    for i in range(7):
        history3.add_user_message(f"Follow-up {i}")
        history3.add_assistant_message(f"Answer {i}")

    print(f"Before: {history3.get_message_count()} messages (with tool calls)")
    history3.manage_context_window(model, max_messages=20, strategy="smart")
    print(f"After smart management: {history3.get_message_count()} messages")
    print("Strategy used: summarize (has tool calls, preserve important context)")


def main():
    """Run all examples."""
    print("Context Window Management Examples")
    print("=" * 60)

    # Example 1: Trim messages
    example_1_trim_messages()

    # Example 2: Delete messages
    example_2_delete_messages()

    # Example 3: Summarize messages
    example_3_summarize_messages()

    # Example 4: Auto context management (legacy)
    example_4_auto_context_management()

    # Example 5: Manual management
    example_5_manual_context_management()

    # Example 6: NEW HistoryConfig DSL
    example_6_history_config_dsl()

    # Example 7: Smart strategy selection
    example_7_smart_strategy_selection()

    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
