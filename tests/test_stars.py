"""Tests for stars validation logic."""

import pytest
from src.bmi.logic.stars import validate_stars


def test_validate_stars_negative():
    """Test that negative values are clamped to 0."""
    assert validate_stars(-1) == 0


def test_validate_stars_zero():
    """Test that zero is valid."""
    assert validate_stars(0) == 0


def test_validate_stars_middle():
    """Test that middle values pass through."""
    assert validate_stars(5) == 5


def test_validate_stars_max():
    """Test that max value (10) is valid."""
    assert validate_stars(10) == 10


def test_validate_stars_over_max():
    """Test that values over 10 are clamped to 10."""
    assert validate_stars(11) == 10


def test_validate_stars_string_valid():
    """Test that valid numeric strings are converted."""
    assert validate_stars("7") == 7
    assert validate_stars(" 7 ") == 7


def test_validate_stars_string_invalid():
    """Test that invalid strings raise ValueError."""
    with pytest.raises(ValueError, match="not an integer string"):
        validate_stars("x")


def test_validate_stars_none_typeerror():
    """None should raise TypeError."""
    with pytest.raises(TypeError):
        validate_stars(None)


def test_validate_stars_booleans_typeerror():
    """Booleans are not valid (bool is subclass of int)."""
    with pytest.raises(TypeError):
        validate_stars(True)
    with pytest.raises(TypeError):
        validate_stars(False)


def test_validate_stars_floats_and_float_strings_rejected():
    """Floats and float-like strings are not accepted in strict policy."""
    with pytest.raises(TypeError):
        validate_stars(7.5)
    with pytest.raises(ValueError):
        validate_stars("7.5")
    with pytest.raises(ValueError):
        validate_stars("7.0")


def test_validate_stars_large_values_clamped():
    """Extremely large and small ints are clamped correctly."""
    assert validate_stars(10**9) == 10
    assert validate_stars(-10**9) == 0


def test_validate_stars_other_types_rejected():
    """Lists, dicts, etc. should raise TypeError."""
    with pytest.raises(TypeError):
        validate_stars([])
    with pytest.raises(TypeError):
        validate_stars({})
