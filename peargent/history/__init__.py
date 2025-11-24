"""
History module for peargent.

Provides conversation history management with multiple storage backends.
"""

# Import base classes and storage implementations from peargent.storage
from peargent.storage import (
    Message,
    Thread,
    HistoryStore,
    FunctionalHistoryStore,
    InMemoryHistoryStore,
    FileHistoryStore,
    PostgreSQLHistoryStore,
    SQLiteHistoryStore,
    RedisHistoryStore,
)

# Export high-level interface
from .history import ConversationHistory

__all__ = [
    'Message',
    'Thread',
    'HistoryStore',
    'FunctionalHistoryStore',
    'InMemoryHistoryStore',
    'FileHistoryStore',
    'PostgreSQLHistoryStore',
    'SQLiteHistoryStore',
    'RedisHistoryStore',
    'ConversationHistory',
]
