"""

Question #2 - FIGI Validation

FIGI (Financial Instrument Global Identifier) is an open standard, unique identifier for financial instruments. The identifiers have a pre-defined structure that is based on the specification provided by the Object Management Group.
 
Design a validator that takes in a string as an input and provides:
1. An output indicating if the string is a valid FIGI
2. Error messages that indicate why the string is not a valid FIGI (if it is erroneous).
 
Use the following references to understand more about FIGI and the validation rules:
1. https://www.openfigi.com/about/figi
2. https://www.omg.org/spec/FIGI/1.0/PDF (Section 6.1.2 Syntax)

"""

# Consider loading-parsing the docs outlined in the spec to test

ISO_8859_1_LETTERS = "BCDFGHJKLMNPQRSTVWXYZ"
ISO_8859_1_ALPHANUM = ISO_8859_1_LETTERS + "0123456789"
RESERVED_PROVIDERS = (
    "BS",
    "BM",
    "GG",
    "GB",
    "GH",
    "KY",
    "VG",
)  # to avoid conflict with ISIN country codes ending in "G"
LETTER_TO_INT_MAP = {
    "B": 11,
    "C": 12,
    "D": 13,
    "F": 15,
    "G": 16,
    "H": 17,
    "J": 19,
    "K": 20,
    "L": 21,
    "M": 22,
    "N": 23,
    "P": 25,
    "Q": 26,
    "R": 27,
    "S": 28,
    "T": 29,
    "V": 31,
    "W": 32,
    "X": 33,
    "Y": 34,
    "Z": 35,
}
RESULT_STR = {True: "PASS", False: "FAIL"}


class FigiValidator:
    @classmethod
    def is_figi(cls, identifier):
        print(f"ID: {identifier}")
        out = all(cls.run_active_checks(identifier))
        print(f"ID is FIGI: {out}\n")
        return out

    @classmethod
    def get_active_checks(cls):
        active_checks = {
            "Provider": cls.check_provider,
            "Is Global": cls.check_is_global,
            "Associations": cls.check_associations,
            "Encoding": cls.check_encoding,
        }
        return active_checks

    @classmethod
    def run_active_checks(cls, identifier):
        results = []
        active_checks = cls.get_active_checks()
        for check_name, func in active_checks.items():
            result = func(identifier)
            results.append(result)
            print(f"{check_name:20}{RESULT_STR[result]:>6}")
        return results

    @staticmethod
    def do_mod_10_dbl_add_dbl(identifier):
        """
        Simple implementation of Mod 10 Double Add Double technique
        described in https://www.omg.org/spec/FIGI/1.0/PDF, pp 16-17

        Returns the check digit if valid, otherwise -1
        """
        nums = ""
        for n, char in enumerate(identifier[-2::-1], 1):
            if n % 2 == 0:
                multiplier = 2
            else:
                multiplier = 1
            try:
                num = int(char)
            except ValueError:
                try:
                    num = LETTER_TO_INT_MAP[char]  # don't allow random success
                except KeyError:
                    return -1
            nums += str(num * multiplier)
        result = sum(map(int, nums))  # sum up all individual ints from this series
        check_digit = 10 - (result % 10)
        return check_digit

    @staticmethod
    def check_provider(identifier):
        """
        Characters 1-2
        Designates the Certified Provider that issued (minted) the corresponding FIGI
        """
        chars = identifier[:2]
        return chars not in RESERVED_PROVIDERS

    @staticmethod
    def check_is_global(identifier):
        """
        Character 3
        Always 'G' to designate it as a Global Identifier
        """
        chars = identifier[2]
        return chars == "G"

    @staticmethod
    def check_associations(identifier):
        """
        Characters 4-11
        Randomly assigned values that complete the reference ID for the set of associated metadata. Alpha-numeric values allowed, excluding vowels.
        """
        chars = identifier[3:11]
        return set(chars).issubset(ISO_8859_1_ALPHANUM)

    @staticmethod
    def check_encoding(identifier):
        """
        Character 12
        Check digit formula is based on the Modulus 10 Double Add Double technique and will be applied to every FIGI number.
        """
        check_digit = FigiValidator.do_mod_10_dbl_add_dbl(identifier)
        return int(identifier[-1]) == check_digit


def test_is_figi_1():
    "Validate if identifier conforms to FIGI standard"
    identifier = "BBG000BLNQ16"
    assert FigiValidator.is_figi(identifier)


def test_is_figi_2():
    identifier = "NRG92C84SB39"
    assert FigiValidator.is_figi(identifier)


def test_encoding_is_not_figi():
    identifier = "NRG92C84SB38"
    assert not FigiValidator.is_figi(identifier)


def test_associations_is_not_figi():
    identifier = "NRG92A84SB39"
    assert not FigiValidator.is_figi(identifier)


def test_global_character_is_not_figi():
    identifier = "NRC92C84SB39"
    assert not FigiValidator.is_figi(identifier)


def test_provider_is_not_figi():
    identifier = "GBG92C84SB39"
    assert not FigiValidator.is_figi(identifier)


test_is_figi_1()
test_is_figi_2()
test_encoding_is_not_figi()
test_associations_is_not_figi()
test_global_character_is_not_figi()
test_provider_is_not_figi()
