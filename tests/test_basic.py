"""Basic test to verify setup is working."""

def test_basic_functionality():
    """Test that our testing framework is working."""
    assert 1 + 1 == 2

def test_imports():
    """Test that we can import our modules"""
    try:
        import drift_detector
        assert True
    except ImportError:
        assert False, "Could not import drift_detector package"