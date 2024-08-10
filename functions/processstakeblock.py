from functions.getrawtransaction import get_rawtransaction
from functions.processtxncoinbase import processTransactionCoinbase
from functions.processtxnstaking import processTransactionStaking

def processStakeBlock(transactions, block):
    coinbaseRewardAddress = None
    stakingAmount = None
    block_reward = block.get("reward", {})
    block_height = block.get("height", "")
    block_hash = block.get("hash", "")
    validation_type = block.get("validationtype", "")
    
    new_blocks = []

    for transactionId in transactions:
        try:
            transaction = get_rawtransaction(transactionId)

            if not coinbaseRewardAddress:
                coinbaseReward = processTransactionCoinbase(transaction)
                if coinbaseReward:
                    coinbaseRewardAddress = coinbaseReward["address"]
            if coinbaseRewardAddress:
                staking_reward = processTransactionStaking(transaction, coinbaseRewardAddress)
                if staking_reward:
                    stakingAmount = staking_reward["amount"]
                    new_block = {
                        "blockHeight": block_height,
                        "blockHash": block_hash,
                        "validationType": validation_type,
                        "coinbaseRewardAddress": coinbaseRewardAddress,
                        "stakingAmount": stakingAmount,
                        "stakingAddress": staking_reward["address"],
                        "blockRewards": block_reward
                    }
                    new_blocks.append(new_block)
                    print(new_block)

        except Exception as error:
            print('Error fetching transaction data:', error)

    return new_blocks