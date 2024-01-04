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

#Step 2: chunk all sids into blocks of 50 each to abide the using policy, get total number of chunks
chunk_size = 50

if len(sids) % chunk_size == 0:
    num_chunks = int(len(sids)/chunk_size)
else:
    num_chunks = int(len(sids)/chunk_size) + 1

#Step 3: prepare the sdf to write
file_name = f"cid2sids_with_cid_{cid}.sdf" #this name means convert cid to sids with cid determined by user at the beginning

with open(file_name, "w") as f:
    for i in range(num_chunks):
        print("Processing chunk:", i)
        idx_init = chunk_size * i #the index of starting sid of this chunk
        idx_final = chunk_size * (i+1) #the index of final sid of this chunk
        these_sids = ",".join(sids[idx_init:idx_final]) #note that slicing in this way would not cover idx_final itself
        url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/" + these_sids + "/record/sdf" #note the substance, sid, record, sdf
        res = requests.get(url)
        f.write(res.text) #here we don't need rstrip as we need to keep the \n
        time.sleep(0.2)


#optional: see how it looks like
with open(file_name, "r") as f:
    this_file = f.read()
    print(this_file)

#Next, we can do other things based on the sdf we just obtained, for example, get their smiles one by one, get their structures, etc. Describe in other documents.





