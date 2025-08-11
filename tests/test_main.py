# tests/test_main.py
import importlib


def test_main_module() -> None:
    """Test that __main__ module can be imported and executed"""
    # Import the module
    main = importlib.import_module("c4py.__main__")
    assert main is not None
