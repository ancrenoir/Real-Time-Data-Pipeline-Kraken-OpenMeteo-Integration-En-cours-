import requests
from decouple import config
from fastapi import HTTPException
from app.models.Crypto_models.DataModel_crypto import data_asks_bids, Data_crypto, recent_trades_object, \
    recent_trades_crypto_final, data_asks_bids_endpoint, data_spread_object, data_spread_final

CRYPTO_URL = config("URL_CRYPTO", default="https://api.kraken.com/0/public")

def build_url(endpoint: str):
    return f"{"/".join([CRYPTO_URL, endpoint])}"

def config_kraken(symbol: str, url: str):
    params={ 'pair': symbol}
    headers= {'accept': 'application/json'}
    payload= {}
    request_timeout= 10
    return requests.get(url=url, params=params,headers=headers,
                        data=payload, timeout=request_timeout)


def get_crypto_pair_data_depth(symbol: str) -> data_asks_bids_endpoint:

    '''
    Renvoir la endpoint kraken Order book ordre de commande
    :param: symbol / contient les pairs crypto visées
    :return: une instance du model pydantic data_asks_bids contenant asks/bids les objets /
    qui contiennent les données(les données récupérés) de la classe Data_crypto
    ->
    l'offre/demande de la crypto
    '''

    try:

       ## Innitialisation des variables necessaire au réquettage de l'api de kraken - endpoint "order bokk"

        url= build_url("Depth")
        reponses = config_kraken(symbol, url= url)
        reponses.raise_for_status()
        data = reponses.json()

        print(f"statut de la reponse : {reponses.status_code}")
        print(f"reponse brute : {reponses.text}")

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
            for liste_data in data_bids:
                for index, valeur in enumerate(liste_data):
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

            '''Instance de la classe data_asks_bids_endpoint qui contient une instance
             de la classe data_asks_bids plus le nom de la endpoint kraken '''
            instance_data_asks_bids_with_endpoint= data_asks_bids_endpoint(
                Data_endpoint_order_book= instance_data_asks_bids
            )
            return instance_data_asks_bids_with_endpoint.dict()

        raise HTTPException(
            status_code=500,
            detail="erreur dans le format attendu dans la reponse"
        )

    except requests.exceptions.RequestException as e:
        return f"probleme à l'appel de l'api de kraken : {str(e)}"


def get_crypto_data_recent_trades(symbol: str) -> recent_trades_crypto_final:

    '''
    Renvoie la endpoint "recent trades" de kraken
    :param symbol pairs de crypto ciblé
    :return: Me renvoie une instance de la classe recent_trades_crypto_final contenant nos données
    '''


    try:

        url= build_url("Trades")
        reponses= config_kraken(symbol, url= url)
         ## récuperer le code de reponse après le requetage de l'api 200, 404
        reponse= reponses.json()


        print("------------------------------------------------------------------------")
        print(f">>> reponses status : {reponses.status_code}")
        print("------------------------------------------------------------------------")
        print(f">>> reponses : {reponses.text}")

        if isinstance(reponse.get("error"), list) and len(reponse.get("error")) > 0:
            raise HTTPException()
        ## si le status de la reponse est 200 et que l'objet reponse contient une clé result
        if reponse.get("result"):
            couple_crypto= list(reponse.get("result").keys())[0]
            data_recent_trades= reponse.get("result").get(couple_crypto)

        nb_colonnes = len(data_recent_trades[0])

        ## crée une dictionnaire de comprehension pour recupérer plus preprement les données avec le nom
        data_recent_trades_dict= {str(i): [] for i in range(nb_colonnes)}

        for liste_data in data_recent_trades:
            for index, valeur in enumerate(liste_data):
                data_recent_trades_dict[str(index)].append(valeur)

        ## Les variables ci, contiennent les données en forme de liste pour etre stocké dans l'instance des classes pour une meilleur structure

        price= data_recent_trades_dict["0"]
        volume= data_recent_trades_dict["1"]
        temps= data_recent_trades_dict["2"]
        order_type= data_recent_trades_dict["3"]
        market_limit= data_recent_trades_dict["4"]
        miscellaneous= data_recent_trades_dict["5"]
        trade_id= data_recent_trades_dict["6"]


        ## Instance des classes recent_trades_object pour le stockage des données et recent_trades_data_final pour le stockage en format dict

        instance_recent_trades_object= recent_trades_object(
            couple_crypto= couple_crypto,
            Price= price,
            volume= volume,
            temps= temps,
            order_type= order_type,
            market_limit= market_limit,
            miscellaneous= miscellaneous,
            trade_id= trade_id)

        instance_recent_trades_data_final= recent_trades_crypto_final(
            Data_endpoint_recent_trades= instance_recent_trades_object
        )
        return instance_recent_trades_data_final.model_dump()
    except requests.exceptions.RequestException as e:
        str(f"{e}")

def get_crypto_data_Spreads(symbol: str) -> data_spread_final:
    try:
        url= build_url("Spread")
        reponses= config_kraken(symbol= symbol, url= url)
        reponse= reponses.json()

        '''
         Pour le debocage
        '''
        print("-----------------------------------------------------------------------------------------------")
        print(f">>> reponses status: {reponses.status_code}")
        print("--------------------------------------------------------------------------------------------------")

        print(f">>> reponses brute: {reponses.text}")
        print("-------------------------------------------------------------------------------------------------")

        if isintance(reponse.get("error"), list) and len(reponse.get("error")) > 0:
            raise HTTPException(status_code=404, detail="probleme coté server api de kraken dans"
                                                        " la recuperation de la donnée")
        if reponse.get("result"):
            couple_crypto= list(reponse.get("result").keys())[0]

            """
            élaboration d'un dictionnaire dynamique, c'est à dire grandisant en fonction de la taille de la dimension
            que prendra la donnée, il est crée ce dictionnaire pour bien strucutrer la donnée toute les valeur d'une dimension 
            est mise dans une unique liste pour faciliter les manipulation future avec spark
            DIMENSION : (timetamp, bids(meilleur prix vente), asks(meilleur prix achat))
            """
            taille_dimension = len(list(reponse.get("result").get(couple_crypto))[0])
            dictionnaire_spread={str(i): [] for i in range(taille_dimension)}

            for liste_data in reponse.get("result").get(couple_crypto):
                for index, valeur in enumerate(liste_data):
                    dictionnaire_spread[str(index)].append(float(valeur))

        """
        Validation de la données avec pydantic
        
        """
        # Récupearion des listes contenant les données
        temps= dictionnaire_spread.get("0")
        bid= dictionnaire_spread.get("1")
        ask= dictionnaire_spread.get("2")

        instance_data_spread_object= data_spread_object(
            couple_crypto= couple_crypto,
            temps=temps,
            bid=bid,
            ask=ask
        )

        instance_data_spread_final= data_spread_final(
            Data_endpoint_spread= instance_data_spread_object
        )
        return instance_data_spread_final.model_dump()

    except requests.exceptions.RequestException as e:
        str(f"{e}")

