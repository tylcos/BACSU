from urllib.parse import *


class BannerClass:
    def __init__(self):
        self.data = {}

    def __str__(self):
        # Can be used for dropping classes
        classAction = 'RSTS_IN=&'

        return classAction + '&'.join(
            [quote_plus('='.join(kvp), '=') for kvp in self.data.items()])
