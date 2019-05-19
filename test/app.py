import sys
import traceback

from flask import Flask, Response, request
import json
from datetime import datetime
from util import *

app = Flask(__name__)

city_dct = construct_city_dct()


@app.route("/", methods=["POST"])
def main():
    try:

        req = request.get_json(silent=True, force=True)
        print(req)

        intent_name = req['queryResult']['intent']['displayName']
        print('intent: {}'.format(intent_name))

        if intent_name == "GetWeatherIntent":
            country_name = req["queryResult"]["parameters"]["location"]["country"]
            city_name = req["queryResult"]["parameters"]["location"]["city"]
            street_name = req["queryResult"]["parameters"]["location"]["street-address"]
            if city_name == "":
                city_name = country_name

            if city_name == "":
                city_name = street_name

            weather_status = get_weather_status(city_name, city_dct)
            resp = f"Currently, it is mostly {weather_status} in {city_name}."
        elif intent_name == 'GetCourseInfoIntent':
            program_name = req['queryResult']['parameters']['ProgrammeName']
            query_text = req['queryResult']['queryText']
            context_programme = req['queryResult']['outputContexts'][0]['parameters']['ProgrammeName']

            resp = f"Your want to learn {program_name} in context {context_programme}"
        elif intent_name == 'GetCourseFeeInfoIntent':
            training_fee_type = req['queryResult']['parameters']['TrainingFee']
            training_course_info = req['queryResult']['parameters']['any']
            resp = f"You want to learn {training_fee_type} on {training_course_info}"
        else:
            resp = 'No intent detected'
            pass

        raise Exception("Test error!")
    except:
        resp = 'Can you provide more information?'
        traceback.print_exc(file=sys.stdout)

    resp_text =  {
        "fulfillmentText" : resp
    }
    resp_text = json.dumps(resp_text)
    return Response(resp_text, 200, content_type="application/json")


    return Res

app.run(host='0.0.0.0', port=5000, debug=True)
