
import requests
from unittest.mock import Mock, patch, call

# Import the REAL function from your project
from src.scrapers.retailers.sigma import fetch_page


def test_fetch_page_retries_after_timeouts():
    # Step 1: Create a fake successful HTTP response
    mock_response = Mock(status_code=200)

    # Step 2: Simulate two timeouts, then success
    mock_get = Mock(
        side_effect=[
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            mock_response
        ]
    )

    # Step 3: Replace real network requests and sleeping
    with patch("requests.get", mock_get), patch("time.sleep") as mock_sleep:

        # Step 4: Call your ACTUAL fetch_page function
        response = fetch_page("https://example.com")

        # Step 5: Verify its behavior
        assert response is mock_response
        assert mock_get.call_count == 3
        assert mock_sleep.call_args_list == [call(2), call(4)]

def test_fetch_page_stops_on_404():
    mock_response = Mock(status_code=404)

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError(response=mock_response)
    )

    mock_get = Mock(return_value=mock_response)

    with patch("requests.get", mock_get), patch("time.sleep") as mock_sleep:
        result = fetch_page("https://example.com/missing")

        # YOUR ASSERTIONS HERE
def test_fetch_page_exhausts_retries_on_503():
    mock_response = Mock(status_code=503)

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError(response=mock_response)
    )

    mock_get = Mock(return_value=mock_response)

    with patch("requests.get", mock_get), patch("time.sleep") as mock_sleep:
        result = fetch_page("https://example.com")

        # Your assertions here
        assert mock_get.call_count == 4
        assert mock_sleep.call_args_list == [call(2), call(4), call(8)]        