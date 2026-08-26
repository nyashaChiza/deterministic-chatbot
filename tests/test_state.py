from src.app.state import MemoryState


def test_set_and_get_state():
    state = MemoryState()
    state.set_state("user1", {"intent": "greeting"})
    assert state.get_state("user1") == {"intent": "greeting"}


def test_get_state_missing_user_returns_none():
    state = MemoryState()
    assert state.get_state("missing") is None


def test_set_state_overwrites_existing_value():
    state = MemoryState()
    state.set_state("user1", {"intent": "greeting"})
    state.set_state("user1", {"intent": "good_bye"})
    assert state.get_state("user1") == {"intent": "good_bye"}


def test_clear_state_removes_single_user():
    state = MemoryState()
    state.set_state("user1", {"intent": "greeting"})
    state.set_state("user2", {"intent": "greeting"})
    state.clear_state("user1")
    assert state.get_state("user1") is None
    assert state.get_state("user2") == {"intent": "greeting"}


def test_clear_state_missing_user_is_noop():
    state = MemoryState()
    state.clear_state("missing")  # should not raise
    assert state.get_all() == {}


def test_clear_all_removes_every_user():
    state = MemoryState()
    state.set_state("user1", {"a": 1})
    state.set_state("user2", {"b": 2})
    state.clear_all()
    assert state.get_all() == {}


def test_get_all_returns_every_user_state():
    state = MemoryState()
    state.set_state("user1", {"a": 1})
    state.set_state("user2", {"b": 2})
    assert state.get_all() == {"user1": {"a": 1}, "user2": {"b": 2}}
