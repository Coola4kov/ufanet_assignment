class WrongMacFormat(Exception):
    def __init__(self, mac_add: str):
        self.mac_add = mac_add

    def __str__(self):
        return 'Passed value for mac = {} has wrong ' \
               'format or length and is not valid'.format(self.mac_add)