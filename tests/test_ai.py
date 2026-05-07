import pytest
import os
from unittest.mock import MagicMock, patch
from my_bot.ai_logic import get_new_chat


@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_get_new_chat_success(mock_model_class, mock_configure):
    """Gemini Chat Successful Initialization Test."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance

        expected_chat = MagicMock()
        mock_model_instance.start_chat.return_value = expected_chat

        chat = get_new_chat()

        mock_configure.assert_called_once_with(api_key="fake_key")
        mock_model_instance.start_chat.assert_called_once_with(history=[])
        assert chat == mock_model_instance.start_chat.return_value


def test_get_new_chat_no_api_key():
    """Test for error when API key is missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY not found"):
            get_new_chat()
