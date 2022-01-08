import datetime
import hashlib
import json
from flask import Flask, jsonify,request

# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(owner='creator' , Reg_no ='001' , proof = 1 , prev_hash='0')

    def create_block(self, owner ,Reg_no , proof, prev_hash):
        block = {'owner':owner,
                 'Reg_no':Reg_no,
                 'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}
        self.chain.append(block)
        return block

    def proof_of_work(self , prev_proof):

        new_proof = 1 
        check_proof = False
        while check_proof is False:
            hash_val = hashlib.sha256( str(new_proof**2 - prev_proof**2).encode()).hexdigest()

            if hash_val[:4] == '0000' :
                check_proof = True
            else:
                new_proof+=1
        
        return new_proof

    def hash(self , block):
        encoded_block = json.dumps(block).encode()

        return hashlib.sha256(encoded_block).hexdigest()
        
