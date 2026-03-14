from unittest.mock import patch

import pytest
from youtube_transcript_api import TranscriptsDisabled, VideoUnavailable

from reshaper import fetch_transcript


class TestFetchTranscript:
    def test_joins_transcript_entries(self) -> None:
        mock_entries = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "world", "start": 1.0, "duration": 1.0},
        ]
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.return_value.fetch.return_value.to_raw_data.return_value = mock_entries
            result = fetch_transcript("dQw4w9WgXcQ")

        assert result == "Hello world"

    def test_single_entry(self) -> None:
        mock_entries = [{"text": "Only line", "start": 0.0, "duration": 2.0}]
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.return_value.fetch.return_value.to_raw_data.return_value = mock_entries
            result = fetch_transcript("abc123")

        assert result == "Only line"

    def test_passes_video_id_to_api(self) -> None:
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.return_value.fetch.return_value.to_raw_data.return_value = []
            fetch_transcript("test_id")

        mock_api.return_value.fetch.assert_called_once_with("test_id")

    def test_raises_runtime_error_on_video_unavailable(self) -> None:
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.return_value.fetch.side_effect = VideoUnavailable("bad_id")
            with pytest.raises(RuntimeError, match="Could not fetch transcript for bad_id"):
                fetch_transcript("bad_id")

    def test_raises_runtime_error_on_transcripts_disabled(self) -> None:
        with patch("reshaper.YouTubeTranscriptApi") as mock_api:
            mock_api.return_value.fetch.side_effect = TranscriptsDisabled("bad_id")
            with pytest.raises(RuntimeError, match="Could not fetch transcript for bad_id"):
                fetch_transcript("bad_id")
