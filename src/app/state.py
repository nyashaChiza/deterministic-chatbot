class State:
    def __init__(self):
        self.state = {}

    def get_state(self, id: str) -> str | None:
        """Retrieve the current state for a given id."""
        return self.state.get(id)

    def set_state(self, id: str, state: str) -> None:
        """Set the state for a given id."""
        self.state[id] = state

    def clear_state(self, id: str) -> None:
        """Clear the state for a given id."""
        if id in self.state:
            del self.state[id]

    def clear_all(self) -> None:
        """Clear all states."""
        self.state.clear()