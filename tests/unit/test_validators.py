"""Unit tests for validators module."""

import pytest

from src.lib.validators import (
    validate_title,
    validate_description,
    validate_task_id,
    MAX_TITLE_LENGTH,
    MAX_DESCRIPTION_LENGTH,
)
from src.lib.exceptions import (
    EmptyTitleError,
    TitleTooLongError,
    DescriptionTooLongError,
    InvalidIDFormatError,
)


class TestValidateTitle:
    """Tests for validate_title function."""

    def test_valid_title(self):
        """Test that valid title is returned."""
        result = validate_title("Buy groceries")
        assert result == "Buy groceries"

    def test_title_trimmed(self):
        """Test that whitespace is trimmed."""
        result = validate_title("  Buy groceries  ")
        assert result == "Buy groceries"

    def test_empty_title_raises_error(self):
        """Test that empty string raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            validate_title("")

    def test_whitespace_title_raises_error(self):
        """Test that whitespace-only raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            validate_title("   ")

    def test_title_exactly_max_length(self):
        """Test that title of exactly MAX_TITLE_LENGTH is valid."""
        title = "x" * MAX_TITLE_LENGTH
        result = validate_title(title)
        assert len(result) == MAX_TITLE_LENGTH

    def test_title_exceeds_max_length(self):
        """Test that title > MAX_TITLE_LENGTH raises TitleTooLongError."""
        title = "x" * (MAX_TITLE_LENGTH + 1)
        with pytest.raises(TitleTooLongError):
            validate_title(title)


class TestValidateDescription:
    """Tests for validate_description function."""

    def test_valid_description(self):
        """Test that valid description is returned."""
        result = validate_description("Milk, eggs, bread")
        assert result == "Milk, eggs, bread"

    def test_empty_description_valid(self):
        """Test that empty description is valid."""
        result = validate_description("")
        assert result == ""

    def test_description_exactly_max_length(self):
        """Test that description of exactly MAX_DESCRIPTION_LENGTH is valid."""
        desc = "x" * MAX_DESCRIPTION_LENGTH
        result = validate_description(desc)
        assert len(result) == MAX_DESCRIPTION_LENGTH

    def test_description_exceeds_max_length(self):
        """Test that description > MAX_DESCRIPTION_LENGTH raises error."""
        desc = "x" * (MAX_DESCRIPTION_LENGTH + 1)
        with pytest.raises(DescriptionTooLongError):
            validate_description(desc)


class TestValidateTaskId:
    """Tests for validate_task_id function."""

    def test_valid_uppercase_id(self):
        """Test that valid uppercase ID is returned."""
        result = validate_task_id("T001")
        assert result == "T001"

    def test_lowercase_id_normalized(self):
        """Test that lowercase ID is normalized to uppercase."""
        result = validate_task_id("t001")
        assert result == "T001"

    def test_mixed_case_normalized(self):
        """Test that mixed case is normalized."""
        result = validate_task_id("T001")
        assert result == "T001"

    def test_single_digit_valid(self):
        """Test that single digit ID is valid."""
        result = validate_task_id("T1")
        assert result == "T1"

    def test_large_number_valid(self):
        """Test that large number ID is valid."""
        result = validate_task_id("T12345")
        assert result == "T12345"

    def test_invalid_prefix_raises_error(self):
        """Test that wrong prefix raises InvalidIDFormatError."""
        with pytest.raises(InvalidIDFormatError):
            validate_task_id("X001")

    def test_no_number_raises_error(self):
        """Test that ID without number raises error."""
        with pytest.raises(InvalidIDFormatError):
            validate_task_id("T")

    def test_letters_in_number_raises_error(self):
        """Test that letters in number part raises error."""
        with pytest.raises(InvalidIDFormatError):
            validate_task_id("Tabc")

    def test_empty_string_raises_error(self):
        """Test that empty string raises error."""
        with pytest.raises(InvalidIDFormatError):
            validate_task_id("")

    def test_no_prefix_raises_error(self):
        """Test that number without T prefix raises error."""
        with pytest.raises(InvalidIDFormatError):
            validate_task_id("001")
