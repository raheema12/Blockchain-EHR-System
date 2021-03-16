

#block.py file

import datetime
from hashlib import sha256

#changed data to transactions

class Block:
    def __init__(self, transactions, previous_hash):
        self.time_stamp = datetime.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.generate_hash()

    def generate_hash(self):
        block_header = str(self.time_stamp) + str(self.transactions) +str(self.previous_hash) + str(self.nonce)
        block_hash = sha256(block_header.encode())
        return block_hash.hexdigest()

    def print_contents(self):
        print("timestamp:", self.time_stamp)
        print("transactions:", self.transactions)
        print("current hash:", self.generate_hash())
        print("previous hash:", self.previous_hash)



#blockchain.py file
from block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.genesis_block()

    def genesis_block(self):
        transactions = []
        genesis_block = Block(transactions, "0")
        genesis_block.generate_hash()
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        previous_hash = (self.chain[len(self.chain)-1]).hash
        new_block = Block(transactions, previous_hash)
        new_block.generate_hash()
        # proof = proof_of_work(block)
        self.chain.append(new_block)

    def print_blocks(self):
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            print("Block {} {}".format(i, current_block))
            current_block.print_contents()

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if(current.hash != current.generate_hash()):
                print("Current hash does not equal generated hash")
                return False
            if(current.previous_hash != previous.generate_hash()):
                print("Previous block's hash got changed")
                return False
        return True
 
    def proof_of_work(self, block, difficulty=2):
        proof = block.generate_hash()
        while proof[:2] != "0"*difficulty:
            block.nonce += 1
            proof = block.generate_hash()
        block.nonce = 0
        return proof




#script.py file
from blockchain import Blockchain

block_one_transactions = {"sender":"Alice", "receiver": "Bob", "amount":"50"}
block_two_transactions = {"sender": "Bob", "receiver":"Cole", "amount":"25"}
block_three_transactions = {"sender":"Alice", "receiver":"Cole", "amount":"35"}
fake_transactions = {"sender": "Bob", "receiver":"Cole, Alice", "amount":"25"}

local_blockchain = Blockchain()
local_blockchain.print_blocks()

local_blockchain.add_block(block_one_transactions)
local_blockchain.add_block(block_two_transactions)
local_blockchain.add_block(block_three_transactions)
local_blockchain.print_blocks()
local_blockchain.chain[2].transactions = fake_transactions
local_blockchain.validate_chain()


#test1.py file

load_file_in_context('blockchain.py')

test_block = Block(1,0)

test_blockchain = Blockchain()

test_proof = test_blockchain.proof_of_work(test_block)

try:
  proof
  if proof == test_proof:
    pass_tests()
except:
  fail_tests("Did you create a variable called proof?")



#test2.py file
load_file_in_context('script.py')
import gc
import re

objs = gc.get_objects()[:]
blockchain_objects = []

for obj in objs:
  if(isinstance(obj, Blockchain)):
    blockchain_objects.append(obj)
    
blockchain = blockchain_objects[0]

if len(blockchain.chain) != 4:
  fail_tests('Did you add all three blocks to the blockchain?')

if blockchain.chain[1].transactions == block_one_transactions:
  if blockchain.chain[2].transactions == block_two_transactions:
    if blockchain.chain[3].transactions == block_three_transactions:
      with open('script.py','r') as file:
        occurences = len(re.findall('(local_blockchain)(\\.)(print_blocks)(\\(\\))', file.read()))
        if occurences == 2:
          pass_tests()
        else:
          fail_tests('Did you use the correct method to print the contents of the blockchain?')
    else:
      fail_tests('Did you add block_three_transactions into the correct block?')
  else:
    fail_tests('Did you add block_two_transactions into the correct block?')
else:
  fail_tests('Did you add block_one_transactions into the correct block?')


#test3.py file
load_file_in_context('script.py')
import gc
import re

objs = gc.get_objects()[:]
blockchain_objects = []

for obj in objs:
  if(isinstance(obj, Blockchain)):
    blockchain_objects.append(obj)
    
blockchain = blockchain_objects[0]

if blockchain.chain[2].transactions != fake_transactions:
  fail_tests('Did you modify the transactions to fake_transactions in the second block that was added?')
  
with open('script.py','r') as file:
  if re.search('(local_blockchain)(\\.)(validate_chain)(\\(\\))', file.read()):
    pass_tests()
  else:
    fail_tests('Did you use the correct method to validate the blockchain?')
