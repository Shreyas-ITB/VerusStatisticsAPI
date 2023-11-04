# VerusStatisticsAPI

This is a Multipurpose VerusCoin API is created to provide the information of the verus-ethereum bridge, it also provides a variety of different transaction handling functions, that you can use to fetch various different price information, weights, currencystate and many more.

## API URL
``http://116.203.53.84:5000``

## Endpoints

- `/ ` Returns the API is running.
- ```/price/<ticker>``` Returns the price of VRSC in different currencies and values along with the 24 hour change.
- ```/difficulty``` Returns the current network difficulty and formats it into readable form.
- ```/getcurrencystate/<currency>/<height>``` Returns the currency state of bridged coins.
- ```/getrawtransaction/<txid>``` Returns the raw transaction details.
- ```/decoderawtransaction/<hex>d``` Returns the decoded data of a raw transaction.
- ```/blockcount``` Returns the block height of verus.
- ```/getcurrencies``` Returns the available currencies on the bridge network.
- ```/dai_reserves``` Returns the reserve value of DAI on the bridge network.
- ```/vrsc_reserves``` Returns the reserve value of VRSC on the bridge network.
- ```/mkr_reserves``` Returns the reserve value of MKR on the bridge network.
- ```/eth_reserves``` Returns the reserve value of vETH on the bridge network.
- ```/getticker/<currency_id>``` Returns the ticker of the given currencyID.
- ```/fetchblockhash/<longest_chain>``` Returns the fetched blockhash.
- ```/fetchtransactiondata/<transaction_id>``` Returns the transaction data of a transaction ID.
- ```/getmoneysupply``` Returns the money supply of VRSC.
- ```/distribution``` Returns the distribution of VRSC in the network.
- ```/getnethashpower``` Returns the network hashrate and formats it into readable form.
- ```/getweight``` Returns the weights of the currencies on the bridge.
- ```/getbridgedaiprice``` Returns the bridge reserve price of DAI.
- ```/getbridgevrscprice``` Returns the bridge reserve price of VRSC.
- ```/getbridgemkrprice``` Returns the bridge reserve price of MKR.
- ```/getbridgeethprice``` Returns the bridge reserve price of ETH.
- ```/getdaiveth_daireserveprice``` Returns the DAI.veth price in DAI reserve.
- ```/getvrsc_daireserveprice``` Returns the VRSC price in DAI reserve.
- ```/getmkrveth_daireserveprice``` Returns the MKR.veth price in DAI reserve.
- ```/getveth_daireserveprice``` Returns the vETH price in DAI reserve.
- ```/getdaiveth_vrscreserveprice``` Returns DAI.veth price in VRSC reserve.
- ```/getvrsc_vrscreserveprice``` Returns VRSC price in VRSC reserve.
- ```/getmkrveth_vrscreserveprice``` Returns MKR.veth price in VRSC reserve.
- ```/getveth_vrscreserveprice``` Returns vETH price in VRSC reserve.
- ```/getdaiveth_mkrreserveprice``` Returns DAI.veth price in MKR reserve.
- ```/getvrsc_mkrreserveprice``` Returns VRSC price in MKR reserve.
- ```/getmkrveth_mkrreserveprice``` Returns MKR.veth price in MKR reserve.
- ```/getveth_mkrreserveprice``` Returns vETH price in MKR reserve.
- ```/getdaiveth_vethreserveprice``` Returns DAI.veth price in vETH reserve.
- ```/getvrsc_vethreserveprice``` Returns VRSC price in vETH reserve.
- ```/getmkrveth_vethreserveprice``` Returns MKR.veth price in vETH reserve.
- ```/getveth_vethreserveprice``` Returns vETH price in vETH reserve.
- ```/getvolume/<currency>/<fromblock>/<toblock>``` Returns the volume and import details of the currency from block to block. 

More API Endpoints will be added in the future..

## Contributors
[![](https://avatars.githubusercontent.com/u/148117518?v=4?size=10)](https://github.com/ShreyaPrincess)
