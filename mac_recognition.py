import re
import random
from functools import total_ordering

from errors import WrongMacFormat

MAC_TYPE_CONF = {0: {'reg': r'([0-9A-F]{2}-){5}[0-9A-F]{2}', 'len': 17, 'sep': '-', 'freq': 2},
                 1: {'reg': r'([0-9A-F]{2}:){5}[0-9A-F]{2}', 'len': 17, 'sep': ':', 'freq': 2},
                 2: {'reg': r'([0-9A-F]{4}\.){2}[0-9A-F]{4}', 'len': 14, 'sep': '.', 'freq': 4},
                 3: {'reg': r'[0-9A-F]{12}', 'len': 12, 'sep': None, 'freq': None}}


@total_ordering
class Mac:
    def __init__(self, mac: str):
        self.initial_mac_add = mac
        self.valid_mac_add = ''
        self.type = 0
        self.mac_validation()

    def mac_validation(self):
        if not isinstance(self.initial_mac_add, str):
            raise TypeError('mac value should be str type')
        self.set_type(self._determine_mac_type(self.initial_mac_add))
        regex_search = self._mac_regex_search()
        if not regex_search:
            raise WrongMacFormat(self.initial_mac_add)
        else:
            self.valid_mac_add = self._convert_to_type3(regex_search.group(0))

    def set_type(self, value: int = 0):
        if not isinstance(value, int):
            raise TypeError('Type value should be int type')
        if 0 <= value <= 3:
            self.type = value
        else:
            raise ValueError('Wrong type value, should be between 0 and 3')

    def _determine_mac_type(self, mac_add: str):
        if '-' in mac_add:
            type_ = 0
        elif ':' in mac_add:
            type_ = 1
        elif '.' in mac_add:
            type_ = 2
        else:
            type_ = 3
        return type_

    def _mac_regex_search(self):
        type_conf = MAC_TYPE_CONF.get(self.type)
        if not len(self.initial_mac_add) == type_conf.get('len'):
            raise WrongMacFormat(self.initial_mac_add)
        reg_pattern = type_conf.get('reg')
        if reg_pattern:
            result = re.search(reg_pattern, self.initial_mac_add.upper())
        else:
            result = None
        return result

    def _convert_to_type3(self, mac_address: str):
        type_ = self._determine_mac_type(mac_address)
        sep = MAC_TYPE_CONF.get(type_).get('sep')
        return ''.join(mac_address.split(sep))

    def convert_to_current_type(self):
        type_conf = MAC_TYPE_CONF.get(self.type)
        sep = type_conf.get('sep')
        len = type_conf.get('len')
        freq = type_conf.get('freq')
        if sep:
            splited_mac = [self.valid_mac_add[i:i + freq] for i in range(0, len, freq)
                           if self.valid_mac_add[i:i + freq]]
            result = '{}'.format(sep).join(splited_mac)
        else:
            result = self.valid_mac_add
        return result

    def __str__(self):
        return self.convert_to_current_type()

    def __repr__(self):
        return 'Initial mac-address: {}\ncurrent_type: {}'.format(self.initial_mac_add, self.type)

    def __eq__(self, other):
        if isinstance(other, Mac):
            result = self.valid_mac_add == other.valid_mac_add
        else:
            result = self.valid_mac_add == other
        return result

    def __lt__(self, other):
        if not isinstance(other, Mac):
            return NotImplemented
        return self.valid_mac_add < other.valid_mac_add

    def __hash__(self):
        return hash(self.valid_mac_add)


def generate_random_mac(amount: int = 10):
    macs_list = []
    for i in range(amount):
        tmp = Mac(''.join([random.choice('0123456789ABCDEF') for _ in range(12)]))
        tmp.set_type(random.choice(range(4)))
        macs_list.append(tmp)
    return macs_list



if __name__ == '__main__':
    type0 = Mac('73-23-18-10-35-17')
    type1 = Mac('21:DB:F6:A6:5A:C7')
    type2 = Mac('205B.0F06.0F9B')
    type3 = Mac('0E476D3EA453')
    # type_wrong0 = Mac({})
    # type_wrong1 = Mac('1')
    # type_wrong2 = Mac('ytytyt')
    # type_wrong3 = Mac('21:DB:F6:A6:5A:C7123')
    # type_wrong4 = Mac('0E476D3EA453FDBC')
    # type_wrong5 = Mac('73.23-18-10-35-17')


    test = Mac('1122.3344.55aa')
    print(test.initial_mac_add)
    test.set_type(3)
    print(test)
    test2 = Mac('11-22-33-44-55-AA')
    print(test == 1)
    print(test == test2)
    print(hash(test) == hash(test2))
    test3 = Mac('223344556677')
    print(test != test3)


    macs = generate_random_mac()
    print('\nINITIAL MAC LIST')
    print(macs)
    print('\nBEFORE SORTING')
    for i in macs:
        print(i, sep='')
    macs.sort()
    print('\nAFTER SORTING')
    for i in macs:
        print(i, sep='')