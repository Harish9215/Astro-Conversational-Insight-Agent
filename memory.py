
class ConversationMemory:

    def __init__(self, max_turns=5):
        self.store = {}
        self.max_turns = max_turns

    def get_history(self, session_id):
        return self.store.get(session_id, [])

    def add_turn(self, session_id, user_message, assistant_message):

        if session_id not in self.store:
            self.store[session_id] = []

        self.store[session_id].append({
           
            "user": user_message,
            "assistant": assistant_message
        })

        print("MEMORY STATE:", self.store)

        # keep only last N turns
        if len(self.store[session_id]) > self.max_turns:
            self.store[session_id] = self.store[session_id][-self.max_turns:]