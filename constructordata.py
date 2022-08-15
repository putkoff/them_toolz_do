from sha3 import sha3_256
from eth_abi import encode_abi
from datetime import date
def const_it(x):
    print(x)
    
    x[1] = x[1].replace("'",'"')
    return read_hex(encode_abi([x[0].replace("'",'"')],[x[1]]))
def read_hex(hb):
    h = "".join(["{:02X}".format(b) for b in hb])
    return h

y = []
x = ['string','tier_1'],['string','TR1']
for i in range(0,len(x)):
    y.append('0x'+const_it(x[i]))
print(y)
