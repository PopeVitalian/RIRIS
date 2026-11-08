"""Sestavi FastAPI aplikacijo in registriraj routerje."""
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from .auth import safe_user
from .routers import admin, auth, buyer, public, seller
from .settings import FRONTEND_DIR, SECRET_KEY, templates

app = FastAPI(title="AvtoTrg")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, https_only=False)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

app.include_router(auth.router)
app.include_router(public.router)
app.include_router(buyer.router)
app.include_router(seller.router)
app.include_router(admin.router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401:
        return RedirectResponse("/auth/login", status_code=303)
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "request": request,
            "user": safe_user(request),
            "messages": [],
            "code": exc.status_code,
            "message": exc.detail or "Napaka.",
        },
        status_code=exc.status_code,
    )
