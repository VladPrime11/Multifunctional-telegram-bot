# utils/state_manager.py

class StateManager:
    def __init__(self):
        self.user_states = {}

    def set_state(self, user_id, state):
        self.user_states[user_id] = state

    def get_state(self, user_id):
        return self.user_states.get(user_id, 'OFF')
