import pandas as pd

df = pd.DataFrame(columns=["ID", "patient_tx_hash", "last_saved_hash", "DR_PRKey"])
df.set_index("ID")


def get_last_saved_hash(ID):
    return df[df["ID"] == ID]["last_saved_hash"].tolist()[0]


def get_DR_PRKey(ID):
    return df[df["ID"] == ID]["DR_PRKey"].tolist()[0]


def get_patient_tx_hash(ID):
    return df[df["ID"] == ID]["patient_tx_hash"].tolist()[0]


def set_last_saved_hash(ID, NewValue):
    df.iloc[[ID], [2]] = NewValue
    df.to_csv("Data.csv")


def set_DR_PRKey(ID, NewValue):
    df.iloc[[ID], [3]] = NewValue
    df.to_csv("Data.csv")


def set_patient_tx_hash(ID, NewValue):
    df.iloc[[ID], [1]] = NewValue
    df.to_csv("Data.csv")


Dr_df = pd.DataFrame(
    columns=[
        "PrivateKey",
        "RSA_Public",
        "RSA_Private",
        "contract_Adress",
        "TX_contract_hash",
    ]
)
# Dr_df = pd.read_csv("DRData.csv")
Dr_df.set_index("PrivateKey")


def get_RSA_Public(PrivateKey):
    return Dr_df[Dr_df["PrivateKey"] == PrivateKey]["RSA_Public"].tolist()[0]


def get_RSA_Private(PrivateKey):
    return Dr_df[Dr_df["PrivateKey"] == PrivateKey]["RSA_Private"].tolist()[0]


def get_contract_Adress(PrivateKey):
    return Dr_df[Dr_df["PrivateKey"] == PrivateKey]["contract_Adress"].tolist()[0]


def get_TX_contract_hash(PrivateKey):
    return Dr_df[Dr_df["PrivateKey"] == PrivateKey]["TX_contract_hash"].tolist()[0]
