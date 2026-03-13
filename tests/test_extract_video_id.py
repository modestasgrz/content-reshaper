import pytest

from reshaper import extract_video_id


class TestExtractVideoId:
    def test_youtu_be(self) -> None:
        assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_youtube_watch(self) -> None:
        assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_youtube_watch_no_www(self) -> None:
        assert extract_video_id("https://youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_youtube_shorts(self) -> None:
        assert extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_invalid_url_raises(self) -> None:
        with pytest.raises(ValueError, match="Cannot extract video ID"):
            extract_video_id("https://vimeo.com/123456")

    def test_invalid_domain_raises(self) -> None:
        with pytest.raises(ValueError, match="Cannot extract video ID"):
            extract_video_id("https://notasite.com/watch?v=dQw4w9WgXcQ")
