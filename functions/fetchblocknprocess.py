from functions.send_request import send_request
from var.vars import RPCURL
from functions.processstakeblock import processStakeBlock

def fetchBlocksAndProcess(num_blocks, block_hash):
    current_block_hash = block_hash
    blocks_processed = 0
    request_config_get_block = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getblock",
            "params": [],
            "id": 1
        }
    }

    def process_next_block():
        nonlocal blocks_processed, current_block_hash

        if blocks_processed >= num_blocks:
            return {"result": "Process completed"}
        request_config_get_block["data"]["params"] = [current_block_hash, True]

        try:
            # Simulate sending the request
            response = send_request(request_config_get_block)
            block = response["result"]
            validation_type = block["validationtype"]

            if validation_type == "stake":
                # Replace this with your actual implementation
                processStakeBlock(block)
                blocks_processed += 1

            current_block_hash = block["previousblockhash"]
        except Exception as error:
            return {"error": str(error)}

        return process_next_block()

    # Start the process with the initial call
    return process_next_block()