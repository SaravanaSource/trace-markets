class TraceMarketsError(Exception):
    """Base exception."""


class HTTPClientError(TraceMarketsError):
    """Base class for all HTTP-related exceptions."""


class RetryLimitExceededError(HTTPClientError):
    """Retries exhausted."""


class InvalidResponseError(HTTPClientError):
    """Invalid JSON or malformed response."""


class AuthenticationError(HTTPClientError):
    """401 Unauthorized."""


class RateLimitExceededError(HTTPClientError):
    """429 Too Many Requests."""


class ServiceUnavailableError(HTTPClientError):
    """503 Service Unavailable."""