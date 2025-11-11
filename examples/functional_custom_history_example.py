"""
Example: Creating Custom History Storage with Functions

This example demonstrates how to create custom storage backends using simple
functions instead of subclassing HistoryStore. This is the EASIEST way to
create custom backends!

Two approaches are shown:
1. FunctionalHistoryStore: Define simple functions (NEW - easy!)
2. Subclassing HistoryStore: Full class implementation (advanced)

Use FunctionalHistoryStore when:
- You want quick prototyping
- Your storage logic is simple
- You prefer functional programming
- You want minimal boilerplate

Use Subclassing when:
- You need complex initialization
- You want to add custom methods
- You need class-based organization
- You're building a reusable library
"""

from peargent import create_agent, ConversationHistory, FunctionalHistoryStore, HistoryConfig
from peargent.core.history import Thread, Message
from peargent.models import groq


def example_1_simple_dict_storage():
    """Example 1: Simplest custom storage - in-memory dict using functions."""
    print("\n" + "="*60)
    print("Example 1: Simple Dictionary Storage (Functional)")
    print("="*60)

    # Your custom storage (could be Redis, MongoDB, etc.)
    storage = {}

    # Define your storage functions
    def create_thread(metadata=None):
        """Create a new thread."""
        thread = Thread(metadata=metadata)
        storage[thread.id] = thread
        print(f"  📝 Created thread: {thread.id}")
        return thread.id

    def get_thread(thread_id):
        """Get a thread by ID."""
        return storage.get(thread_id)

    def append_message(thread_id, role, content, agent=None, tool_call=None, metadata=None):
        """Add a message to a thread."""
        thread = storage.get(thread_id)
        if not thread:
            raise ValueError(f"Thread {thread_id} not found")

        msg = Message(
            role=role,
            content=content,
            agent=agent,
            tool_call=tool_call,
            metadata=metadata
        )
        thread.add_message(msg)
        print(f"  💬 Added {role} message")
        return msg

    def get_messages(thread_id):
        """Get all messages in a thread."""
        thread = storage.get(thread_id)
        return thread.messages if thread else []

    def list_threads():
        """List all thread IDs."""
        return list(storage.keys())

    def delete_thread(thread_id):
        """Delete a thread."""
        deleted = storage.pop(thread_id, None) is not None
        if deleted:
            print(f"  🗑️ Deleted thread: {thread_id}")
        return deleted

    # Create functional store - just pass your functions!
    store = FunctionalHistoryStore(
        create_thread_fn=create_thread,
        get_thread_fn=get_thread,
        append_message_fn=append_message,
        get_messages_fn=get_messages,
        list_threads_fn=list_threads,
        delete_thread_fn=delete_thread
    )

    # Use with ConversationHistory
    history = ConversationHistory(store=store)

    # Create agent using HistoryConfig DSL
    agent = create_agent(
        name="Assistant",
        description="A helpful assistant",
        persona="You are a helpful AI assistant.",
        model=groq("llama-3.3-70b-versatile"),
        tools=[],
        history=HistoryConfig(
            auto_manage_context=True,
            max_context_messages=12,
            strategy="smart",
            summarize_model=groq("llama-3.1-8b-instant"),
            store=history  # Use custom functional store
        )
    )

    # Have conversation
    print("\n--- Conversation ---")
    response1 = agent.run("Hi! My name is Bob.")
    print(f"Agent: {response1[:100]}...")

    response2 = agent.run("What's my name?")
    print(f"Agent: {response2[:100]}...")

    print(f"\n✅ Storage contains {len(storage)} thread(s)")
    print(f"✅ Thread has {len(history.get_messages())} messages")


def example_2_mongodb_style():
    """Example 2: MongoDB-style storage using functions."""
    print("\n" + "="*60)
    print("Example 2: MongoDB-Style Storage (Functional)")
    print("="*60)

    # Simulate MongoDB collections
    class FakeMongoClient:
        def __init__(self):
            self.threads_collection = {}
            self.messages_collection = {}

        def insert_thread(self, thread_data):
            thread_id = thread_data['id']
            self.threads_collection[thread_id] = thread_data
            return thread_id

        def find_thread(self, thread_id):
            return self.threads_collection.get(thread_id)

        def insert_message(self, thread_id, message_data):
            if thread_id not in self.messages_collection:
                self.messages_collection[thread_id] = []
            self.messages_collection[thread_id].append(message_data)

        def find_messages(self, thread_id):
            return self.messages_collection.get(thread_id, [])

        def delete_thread_data(self, thread_id):
            thread_deleted = self.threads_collection.pop(thread_id, None) is not None
            self.messages_collection.pop(thread_id, None)
            return thread_deleted

        def list_thread_ids(self):
            return list(self.threads_collection.keys())

    # Create "MongoDB" client
    mongo = FakeMongoClient()

    # Define storage functions that use MongoDB
    def create_thread(metadata=None):
        thread = Thread(metadata=metadata)
        mongo.insert_thread(thread.to_dict())
        print(f"  📝 Inserted to MongoDB: {thread.id}")
        return thread.id

    def get_thread(thread_id):
        thread_data = mongo.find_thread(thread_id)
        if not thread_data:
            return None
        return Thread.from_dict(thread_data)

    def append_message(thread_id, role, content, agent=None, tool_call=None, metadata=None):
        # Verify thread exists
        if not mongo.find_thread(thread_id):
            raise ValueError(f"Thread {thread_id} not found")

        msg = Message(role=role, content=content, agent=agent,
                     tool_call=tool_call, metadata=metadata)
        mongo.insert_message(thread_id, msg.to_dict())
        print(f"  💬 Inserted message to MongoDB")
        return msg

    def get_messages(thread_id):
        messages_data = mongo.find_messages(thread_id)
        return [Message.from_dict(msg_data) for msg_data in messages_data]

    def list_threads():
        return mongo.list_thread_ids()

    def delete_thread(thread_id):
        return mongo.delete_thread_data(thread_id)

    # Create functional store
    store = FunctionalHistoryStore(
        create_thread_fn=create_thread,
        get_thread_fn=get_thread,
        append_message_fn=append_message,
        get_messages_fn=get_messages,
        list_threads_fn=list_threads,
        delete_thread_fn=delete_thread
    )

    history = ConversationHistory(store=store)

    # Create multiple threads
    print("\n--- Creating threads ---")
    thread1 = history.create_thread(metadata={"user": "alice", "topic": "python"})
    thread2 = history.create_thread(metadata={"user": "bob", "topic": "javascript"})

    # Add messages to different threads
    history.use_thread(thread1)
    history.add_user_message("How do I use decorators in Python?")
    history.add_assistant_message("Decorators wrap functions to modify behavior.")

    history.use_thread(thread2)
    history.add_user_message("Explain async/await in JavaScript")
    history.add_assistant_message("Async/await handles promises elegantly.")

    print(f"\n✅ MongoDB has {len(mongo.threads_collection)} threads")
    print(f"✅ Thread 1 has {len(mongo.find_messages(thread1))} messages")
    print(f"✅ Thread 2 has {len(mongo.find_messages(thread2))} messages")


def example_3_dynamodb_style():
    """Example 3: DynamoDB-style storage with partition/sort keys."""
    print("\n" + "="*60)
    print("Example 3: DynamoDB-Style Storage (Functional)")
    print("="*60)

    # Simulate DynamoDB table
    class FakeDynamoDB:
        def __init__(self):
            self.table = {}

        def put_item(self, pk, sk, data):
            """Put item with partition key and sort key."""
            key = f"{pk}#{sk}"
            self.table[key] = {"PK": pk, "SK": sk, "Data": data}

        def get_item(self, pk, sk):
            """Get item by keys."""
            key = f"{pk}#{sk}"
            item = self.table.get(key)
            return item["Data"] if item else None

        def query(self, pk):
            """Query all items with partition key."""
            results = []
            for key, item in self.table.items():
                if item["PK"] == pk:
                    results.append(item["Data"])
            return results

        def delete_item(self, pk, sk):
            """Delete item."""
            key = f"{pk}#{sk}"
            return self.table.pop(key, None) is not None

        def delete_by_pk(self, pk):
            """Delete all items with partition key."""
            keys_to_delete = [k for k, v in self.table.items() if v["PK"] == pk]
            for key in keys_to_delete:
                del self.table[key]
            return len(keys_to_delete) > 0

        def scan_threads(self):
            """Get all thread IDs."""
            thread_ids = set()
            for item in self.table.values():
                if item["SK"] == "METADATA":
                    thread_ids.add(item["PK"])
            return list(thread_ids)

    # Create DynamoDB table
    dynamo = FakeDynamoDB()

    # Define storage functions using DynamoDB pattern
    def create_thread(metadata=None):
        thread = Thread(metadata=metadata)
        # Store thread metadata with PK=thread_id, SK=METADATA
        dynamo.put_item(
            pk=thread.id,
            sk="METADATA",
            data=thread.to_dict()
        )
        print(f"  📝 Put item to DynamoDB: PK={thread.id}, SK=METADATA")
        return thread.id

    def get_thread(thread_id):
        thread_data = dynamo.get_item(pk=thread_id, sk="METADATA")
        if not thread_data:
            return None

        # Reconstruct thread with messages
        thread = Thread.from_dict(thread_data)

        # Query all messages for this thread
        all_items = dynamo.query(pk=thread_id)
        for item in all_items:
            if isinstance(item, dict) and item.get('role'):  # It's a message
                thread.messages.append(Message.from_dict(item))

        return thread

    def append_message(thread_id, role, content, agent=None, tool_call=None, metadata=None):
        # Verify thread exists
        if not dynamo.get_item(pk=thread_id, sk="METADATA"):
            raise ValueError(f"Thread {thread_id} not found")

        msg = Message(role=role, content=content, agent=agent,
                     tool_call=tool_call, metadata=metadata)

        # Store message with PK=thread_id, SK=MESSAGE#{timestamp}#{msg_id}
        dynamo.put_item(
            pk=thread_id,
            sk=f"MESSAGE#{msg.timestamp.isoformat()}#{msg.id}",
            data=msg.to_dict()
        )
        print(f"  💬 Put message to DynamoDB")
        return msg

    def get_messages(thread_id):
        thread = get_thread(thread_id)
        return thread.messages if thread else []

    def list_threads():
        return dynamo.scan_threads()

    def delete_thread(thread_id):
        return dynamo.delete_by_pk(pk=thread_id)

    # Create functional store
    store = FunctionalHistoryStore(
        create_thread_fn=create_thread,
        get_thread_fn=get_thread,
        append_message_fn=append_message,
        get_messages_fn=get_messages,
        list_threads_fn=list_threads,
        delete_thread_fn=delete_thread
    )

    history = ConversationHistory(store=store)

    # Use it
    print("\n--- Using DynamoDB storage ---")
    thread_id = history.create_thread(metadata={"app": "chatbot"})
    history.add_user_message("Hello DynamoDB!")
    history.add_assistant_message("Hello! Data stored with partition keys.")

    print(f"\n✅ DynamoDB has {len(dynamo.table)} items")
    print(f"✅ Thread has {len(history.get_messages())} messages")


def example_4_comparison():
    """Example 4: Compare functional vs class-based approach."""
    print("\n" + "="*60)
    print("Example 4: Functional vs Class-Based Comparison")
    print("="*60)

    print("\n📊 Comparison:")
    print("\nFunctional Approach (FunctionalHistoryStore):")
    print("  ✅ Pros:")
    print("     - Less boilerplate code (~30 lines vs ~200 lines)")
    print("     - Easier to understand for beginners")
    print("     - Great for prototyping")
    print("     - No class inheritance needed")
    print("     - Works with any storage backend")
    print("\n  ⚠️  Cons:")
    print("     - Can't add custom methods easily")
    print("     - Less organized for complex logic")
    print("     - No shared state/initialization beyond closures")

    print("\nClass-Based Approach (Subclassing HistoryStore):")
    print("  ✅ Pros:")
    print("     - Full control and flexibility")
    print("     - Can add custom methods (e.g., get_stats())")
    print("     - Better for complex initialization")
    print("     - More organized for large backends")
    print("     - Better for library distribution")
    print("\n  ⚠️  Cons:")
    print("     - More boilerplate code")
    print("     - Steeper learning curve")
    print("     - Must implement all abstract methods")

    print("\n💡 Recommendation:")
    print("   - Quick prototype or simple backend? Use FunctionalHistoryStore")
    print("   - Building a library or complex backend? Subclass HistoryStore")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Functional Custom History Storage Examples")
    print("=" * 60)
    print("\n🎯 Create custom backends with simple functions!")

    # Example 1: Simple dictionary storage
    example_1_simple_dict_storage()

    # Example 2: MongoDB-style
    example_2_mongodb_style()

    # Example 3: DynamoDB-style
    example_3_dynamodb_style()

    # Example 4: Comparison
    example_4_comparison()

    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
    print("\n📚 Key Takeaways:")
    print("1. FunctionalHistoryStore = easiest way to create custom backends")
    print("2. Just define 6 functions and pass them in")
    print("3. Works with ANY storage: MongoDB, DynamoDB, Firebase, etc.")
    print("4. No need to subclass or understand inheritance")
    print("5. Perfect for prototyping and simple use cases")
    print("\n🚀 Next Steps:")
    print("   - Try with your own storage backend!")
    print("   - Combine with cloud services (AWS, GCP, Azure)")
    print("   - Add custom logic in your functions")


if __name__ == "__main__":
    main()
