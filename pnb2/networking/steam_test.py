from steampak import SteamApi

LIBRARY_PATH = 'steam/libsteam_api.so'
APP_ID = 480

api = SteamApi(LIBRARY_PATH, app_id=APP_ID)

for user in api.friends():
    print(user.name)


