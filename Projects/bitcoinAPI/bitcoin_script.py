from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# rpc_user and rpc_password are set in the bitcoin.conf file
# enter ip address and port (18332 if testnet)
rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (user, password, ip, port))

'''
# to create a new address
# to run in terminal: 
# python -c "import bitcoin_script; NEW_ADDRESS1 = bitcoin_script.getaddress()"
'''


def getaddress():
    new_add = rpc_connection.getnewaddress()
    print("This is the new address: " + new_add)
    return new_add


'''
# to add a multisig address to wallet
# @param n is number of signatures required for multisig transaction 
# @param *args is the list of addresses
# @return p2sh is the pay-to-script-hash (multisig address) 
#
# python -c "import bitcoin_script; bitcoin_script.createmultisig(1, '$NEW_ADDRESS1', '$NEW_ADDRESS2')"
'''


def createmultisig(n, addList):
    pubList = []
    print(addList)
    for add in addList:  # We add the public key to a list (instead of the address)
        pubList.append(rpc_connection.validateaddress(add)['pubkey'])

    if int(n) > len(addList):  # more signatures required than addresses provided
        print("More signatures needed than addresses provided.")
        return -1
    p2sh = rpc_connection.addmultisigaddress(int(n), pubList)
    p2sh_address = p2sh['address']
    p2sh_redeem_script = p2sh['redeemScript']
    print("P2SH_Address: " + p2sh_address + "\n" + "P2SH_redeemScript: " + p2sh_redeem_script)
    return p2sh


# to validate addresses
def validateaddress(address):
    validation = rpc_connection.validateaddress(address)
    print("Is valid? ")
    print(validation['isvalid'])
    return validation


'''
# to send btc from a utxo multisig transaction to address 
# @param amount: amount to send from multisig to address
# @param utxo_txid: txid of previous multisig transaction 
# @param p2sh_redeem_script: of the previous multisig transaction 
# @param to_address: address to send to 
# @param privKeyList: list of private keys to sign the transaction 
# @return txid of signed transaction
'''


def multisigTransaction(amount, utxo_txid, p2sh_redeem_script, to_address, privKeyList):
    utxo = rpc_connection.getrawtransaction(utxo_txid, True)
    utxo_vout = utxo['vout'][0]['n']
    utxo_output_script = utxo['vout'][0]['scriptPubKey']['hex']
    raw_tx = rpc_connection.createrawtransaction([{"txid": str(utxo_txid), "vout": int(utxo_vout)}], {str(to_address):
                                                                                                          float(
                                                                                                              amount)})
    signed_raw_tx = rpc_connection.signrawtransaction(str(raw_tx), [{"txid": str(utxo_txid), "vout": int(utxo_vout),
                                                               "scriptPubKey": str(utxo_output_script),
                                                               "redeemScript": str(p2sh_redeem_script)}], privKeyList)
    print("Transaction id: ")
    print(signed_raw_tx)
    print(len(privKeyList))
    return rpc_connection.sendrawtransaction(signed_raw_tx['hex'], True)


# @return private key for address
def dumpprivkey(address):
    return rpc_connection.dumpprivkey(address)


'''
# send simple transactions
# create new address if no address provided by default
# to call function from terminal line: 
# python -c "import bitcoin_script; bitcoin_script.sendbtcto(0.001)"
'''


def sendbtcto(amount, address=rpc_connection.getnewaddress()):
    utxo_txid = rpc_connection.sendtoaddress(address, float(amount))
    print("Current balance is: " + str(rpc_connection.getbalance()))
    return utxo_txid


# sendbtcto(input("How much to send?"))


# list address groupings
def listaddressgroupings():
    addList = rpc_connection.listaddressgroupings()
    for add in addList:
        print(add)


'''
# to add a multisig address to wallet
# python -c "import bitcoin_script; bitcoin_script.createmultisig(1, '$NEW_ADDRESS1', '$NEW_ADDRESS2')"

def createmultisig(n, *args):
  addList=[]
  for add in args: #We add the public key to a list (instead of the address)
    addList.append(rpc_connection.validateaddress(add))
  if int(n) > len(addList): #more signatures required than addresses provided
    print ("More signatures needed than addresses provided.")  
  P2SH = rpc_connection.addmultisigaddress(int(n), addList[0], addList[1])
'''

'''
#getbalance
print(rpc_connection.getbalance())

#getnewaddress
new_add = rpc_connection.getnewaddress()
print(new_add)

best_block_hash = rpc_connection.getbestblockhash()
print(rpc_connection.getblock(best_block_hash))

# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
commands = [ [ "getblockhash", height] for height in range(100) ]
block_hashes = rpc_connection.batch_(commands)
blocks = rpc_connection.batch_([ [ "getblock", h  ] for h in block_hashes ])
block_times = [ block["time"] for block in blocks ]
print(block_times)
'''
