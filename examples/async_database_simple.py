"""
Simple example of async database tracing.

Shows how easy it is to enable non-blocking database writes.
"""

from peargent import create_agent
from peargent.telemetry import enable_tracing
from peargent.models import groq


def main():
    print("Async Database Tracing - Simple Example")
    print("=" * 60)

    # Enable async database writes - just add async_db=True!
    tracer = enable_tracing(
        store_type="sqlite",
        connection_string="sqlite:///./async_example.db",
        async_db=True,        # ← This enables async writes
        num_workers=2,
        enabled=True
    )

    print("[OK] Async tracing enabled")
    print(f"  Store: {type(tracer.store).__name__}")
    print(f"  Workers: 2")
    print()

    # Create agent
    agent = create_agent(
        name="example_agent",
        description="Example agent with async tracing",
        persona="You are helpful. Answer briefly.",
        model=groq("llama-3.3-70b-versatile"),
        tracing=True
    )

    # Run agent - database writes happen in background!
    print("Running agent queries (non-blocking writes)...")
    for i in range(3):
        result = agent.run(f"What is {i} times 2? Answer in one word.")
        print(f"  Query {i+1}: {result}")

    print()
    print("[OK] All queries completed!")
    print(f"  Pending writes in queue: {tracer.store._write_queue.qsize()}")

    # Wait for all writes to complete
    print("\nFlushing pending writes...")
    tracer.store.flush()
    print("[OK] All writes completed!")

    # Check database
    traces = tracer.list_traces()
    print(f"\n[OK] Traces in database: {len(traces)}")

    # Shutdown gracefully
    tracer.store.shutdown()
    print("\n[OK] Async store shutdown complete")

    print("\n" + "=" * 60)
    print("KEY TAKEAWAY:")
    print("  Just add async_db=True to enable_tracing() for")
    print("  non-blocking database writes. That's it!")
    print("=" * 60)


if __name__ == "__main__":
    main()
