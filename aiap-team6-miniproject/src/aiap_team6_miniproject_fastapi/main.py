import logging
import fastapi
from fastapi.middleware.cors import CORSMiddleware

import aiap_team6_miniproject as team6_miniproject
import aiap_team6_miniproject_fastapi as team6_miniproject_fapi


LOGGER = logging.getLogger(__name__)
LOGGER.info("Setting up logging configuration.")
team6_miniproject.general_utils.setup_logging(
    logging_config_path=team6_miniproject_fapi.config.SETTINGS.LOGGER_CONFIG_PATH)

API_V1_STR = team6_miniproject_fapi.config.SETTINGS.API_V1_STR
APP = fastapi.FastAPI(
    title=team6_miniproject_fapi.config.SETTINGS.API_NAME,
    openapi_url=f"{API_V1_STR}/openapi.json")
API_ROUTER = fastapi.APIRouter()
API_ROUTER.include_router(
    team6_miniproject_fapi.v1.routers.model.ROUTER, prefix="/model", tags=["model"])
APP.include_router(
    API_ROUTER, prefix=team6_miniproject_fapi.config.SETTINGS.API_V1_STR)

ORIGINS = ["*"]

APP.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
