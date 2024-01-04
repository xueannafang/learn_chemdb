#This is part of the exercises to understand the difference between compounds and substances
#Same compound can have different substances version (indexed by SIDs)

#Step 1: get all substances with the same CID: 1174
import requests
import time
cid = 1174
prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"

url = prolog + str(cid) + "sids/txt" #to get all sids with the same cid, formatting as txt

res = requests.get(url)
sids = res.text.split()

#print(len(sids))

#Step 2: chunk all sids into blocks of 50 each to a