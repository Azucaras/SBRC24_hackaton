



data = [ { "id": 16, "origin": "Engenhoca", "destination": "Barreto", "distance": "2 km", "elevation": "Alto", "date": "5/12/14 5h40", "values": [37.3, 44.8, 44.8, 44.8, 44.8, 44.8, 44.8, 44.8, 85.9] }, { "id": 20, "origin": "Maria Paula", "destination": "Maria Paula", "distance": "1 km", "elevation": "Alto", "date": "31/1/15 4h50", "values": [45.3, 45.3, 46.9, 46.9, 46.9, 46.9, 53.1, 53.1, 88.0] }, { "id": 22, "origin": "Cantagalo", "destination": "Fonseca", "distance": "2 km", "elevation": "Alto", "date": "3/2/15 22h10", "values": [52.1, 74.2, 74.2, 74.2, 74.2, 74.2, 74.2, 74.2, 226.5] }, { "id": 24, "origin": "Maceió", "destination": "Largo da Batalha", "distance": "1 km", "elevation": "Alto", "date": "4/2/15 21h20", "values": [33.7, 37.3, 37.3, 37.3, 43.6, 46.2, 54.3, 55.9, 138.2] }, { "id": 29, "origin": "Cubango", "destination": "Fonseca", "distance": "2 km", "elevation": "Alto", "date": "17/2/15 19h40", "values": [43.7, 46.0, 46.0, 46.0, 46.0, 68.3, 68.7, 68.7, 167.9] }, { "id": 48, "origin": "Baldeador", "destination": "Várzea das Moças", "distance": "2 km", "elevation": "Alto", "date": "11/9/15 9h50", "values": [42.4, 43.8, 43.8, 43.8, 43.8, 45.4, 45.4, 62.7, 152.8] }, { "id": 123, "origin": "Itaipu", "destination": "Itaipu", "distance": "2 km", "elevation": "Alto", "date": "29/2/16 15h40", "values": [53.7, 54.1, 54.1, 54.1, 54.1, 54.1, 54.1, 54.1, 249.4] }, { "id": 133, "origin": "Jurujuba", "destination": "Jurujuba", "distance": "2 km", "elevation": "Alto", "date": "16/3/16 16h00", "values": [86.3, 118.0, 118.0, 118.0, 118.6, 118.6, 118.6, 143.0, 342.4] }, { "id": 149, "origin": "Cantagalo", "destination": "Badu", "distance": "2 km", "elevation": "Alto", "date": "8/4/17 4h20", "values": [64.1, 66.4, 66.4, 66.4, 66.8, 66.8, 66.8, 66.8, 193.7] }, { "id": 154, "origin": "Maceió", "destination": "Piratininga 1 - Cafubá", "distance": "1 km", "elevation": "Alto", "date": "20/6/17 19h10", "values": [54.7, 54.7, 54.7, 54.7, 97.4, 97.4, 97.4, 97.4, 135.1] }, { "id": 172, "origin": "Fonseca", "destination": "Visconde de Itaboraí", "distance": "2 km", "elevation": "Alto", "date": "21/2/18 22h50", "values": [50.6, 50.6, 50.6, 50.6, 50.6, 50.6, 52.3, 52.3, 132.2] }]



for i in data:
    # lista com os valores pluviométricos
    pluv_values = i["values"]
    # print(pluv_values[0])
    # print(type(pluv_values))
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

    elif (80 < pluv_values[0] and pluv_values[0] < 100) or pluv_values[1] > 100 and pluv_values[4] > 120 and pluv_values[7] > 180:
        probability = "Probabilidade muito alta"
    print(probability)

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
