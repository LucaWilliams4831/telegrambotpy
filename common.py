# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0

import os
#https://fullnode.mainnet.aptoslabs.com
#https://fullnode.devnet.aptoslabs.com/v1
#:!:>section_1
NODE_URL = os.getenv("APTOS_NODE_URL", "https://fullnode.mainnet.aptoslabs.com")
FAUCET_URL = os.getenv(
    "APTOS_FAUCET_URL",
    "https://tap.devnet.prod.gcp.aptosdev.com",  # "https://faucet.testnet.aptoslabs.com"
)  # <:!:section_1
