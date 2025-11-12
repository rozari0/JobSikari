from ninja_extra import NinjaExtraAPI

from users.views import NinjaJWTController, RegisterAPI, UserAPI

api = NinjaExtraAPI()

api.register_controllers(UserAPI, RegisterAPI, NinjaJWTController)
