import datetime
import hashlib
import json
from flask import Flask, jsonify,request
#from werkzeug.datastructures import T

#creating the blockchain

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

    def is_chain_valid(self,chain): 

        prev_block = chain[0]
        block_idx = 1 

        while block_idx<len(chain):
            block = chain[block_idx]

            if block['prev_hash'] != self.hash(prev_block):
                return False
            
            prev_proof = prev_block['proof']
            proof=block['proof']

            hash_val = hashlib.sha256(str( proof**2 - prev_proof**2 ).encode()).hexdigest()
            if hash_val[:4] != '0000':
                return False

            prev_block = block
            block_idx+=1

        return True

    def get_previous_block(self):
        return self.chain[-1]



# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'We have a problem. The Blockchain is not valid.'}
        
    return jsonify(response), 200

@app.route('/mine_block' , methods = ['POST'])

def mine_block():

    values = request.get_json()

    required = ['owner' , 'Reg_no']

    if not all (k in values for k in required):
        return 'Missing values' , 400 #error 400 means syntax error

    owner = values['owner']

    Reg_no = values['Reg_no']

    prev_block = blockchain.get_previous_block()

    prev_proof = prev_block['proof']

    proof = blockchain.proof_of_work(prev_proof)

    prev_hash = blockchain.hash(prev_block)

    block = blockchain.create_block( owner , Reg_no , proof , prev_hash )

    response = { 'message' : 'The record has been added in the blockchain' }

    return jsonify(response) , 200
    
app.run( host = '0.0.0.0' , port = 5000 , debug=True ) # this host to allow local network p2p 


