from urllib.parse import *


class BannerClass:
    def __init__(self):
        self.data = {}

    def __str__(self):
        # Action for each class, DW = Drop, RW = Empty or Signing up, '' = Signed up
        classAction = 'RSTS_IN=&'

        return classAction + '&'.join(
            [quote_plus('='.join(kvp), '=') for kvp in self.data.items()])
