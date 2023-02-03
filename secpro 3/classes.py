import enum

# from rsaencrypt import generate_public_private_keys
# from rsaencrypt import encrypt
# from rsaencrypt import decrypt
# from rsaencrypt import sign
import base64


class Sex(enum.Enum):
    Female = "Female"
    Male = "Male"


class Reason(enum.Enum):
    Periodic_Checkup = "Periodic Checkup"
    Management_Of_A_Case = "Management of a case"
    Complaint = "Complaint"


class patient:
    def __init__(self, name, age, weight, height, sex, readings):
        self.name = name  # String
        self.age = age  # Integer
        self.weight = weight  # Integer
        self.height = height  # Integer
        self.sex = sex  # String or Enum
        self.readings = readings  # Dictionary mapping each reading type to value

    def __str__(self) -> str:
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )


class medication:
    def __init__(self, dose, intake_periods):
        self.dose = dose  # String
        self.intake_periods = intake_periods  # Array of dates

    def __str__(self) -> str:
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )


class prescription:
    def __init__(self, medications, referrals, followup_app, lab_tests):
        self.medications = medications  # Array of medication of objects
        self.referrals = referrals  # Arrays of doctor names (String)
        self.followup_app = followup_app  # Array of dates
        self.lab_tests = lab_tests  # Arrays of test names (String)

    def __str__(self) -> str:
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )


class visit:
    def __init__(
        self,
        reason,
        diagnosis,
        prescription,
        readings,
        previous_hash,
        doctor_name,
        patient_id,
    ):
        self.reason = reason  # String or Enum
        self.diagnosis = diagnosis  # String
        self.prescription = prescription  # Prescription object
        self.readings = readings  # Dictionary mapping each reading type to value
        self.previous_hash = previous_hash
        self.doctor_name = doctor_name
        self.patient_id = patient_id

    def __str__(self) -> str:
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )


readings = {
    "blood_pressure": "90/60mmHg ",
    "pulse": "100bpm",
    "oxygen": "100%",
    "glucose": "100 mg/dL (5.6 mmol/L)",
}
patient_1 = patient("Yousra", 23, 60, 167, "female", readings)
# patient_visit_1 = visit(
#     Reason.Complaint,
#     "Corona",
#     prescription(
#         [
#             medication("50mg", ["Morning", "Evening"]),
#             medication("100mg", ["Morning", "Evening"]),
#         ],
#         ["doctor john", "doctor ay haga"],
#         ["2022/06/02 Saturday", "2022/06/03 Sunday"],
#         ["pcr"],
#     ),
#     readings,
#     "12345",
#     "Maria",
# )

# # Keys
# (publicKey, privateKey) = generate_public_private_keys()

# print("Patient")
# print("--------------------ENCRYPTED----------------")
# ciphertext = encrypt(str(patient_1), publicKey)
# print(type(ciphertext))
# print(ciphertext)
# print("--------------------DECRYPTED----------------")
# text = decrypt(ciphertext, privateKey)
# print(text)

# print("Patient_Visit")
# print("--------------------ENCRYPTED----------------")
# ciphertext = encrypt(str(patient_visit_1), publicKey)
# ciphertextB64 = base64.b64encode(ciphertext).decode("utf8")
# print(type(ciphertextB64))
# print(ciphertextB64)
# print("--------------------DECRYPTED----------------")
# text = decrypt(base64.b64decode(ciphertextB64), privateKey)
# print(text)
