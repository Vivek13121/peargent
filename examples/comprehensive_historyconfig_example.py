"""
Comprehensive examples showing the new HistoryConfig DSL in different scenarios.

This demonstrates various HistoryConfig patterns and use cases.
"""

from peargent import create_agent, create_pool, HistoryConfig, File, Memory, Sqlite, Postgresql
from peargent.models import groq
import os


def example_1_basic_historyconfig():
    """Example 1: Basic HistoryConfig patterns."""
    print("\n" + "="*60)
    print("Example 1: Basic HistoryConfig Patterns")
    print("="*60)

    # Pattern 1: Smart strategy with file storage
    print("\n--- Pattern 1: Smart + File Storage ---")
    agent1 = create_agent(
        name="FileAgent",
        description="Agent with file-based history",
        persona="You are helpful and remember conversations across sessions.",
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=8,
            strategy="smart",
            summarize_model=groq("llama-3.1-8b-instant"),
            store=File(storage_dir="./smart_conversations")
        )
    )
    
    response = agent1.run("Hello, I'm working on a Python project.")
    print(f"Response: {response[:100]}...")
    
    # Pattern 2: Trim strategy with memory
    print("\n--- Pattern 2: Trim + Memory Storage ---")
    agent2 = create_agent(
        name="MemoryAgent", 
        description="Agent with memory-only history",
        persona="You are efficient and focused.",
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=5,
            strategy="trim_last",  # Always trim, no summarization
            store=SessionBuffer()
        )
    )
    
    response = agent2.run("Tell me about machine learning.")
    print(f"Response: {response[:100]}...")

    # Pattern 3: No auto-management
    print("\n--- Pattern 3: Manual Management ---")
    agent3 = create_agent(
        name="ManualAgent",
        description="Agent with manual history management",
        persona="You are thorough and detailed.", 
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=False,  # Manual management
            store=SessionBuffer()
        )
    )
    
    response = agent3.run("Explain quantum computing.")
    print(f"Response: {response[:100]}...")


def example_2_database_patterns():
    """Example 2: Database storage patterns."""
    print("\n" + "="*60)
    print("Example 2: Database Storage Patterns")
    print("="*60)

    # SQLite pattern
    print("\n--- SQLite Pattern ---")
    sqlite_agent = create_agent(
        name="SQLiteAgent",
        description="Agent with SQLite history",
        persona="You are reliable and persistent.",
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=12,
            strategy="summarize",  # Always summarize for database efficiency
            summarize_model=groq("llama-3.1-8b-instant"),
            store=Sqlite(
                database_path="./agent_conversations.db",
                table_prefix="chat"
            )
        )
    )
    
    response = sqlite_agent.run("I'm learning about databases.")
    print(f"SQLite Agent: {response[:100]}...")

    # PostgreSQL pattern (if connection string available)
    connection_string = os.getenv("DATABASE_URL")
    if connection_string:
        print("\n--- PostgreSQL Pattern ---")
        pg_agent = create_agent(
            name="PostgreSQLAgent",
            description="Agent with PostgreSQL history",
            persona="You are enterprise-ready and scalable.",
            model=groq("llama-3.3-70b-versatile"),
            history=HistoryConfig(
                auto_manage_context=True,
                max_context_messages=20,
                strategy="smart",
                summarize_model=groq("llama-3.1-8b-instant"),
                store=Postgresql(
                    connection_string=connection_string,
                    table_prefix="enterprise"
                )
            )
        )
        
        response = pg_agent.run("Tell me about scalable systems.")
        print(f"PostgreSQL Agent: {response[:100]}...")
    else:
        print("\n--- PostgreSQL Pattern: Skipped (no DATABASE_URL) ---")


def example_3_pool_configurations():
    """Example 3: Pool configurations with HistoryConfig."""
    print("\n" + "="*60) 
    print("Example 3: Pool Configurations")
    print("="*60)

    # Create agents for the pool
    researcher = create_agent(
        name="Researcher",
        description="Research specialist",
        persona="You research topics thoroughly.",
        model=groq("llama-3.3-70b-versatile")
    )
    
    writer = create_agent(
        name="Writer", 
        description="Content writer",
        persona="You write clear, engaging content.",
        model=groq("llama-3.3-70b-versatile")
    )

    # Pool with shared history configuration
    print("\n--- Pool with Shared History ---")
    pool = create_pool(
        agents=[researcher, writer],
        max_iter=3,
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=10,
            strategy="smart",
            summarize_model=groq("llama-3.1-8b-instant"),
            store=File(storage_dir="./pool_conversations")
        )
    )
    
    result = pool.run("Research renewable energy and write a brief summary.")
    print(f"Pool Result: {result[:150]}...")


def example_4_strategy_comparison():
    """Example 4: Compare different context strategies."""
    print("\n" + "="*60)
    print("Example 4: Context Strategy Comparison")  
    print("="*60)

    strategies = [
        ("smart", "Intelligently chooses between trim and summarize"),
        ("trim_last", "Always keeps recent messages, discards old ones"),
        ("trim_first", "Always keeps first messages, discards recent ones"), 
        ("summarize", "Always creates summaries of old messages")
    ]

    agents = {}
    
    for strategy, description in strategies:
        print(f"\n--- {strategy.upper()} Strategy ---")
        print(f"Description: {description}")
        
        agent = create_agent(
            name=f"{strategy.title()}Agent",
            description=f"Agent using {strategy} strategy",
            persona="You are helpful and demonstrate context management.",
            model=groq("llama-3.3-70b-versatile"),
            history=HistoryConfig(
                auto_manage_context=True,
                max_context_messages=6,  # Small for demonstration
                strategy=strategy,
                summarize_model=groq("llama-3.1-8b-instant"),
                store=SessionBuffer()
            )
        )
        
        # Have a brief conversation
        agent.run("Hello, I'm testing context strategies.")
        agent.run("Tell me about artificial intelligence.")
        response = agent.run("What did we discuss before?")
        
        print(f"Agent response: {response[:120]}...")
        agents[strategy] = agent

    print(f"\n✅ Created {len(agents)} agents with different strategies")


def example_5_advanced_configurations():
    """Example 5: Advanced HistoryConfig patterns."""
    print("\n" + "="*60)
    print("Example 5: Advanced Configurations")
    print("="*60)

    # High-throughput configuration
    print("\n--- High-Throughput Config ---")
    high_throughput = create_agent(
        name="HighThroughputAgent",
        description="Optimized for high message volume", 
        persona="You handle lots of messages efficiently.",
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=30,  # Higher threshold
            strategy="trim_last",      # Fast trimming
            store=SessionBuffer()            # Fast memory storage
        )
    )
    
    print("Config: High message limit, fast trimming, memory storage")

    # Long-term memory configuration  
    print("\n--- Long-Term Memory Config ---")
    long_term = create_agent(
        name="LongTermAgent",
        description="Preserves conversation context over time",
        persona="You remember important details from long conversations.", 
        model=groq("llama-3.3-70b-versatile"),
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=15,
            strategy="summarize",     # Always preserve context via summaries
            summarize_model=groq("llama-3.1-8b-instant"), # Fast summarization
            store=File(storage_dir="./longterm_memory")
        )
    )
    
    print("Config: Moderate limit, always summarize, persistent storage")

    # Low-resource configuration
    print("\n--- Low-Resource Config ---")
    low_resource = create_agent(
        name="LowResourceAgent", 
        description="Optimized for minimal resource usage",
        persona="You are efficient with limited resources.",
        model=groq("llama-3.1-8b-instant"),  # Smaller model
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=8,   # Low threshold 
            strategy="trim_last",     # No LLM calls for summarization
            store=SessionBuffer()           # No I/O overhead
        )
    )
    
    print("Config: Low message limit, trim only, memory storage, small model")


def main():
    """Run all examples."""
    print("HistoryConfig DSL Comprehensive Examples")
    print("=" * 60)
    
    try:
        # Example 1: Basic patterns
        example_1_basic_historyconfig()
        
        # Example 2: Database patterns  
        example_2_database_patterns()
        
        # Example 3: Pool configurations
        example_3_pool_configurations()
        
        # Example 4: Strategy comparison
        example_4_strategy_comparison()
        
        # Example 5: Advanced configurations
        example_5_advanced_configurations()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)
        
        print("\n💡 Key Benefits of HistoryConfig DSL:")
        print("1. 📝 Single configuration object for all history settings")
        print("2. 🧠 Built-in context management with smart strategies") 
        print("3. 🔧 Easy to switch between storage backends")
        print("4. ⚡ Dedicated models for summarization performance")
        print("5. 🎛️  Fine-grained control over behavior")
        
        print("\n🎯 Choose Your Pattern:")
        print("• Smart + File: Best for most applications")
        print("• Trim + Memory: High-performance, temporary conversations")  
        print("• Summarize + Database: Long-term, scalable conversations")
        print("• Manual: Full control for specialized use cases")
        
    except Exception as e:
        print(f"\n❌ Error in examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()