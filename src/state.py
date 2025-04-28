
class State:
    def __init__(self):
        self.state = {}

    def get_state(self, id) -> str:
        return self.state.get(id, None)
    
    def add_state(self, id, state) -> None:
        self.state[id] = state