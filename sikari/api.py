from ninja_extra import NinjaExtraAPI

from users.views import NinjaJWTController, RegisterAPI, UserAPI
from users.dashboard import MatchingAPI, DashboardAPI
from resources.views import ResourcesAPI
from jobs.views import JobsAPI

api = NinjaExtraAPI()

api.register_controllers(
    UserAPI,
    RegisterAPI,
    NinjaJWTController,
    ResourcesAPI,
    JobsAPI,
    MatchingAPI,
    DashboardAPI,
)
