
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from time import perf_counter
from uuid import uuid4

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-suqeg4.example.com"


class RequestHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            response = JSONResponse(
                {"detail": "Internal Server Error"},
                status_code=500,
            )

        response.headers["X-Request-ID"] = str(uuid4())
        response.headers["X-Process-Time"] = (
            f"{perf_counter() - start:.6f}"
        )
        return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.add_middleware(RequestHeadersMiddleware)


@app.get("/")
def home():
    return {"status": "ok", "service": "IITM Stats API"}


@app.get("/stats")
def stats(values: str):
    try:
        numbers = [int(x.strip()) for x in values.split(",")]
        if not numbers:
            raise ValueError("Empty input")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Provide comma-separated integers"
        )

    return {
        "email": "24f2005272@ds.study.iitm.ac.in",
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }
