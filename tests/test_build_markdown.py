from reshaper import build_markdown

RESULTS = {
    "blog_post": "Blog content",
    "twitter_thread": "Twitter content",
    "linkedin_post": "LinkedIn content",
    "email_newsletter": "Email content",
    "summary": "Summary content",
}


class TestBuildMarkdown:
    def test_output_structure(self) -> None:
        output = build_markdown("dQw4w9WgXcQ", RESULTS)

        assert "# Repurposed Content" in output
        assert "dQw4w9WgXcQ" in output
        assert "## Blog Post" in output
        assert "## Twitter Thread" in output
        assert "## LinkedIn Post" in output
        assert "## Email Newsletter" in output
        assert "## Summary" in output
        for content in RESULTS.values():
            assert content in output
        assert "---" in output
        assert output.endswith("\n")
