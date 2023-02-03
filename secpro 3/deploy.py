from solcx import compile_standard, install_solc
from web3 import Web3
import json
from rsaAlgo import encrypt, decrypt, generateKeys, loadKeys
from classes import patient, visit
import pandas as pd

from pickledata import (
    Dr_Data_store,
    Dr_Exists,
    Get_Dr_list,
    Get_Patient_list,
    get_DR_PRKey,
    get_RSA_private_key,
    get_RSA_public_key,
    get_TX_contract_hash,
    get_contract_adress,
    Data_store,
    get_last_saved_hash,
    update_last_saved_hash,
)


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
# my_address = "0x9ec4c0f89D490aADA64f7Df4D018796155F13562"
# private_key = "0x23f9cb33d033ce1c91e98d53baf1c59222eb52be4724b906c4425d398cc22f7e"


def create_contract_dr(address, privateKey):

    generateKeys()
    privateKeyRSA, publicKeyRSA = loadKeys()
    # print(
    #     "ORGINAL RSA PUBLIC KEY", publicKeyRSA, "ORGINAL RSA PRIVATE KEY", privateKeyRSA
    # )
    # print("RSAType:", type(publicKeyRSA))
    nonce = w3.eth.getTransactionCount(address)
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )
    # print("Trans ", transaction)
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=privateKey)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # object = ["Private key", "RSA public key", "RSA private key", "TX_contract_hash"]
    newDr = [privateKey, publicKeyRSA, privateKeyRSA, tx_hash, address]
    Dr_Data_store(newDr)


def send_patient(Dr_Private_Key, patient_data):

    # new patient variable is global up so each patient is increased
    # TODO: counter of patients i didnt get to here , for each doctor to insert its id in the list at ID similar to df.shape[0]
    # newPatientID=0
    newPatientID = len(Get_Patient_list())
    # TODO
    # retrieve DR information

    privateKeyRSA = get_RSA_private_key(Dr_Private_Key)
    publicKeyRSA = get_RSA_public_key(Dr_Private_Key)

    # print(type(publicKeyRSA), "RSAAAAAAAAAAAAAAAAAAAAAA:", publicKeyRSA)
    conract_adress = get_contract_adress(Dr_Private_Key)
    tx_contract_hash = get_TX_contract_hash(Dr_Private_Key)

    tx_contract_receipt = w3.eth.wait_for_transaction_receipt(tx_contract_hash)
    # tx_contract_receipt=json.loads(tx_contract_receipt)
    simple_storage = w3.eth.contract(
        address=tx_contract_receipt.contractAddress, abi=abi
    )
    # encrypt patient data
    encryptedPatient = encrypt(patient_data, publicKeyRSA)

    # send patient data
    nonce = w3.eth.getTransactionCount(conract_adress)
    bytes = "".encode("utf-8")

    store_transaction = simple_storage.functions.store(
        encryptedPatient, bytes
    ).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": conract_adress,
            "nonce": nonce,
        }
    )
    signed_store_txn = w3.eth.account.sign_transaction(
        store_transaction, private_key=Dr_Private_Key
    )

    tx_store_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
    # [ID, patient_tx_hash, last_saved_hash, DR_PRKey]
    newPatient = [newPatientID, tx_store_hash, tx_store_hash, Dr_Private_Key]
    # Update patiient info

    Data_store(newPatient)

    #  sendPatient(simple_storage, patient, newPatientID, publicKeyRSA)
    return newPatientID


def sendVisit(DR_PrivKey, patient_id, visit_data):
    # privatekeyRSA_, publicKeyRSA_ = loadKeys()
    # retrieve using patient id

    PatientـdrPrivateKey = get_DR_PRKey(patient_id)

    if PatientـdrPrivateKey == DR_PrivKey:
        print("The Dr owns this patient and can add visits to him")
        # retrieve DR information
        publicKeyRSA = get_RSA_public_key(DR_PrivKey)

        conract_adress = get_contract_adress(DR_PrivKey)
        tx_contract_hash = get_TX_contract_hash(DR_PrivKey)

        last_saved_hash = get_last_saved_hash(patient_id)
        nonce = w3.eth.getTransactionCount(conract_adress)
        # visit_data += ",Previous_Tx_hash:" + hex(last_saved_hash)
        encryptedVisit = encrypt(visit_data, publicKeyRSA)

        tx_contract_receipt = w3.eth.wait_for_transaction_receipt(tx_contract_hash)
        simple_storage = w3.eth.contract(
            address=tx_contract_receipt.contractAddress, abi=abi
        )
        store_transaction = simple_storage.functions.store(
            encryptedVisit, last_saved_hash
        ).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": conract_adress,
                "nonce": nonce,
            }
        )
        signed_store_txn = w3.eth.account.sign_transaction(
            store_transaction, private_key=DR_PrivKey
        )

        tx_store_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        #  print(tx_store_hash, ":STORE HASHHHH")
        #  print("TYPEEE STORE HASSHHH", type(tx_store_hash))
        update_last_saved_hash(patient_id, tx_store_hash)

    else:
        print("The Dr doesn't own this patient and can't add visits to him")


def retrieve(Pre_hash, DRPR):
    global abi
    privateKeyRSA = get_RSA_private_key(DRPR)
    tx_hash = Pre_hash
    trans = w3.eth.get_transaction(tx_hash)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    input = trans["input"]
    contract = w3.eth.contract(address=receipt["contractAddress"], abi=abi)
    data = contract.decode_function_input(input)
    # print(data)
    (data, hashed) = data
    out = decrypt(hashed["hashed_Data_"], privateKeyRSA)
    Pre_hash = hashed["previous_hash_"]
    return out, Pre_hash


def retrieveData(patientid, DRPR):
    global abi  # retrieve kol haga starting last hash

    Dr_Private_Key = get_DR_PRKey(patientid)
    if DRPR == Dr_Private_Key:
        privateKeyRSA = get_RSA_private_key(Dr_Private_Key)
        tx_hash = get_last_saved_hash(patientid)

        trans = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        input = trans["input"]
        contract = w3.eth.contract(address=receipt["contractAddress"], abi=abi)
        data = contract.decode_function_input(input)
        # print(data)
        (data, hashed) = data
        out = decrypt(hashed["hashed_Data_"], privateKeyRSA)
        visits = [out]
        Pre_hash = hashed["previous_hash_"]
        bytes = "".encode("utf-8")
        while not (Pre_hash == bytes):
            out, Pre_hash = retrieve(Pre_hash, DRPR)
            visits.append(out)
        return visits
    else:
        print("Dr not authorized to reeead this data")


# retrieveData(tx_store_hash, abi)
# print(simple_storage.functions.retrieve().call())


# print(decrypt(simple_storage.functions.retrieve().call(), private_key))


def patientInstance():
    name = input("patient name: ")
    age = input("patient age: ")
    weight = input("patient weight: ")
    height = input("patient height: ")
    sex = input("patient sex: ")
    readings = input("patient readings: ")
    newPatient = str(patient(name, age, weight, height, sex, readings))
    return newPatient


def visitInstance():
    reason = input("visit's reason: ")
    diagnosis = input("diagnosis: ")
    prescription = input("prescription: ")
    readings = input("readings: ")
    previous_hash = ""
    doctor_name = input("Doctor's name: ")
    patient_id = input("patient_id: ")
    newVisit = str(
        visit(
            reason,
            diagnosis,
            prescription,
            readings,
            previous_hash,
            doctor_name,
            patient_id,
        )
    )
    return newVisit


def storeVisits(visits):
    i = len(visits) - 1
    sorted = [visits[i]]
    i = i - 1
    while i >= 0:
        sorted.append(visits[i])
        i = i - 1
    return sorted


def main():
    # privateKeyAccount = input("Enter the privateKey acount: ")
    # addressAcount = input("Enter the address acount: ")
    privateKeyAccount = (
        0x6B168FEE038C16726978F68A1205916D32A408D59255256161AE0A2FA22D2D3A
    )
    addressAcount = "0x0E45C6f8151557e5540bf77Ca2b1D3b977eDEE1c"
    # newPatient = patientInstance()
    # newVisit = visitInstance()

    # check if dr already exists in the csv file
    if Dr_Exists(privateKeyAccount):
        print("Dr already exists")

    else:
        # create_contract_dr(addressAcount, privateKeyAccount)
        print("cintract created ")
        create_contract_dr(addressAcount, privateKeyAccount)
    #  create_contract_dr(addressAcount, privateKeyAccount)
    # patient_id = send_patient(privateKeyAccount, newPatient)
    # print("patient id", patient_id)
    print("numbeer of pat ", len(Get_Patient_list()))
    print("numbeer of DRs ", len(Get_Dr_list()))
    # sendVisit(privateKeyAccount, 5, newVisit)
    visits = retrieveData(5, privateKeyAccount)
    visits = storeVisits(visits)
    print("visits", visits)
    visitNo = int(
        input("if you want a specific visit enter its number, else enter t: ")
    )
    # def part_visit(id){
    #     visitarr=retrieveData
    #     return visitarr[id]
    # }
    if visitNo >= 0 and visitNo < len(visits):
        print("visit number ", visitNo, " : ", visits[visitNo])
    else:
        print("please enter a number between 0 and ", len(visits) - 1)

    print("visits", visits)
    # print("Pre", prevHash)


# print(Dr_df.loc[0])
# print(generateKeys())


if __name__ == "__main__":
    main()
