

# _class_ Blockchain
## A very simple blockchain
------
This is a very simple example of a blockchain (data) structure. Example file runs through all methods.

_Add a consensus algorithm to make it distributed or use it as a single source of truth._

```python
class Blockchain(object):
    def __init__(self, path=None, filename=None):
        """
        Initialise the class
        :param path: (string) Path to filename
        :param filename: (string) Filename
        """
    def append(value):
        """
        Append data/value to the blockchain
        :param value: (any) Value/Dictionary
        :return: (int) Index number
        """

    def get_index(index):
        """
        Return the data at the current index
        :param index:
        :return: (dict) Block
        """

    def get_verified_index(index):
        """
        Return the block if verified
        :param index: (int) Index
        :return: (dict/None) Dictionary/None if not found
        """

    def verify_index(index):
        """
        Verify a block by index
        :param index: (int) index
        :return: (bool/None) Verified/None if not found
        """

    def get_index_metadata(index):
        """
        Return the metadata of the block
        :param index:
        :return: (dict) Block
        """

    def get_indexes(start, end):
        """
        Return a range of indexes
        :param start: (int) Start index
        :param end: (int) End index
        :return: (list) Subsection of the blockchain
        """

    def get_date_range(start, end):
        """
        Return a range by dates
        :param start: (int) Start epoch
        :param end: (int) End epoch
        :return: (list) Subsection of the blockchain
        """

    def get_chain(self):
        """
        Return the entire chain
        :return: (List) Blocks
        """

    def get_chain_length(self):
        """
        Return the chain length
        :return: (int) Length
        """

    def find_key_value(key, value, insensitive=False):
        """
        Find a block by a key and value
        :param key: (string) Key name
        :param value: (any) value
        :param insensitive: (bool) Case insensitive
        :return: (list) Subsection of the blockchain
        """

    def find_key_value_range(key, lower, upper):
        """
        Find a block by a key and value
        :param key: (string) Key name
        :param lower: (int) Lower range
        :param supper: (int) Upper range
        :return: (list) Subsection of the blockchain
        """

    def find_key_value_any(value, insensitive=False):
        """
        Find a block by a key and value
        :param key: (string) Key name
        :param lower: (int) Lower range
        :param supper: (int) Upper range
        :return: (list) Subsection of the blockchain
        """

    def validate(self):
        """
        Validate the entire chain
        :return: (bool) Verified
        """

    def autosave(save=None):
        """
        Set/Get the autosave feature
        :param save: (bool) Enable/Disable the autosave
        :return: (bool) Current state
        """

    def auto_save_freq(freq=None):
        """
        Set/Get the autosave frequency
        :param freq: (int) 1/nth records
        :return: (int) Current state
        """

    def save(path=None, filename=None):
        """
        Save the blockchain
        :param path: (string) Path to filename
        :param filename: (string) Filename
        :return: (void)
        """

    def quick_save(report=False):
        """
        Call a save using the last known file
        :param report:
        :return:
        """

    def load(path=None, filename=None):
        """
        Load the blockchain
        :param path: (string) Path to filename
        :param filename: (string) Filename
        :return: (bool) File loaded
        """
```
