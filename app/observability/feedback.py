import contextvars
import json
import logging
from datetime import datetime, timezone
from typing import Any, Protocol


class LoggingSettings(Protocol):
    log_level: str
    log_json: bool
    log_service_name: str
    app_env: str


_REQUEST_ID: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)
_REDACTED = "[REDACTED]"
_SENSITIVE_KEYS = {"password", "token", "authorization", "api_key", "secret"}
_BASE_LOG_FIELDS = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys())


def set_request_id(request_id: str) -> None:
    _REQUEST_ID.set(request_id)


def get_request_id() -> str | None:
    return _REQUEST_ID.get()


def clear_request_id() -> None:
    _REQUEST_ID.set(None)


def _is_sensitive(key: str) -> bool:
    lowered = key.lower()
    return any(part in lowered for part in _SENSITIVE_KEYS)


def _sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(k): (_REDACTED if _is_sensitive(str(k)) else _sanitize(v))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_sanitize(item) for item in value)
    return value


class JsonLogFormatter(logging.Formatter):
    def __init__(self, *, service_name: str, environment: str) -> None:
        super().__init__()
        self._service_name = service_name
        self._environment = environment

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self._service_name,
            "environment": self._environment,
        }

        request_id = getattr(record, "request_id", None) or get_request_id()
        if request_id:
            payload["request_id"] = request_id

        extras = {
            key: value
            for key, value in record.__dict__.items()
            if key not in _BASE_LOG_FIELDS and key not in {"message", "asctime"}
        }
        for key, value in extras.items():
            payload[key] = _REDACTED if _is_sensitive(key) else _sanitize(value)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def configure_logging(settings: LoggingSettings) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    handler = next(
        (h for h in root_logger.handlers if getattr(h, "_starter_structured_logging", False)),
        None,
    )

    if handler is None:
        handler = logging.StreamHandler()
        setattr(handler, "_starter_structured_logging", True)
        root_logger.addHandler(handler)

    if settings.log_json:
        handler.setFormatter(JsonLogFormatter(service_name=settings.log_service_name, environment=settings.app_env))
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
