import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from generators.api.converter_api import router
from generators.exceptions import http_exception_handler
from generators.middlewares.static import SPAStaticFiles

app = FastAPI(title="fleuntqa-helper", description="Convert from json/xml to Pydantic/Go/Rust etc.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(router, prefix="/api")
app.add_exception_handler(HTTPException, http_exception_handler)
app.mount("/", SPAStaticFiles(directory="static", html=True), name="static")


def run():
    uvicorn.run(app, host="0.0.0.0", port=9090)


if __name__ == '__main__':
    run()
