from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import struct
import time

try:  # pragma: no cover
    import pyotp as _pyotp
except Exception:  # pragma: no cover
    _pyotp = None


def random_base32(length: int = 16) -> str:
    return base64.b32encode(secrets.token_bytes(length)).decode("utf-8").rstrip("=")


def _totp(secret: str, digits: int = 6, interval: int = 30, for_time: int | None = None) -> str:
    if for_time is None:
        for_time = int(time.time())
    key = base64.b32decode(secret + "=" * ((8 - len(secret) % 8) % 8))
    counter = int(for_time / interval)
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[-1] & 0x0F
    code = (struct.unpack(">I", h[o:o + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return f"{code:0{digits}d}"


class _FallbackTOTP:
    def __init__(self, secret: str, interval: int = 30, digits: int = 6):
        self.secret = secret
        self.interval = interval
        self.digits = digits

    def now(self) -> str:
        return _totp(self.secret, digits=self.digits, interval=self.interval)

    def verify(self, token: str, valid_window: int = 1) -> bool:
        current_time = int(time.time())
        for offset in range(-valid_window, valid_window + 1):
            if _totp(self.secret, digits=self.digits, interval=self.interval, for_time=current_time + offset * self.interval) == token:
                return True
        return False


if _pyotp:  # pragma: no cover
    TOTP = _pyotp.TOTP
    random_base32 = _pyotp.random_base32
else:
    TOTP = _FallbackTOTP
