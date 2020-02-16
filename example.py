#!/usr/bin/env python3

import random
import time

import blockchains


class Timer:
    """
    Simple class to easily time the results
    """

    def __init__(self, message='{:0.3f}'):
        self.__message = message
        self.__start_time = time.time()

    def __del__(self):
        self.__end_time = time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.print()

    def get_time(self):
        return time.time() - self.__start_time

    def print(self):
        print(self.__message.format(self.get_time()))


def main():
    """
    Demonstrate the functions of the data structure
    :return: (void)
    """

    # Set a path for our block chain
    blockchain_path = '/tmp/'
    title_width = 120

    """
    Creation
    """
    title('Creation', title_width)

    # Create out block chain
    print('\nCreating a new blockchain...')
    blockchain = blockchains.Blockchain()

    # Save our block chain
    print('\nSave chain...')
    blockchain.save(path=blockchain_path)

    # Create some data and add some indexes
    records_to_add = 50
    print('\nCreate some data...')
    # Create at least one record that we know will exist for the purposes of this test
    block_id = blockchain.append({'sender': 'Karen', 'recipient': 'William', 'transaction': 100001, 'amount': 30})
    print('Created index: {}'.format(block_id))
    # Create random data
    for index in range(records_to_add):
        block_id = blockchain.append(fake_transaction())
        if block_id % (records_to_add / 10) == 0:
            print('Created index: {}'.format(block_id))

    """
    Searching
    """
    title('Searching', title_width)

    # Search for a record by key and value, the key does not need to be in the record
    key = 'sender'
    for value in ['Linda', 'Susan', 'Karen', 'William', 'James', 'David', 'Christopher']:
        print('\nSearch blockchain for {}: {}'.format(key, value))
        results = blockchain.find_key_value(key, value, insensitive=True)
        if len(results) > 0:
            for result in results:
                print('Found data: {}'.format(result))
        else:
            print('No results found')

    # Search for a record by key and with a range of values, the key does not need to be in the record
    key = 'amount'
    lower = random.randrange(0, 250)
    upper = random.randrange(lower + 1, 250)
    print('\nSearch blockchain for {}s in the range of {} - {}'.format(key, lower, upper))
    results = blockchain.find_key_value_range(key, lower, upper)
    if len(results) > 0:
        for result in results:
            print('Found data: {}'.format(result))
    else:
        print('No results found')

    # Search for a  value in any key,
    value = 'Susan'
    print('\nSearch blockchain for any key with the value of {}'.format(value))
    results = blockchain.find_key_value_any(value, insensitive=True)
    if len(results) > 0:
        for result in results:
            print('Found data: {}'.format(result))
    else:
        print('No results found')

    """
    Retrieving sections
    """
    title('Retrieving sections', title_width)

    # Get a specific record
    index = random.randint(0, records_to_add)
    print('\nReturn index {} in blockchain'.format(index))
    block = blockchain.get_index(index)
    if block is None:
        print('Block not found')
    else:
        print(block)

    # Get a block while verifying it
    index = random.randint(0, records_to_add)
    print('\nReturn index {} in blockchain if verified'.format(index))
    block = blockchain.get_verified_index(index)
    if block is None:
        print('Block not found')
    else:
        if not block:
            print('Block is compromised')
        else:
            print(block)
            # Get the metatdata of the block if verified
            print('Metadata:')
            print(blockchain.get_index_metadata(index))

    # Validate a block number
    print('\nVerify a block:')
    index = random.randint(0, records_to_add)
    if blockchain.verify_index(index):
        print('Block {} is intact'.format(index))
    else:
        print('Block {} is compromised'.format(index))

    # Return a range of blocks
    index_low = random.randint(0, records_to_add)
    index_high = random.randint(index_low, (records_to_add - 1))
    print('\nReturn range ({}, {}) in blockchain:'.format(index_low, index_high))
    for block in blockchain.get_indexes(index_low, index_high):
        print(block)

    # Return a range by dates
    date_start = 0
    date_end = time.time() - 0.002
    print('\nReturn a date range ({} to {}):'.format(time.ctime(date_start), time.ctime(date_end)))
    for block in blockchain.get_date_range(date_start, date_end):
        print(block)

    # Get the whole chain
    print('\nReturn the whole blockchain:')
    for block in blockchain.get_chain():
        print(block)

    # Get the length
    print('\nReturn the length of the chain:')
    print('Chain is {} in length'.format(blockchain.get_chain_length()))

    # Verify the whole chain
    print('\nVerify the whole blockchain:')
    if blockchain.validate():
        print('Chain is intact')
    else:
        print('Chain is compromised')

    """
    Starting a new chain and loading in previous data
    """
    title('Starting a new chain and loading in previous data', title_width)

    # Create a new block chain to see saving and loading of data, will automatically save on deconstruction
    print('\nCreate new blockchain...')
    blockchain = blockchains.Blockchain()

    # Get the chain to see that our data is gone and it is a new chain
    print('\nCurrent blockchain:')
    print(blockchain.get_chain())

    # Load the saved chain
    print('\nLoad blockchain...')
    if blockchain.load(path=blockchain_path):

        # Dividing title
        title('Proof that the chain is again working', title_width)

        # See that our chain is restored
        print('\nCurrent blockchain:')
        for block in blockchain.get_chain():
            print(block)

        # Validate the chain
        print('\nVerify the whole blockchain:')
        if blockchain.validate():
            print('Chain is intact')
        else:
            print('Chain is compromised')

        # Create some more data to see that we are appending to the chain
        print('\nCreate some more data...')
        new_record_count = 10
        for index in range(new_record_count):
            blockchain.append(fake_transaction())
        print('Created {} records'.format(new_record_count))

        # Try to break corrupt the data
        index = 0
        print('\nAttempting to mutate the transaction id of {}'.format(index))
        blockchain.get_chain()[index]['transaction'] = 0
        blockchain.get_index(index)['transaction'] = 0
        blockchain.get_indexes(index, index)[0]['transaction'] = 0
        blockchain.get_verified_index(index)['transaction'] = 0
        blockchain.get_date_range(0, time.time())[0]['transaction'] = 0
        blockchain.find_key_value('sender', 'Karen', insensitive=True)[0]['transaction'] = 0
        blockchain.get_index_metadata(index)['block_epoch_time'] = 0

        try:
            # Try to access the resource directly from the class
            blockchain.__chain[0]['block_epoch_time'] = 0
        except Exception as err:
            print(err)

        # Validate the chain again.  Not matter which way we get the data, the data is immutable
        print('\nVerify the whole blockchain:')
        if blockchain.validate():
            print('Chain is intact')
        else:
            print('Chain is compromised')

        """
        Pushing the block chain past a few data points
        Seeing how the data structure performs
        """
        title('Pushing the block chain past a few data points', title_width)

        # Number or records to create for the tests
        new_record_count = 1000000

        # Reduce the save frequency to speed up results
        save_freq = new_record_count / 20
        blockchain.autosave_freq(save_freq)

        with Timer('Time create {:,} records: {{:0.3f}}'.format(new_record_count)):
            # Create a ton more data to gauge performance
            print('\nCreate a ton more data...')
            for index in range(new_record_count + 1):
                blockchain.append(fake_transaction())
                if index % save_freq == 0:
                    # So we know ho far along we are in the test
                    print('{:,} records'.format(index))

        with Timer('Time to verify the chain: {:0.3f} seconds'):
            # Validate the chain again for gauging performance
            print('\nVerify the whole blockchain:')
            if blockchain.validate():
                print('Chain is intact')
            else:
                print('Chain is compromised')

        key = 'sender'
        value = 'Linda'
        with Timer('Time to find {}: {} {{:0.3f}} seconds'.format(key, value)):
            # Search for a record by key, the key does not need to be in the record
            print('\nSearch blockchain for {}: {}'.format(key, value))
            results = blockchain.find_key_value(key, value, insensitive=True)
            print('Found {:,} record(s)'.format(len(results)))

        key = 'amount'
        lower = random.randrange(0, 250)
        upper = random.randrange(lower + 1, 250)
        with Timer('Time to find {}s from {} to {}: {{:0.3f}} seconds'.format(key, lower, upper)):
            # Search for a record by key and with a range of values, the key does not need to be in the record
            print('\nSearch blockchain for {}s in the range of {} - {}'.format(key, lower, upper))
            results = blockchain.find_key_value_range(key, lower, upper)
            print('Found {:,} record(s)'.format(len(results)))

        value = 'Susan'
        with Timer('Time to find {}: {{:0.3f}} seconds'.format(value)):
            # Searching for all records with a value
            print('\nSearch blockchain for any key with the value of {}'.format(value))
            results = blockchain.find_key_value_any(value, insensitive=True)
            print('Found {:,} record(s)'.format(len(results)))

        # Dividing title
        title('Finished', title_width)


def fake_transaction():
    """
    Generate random data for the example
    :return: (dict) Fake transactional data
    """
    fake_user_names = ['Linda', 'Susan', 'Karen', 'Carol', 'Sarah', 'Barbara', 'Margaret', 'Betty', 'Ruth', 'Kimberly',
                       'James', 'David', 'Christopher', 'George', 'Ronald', 'John', 'Richard', 'Daniel', 'Kenneth', 'Anthony']
    fake_user_count = len(fake_user_names) - 1

    first_user_id = random.randint(0, fake_user_count)
    first_user = fake_user_names[first_user_id]

    fake_user_names_alt = fake_user_names.copy()
    del fake_user_names_alt[first_user_id]

    second_user_id = random.randint(0, fake_user_count - 1)
    second_user = fake_user_names_alt[second_user_id]

    return {'sender': first_user, 'recipient': second_user, 'transaction': random.randrange(100000, 999999), 'amount': random.randint(0, 25000) / 100}


def title(title_text='', width=40):
    """
    Create a dividing title
    :param title_text: (str) Title text
    :param width: (str) Width of the divider
    :return: (void)
    """
    sides = int(((width - len(title_text)) / 2) - 2)
    print('\n', '-' * sides, title_text, '-' * sides)


if __name__ == '__main__':
    main()
