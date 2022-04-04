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
RESERVED_PROVIDERS = ("BS","BM","GG","GB","GH","KY","VG")  # to avoid conflict with ISIN country codes ending in "G"
LETTER_TO_INT_MAP = {
    "B": 11,
    "F": 15,
    "J": 19,
    "M": 22,
    "Q": 26,
    "T": 29,
    "X": 33,
    "C": 12,
    "G": 16,
    "K": 20,
    "N": 23,
    "R": 27,
    "V": 31,
    "Y": 34,
    "D": 13,
    "H": 17,
    "L": 21,
    "P": 25,
    "S": 28, 
    "W": 32,
    "Z": 35
}


class FigiValidator:
    def __init__(self, identifier):
        self.identifier = identifier
        self.active_checks = {
            "Provider": self.check_provider,
            "Is Global": self.check_is_global,
            "Associations": self.check_associations,
            "Encoding": self.check_mod_10_dbl_add_dbl
        }
    
    def is_figi(self):
        print(f"ID: {self.identifier}")
        out = all(self.run_active_checks())
        print(F"ID is FIGI: {out}\n")
        return out

    def run_active_checks(self):
        results = []
        for check_name, func in self.active_checks.items():
            result = func()
            results.append(result)
            print(f"{check_name} Passed: {result}")
        return results

    def _do_mod_10_dbl_add_dbl(self, identifier):
        """
        Simple implementation of Mod 10 Double Add Double technique 
        described in https://www.omg.org/spec/FIGI/1.0/PDF, pp 16-17
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

    def check_provider(self):
        """
        Characters 1-2
        Designates the Certified Provider that issued (minted) the corresponding FIGI
        """
        chars = self.identifier[:2]
        return chars not in RESERVED_PROVIDERS

    def check_is_global(self):
        """
        Character 3
        Always 'G' to designate it as a Global Identifier
        """
        chars = self.identifier[2]
        return chars == "G"

    def check_associations(self):
        """
        Characters 4-11
        Randomly assigned values that complete the reference ID for the set of associated metadata. Alpha-numeric values allowed, excluding vowels.
        """
        chars = self.identifier[3:11]
        return set(chars).issubset(ISO_8859_1_ALPHANUM)

    def check_mod_10_dbl_add_dbl(self):
        """
        Character 12
        Check digit formula is based on the Modulus 10 Double Add Double technique and will be applied to every FIGI number.
        """
        check_digit = self._do_mod_10_dbl_add_dbl(self.identifier)
        return int(self.identifier[-1]) == check_digit


def test_is_figi_1():
    "Validate if identifier conforms to FIGI standard"
    identifier = "BBG000BLNQ16"
    assert FigiValidator(identifier).is_figi()


def test_is_figi_2():
    identifier = "NRG92C84SB39"
    assert FigiValidator(identifier).is_figi()


def test_encoding_is_not_figi():
    identifier = "NRG92C84SB38"
    assert not FigiValidator(identifier).is_figi()


def test_associations_is_not_figi():
    identifier = "NRG92A84SB39"
    assert not FigiValidator(identifier).is_figi()


def test_global_character_is_not_figi():
    identifier = "NRC92C84SB39"
    assert not FigiValidator(identifier).is_figi()


def test_provider_is_not_figi():
    identifier = "GBG92C84SB39"
    assert not FigiValidator(identifier).is_figi()


test_is_figi_1()
test_is_figi_2()
test_encoding_is_not_figi()
test_associations_is_not_figi()
test_global_character_is_not_figi()
test_provider_is_not_figi()