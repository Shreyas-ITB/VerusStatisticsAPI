from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
RPCURL = os.environ.get("VRSCRPCURL")
VARRRRPCURL = os.environ.get("VARRRRPCURL")
VDEXRPCURL = os.environ.get("VDEXRPCURL")
PORT = os.environ.get("APIPORT")
ETHERSCANAPI = os.environ.get("ETHERSCANAPIKEY")
INFURAURL = os.environ.get("INFURAURL")
# RPCUSER=
# RPCPASS=