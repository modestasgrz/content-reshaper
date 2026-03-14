from unittest.mock import AsyncMock, MagicMock

import pytest
from google.genai.errors import APIError

from reshaper import generate


class TestGenerate:
    async def test_generate(self) -> None:
        mock_response = MagicMock()
        mock_response.text = "Generated content"

        client = MagicMock()
        client.aio.models.generate_content = AsyncMock(return_value=mock_response)

        result = await generate(client, "My prompt", "My transcript")

        assert result == "Generated content"
        call_kwargs = client.aio.models.generate_content.call_args
        assert "My prompt\n\nMy transcript" in call_kwargs.kwargs["contents"]

    async def test_raises_on_none_response_text(self) -> None:
        mock_response = MagicMock()
        mock_response.text = None

        client = MagicMock()
        client.aio.models.generate_content = AsyncMock(return_value=mock_response)

        with pytest.raises(RuntimeError, match="Gemini returned an empty response"):
            await generate(client, "prompt", "transcript")

    async def test_raises_runtime_error_on_api_error(self) -> None:
        client = MagicMock()
        client.aio.models.generate_content = AsyncMock(
            side_effect=APIError(500, {"error": {"message": "quota exceeded", "status": "RESOURCE_EXHAUSTED", "details": []}})
        )

        with pytest.raises(RuntimeError, match="Gemini API error"):
            await generate(client, "prompt", "transcript")
