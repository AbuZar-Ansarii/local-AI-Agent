# Short-term memory management
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class ConversationBuffer:
    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.history = {}

    def get_history(self, user_id: int):
        if user_id not in self.history:
            self.history[user_id] = []
        return self.history[user_id]

    def add_message(self, user_id: int, message):
        if user_id not in self.history:
            self.history[user_id] = []
        self.history[user_id].append(message)
        if len(self.history[user_id]) > self.max_messages:
            self.history[user_id] = self.history[user_id][-self.max_messages:]

    def clear(self, user_id: int):
        self.history[user_id] = []

short_term_memory = ConversationBuffer()
