from brownie import FundMe, MockV3Aggregator, accounts, config, network
from web3 import Web3
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

# LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"] # these lines should be in a diffrent helper file

# DECIMALS = 18
# STARTING_PRICE = 2000

def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    #if we are on a presistent network like rinkeby, use the associated address, otherwise deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account}, 
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"contract deployed to {fund_me.address}")
    return fund_me

# def get_account():
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#         return accounts[0]
#     else:
#         return accounts.add(config["wallets"]["from_key"]) 


def main():
    deploy_fund_me()