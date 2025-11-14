from ninja_extra import NinjaExtraAPI

from jobs.views import ExternalJobs, JobsAPI
from resources.views import ResourcesAPI
from users.dashboard import DashboardAPI, MatchingAPI
from users.views import (
    NinjaJWTController,
    PDFController,
    RegisterAPI,
    UserAPI,
)

api = NinjaExtraAPI()

api.register_controllers(
    UserAPI,
    RegisterAPI,
    NinjaJWTController,
    ResourcesAPI,
    JobsAPI,
    MatchingAPI,
    DashboardAPI,
    PDFController,
    ExternalJobs,
)
