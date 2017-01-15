# Using US terminology for everything here. For instance, STATE_TYPE is the actual name of this subsection. For US it
# will be state, but for others it may be province, emirate, parish, etc

import csv
import json
from constants import NAME, TYPE, MISSING, COUNTRY_CODE, STATES, STATE_CODE, CITIES, SIMPLE_NAME, CITY_CODE, LAT_LONG

CSV_FILE_PATH = ""
SUBDIVISION_CODE_CSV = "2015-2 SubdivisionCodes.csv"
CODE_LIST_BASE = "2015-2 UNLOCODE CodeListPart"
NUMBER_OF_CODE_LISTS = 3


class SubdivisionCodeCsvColumns():
    COUNTRY_CODE = 0
    STATE_CODE = 1
    STATE_NAME = 2
    STATE_TYPE = 3


class CodeListCsvColumns():
    SPECIAL_INFO = 0
    COUNTRY_CODE = 1
    CITY_CODE = 2
    COUNTRY_OR_NATIVE_CITY_NAME = 3
    SIMPLE_CITY_NAME = 4
    STATE_CODE = 5
    STATUS_INDICATOR = 6
    FUNCTION = 7
    DATE = 8
    IATA = 9
    LAT_LONG = 10
    REMARKS = 11


def get_state_info_from_subdivision_csv(csv_reader):
    state_info = {}

    for row in csv_reader:
        country_code = row[SubdivisionCodeCsvColumns.COUNTRY_CODE]
        state_code = row[SubdivisionCodeCsvColumns.STATE_CODE]
        state_name = row[SubdivisionCodeCsvColumns.STATE_NAME]
        state_type = row[SubdivisionCodeCsvColumns.STATE_TYPE]

        if country_code not in state_info:
            state_info[country_code] = {}

        state_info[country_code][state_code] = {}
        state_info[country_code][state_code][NAME] = state_name
        state_info[country_code][state_code][TYPE] = state_type

    return state_info


def get_info_set_from_code_list_csv(csv_reader, state_info):
    country_name = None
    country_code = None
    info_set = {}

    for row in csv_reader:
        if row[CodeListCsvColumns.COUNTRY_OR_NATIVE_CITY_NAME].startswith("."):
            country_name = row[CodeListCsvColumns.COUNTRY_OR_NATIVE_CITY_NAME][1:].title()
            country_code = row[CodeListCsvColumns.COUNTRY_CODE]
        else:
            state_code = row[CodeListCsvColumns.STATE_CODE]

            if country_code in state_info and state_code:
                try:
                    state_name = state_info[country_code][state_code][NAME]
                    state_type = state_info[country_code][state_code][TYPE]
                except KeyError:
                    state_name = MISSING
                    state_type = MISSING
            else:
                state_name = MISSING
                state_type = MISSING

            native_city_name = row[CodeListCsvColumns.COUNTRY_OR_NATIVE_CITY_NAME]
            simple_city_name = row[CodeListCsvColumns.SIMPLE_CITY_NAME]
            city_code = row[CodeListCsvColumns.CITY_CODE]
            lat_long = row[CodeListCsvColumns.LAT_LONG]

            message = native_city_name + ", " + state_name + " (" + state_type + ") " + country_name

            if MISSING not in message:
                if country_name not in info_set:
                    info_set[country_name] = {}
                    info_set[country_name][COUNTRY_CODE] = country_code
                    info_set[country_name][STATES] = {}

                if state_name not in info_set[country_name][STATES]:
                    info_set[country_name][STATES][state_name] = {}
                    info_set[country_name][STATES][state_name][TYPE] = state_type
                    info_set[country_name][STATES][state_name][STATE_CODE] = state_code
                    info_set[country_name][STATES][state_name][CITIES] = {}

                if native_city_name in info_set[country_name][STATES][state_name][CITIES]:
                    pass
                    # raise ValueError("Duplication of cities")
                else:
                    info_set[country_name][STATES][state_name][CITIES][native_city_name] = {}
                    info_set[country_name][STATES][state_name][CITIES][native_city_name][SIMPLE_NAME] = simple_city_name
                    info_set[country_name][STATES][state_name][CITIES][native_city_name][CITY_CODE] = city_code
                    info_set[country_name][STATES][state_name][CITIES][native_city_name][LAT_LONG] = lat_long

    return info_set


def process():
    csv_reader = csv.reader(open(CSV_FILE_PATH + SUBDIVISION_CODE_CSV, "rU"))
    state_info = get_state_info_from_subdivision_csv(csv_reader)
    full_info_set = {}

    for i in range(NUMBER_OF_CODE_LISTS):
        csv_reader = csv.reader(open(CSV_FILE_PATH + CODE_LIST_BASE + str(i+1) + ".csv", "rU"))
        info_set = get_info_set_from_code_list_csv(csv_reader, state_info)
        full_info_set.update(info_set)

    output_file = open(LOCATION_JSON_FILE_NAME, "wb+")
    json.dump(full_info_set, output_file, encoding="latin1")


process()
