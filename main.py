

from more_itertools import last
import requests
# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0
import time
import os
from dotenv import load_dotenv


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
from coinmarketcapapi import CoinMarketCapAPI


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
            f"0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::dao_storage::Storage<0x1::aptos_coin::AptosCoin, 0x5096d4314db80c0fde2a20ffacec0093e41ce6517bbe11cb9572af2bd8ef0303::tesla_token::TeslaToken, 0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::curves::Uncorrelated>",
        )
        return balance

    def get_reserves(
        self,
        account_address: AccountAddress,
        token_address: str,
    ) -> str:
        """Returns the coin balance of the given account"""

        data = self.account_resource(
            account_address,
            f"0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::dao_storage::Storage<0x1::aptos_coin::AptosCoin, " +
            token_address+", 0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::curves::Uncorrelated>",
        )
        return data["data"]["coin_x"]["value"], data["data"]["coin_y"]["value"]

    def get_liquidity_pool_info(
        self,
        account_address: AccountAddress,
        token_address: str,
    ) -> str:
        """Returns the coin balance of the given account"""

        data = self.account_resource(
            account_address,
            f"0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::liquidity_pool::LiquidityPool<0x1::aptos_coin::AptosCoin, " +
            token_address+", 0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::curves::Uncorrelated>",
        )
        return data


# get the latest price of APT from coinmarketcap

def get_apt_price(amount):
    apt_price = cmc.cryptocurrency_quotes_latest(symbol='APT', convert='USD')
    apt_price = apt_price.data['APT']['quote']['USD']['price']
    return apt_price * amount


def send_video(chat_id, image_path, image_caption=""):
    data = {"chat_id": chat_id, "caption": image_caption}
    url = f"https://api.telegram.org/bot{TOKEN}/sendVideo?chat_id={chat_id}"
    # url = "https://api.telegram.org/%s/sendPhoto" % TOKEN
    with open(image_path, "rb") as image_file:
        ret = requests.post(url, data=data, files={"video": image_file}).json()
        # telegram_request = requests.get(url).json()
        print(ret)


def send_message(token, chat_id, img, message):
    r = requests.get('https://api.telegram.org/bot' + token + '/sendMessage?chat_id='+str(
        chat_id)+'&parse_mode=markdown&text='+"[​​​​​​​​​​​]("+img+")" + message).json()
    print


def get_percentage_increase(num_a, num_b):
    return ((num_a - num_b) / num_b) * 100


def create_message(differ, coin_x, coin_last_x, coin_y, chart, tracker, trending):

    message = "Buy!\n"
    price = round(get_apt_price(differ), 4)
    price_change_percentage = get_percentage_increase(
        int(coin_x), int(coin_last_x))
    price_change_percentage *= 10
    # for x in range(0, int(differ + 1)):
    for x in range(0, int(differ) + 1):
        message += "🟢"
    message += "\n"
    message += "💵" + str(round(differ, 4)) + " APT ($" + str(price) + ")\n"
    # message += str(coin_y) + "  " + str(coin_last_y)

    # message += "🪙"  + str(abs(int(coin_y) - int(coin_last_y))) + " TSLA\n"
    message += "🪙" + \
        str(round(float(coin_y) * 1e-6, 2)) + " TSLA\n"
    message += "⏫ Position +" + \
        str(round(price_change_percentage, 4))+"%\n"
    message += "🔘 Market Cap $" + \
        str(round(get_apt_price(float(coin_x) * 1e-6), 2)) + "\n\n"
    message += '📊 [Chart]('+chart+')'
    message += '⚙️ [Tracker]('+tracker+')'
    message += '🔵 [Trending]('+trending+')'

    return message

# All liquidity pools resources and LP coins currently placed at the following resource account:
# 0x05a97986a9d031c4567e15b797be516910cfcb4156312482efc6a19c0a30c948


# Liquidswap modules are deployed at the following address:
# 0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12
if __name__ == "__main__":
    load_dotenv()
    cmc = CoinMarketCapAPI(os.getenv('CMC_API'))
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    token_address = os.getenv('TOKEN_ADDRESS')
    chat_id = os.getenv('CHAT_ID')
    img = os.getenv('GIF_URL')
    chart = os.getenv('CHART_URL')
    tracker = os.getenv('TRACKER_URL')
    trending = os.getenv('TRENDING_URL')

    coin_last_x = 1
    coin_last_y = 1
    rest_client = CoinClient("https://fullnode.mainnet.aptoslabs.com/v1")
    index = 0

    while True:
        (coin_x, coin_y) = rest_client.get_reserves(
            "0x05a97986a9d031c4567e15b797be516910cfcb4156312482efc6a19c0a30c948", token_address)

        print("coin_x", coin_x)
        print("coin_y", coin_y)
        print("coin_x", coin_last_x)
        print("coin_last_y", coin_last_y)
        print("")

        if int(coin_x) != int(coin_last_x):
            differ = (float(coin_x) - float(coin_last_x)) * 1e-5
            print("differ", differ)
            if differ > 0:
                coin_last_x = coin_x
                coin_last_y = coin_y
                print("BUY")

                message = create_message(differ, coin_x, coin_last_x, coin_y, chart, tracker, trending)

                if index != 0:
                    print("SEND")
                    print(message)
                    #send_message(TOKEN, chat_id, img, message)
            else:
                print("SELL")
        index = index + 1
        time.sleep(2)
