

import requests
# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0

"""
This example depends on the MoonCoin.move module having already been published to the destination blockchain.

One method to do so is to use the CLI:
    * Acquire the Aptos CLI, see https://aptos.dev/cli-tools/aptos-cli-tool/install-aptos-cli
    * `python -m examples.your-coin ~/aptos-core/aptos-move/move-examples/moon_coin`.
    * Open another terminal and `aptos move compile --package-dir ~/aptos-core/aptos-move/move-examples/moon_coin --save-metadata --named-addresses MoonCoin=<Alice address from above step>`.
    * Return to the first terminal and press enter.
"""

import os
import sys

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer
from aptos_sdk.client import FaucetClient, RestClient
from aptos_sdk.transactions import (
    EntryFunction,
    TransactionArgument,
    TransactionPayload,
)
from aptos_sdk.type_tag import StructTag, TypeTag

from common import FAUCET_URL, NODE_URL


class CoinClient(RestClient):
    def register_coin(self, coin_address: AccountAddress, sender: Account) -> str:
        """Register the receiver account to receive transfers for the new coin."""

        payload = EntryFunction.natural(
            "0x1::managed_coin",
            "register",
            [TypeTag(StructTag.from_str(
                f"{coin_address}::moon_coin::MoonCoin"))],
            [],
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            sender, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)

    def mint_coin(
        self, minter: Account, receiver_address: AccountAddress, amount: int
    ) -> str:
        """Mints the newly created coin to a specified receiver address."""

        payload = EntryFunction.natural(
            "0x1::managed_coin",
            "mint",
            [TypeTag(StructTag.from_str(
                f"{minter.address()}::moon_coin::MoonCoin"))],
            [
                TransactionArgument(receiver_address, Serializer.struct),
                TransactionArgument(amount, Serializer.u64),
            ],
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            minter, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)

    def get_balance(
        self,
        coin_address: AccountAddress,
        account_address: AccountAddress,
    ) -> str:
        """Returns the coin balance of the given account"""

        balance = self.account_resource(
            account_address,
            f"0x1::coin::CoinStore<{coin_address}>",
        )
        return balance["data"]["coin"]["value"]

    def get_reserves(
        self,
        coin_address: AccountAddress,
        account_address: AccountAddress,
    ) -> str:
        """Returns the coin balance of the given account"""

        data = self.account_resource(
            account_address,
            f"0x1::coin::CoinStore<{coin_address}::tesla_token::TeslaToken>",
        )
        return data


if __name__ == "__main__":
    # All liquidity pools resources and LP coins currently placed at the following resource account:
    # 0x05a97986a9d031c4567e15b797be516910cfcb4156312482efc6a19c0a30c948

    # Liquidswap modules are deployed at the following address:
    # 0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12

    print("h")
    rest_client = CoinClient("https://fullnode.mainnet.aptoslabs.com/v1")
    # r = rest_client.get_balance("0x5096d4314db80c0fde2a20ffacec0093e41ce6517bbe11cb9572af2bd8ef0303", "0x6c8f6a9c2b66a2590b68c870bb61dd2fdab6d30bed7bc2e7cf7bd59265f04301")
    r = rest_client.get_balance("0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12", "0x05a97986a9d031c4567e15b797be516910cfcb4156312482efc6a19c0a30c948")
    print(r)    
    TOKEN = "5529214043:AAGGnFv6MZPE5-pFcaElPapazNY4_GHlUu8"
    chat_id = -618973730
    message = "hello from your telegram bot from luca"
    # url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    # print(requests.get(url).json()) # this sends the message
