import httpx

from config import settings


class CaptchaError(ValueError):
    pass


async def verify_captcha(token: str | None, remote_ip: str | None = None) -> None:
    if settings.CAPTCHA_PROVIDER == "disabled":
        if settings.DEBUG:
            return
        raise CaptchaError("生产环境必须启用验证码服务")
    if settings.DEBUG and settings.CAPTCHA_BYPASS:
        return
    if not token or not settings.TURNSTILE_SECRET_KEY:
        raise CaptchaError("请完成验证码验证")
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data={"secret": settings.TURNSTILE_SECRET_KEY, "response": token, "remoteip": remote_ip or ""},
            )
            response.raise_for_status()
            if not response.json().get("success"):
                raise CaptchaError("验证码验证失败")
    except httpx.HTTPError as exc:
        raise CaptchaError("验证码服务暂时不可用") from exc
