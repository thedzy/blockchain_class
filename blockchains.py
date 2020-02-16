#!/usr/bin/env python3

"""
Script:	blockchain.py
Date:	2020-01-10
Platform: macOS/Linux
Description:
A very simple blockchain

Example of creating a data structure in python
"""
__author__ = 'thedzy'
__copyright__ = 'Copyright 2020, thedzy'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'thedzy'
__email__ = 'thedzy@hotmail.com'
__status__ = 'Development'

import hashlib
import json
import os
import pickle
import time


class Blockchain(object):
    def __init__(self, path=None, filename=None):
        """
        Initialise the class
        :param path: (string) Path to filename
        :param filename: (string) Filename
        """

        # Initialise the chain with a  stub record
        self.__chain = [{'block_id': 0, 'block_hash': 0}]
        self.__index = 0

        # Set autosave data
        self.__auto_save = True
        self.__auto_save_freq = 1
        if path is None:
            path = os.path.dirname(__file__)
        if filename is None:
            filename = 'blockchain.chain'
        self.__save_file = os.path.join(path, filename)

    def __del__(self):
        """
        Deconstruct the class
        :return: (void)
        """

        # Save on deconstruct
        if self.__auto_save:
            self.quick_save(True)

    def append(self, value):
        """
        Append data/value to the blockchain
        :param value: (any) Value/Dictionary
        :return: (int) Index number
        """
        block_id = self.__index
        block = self.__chain[self.__index]
        block['block_epoch_time'] = time.time()

        if isinstance(value, dict):
            block['block_data'] = value
        else:
            # If we are not receiving a dict, add then create one to store the value
            block['block_data'] = {'value': value}
        self.__create_stub()

        # Save the file after each append
        if self.__auto_save:
            if self.__index % self.__auto_save_freq == 0:
                self.quick_save()

        return block_id

    def __create_stub(self):
        """
        Create the a stub record
        :return:  (void)
        """
        hashed = self.__get_hash(self.__chain[self.__index])
        self.__index += 1
        self.__chain.append({'block_id': self.__index, 'block_hash': hashed})

    def get_index(self, index):
        """
        Return the data at the current index
        :param index:
        :return: (dict) Block
        """
        if index >= 0 and index < self.__index:
            return self.__chain[index]['block_data'].copy()
        else:
            return None

    def get_verified_index(self, index):
        """
        Return the block if verified
        :param index: (int) Index
        :return: (dict/None) Dictionary/None if not found
        """
        if index >= 0 and index < self.__index:
            block = self.get_index(index).copy()

            if self.verify_index(index):
                return block
            else:
                return False
        else:
            return None

    def verify_index(self, index):
        """
        Verify a block by index
        :param index: (int) index
        :return: (bool/None) Verified/None if not found
        """
        if index >= 0 and index < self.__index:
            hashed = self.__get_hash(self.__chain[index])
            check = self.__chain[index + 1]['block_hash']

            if hashed == check:
                return True
            else:
                return False
        else:
            return None

    def get_index_metadata(self, index):
        """
        Return the metadata of the block
        :param index:
        :return: (dict) Block
        """
        if index >= 0 and index < self.__index:
            block = self.__chain[index].copy()
            del block['block_data']
            return block
        else:
            return None

    def get_indexes(self, start, end):
        """
        Return a range of indexes
        :param start: (int) Start index
        :param end: (int) End index
        :return: (list) Subsection of the blockchain
        """
        if start == end:
            return [self.get_index(start)]

        if end <= start:
            print('Invalid range')
            return []

        start = 0 if start < 0 else start
        end = self.__index if end > self.__index else end

        return self.__parse_chain(self.__chain[start:end])

    def get_date_range(self, start, end):
        """
        Return a range by dates
        :param start: (int) Start epoch
        :param end: (int) End epoch
        :return: (list) Subsection of the blockchain
        """
        sub_chain = []

        for block in self.__chain[:self.__index]:
            if block['block_epoch_time'] > start and block['block_epoch_time'] < end:
                sub_chain.append(block.copy())

        return self.__parse_chain(sub_chain)

    def get_chain(self):
        """
        Return the entire chain
        :return: (List) Blocks
        """
        return self.__parse_chain(self.__chain[:self.__index])

    def get_chain_length(self):
        """
        Return the chain length
        :return: (int) Length
        """
        return self.__index

    def find_key_value(self, key, value, insensitive=False):
        """
        Find a block by a key and value
        :param key: (string) Key name
        :param value: (any) value
        :param insensitive: (bool) Case insensitive
        :return: (list) Subsection of the blockchain
        """
        sub_chain = []

        if isinstance(value, str):
            if insensitive:
                value = value.lower()

        for block in self.__chain[:self.__index]:
            if key in block['block_data']:
                key_data = block['block_data'][key]
                if isinstance(key_data, str):
                    if insensitive:
                        key_data = key_data.lower()
                if key_data == value:
                    sub_chain.append(block.copy())

        return self.__parse_chain(sub_chain)

    def find_key_value_range(self, key, lower, upper):
        """
        Find a block by a key and value
        :param key: (string) Key name
        :param lower: (int) Lower range
        :param upper: (int) Upper range
        :return: (list) Subsection of the blockchain
        """
        sub_chain = []

        lower = float(lower)
        upper = float(upper)

        if lower > upper:
            print('Invalid search criteria')
            return sub_chain

        for block in self.__chain[:self.__index]:
            if key in block['block_data']:
                key_data = block['block_data'][key]
                if isinstance(key_data, (int, float)):
                    if key_data >= lower and key_data <= upper:
                        sub_chain.append(block.copy())

        return self.__parse_chain(sub_chain)

    def find_key_value_any(self, value, insensitive=False):
        """
        Find a block by a key and value
        :param value: (any) Search value
        :param insensitive: (bool) Case insensitive
        :return: (list) Subsection of the blockchain
        """
        sub_chain = []

        if isinstance(value, str):
            if insensitive:
                value = value.lower()

        for block in self.__chain[:self.__index]:
            for key in block['block_data']:
                key_data = block['block_data'][key]
                if isinstance(key_data, str):
                    if insensitive:
                        key_data = key_data.lower()
                if key_data == value:
                    sub_chain.append(block.copy())

        return self.__parse_chain(sub_chain)

    def validate(self):
        """
        Validate the entire chain
        :return: (bool) Verified
        """
        validity = True
        for index in range(self.__index):
            if not self.verify_index(index):
                print('Problem with index: {}'.format(index))
                validity = False

        return validity

    def autosave(self, save=None):
        """
        Set/Get the autosave feature
        :param save: (bool) Enable/Disable the autosave
        :return: (bool) Current state
        """
        if save is not None:
            self.__auto_save = bool(save)

        return self.__auto_save

    def autosave_freq(self, freq=None):
        """
        Set/Get the autosave frequency
        :param freq: (int) 1/nth records
        :return: (int) Current state
        """
        if freq is not None:
            self.__auto_save_freq = int(freq)

        return self.__auto_save_freq

    def save(self, path=None, filename=None):
        """
        Save the blockchain
        :param path: (string) Path to filename
        :param filename: (string) Filename
        :return: (void)
        """

        # If the path and filename are not set, create some defaults
        if path is None:
            path = os.path.dirname(__file__)

        if filename is None:
            filename = 'blockchain.chain'

        if os.path.exists(path):
            self.__save_file = os.path.join(path, filename)
            try:
                with open(self.__save_file, 'wb') as file:
                    pickle.dump(self.__chain, file)
                    self.autosave(True)
            except Exception as err:
                print('Save failed, autosave disabled')
                print(err)
                self.autosave(False)
        else:
            print('Path \'{}\', does not exist, autosave disabled'.format(path))

    def quick_save(self, report=False):
        """
        Call a save using the last known file
        :param report:
        :return:
        """
        if self.__save_file is not None:
            try:
                with open(self.__save_file, 'wb') as file:
                    pickle.dump(self.__chain, file)
            except Exception as err:
                print('Quick save failed')
                print(err)
        else:
            if report:
                print('No Save file used, please use save() first')
                return

        if report:
            print('Saved blockchain to: {}'.format(self.__save_file))

    def load(self, path=None, filename=None):
        """
        Load the blockchain
        :param path: (string) Path to filename
        :param filename: (string) Filename
        :return: (bool) File loaded
        """

        if path is None:
            path = os.path.dirname(__file__)

        if filename is None:
            filename = 'blockchain.chain'

        self.__save_file = os.path.join(path, filename)

        if os.path.exists(self.__save_file):
            try:
                with open(self.__save_file, 'rb') as file:
                    self.__chain = pickle.load(file)
                    self.__index = len(self.__chain) - 1
            except Exception as err:
                print(err)
                self.autosave(False)
                return False
        else:
            print('File not found')
            self.autosave(False)
            return False

        if self.validate():
            self.autosave(True)
            return True
        else:
            self.autosave(False)
            return False

    @staticmethod
    def __parse_chain(chain):
        """
        Return the chain with the data only
        :param chain: (list) Blockchain
        :return: (list) Parsed blockchain
        """
        parsed_chain = []
        for block in chain:
            parsed_chain.append(block['block_data'].copy())

        return parsed_chain

    @staticmethod
    def __get_hash(dictionary):
        """
        Calculate a hash
        You can change hashing method here
        Hashing methods: hashlib.algorithms_guaranteed
        :param dictionary: (dict) Dictionary to hash
        :return: (int) Unique hashed value
        """
        string_dictionary = json.dumps(dictionary)
        hashed = hashlib.blake2b(bytes(string_dictionary, 'utf-8')).hexdigest()
        return hashed
