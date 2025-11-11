from peargent import create_agent, HistoryConfig, File, create_history, SessionBuffer
from peargent.models import groq

def testing():
    
    # history = create_history(
    #     store_type="file",
    #     storage_dir="./conversations",
    # )
    
    # thread_id = history.create_thread(metadata={"purpose": "testing"})
    
    # print(f"Created Thread ID: {thread_id}")
    
    agent = create_agent(
        name="Steve",
        description="A helpful assistant",
        persona="You are a helpful AI assistant.",
        model=groq("llama-3.3-70b-versatile"),
        # history=HistoryConfig(
        #     auto_manage_context=True,
        #     max_context_messages=10,
        #     strategy="smart",  # Default smart strategy
        #     summarize_model=groq("llama-3.3-70b-versatile"),
        #     store=SessionBuffer()
        # )
    )
    
    result = agent.run("Hello, I am Tarun? What is your name?")
    print(result)
    # history = agent.history
    # thread_id = history.current_thread_id
    # print(f"Current Thread ID: {thread_id}")
    
    result = agent.run("Can you tell my name?")
    print(result)

if __name__ == "__main__":
    testing()
    