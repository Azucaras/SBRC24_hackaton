from os import environ
import logging
import requests
import json
import asyncio

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")


def landslide_possibility(data):
    probability_dict = {}

    for i in data:
        pluv_values = i["values"]
        probability = " "
        if pluv_values[0] < 20 or pluv_values[1] < 40 or pluv_values[4] < 45:
            probability = "Probabilidade muito baixa"
        elif (20 < pluv_values[0] and pluv_values[0] < 40) or (40 < pluv_values[1] and pluv_values[1] < 60) or (
                45 < pluv_values[4] and pluv_values[4] < 65) or (55 < pluv_values[7] and pluv_values[7] < 90):
            probability = "Probabilidade baixa"
        elif (40 < pluv_values[0] and pluv_values[0] < 60) or (60 < pluv_values[1] and pluv_values[1] < 70) or (
                (65 < pluv_values[4] and pluv_values[4] < 90) and (55 < pluv_values[7] and pluv_values[7] < 90)):
            probability = "Probabilidade moderada"
        elif (60 < pluv_values[0] and pluv_values[0] < 80) or (70 < pluv_values[1] and pluv_values[1] < 100) or (
                (90 < pluv_values[4] and pluv_values[4] < 120) and (55 < pluv_values[7] and pluv_values[7] < 90)):
            probability = "Probabilidade alta"
        elif (80 < pluv_values[0] and pluv_values[0] < 100) or pluv_values[1] > 100 and pluv_values[4] > 120 and \
                pluv_values[7] > 180:
            probability = "Probabilidade muito alta"
        probability_dict[i["origin"]] = probability

    return probability_dict


def map_probabilities_to_percentages(probability_dict):
    probability_mapping = {
        "Probabilidade muito baixa": "0 a 20%",
        "Probabilidade baixa": "20 a 40%",
        "Probabilidade moderada": "40 a 60%",
        "Probabilidade alta": "60 a 80%",
        "Probabilidade muito alta": "80 a 100%"
    }

    percentage_dict = {origin: probability_mapping[prob] for origin, prob in probability_dict.items()}

    return percentage_dict


def handle_advance(probability):
    logger.info(f"Received advance request data {json.dumps(data)}")
    JSONpayload = {}
    try:
        payload_str = bytes.fromhex(data["payload"]).decode('utf-8')
        JSONpayload = json.loads(payload_str)
    except Exception as error:
        error_msg = f"Failed to process command '{data['payload']}'. {error}"
        response = requests.post(f"{rollup_server}/report", json={"payload": error_msg.encode('utf-8').hex()})
        logger.debug(error_msg, exc_info=True)
        return "reject"

    url = None
    hexresult = None
    try:
        # Verificar se JSONpayload é uma lista de dicionários com a estrutura esperada e se cada 'values' tem 9 elementos
        if (isinstance(JSONpayload, list) and
                all('values' in item for item in JSONpayload) and
                all(isinstance(item['values'], list) and len(item['values']) == 9 for item in JSONpayload)):
            logger.info("calculating landslide probabilities")
            probabilities = landslide_possibility(JSONpayload)
            percentage_dict = map_probabilities_to_percentages(probabilities)
            result = json.dumps({"probabilities": percentage_dict})
            hexresult = result.encode('utf-8').hex()
            logger.info(f"probabilities are: {percentage_dict}")
            url = f"{rollup_server}/notice"
        else:
            logger.info("data structure undefined or incorrect")
            result = json.dumps({"error": "data structure undefined or incorrect"})
            hexresult = result.encode('utf-8').hex()
            url = f"{rollup_server}/report"
    except Exception as e:
        logger.info(f"error is: {e}")
        url = f"{rollup_server}/report"
        hexresult = json.dumps({"error": str(e)}).encode('utf-8').hex()

    response = requests.post(url, json={"payload": hexresult})
    return "accept"


def handle_inspect(data):
    # logger.info(f"Received inspect request data {json.dumps(data)}")
    result = None
    try:
        payload_str = bytes.fromhex(data["payload"][2:]).decode('utf-8')
        JSONpayload = json.loads(payload_str)
        probabilities = landslide_possibility(JSONpayload)

        
        if (isinstance(JSONpayload, list) and
                all('values' in item for item in JSONpayload) and
                all(isinstance(item['values'], list) and len(item['values']) == 9 for item in JSONpayload)):
            probabilities = landslide_possibility(JSONpayload)
            result = json.dumps(probabilities).encode('utf-8').hex()
        else:
            result = json.dumps(
                f"This is a simple cartesi Dapp to calculate landslide probabilities. payload is {payload_str}").encode(
                'utf-8').hex()
    except Exception as e:
        result = json.dumps(f"Error:{e}").encode('utf-8').hex()


    def decode_json(response):
        return json.loads(response.decode('utf-8'))

    response = requests.post(f"{rollup_server}/report", json={"payload": result})
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}


while True:
    logger.info("Sending finish")
    response = requests.post(f"{rollup_server}/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")

    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(data)
