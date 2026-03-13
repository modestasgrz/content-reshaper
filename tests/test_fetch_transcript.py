from unittest.mock import patch

import pytest

from reshaper import fetch_transcript


class TestFetchTranscript:
    def test_joins_transcript_entries(self) -> None:
        mock_entries = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "world", "start": 1.0, "duration": 1.0},
        ]
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.get_transcript.return_value = mock_entries
            result = fetch_transcript("dQw4w9WgXcQ")

        assert result == "Hello world"

    def test_single_entry(self) -> None:
        mock_entries = [{"text": "Only line", "start": 0.0, "duration": 2.0}]
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.get_transcript.return_value = mock_entries
            result = fetch_transcript("abc123")

        assert result == "Only line"

    def test_passes_video_id_to_api(self) -> None:
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.get_transcript.return_value = []
            fetch_transcript("test_id")

        mock_api.get_transcript.assert_called_once_with("test_id")

    def test_propagates_api_error(self) -> None:
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.get_transcript.side_effect = Exception("Transcript unavailable")
            with pytest.raises(Exception, match="Transcript unavailable"):
                fetch_transcript("bad_id")
