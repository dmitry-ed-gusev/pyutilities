#!/usr/bin/env python3
# coding=utf-8

"""
    Unit tests for http client.

    Created:  Dmitrii Gusev, 02.06.2021
    Modified: Dmitrii Gusev, 02.10.2022
"""

import pytest
import responses
from requests.exceptions import HTTPError
from responses.registries import OrderedRegistry
from wfleet.scraper.utils.http_client import WebClient, process_url

# HTTP request parameters (should be added to the URL)
http_request_params1 = {"zzz": "ccc"}
http_request_params2 = {"a": "bbb", "c": "ddd"}

# HTTP content types
HTTP_CONTENT_TEXT = "plain/text"
HTTP_CONTENT_JSON = "application/json"

# test data - HTTP OK codes (1xx, 2xx, 3xx), values: [code/status, value/body, content type, params]
testdata_http_ok_codes = [
    # codes 1xx
    (100, "Continue", "", http_request_params1),
    (101, "Switching Protocols", "", http_request_params1),
    (102, "Processing", "", http_request_params1),
    (103, "Early Hints", "", http_request_params1),
    # codes 2xx
    (200, "{'status_name': 'OK'}", "application/json", http_request_params1),
    (201, "Created", HTTP_CONTENT_TEXT, http_request_params1),
    (202, "Accepted", HTTP_CONTENT_TEXT, http_request_params1),
    (203, "Non-Authoritative Information", HTTP_CONTENT_TEXT, http_request_params1),
    (204, "No Content", HTTP_CONTENT_TEXT, http_request_params1),
    (205, "Reset Content", HTTP_CONTENT_TEXT, http_request_params1),
    (206, "Partial Content", HTTP_CONTENT_TEXT, http_request_params1),
    (207, "Multi-Status", HTTP_CONTENT_TEXT, http_request_params1),
    (208, "Already reported", HTTP_CONTENT_TEXT, http_request_params1),
    (226, "IM Used", HTTP_CONTENT_TEXT, http_request_params1),
    # codes 3xx
    (300, "Multiple Choices", HTTP_CONTENT_TEXT, http_request_params1),
    (301, "Moved Permanently", HTTP_CONTENT_TEXT, http_request_params1),
    (302, "Found", HTTP_CONTENT_TEXT, http_request_params1),
    (303, "See Other", HTTP_CONTENT_TEXT, http_request_params1),
    (304, "Not Modified", HTTP_CONTENT_TEXT, http_request_params1),
    (305, "Use Proxy", HTTP_CONTENT_TEXT, http_request_params1),
    (306, "Switch Proxy", HTTP_CONTENT_TEXT, http_request_params1),
    (307, "Temporary Redirect", HTTP_CONTENT_TEXT, http_request_params1),
    (308, "Permanent Redirect", HTTP_CONTENT_TEXT, http_request_params1),
]

# test data - HTTP FAIL codes (4xx, 5xx), values: [code/status, body, content type, params]
testdata_http_err_codes_without_retries = [
    # codes 4xx
    (400, "Bad Request", HTTP_CONTENT_TEXT, http_request_params2),
    (401, "Unauthorized", HTTP_CONTENT_TEXT, http_request_params2),
    (402, "Payment Required", HTTP_CONTENT_TEXT, http_request_params2),
    (403, "Forbidden", HTTP_CONTENT_TEXT, http_request_params2),
    (404, "Not Found", HTTP_CONTENT_TEXT, http_request_params2),
    (405, "Method Not Allowed", HTTP_CONTENT_TEXT, http_request_params2),
    (406, "Not Acceptable", HTTP_CONTENT_TEXT, http_request_params2),
    (407, "Proxy Authentication Required", HTTP_CONTENT_TEXT, http_request_params2),
    (408, "Request Timeout", HTTP_CONTENT_TEXT, http_request_params2),
    (409, "Conflict", HTTP_CONTENT_TEXT, http_request_params2),
    (410, "Gone", HTTP_CONTENT_TEXT, http_request_params2),
    (411, "Length Required", HTTP_CONTENT_TEXT, http_request_params2),
    (412, "Precondition Failed", HTTP_CONTENT_TEXT, http_request_params2),
    (413, "Too Large", HTTP_CONTENT_TEXT, http_request_params2),
    (414, "URI Too Long", HTTP_CONTENT_TEXT, http_request_params2),
    (415, "Unsupported Media Type", HTTP_CONTENT_TEXT, http_request_params2),
    (416, "Range Not Satisfiable", HTTP_CONTENT_TEXT, http_request_params2),
    (417, "Expectation Failed", HTTP_CONTENT_TEXT, http_request_params2),
    (418, "I'm a Teapot", HTTP_CONTENT_TEXT, http_request_params2),
    (421, "Misdirected Request", HTTP_CONTENT_TEXT, http_request_params2),
    (422, "Unprocessable Entity", HTTP_CONTENT_TEXT, http_request_params2),
    (423, "Locked", HTTP_CONTENT_TEXT, http_request_params2),
    (424, "Failed Dependency", HTTP_CONTENT_TEXT, http_request_params2),
    (425, "Too Early", HTTP_CONTENT_TEXT, http_request_params2),
    (426, "Upgrade Required", HTTP_CONTENT_TEXT, http_request_params2),
    (428, "Precondition Required", HTTP_CONTENT_TEXT, http_request_params2),
    (431, "Request Header Fields Too Large", HTTP_CONTENT_TEXT, http_request_params2),
    (451, "Unavailable For Legal Reasons", HTTP_CONTENT_TEXT, http_request_params2),
    # codes 5xx
    (501, "Not Implemented", HTTP_CONTENT_TEXT, http_request_params2),
    (505, "HTTP Version Not Supported", HTTP_CONTENT_TEXT, http_request_params2),
    (506, "Variant Also Negotiates", HTTP_CONTENT_TEXT, http_request_params2),
    (507, "Insufficient Storage", HTTP_CONTENT_TEXT, http_request_params2),
    (508, "Loop Detected", HTTP_CONTENT_TEXT, http_request_params2),
    (510, "Not Extended", HTTP_CONTENT_TEXT, http_request_params2),
    (511, "Network Authentication Required", HTTP_CONTENT_TEXT, http_request_params2),
]

# test data - HTTP FAIL codes for retries, values: [code/status, value/body, content type, params]
testdata_http_err_codes_with_retries = [
    (429, "Too Many Requests", HTTP_CONTENT_TEXT, http_request_params2),
    (500, "Internal Server Error", HTTP_CONTENT_TEXT, http_request_params2),
    (502, "Bad Gateway", HTTP_CONTENT_TEXT, http_request_params2),
    (503, "Service Unavailable", HTTP_CONTENT_TEXT, http_request_params2),
    (504, "Gateway Timeout", HTTP_CONTENT_TEXT, http_request_params2),
]


# WebClient fixture (resource under test)
@pytest.fixture()
def webclient():
    print("- setup fixture -")
    yield WebClient()
    print("- teardown fixture -")


# responses fixture for the pytest (integration)
@pytest.fixture
def mocked_responses():
    with responses.RequestsMock(registry=OrderedRegistry) as rsps:
        yield rsps


# webclient/mocked_responses - pytest fixtures
# status/body/content_type/params - test parameters
@pytest.mark.parametrize("status, body, content_type, params", testdata_http_ok_codes)
def test_webclient_http_ok_codes(webclient, mocked_responses, status, body, content_type, params):

    # given
    url_with_params = "http://example.com/api/1/foobar?zzz=ccc"
    mocked_responses.get(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.post(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.put(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.delete(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.head(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.options(url_with_params, body=body, status=status, content_type=content_type)

    url_without_params = "http://example.com/api/1/foobar"  # URL without parameters
    # WebClient HTTP methods for testing
    webclient_http_methods = [
        webclient.get,
        webclient.post,
        webclient.put,
        webclient.delete,
        webclient.head,
        webclient.options,
    ]

    for method in webclient_http_methods:  # iterate and check each method
        # when
        response = method(url=url_without_params, params=params)
        # then
        assert response.status_code == status
        assert response.text == body
        assert response.headers["Content-Type"] == content_type


@pytest.mark.parametrize("status, body, content_type, params", testdata_http_err_codes_without_retries)
def test_webclient_http_fail_codes(webclient, mocked_responses, status, body, content_type, params):

    # given
    url_with_params = "http://example.com/api/1/foobar?a=bbb&c=ddd"
    mocked_responses.get(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.post(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.put(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.delete(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.head(url_with_params, body=body, status=status, content_type=content_type)
    mocked_responses.options(url_with_params, body=body, status=status, content_type=content_type)

    url_without_params = "http://example.com/api/1/foobar"  # URL without parameters
    # WebClient HTTP methods for testing
    webclient_http_methods = [
        webclient.get,
        webclient.post,
        webclient.put,
        webclient.delete,
        webclient.head,
        webclient.options,
    ]

    for method in webclient_http_methods:  # iterate and check each method
        # when
        with pytest.raises(HTTPError) as ex_info:  # should raise requests.exceptions.HTTPError
            method(url=url_without_params, params=params)

        # then
        assert str(status) in str(ex_info.value)  # check status code
        assert body in str(ex_info.value)  # check status code message


@pytest.mark.parametrize("status, body, content_type, params", testdata_http_err_codes_with_retries)
def test_webclient_retry_on_fail(webclient, mocked_responses, status, body, content_type, params):

    # given
    url_with_params = "http://example.com/api/1/foobar?a=bbb&c=ddd"

    http_mocked_responses = [  # mocked HTTP responses
        mocked_responses.get,
        mocked_responses.post,
        mocked_responses.put,
        mocked_responses.delete,
        mocked_responses.head,
        mocked_responses.options,
    ]

    responses = []
    for mocked_response in http_mocked_responses:  # iterate over HTTP methods

        for counter in range(5):  # add responses for one method
            if counter < 4:  # responses with status == 500
                responses.append(
                    mocked_response(url_with_params, body=body, status=status, content_type=content_type)
                )
            elif counter == 4:  # the latest response with status == 200
                responses.append(
                    mocked_response(url_with_params, body="OK", status=200, content_type=content_type)
                )

    url_without_params = "http://example.com/api/1/foobar"  # URL without parameters
    # WebClient HTTP methods for testing
    webclient_http_methods = [
        webclient.get,
        webclient.post,
        webclient.put,
        webclient.delete,
        webclient.head,
        webclient.options,
    ]

    for method in webclient_http_methods:  # iterate and check each method
        # when
        response = method(url=url_without_params, params=params)
        # then
        assert response.status_code == 200
        assert response.text == "OK"
        assert response.headers["Content-Type"] == content_type

    # assert all mocked responses were hit
    for response in responses:
        assert response.call_count == 1


@pytest.mark.parametrize(
    "url, postfix, format_params, expected",
    [
        ("http://myurl/", "123456", None, "http://myurl/123456"),
        ("http://myurl", "123456", None, "http://myurl/123456"),
        ("http://myurl{}/suburl/", "", ("xxx",), "http://myurlxxx/suburl/"),
        ("http://myurl{}/suburl/", "", ("xxx", "zzz"), "http://myurlxxx/suburl/"),
        (
            "http://myurl{}/suburl{}/{}",
            "",
            (
                "aaa",
                "bbb",
                "ccc",
            ),
            "http://myurlaaa/suburlbbb/ccc",
        ),
        ("http://myurl{}/suburl{}/{}", "", ("aaa", "bbb", "ccc", "www"), "http://myurlaaa/suburlbbb/ccc"),
        (
            "http://myurl{}/suburl{}/{}",
            "2",
            (
                "_a",
                "_b",
                "_c",
            ),
            "http://myurl_a/suburl_b/_c/2",
        ),
    ],
)
def test_process_url(url, postfix, format_params, expected):
    assert process_url(url, postfix, format_params) == expected
