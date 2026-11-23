from sys import exc_info
import time
import pytest
import requests
from unittest.mock import Mock, patch, call

# Import the REAL function from your project
from src.scrapers.retailers.sigma import SigmaScraper
sigma_scraper = SigmaScraper()


def test_fetch_page_stops_on_404():
    mock_response = Mock(status_code=404)

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError(response=mock_response)
    )

    mock_get = Mock(return_value=mock_response)

    with patch("requests.get", mock_get), patch("time.sleep") as mock_sleep:
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            sigma_scraper.fetch_page("https://example.com/missing")

        assert exc_info.value.response.status_code == 404
        assert mock_get.call_count == 1
        assert mock_sleep.call_count == 0


def test_fetch_page_retries_after_timeouts():
    mock_response = Mock(status_code=200)

    mock_get = Mock(
        side_effect=[
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            mock_response
        ]
    )

    with patch("requests.get", mock_get), patch("time.sleep") as mock_sleep:
        response = sigma_scraper.fetch_page("https://example.com")

        assert response is mock_response
        assert mock_get.call_count == 3
        assert mock_sleep.call_args_list == [
            call(2),
            call(4)
        ]



def test_fetch_page_exhausts_retries_on_503():
    mock_response = Mock(status_code=503)

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError(response=mock_response)
    )

    mock_get = Mock(return_value=mock_response)

    with patch("requests.get", mock_get), patch("time.sleep") as mock_sleep:
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            sigma_scraper.fetch_page("https://example.com")

        assert exc_info.value.response.status_code == 503
        assert mock_get.call_count == 4
        assert mock_sleep.call_args_list == [call(2), call(4), call(8)]

