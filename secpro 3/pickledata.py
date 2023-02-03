import pickle
import io
import numpy as np


# object = ["Private key", "RSA public key", "RSA private key", "TX_contract_hash", "contractAdress"]
def Dr_Data_store(new_list):
    #     # updated_list=np.array(updated_list)
    with open("DrData.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
    list_reconstructed.append(new_list)
    with open("DrData.pickle", "wb") as outfile:
        pickle.dump(list_reconstructed, outfile)


#######################################################
#   with open("DrData.pickle", "wb") as outfile:
#        pickle.dump([new_list], outfile)
# print("Written object", updated_list)


def Get_Dr_list():
    with open("DrData.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        return list_reconstructed


def Dr_Exists(Private_key):
    with open("DrData.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][3])
        # print(type(list_reconstructed))
        print(len(list_reconstructed))

    for i in range(len(list_reconstructed)):
        if list_reconstructed[i][0] == Private_key:
            return list_reconstructed[i][1]


def get_RSA_public_key(Private_key):
    with open("DrData.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][3])
    for i in range(len(list_reconstructed)):
        if list_reconstructed[i][0] == Private_key:
            return list_reconstructed[i][1]


def get_RSA_private_key(Private_key):
    with open("DrData.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][3])
    for i in range(len(list_reconstructed)):
        if list_reconstructed[i][0] == Private_key:
            return list_reconstructed[i][2]


def get_TX_contract_hash(Private_key):
    with open("DrData.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][3])
    for i in range(len(list_reconstructed)):
        if list_reconstructed[i][0] == Private_key:
            return list_reconstructed[i][3]


def get_contract_adress(Private_key):
    with open("DrData.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][3])
    for i in range(len(list_reconstructed)):
        if list_reconstructed[i][0] == Private_key:
            return list_reconstructed[i][4]


# object = ["ID", "patient_tx_hash", "last_saved_hash", "DR_PRKey"]
# list.append(object)


# def input_object(ID, patient_tx_hash, last_saved_hash, DR_PRKey):
#   object = de
#  list.append(object)
# print(list)


# input_object(1, "m", "m", "m")

# Serialization=>update append

# list can be set right away with index in deploy "last_saved_hashed"
def Data_store(new_list):

    with open("test.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
    list_reconstructed.append(new_list)
    with open("test.pickle", "wb") as outfile:
        pickle.dump(list_reconstructed, outfile)


######################################################
#  with open("test.pickle", "wb") as outfile:
#     pickle.dump([new_list], outfile)


def update_last_saved_hash(ID, last_saved_hash):
    with open("test.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][3])
        list_reconstructed[ID][2] = last_saved_hash
        with open("test.pickle", "wb") as outfile:
          pickle.dump(list_reconstructed, outfile)
       # Data_store(list_reconstructed)


# Deserialization => getters

# object = ["ID", "patient_tx_hash", "last_saved_hash", "DR_PRKey"]
def get_DR_PRKey(ID):
    with open("test.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][3])
        return list_reconstructed[ID][3]


def Get_Patient_list():
    with open("test.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        return list_reconstructed


def get_last_saved_hash(ID):
    with open("test.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][2])
        return list_reconstructed[ID][2]


def get_patient_tx_hash(ID):
    with open("test.pickle", "rb") as infile:
        list_reconstructed = pickle.load(infile)
        # print("Reconstructed object", list_reconstructed[ID][1])
        return list_reconstructed[ID][1]


# set_last_saved_hash(patient_id, tx_store_hash)
# if list == list_reconstructed:
#   print("Reconstruction success")
