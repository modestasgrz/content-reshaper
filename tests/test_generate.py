from unittest.mock import AsyncMock, MagicMock

import pytest

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

    async def test_asserts_on_none_response_text(self) -> None:
        mock_response = MagicMock()
        mock_response.text = None

        client = MagicMock()
        client.aio.models.generate_content = AsyncMock(return_value=mock_response)

        with pytest.raises(AssertionError):
            await generate(client, "prompt", "transcript")
