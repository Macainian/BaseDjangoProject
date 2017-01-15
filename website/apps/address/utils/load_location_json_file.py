# Using US terminology for everything here. For instance, STATE_TYPE is the actual name of this subsection. For US it
# will be state, but for others it may be province, emirate, parish, etc

import json
import take as take

from constants import LOCATION_JSON_FILE_NAME, STATES, CITIES


def load_json():
    json_file = open(LOCATION_JSON_FILE_NAME, "rU")
    location_json = json.load(json_file)

    count = 0

    for item_name in location_json["Japan"][STATES]["Okinawa"]:
        print(location_json["Japan"][STATES]["Okinawa"][item_name])
        count += 1

        if count == 20:
            break

    # print location_json["Japan"][STATES] #["Indiana"][CITIES]["South Bend"]


load_json()