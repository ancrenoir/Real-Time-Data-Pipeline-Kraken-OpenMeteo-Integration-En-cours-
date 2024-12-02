import requests
from decouple import config
from fastapi import HTTPException
from app.models.Crypto_models.DataModel_crypto import data_asks_bids, Data_crypto

CRYPTO_URL = config("URL_CRYPTO", default="https://api.kraken.com/0/public/Depth")

def get_crypto_pair_data(symbol: str):
    try:
        url = f"{CRYPTO_URL}"
        params = {"pair": symbol}
        headers = {'accept': 'application/json'}
        payload = {}
        request_timeout = 10
        response = requests.get(url, headers=headers, params=params,
                                data=payload, timeout=request_timeout)
        response.raise_for_status()
        data = response.json()

        print(f"statut de la reponse : {response.status_code}")
        print(f"reponse brute : {response.text}")

        if data.get("error") and len(data["error"]) > 0:
            return f"erreur dans data: {data['error']}"
        if data.get("result"):

            couple_crypto = list(data.get("result").keys())[0]
            data_asks = data.get("result").get(couple_crypto).get("asks")
            data_bids = data.get("result").get(couple_crypto).get("bids")

            ### utilsation de liste en comprehension pour innitialiser les dictionnaire qui vont contenir les données asks et bids
            nb_colonnes = len(data_asks[0])
            dictionnaire_asks = {str(i): [] for i in range(nb_colonnes)}
            dictionnaire_bids = {str(i): [] for i in range(nb_colonnes)}
            for liste_data in data_asks:
                for index, valeur in enumerate(liste_data):
                    dictionnaire_asks[str(index)].append(valeur)
                    dictionnaire_bids[str(index)].append(valeur)


            price_asks= dictionnaire_asks["0"]
            volume_asks= dictionnaire_asks["1"]
            temps_asks= dictionnaire_asks["2"]
            price_bids= dictionnaire_bids["0"]
            volume_bids= dictionnaire_bids["1"]
            temps_bids= dictionnaire_bids["2"]



            instance_data_ask = Data_crypto(
                price = price_asks,
                volume = volume_asks,
                temps = temps_asks
            )
            instance_data_bid = Data_crypto(
                price= price_bids,
                volume= volume_bids,
                temps= temps_bids
            )
            instance_data_asks_bids = data_asks_bids(
                couple_crypto= couple_crypto,
                asks= instance_data_ask,
                bids= instance_data_bid
            )
            return instance_data_asks_bids.dict()

        raise HTTPException(
            status_code=500,
            detail="erreur dans le format attendu dans la reponse"
        )

    except requests.exceptions.RequestException as e:
        return f"probleme à l'appel de l'api de kraken : {str(e)}"
