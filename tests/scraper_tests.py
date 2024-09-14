"""Module contains tests for the Scraper class."""
from unittest.mock import Mock, patch

import pytest
import requests
from requests import HTTPError

from scraper.scraper import Scraper  # Import the Scraper class
from utilities.error_handling import UnknownError


@pytest.fixture()
def scraper_instance() -> Scraper:
    """Fixture to create an instance of the Scraper."""
    return Scraper(categories={}, recipes={})

@pytest.mark.parametrize(
    ("url", "retries", "mock_response", "expected_result"),
    [
        ("http://example.com", 3, Mock(status_code=200, raise_for_status=lambda: None), Mock(status_code=200)),
        ("http://example.com", 1, Mock(status_code=200, raise_for_status=lambda: None), Mock(status_code=200)),
    ],
    ids=["happy_path_3_retries", "happy_path_1_retry"])
def test_make_request_happy_path(
    scraper_instance: Scraper, url: str, retries: int, mock_response: Mock, expected_result: Mock) -> None:

    with patch("requests.get", return_value=mock_response):

        result = scraper_instance.make_request(url, retries)

        assert (result.status_code == expected_result.status_code)

@pytest.mark.parametrize(
    ("url", "retries", "side_effect", "expected_exception", "expected_message"),
    [
        ("http://example.com", 3, requests.exceptions.ConnectionError, ConnectionError,
         "Connection error occurred after multiple attempts."),
        ("http://example.com", 3, requests.exceptions.HTTPError, HTTPError, "HTTP error occurred."),
        ("http://example.com", 3, Exception("Unexpected error"), UnknownError,
         "Unexpected error occurred: Unexpected error"),
    ],
    ids=["connection_error", "http_error", "unexpected_error"])
def test_make_request_error_cases(
    scraper_instance: Scraper, url: str, retries: int, side_effect: Exception,
    expected_exception: type[Exception], expected_message: str) -> None:

    with patch("requests.get", side_effect=side_effect):

        with pytest.raises(expected_exception) as exc_info:
            scraper_instance.make_request(url, retries)
        assert (str(exc_info.value) == expected_message)

@pytest.mark.parametrize(
    ("url", "retries", "side_effect", "expected_log_message"),
    [
        ("http://example.com", 3, requests.exceptions.ConnectionError,
         "Connection error occurred, retrying... (1/3)"),
    ],
    ids=["connection_error_retry"])
def test_make_request_logging(
    scraper_instance: Scraper, url: str, retries: int, side_effect: Exception,
    expected_log_message: str, caplog: pytest.LogCaptureFixture) -> None:

    with patch("requests.get", side_effect=side_effect):

        with pytest.raises(ConnectionError):
            scraper_instance.make_request(url, retries)

        assert (expected_log_message in caplog.text)
