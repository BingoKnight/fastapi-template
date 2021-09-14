from app.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from app.exceptions.request_validation_exception import request_validation_exception_handler
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.api.api_v1.api import api_router
from app.common.config import settings
from app.utils.is_deployed import is_deployed
from fastapi.openapi.utils import get_openapi
from app.db.session import engine
import json


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)

@app.middleware('http')
async def add_access_log(request: Request, call_next):
    response = await call_next(request)
    print(f'''
          {request.method} {request.url.path} - {response.status_code}
          Headers: {json.dumps(jsonable_encoder(request.headers))}
          ''')
    return response


def custom_openapi():
    # https://fastapi.tiangolo.com/tutorial/path-params/#openapi-support
    try:
        # print(f"In custom_openapi {os.environ}")
        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.API_V1_STR,
            description="{{cookiecutter.project_name}} OpenAPI schema",
            openapi_version="3.0.0",
            routes=app.routes,
        )

        app.openapi_schema = openapi_schema
    except Exception as e:
        print(f"Exception in custom_openapi: {str(e)}")
    return app.openapi_schema


app.openapi = custom_openapi


if is_deployed():
    handler = Mangum(app, enable_lifespan=False)

