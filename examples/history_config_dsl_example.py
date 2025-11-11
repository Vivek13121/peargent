"""
Example: HistoryConfig DSL - Clean and Simple Configuration

This example demonstrates the improved HistoryConfig DSL that intelligently
handles which parameters are needed based on your strategy.

Key improvements:
1. No need to specify summarize_model for trim strategies
2. Auto-warning if you specify unnecessary parameters
3. Falls back to agent's model for summarization if not specified
4. Clean, intuitive API
"""

from peargent import create_agent, HistoryConfig, File, Sqlite
from peargent.core.history.storage_types import SessionBuffer
from peargent.models import groq


def example_1_trim_strategy():
    """Example 1: Trim strategy - NO summarize_model needed!"""
    print("\n" + "="*60)
    print("Example 1: Trim Strategy (Cleanest Config)")
    print("="*60)

    # Clean config - only specify what you need!
    agent = create_agent(
        name="Assistant",
        description="A helpful assistant",
        persona="You are a helpful AI assistant.",
        model=groq("llama-3.3-70b-versatile"),
        tools=[],
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=15,
            strategy="trim_last",  # Trim doesn't need summarize_model!
            store=SessionBuffer()
        )
    )

    print("✅ Created agent with trim strategy")
    print("✅ No summarize_model needed - trim is LLM-free!")
    print(f"\nConfig: {agent.history}")


def example_2_smart_strategy_auto_model():
    """Example 2: Smart strategy - auto-uses agent's model for summarization."""
    print("\n" + "="*60)
    print("Example 2: Smart Strategy (Auto Model)")
    print("="*60)

    # Smart strategy will use agent's model when it needs to summarize
    agent = create_agent(
        name="Assistant",
        description="A helpful assistant",
        persona="You are a helpful AI assistant.",
        model=groq("llama-3.3-70b-versatile"),
        tools=[],
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=20,
            strategy="smart",  # Will auto-use agent's model for summarization
            store=File(storage_dir="./smart_conversations")
        )
    )

    print("✅ Created agent with smart strategy")
    print("✅ Will use agent's model (llama-3.3-70b) for summarization")
    print("✅ No need to specify summarize_model explicitly!")


def example_3_explicit_summarize_model():
    """Example 3: Explicit summarize model for better cost optimization."""
    print("\n" + "="*60)
    print("Example 3: Explicit Summarize Model (Cost Optimization)")
    print("="*60)

    # Use a cheaper/faster model for summarization
    agent = create_agent(
        name="Assistant",
        description="A helpful assistant",
        persona="You are a helpful AI assistant.",
        model=groq("llama-3.3-70b-versatile"),  # Expensive main model
        tools=[],
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=20,
            strategy="smart",
            summarize_model=groq("llama-3.1-8b-instant"),  # Cheaper for summaries!
            store=Sqlite(database_path="./optimized_chat.db")
        )
    )

    print("✅ Created agent with separate summarize model")
    print("✅ Main: llama-3.3-70b (high quality responses)")
    print("✅ Summary: llama-3.1-8b-instant (fast & cheap)")
    print("💰 Cost optimized!")


def example_4_warning_demo():
    """Example 4: Warning when summarize_model is unnecessary."""
    print("\n" + "="*60)
    print("Example 4: Unnecessary Parameter Warning")
    print("="*60)

    print("\n⚠️  This config will trigger a warning:")
    print("   - strategy='trim_last' doesn't need summarize_model")
    print("   - But summarize_model is provided anyway\n")

    # This will show a warning
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        agent = create_agent(
            name="Assistant",
            description="A helpful assistant",
            persona="You are helpful.",
            model=groq("llama-3.3-70b-versatile"),
            tools=[],
            history=HistoryConfig(
                auto_manage_context=True,
                max_context_messages=15,
                strategy="trim_last",  # Doesn't need LLM
                summarize_model=groq("llama-3.1-8b-instant"),  # Unnecessary!
                store=SessionBuffer()
            )
        )

        if w:
            print(f"⚠️  Warning shown: {w[0].message}")
            print("\n💡 Fix: Remove summarize_model from config")


def example_5_comparison():
    """Example 5: Compare all strategies."""
    print("\n" + "="*60)
    print("Example 5: Strategy Comparison")
    print("="*60)

    print("\n📊 Strategy Guide:")
    print("\n1. trim_last (Simple & Fast)")
    print("   - Removes oldest messages")
    print("   - No LLM needed (free!)")
    print("   - Good for: Simple chats, cost-sensitive apps")
    print("   Config:")
    print("   HistoryConfig(strategy='trim_last', store=SessionBuffer())")

    print("\n2. trim_first (Keep History)")
    print("   - Removes newest messages, keeps old context")
    print("   - No LLM needed (free!)")
    print("   - Good for: When early context is important")
    print("   Config:")
    print("   HistoryConfig(strategy='trim_first', store=SessionBuffer())")

    print("\n3. summarize (Preserve Context)")
    print("   - Summarizes old messages with LLM")
    print("   - Uses LLM (costs tokens)")
    print("   - Good for: Long conversations where context matters")
    print("   Config:")
    print("   HistoryConfig(strategy='summarize', summarize_model=groq(), store=SessionBuffer())")

    print("\n4. smart (Best of Both)")
    print("   - Auto-chooses between trim and summarize")
    print("   - Small overflow → trim (free)")
    print("   - Large overflow → summarize (preserves context)")
    print("   - Good for: General use, auto-optimization")
    print("   Config:")
    print("   HistoryConfig(strategy='smart', store=SessionBuffer())")


def example_6_minimal_configs():
    """Example 6: Minimal configs for common use cases."""
    print("\n" + "="*60)
    print("Example 6: Minimal Configs (Copy & Paste Ready)")
    print("="*60)

    print("\n# Multi-user web app (trim for speed)")
    print("""
agent = create_agent(
    name="ChatBot",
    description="Web chatbot",
    persona="You are helpful",
    model=groq(),
    history=HistoryConfig(
        auto_manage_context=True,
        max_context_messages=15,
        strategy="trim_last",
        store=Sqlite(database_path="./webapp.db")
    )
)
""")

    print("\n# Knowledge assistant (smart context)")
    print("""
agent = create_agent(
    name="KnowledgeBot",
    description="Research assistant",
    persona="You are a research assistant",
    model=groq("llama-3.3-70b-versatile"),
    history=HistoryConfig(
        auto_manage_context=True,
        max_context_messages=30,
        strategy="smart",  # Auto uses agent's model
        store=File(storage_dir="./research")
    )
)
""")

    print("\n# Cost-optimized assistant (cheap summaries)")
    print("""
agent = create_agent(
    name="CostOptimized",
    description="Budget-friendly assistant",
    persona="You are helpful",
    model=groq("llama-3.3-70b-versatile"),  # Premium model
    history=HistoryConfig(
        auto_manage_context=True,
        max_context_messages=25,
        strategy="smart",
        summarize_model=groq("llama-3.1-8b-instant"),  # Budget model
        store=Sqlite()
    )
)
""")


def main():
    """Run all examples."""
    print("=" * 60)
    print("HistoryConfig DSL Examples - Clean & Simple!")
    print("=" * 60)

    # Example 1: Trim strategy (no summarize_model)
    example_1_trim_strategy()

    # Example 2: Smart strategy (auto model)
    example_2_smart_strategy_auto_model()

    # Example 3: Explicit summarize model
    example_3_explicit_summarize_model()

    # Example 4: Warning demo
    example_4_warning_demo()

    # Example 5: Comparison
    example_5_comparison()

    # Example 6: Minimal configs
    example_6_minimal_configs()

    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
    print("\n📚 Key Takeaways:")
    print("1. Trim strategies DON'T need summarize_model")
    print("2. Smart/summarize auto-use agent's model if not specified")
    print("3. Specify summarize_model only for cost optimization")
    print("4. HistoryConfig warns about unnecessary parameters")
    print("5. Choose strategy based on your needs (see comparison)")
    print("\n✨ The DSL is now cleaner and smarter!")


if __name__ == "__main__":
    main()
