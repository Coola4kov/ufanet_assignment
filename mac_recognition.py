import re


class Mac:
    def __init__(self, mac: str):
        self.initial_mac_add = mac
        self.valid_mac_add = ''
        self.type = 0
        self.mac_validation()

    def _mac_regex_search(self):
        pattern = {0: r'([0-9A-F]{2}-){5}[0-9A-F]{2}',
                   1: r'([0-9A-F]{2}:){5}[0-9A-F]{2}',
                   2: r'([0-9A-F]{4}\.){2}[0-9A-F]{4}',
                   3: r'[0-9A-F]{12}'}.get(self.type)
        result = None
        if pattern:
            result = re.search(pattern, self.initial_mac_add.upper())
        return result

    def _determine_mac_type(self, mac_add):
        if '-' in mac_add:
            type_ = 0
        elif ':' in mac_add:
            type_ = 1
        elif '.' in mac_add:
            type_ = 2
        else:
            type_ = 3
        return type_

    def _convert_to_type3(self, mac_address: str):
        sep = {0: '-',
               1: ':',
               2: '.',
               3: None}
        type_ = self._determine_mac_type(mac_address)
        return ''.join(mac_address.split(sep[type_]))

    def convert_to_current_type(self):
        pass

    def mac_validation(self):
        if not isinstance(self.initial_mac_add, str):
            raise TypeError('mac value should be str type')

        self.set_type(self._determine_mac_type(self.initial_mac_add))

        regex_search = self._mac_regex_search()
        if not regex_search:
            raise ValueError('Passed value for mac = {} has wrong '
                             'format and is not valid'.format(self.initial_mac_add))
        else:
            self.valid_mac_add = self._convert_to_type3(regex_search.group(0))

    def set_type(self, value: int = 0):
        if not isinstance(value, int):
            raise TypeError('type value should be int type')
        if 0 <= value <= 4:
            self.type = value
        else:
            raise ValueError('Wrong type value, should be between 0 and 3')

    def __str__(self):
        pass

    def __repr__(self):
        return 'Initial mac-address: {}\ncurrent_type: {}'.format(self.initial_mac_add, self.type)

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass


if __name__ == '__main__':
    test = Mac('1122334455aa6')
    print(test.type)
    print(test.initial_mac_add)
    print(test.valid_mac_add)
