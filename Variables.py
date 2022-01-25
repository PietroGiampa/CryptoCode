###########################
# Variables.py            #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

tags = ['1INCH-USD',
        'AVAX-USD',
        'AAVE-USD',
        'AXS-USD',
        'BTC-USD',
        'GCH-USD',
        'BAL-USD',
        'ADA-USD',
        'ATOM-USD',
        'CRV-USD',
        'COMP-USD',
        'LINK-USD',
        'DOGE-USD',
        'MANA-USD',
        'FIL-USD',
        'FTM-USD',
        'ETH-USD',
        'KNC-USD',
        'LTC-USD',
        'MKR-USD',
        'DOT-USD',
        'MATIC-USD',
        'REN-USD',
        'SHIB-USD',
        'SNX-USD',
        'SOL-USD',
        'SUSHI-USD',
        'XLM-USD',
        'XTZ-USD',
        'UMA-USD',
        'UNI-USD',
        'YFI-USD',
        'ZRX-USD']

names = ['1inch',
         'Avalanche', 
         'Aave',  
         'AxieInfinity', 
         'Bitcoin', 
         'Bitcoin Cash', 
         'Balancer',
         'Cardano', 
         'Cosmos', 
         'Curve', 
         'Compound', 
         'Chainlink', 
         'Dogecoin', 
         'Decentraland', 
         'Filecoin', 
         'Fantom', 
         'Ethereum', 
         'Kyber Network Crystal', 
         'Litecoin', 
         'Maker', 
         'Polkadot', 
         'Polygon', 
         'Ren', 
         'Shiba', 
         'Synthetix', 
         'Salana', 
         'Sushi Swap', 
         'Stellar', 
         'Tezos', 
         'Uma', 
         'Uniswap',
         'Yearn Finance',
         'Ox']

# Get the Yahoo Tag for A Selected Crypto Currency
# Need to specify cryptocurrency full name
# -----
# crypto_name - String
def GetCurrencyTag(crypto_name):
    
    #Set flag to check if crypto was found
    name_flag = False

    #Loop through all currencies
    for k in range(len(names)):
        #Find crypto name match
        if crypto_name==names[k]:
            name_tag = tags[k]
            name_flag = True
            
    #Notify if the input currency is missing
    if name_tag==False:
        print('Missing Crypto Currency')
        return 0

    #Return the Tag
    return name_tag
