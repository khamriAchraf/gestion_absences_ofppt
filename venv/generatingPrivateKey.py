# import bitcoin
from bitcoin import *
from geopandas import *


# Generate a private key
my_private_key = random_key()
# display the private key
print("Private Key:%s\n" % my_private_key)
# Generate a public key, derived from private key
my_public_key = privtopub(my_private_key)
# display the public key
print("Public Key:%s\n" % my_public_key)
# Generate a Bitcoin Address
my_bitcoin_address = pubtoaddr(my_public_key)
# display the Bitcoin address
print("Bitcoin Address Key:%s\n" % my_bitcoin_address)
