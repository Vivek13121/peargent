"""
Simple example demonstrating the new HistoryConfig DSL.

This shows the streamlined way to configure history management for agents.
"""

from peargent import create_agent, HistoryConfig, File, Memory
from peargent.models import groq


def main():
    """Demonstrate the new HistoryConfig DSL."""
    print("HistoryConfig DSL Examples")
    print("=" * 50)

    # Example 1: Smart context management with file storage
    print("\nExample 1: Smart Strategy with File Storage")
    agent = create_agent(
        name="Assistant",
        description="A helpful assistant",
        persona="You are a helpful AI assistant.",
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=10,
            strategy="smart",  # Default smart strategy
            summarize_model=groq("llama-3.3-70b-versatile"),
            store=File(storage_dir="./conversations")
        )
    )
    
    print(f"  - Agent: {agent.name}")
    print(f"  - Auto manage: {agent.auto_manage_context}")
    print(f"  - Max messages: {agent.max_context_messages}")
    print(f"  - Strategy: {agent.context_strategy}")
    print(f"  - Has history: {agent.history is not None}")
    
    # Example 2: Memory storage with trim strategy
    print("\nExample 2: Trim Strategy with Memory Storage")
    pool_agent = create_agent(
        name="PoolAgent",
        description="An agent for pools",
        persona="You work well in teams.",
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=5,
            strategy="trim_last",
            store=SessionBuffer()
        )
    )
    
    print(f"  - Agent: {pool_agent.name}")
    print(f"  - Strategy: {pool_agent.context_strategy}")
    print(f"  - Storage: Memory")
    
    # Example 3: No history (None store)
    print("\nExample 3: No History Configuration")
    simple_agent = create_agent(
        name="SimpleAgent",
        description="A simple agent without history",
        persona="You are simple and direct.",
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=False,
            store=None  # No persistent storage
        )
    )
    
    print(f"  - Agent: {simple_agent.name}")
    print(f"  - Auto manage: {simple_agent.auto_manage_context}")
    print(f"  - Has history: {simple_agent.history is not None}")

    # Test a quick conversation
    print("\nTesting conversation...")
    response = agent.run("Hello, how are you?")
    print(f"Response: {response[:100]}...")


if __name__ == "__main__":
    main()