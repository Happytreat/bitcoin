import bitcoin_script as rpc

''' 
# Create a multisig address in wallet. 
# Send x btc to multisig address. 
# Send back x btc to another address. 
'''

addList = []  # list of addresses
privKeyList = list()  # list of private keys for addresses

numSig = raw_input("Number of signatures required for multisig?")
numAdd = raw_input("Number of addresses?")

for i in range(int(numAdd)):
    new_address = rpc.getaddress()
    addList.append(new_address)
    if (i < int(numSig)):
        privKeyList.append(rpc.dumpprivkey(new_address))

print(rpc.validateaddress(addList[0]))
p2sh = rpc.createmultisig(numSig, addList)
p2sh_address = p2sh['address']
p2sh_redeem_script = p2sh['redeemScript']

x = raw_input("How much to send to multisig?")
utxo_txid = rpc.sendbtcto(x, p2sh_address)

x = raw_input("How much to send back from multisig?")
to_address = rpc.getaddress()
rpc.multisigTransaction(x, utxo_txid, p2sh_redeem_script, to_address, privKeyList)



