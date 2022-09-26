
import math
from tkinter import ARC
import matplotlib.pyplot as plt
import numpy as np

# 31556926 = seconds per year
# 384 = seconds per epoch
# 31556926 / 384 = epochs per year
# 64 = BASE_REWARD_FACTOR
# 31622 = sqrt(gwei per ETH) = so it's basically sqrt(10^9)
# x -> math.exp(x)-1 to account for compounding

## ETH PARAMETERS
# CIRRCULATING_SUPPLY = 122500000;
# TOTAL_STAKED_SUPPLY = 14602000;
# DEPOSIT_REQ = 32;
# VALIDATOR_COUNT = 456312;    #TOTAL_STAKED_SUPPLY/DEPOSIT_REQ;

# SECONDS_PER_EPOCH = 384;
# EPOCHS_PER_YEAR = 31556926 / SECONDS_PER_EPOCH;
# BASE_REWARD_FACTOR = 64;
# BASE_REWARDS_PER_EPOCH = 4;

## SOAR PARAMETERS
ESTIMATED_MARKET_CAP = 500_000_000 # $500.000.000
MAX_SUPPLY = 100_000_000;
CIRRCULATING_SUPPLY = MAX_SUPPLY / 2;

ESTIMATED_PRICE = ESTIMATED_MARKET_CAP / CIRRCULATING_SUPPLY # $5 per SOAR coin

# CIRRCULATING_SUPPLY = ESTIMATED_MARKET_CAP / ESTIMATED_PRICE;

TOTAL_STAKED_SUPPLY = CIRRCULATING_SUPPLY * 0.2;     # ETH: 14602000;
DEPOSIT_REQ = 3000;                                  # $30.000 cost for being a validator
VALIDATOR_COUNT = TOTAL_STAKED_SUPPLY/DEPOSIT_REQ;

SECONDS_PER_EPOCH = 300;              # ETH: 384;
EPOCHS_PER_YEAR = 31556926 / SECONDS_PER_EPOCH;
BASE_REWARD_FACTOR = 50               # ETH: 64;
BASE_REWARDS_PER_EPOCH = 4;

SQRT_GWEI = 31622;
GWEI = 10**9;
# Protocol:
BASE_REWARDS_PROPOTIONAL_TO_VALIDATORS_ONLINE = 3
AVRG_ONLINE = 0.98

# Vitalik's formula
def calc_annual_reward(total_staked):
    return (math.exp(EPOCHS_PER_YEAR * BASE_REWARD_FACTOR / (GWEI* total_staked) ** 0.5) - 1) * 100

# Protocol formula
def calc_base_reward(total_staked, deposit_amount):
    result = (deposit_amount * GWEI) * BASE_REWARD_FACTOR / (((total_staked * GWEI) ** 0.5) * BASE_REWARDS_PER_EPOCH)
    # print("Base reward: " , result)
    return result

def calc_validator_interest(total_staked, deposit_amount):
    # baseReward = (deposit_amount * GWEI) * BASE_REWARD_FACTOR / ((total_staked * GWEI) ** 0.5) / BASE_REWARDS_PER_EPOCH
    baseReward = calc_base_reward(total_staked, deposit_amount)
    # print(baseReward)

    ## Online per validator reward
    step1 = baseReward * BASE_REWARDS_PROPOTIONAL_TO_VALIDATORS_ONLINE * AVRG_ONLINE
    step2 =  1*(0.125*baseReward*AVRG_ONLINE + 0.875*baseReward*(AVRG_ONLINE+AVRG_ONLINE*(1 - AVRG_ONLINE)*(1 - BASE_REWARDS_PROPOTIONAL_TO_VALIDATORS_ONLINE)+AVRG_ONLINE*(1 - AVRG_ONLINE)**2*(1 - 2*BASE_REWARDS_PROPOTIONAL_TO_VALIDATORS_ONLINE)));
    online_per_validator_reward_per_epoch = step1 + step2;
    # print(online_per_validator_reward_per_epoch)

    ## Offline validator penalty
    offline_per_validator_penalty_per_epoch = baseReward * BASE_REWARDS_PER_EPOCH
    # print(offline_per_validator_penalty_per_epoch)

    validatorInterest = (online_per_validator_reward_per_epoch * AVRG_ONLINE - offline_per_validator_penalty_per_epoch * (1 - AVRG_ONLINE)) * EPOCHS_PER_YEAR / GWEI / deposit_amount;
    return (math.exp(validatorInterest) - 1) * 100;

def generated_coin_per_year(total_staked, deposit_amount, validator_count):
    baseReward = calc_base_reward(total_staked, deposit_amount)
    ## Online per validator reward
    step1 = baseReward * BASE_REWARDS_PROPOTIONAL_TO_VALIDATORS_ONLINE * AVRG_ONLINE
    step2 =  1*(0.125*baseReward*AVRG_ONLINE + 0.875*baseReward*(AVRG_ONLINE+AVRG_ONLINE*(1 - AVRG_ONLINE)*(1 - BASE_REWARDS_PROPOTIONAL_TO_VALIDATORS_ONLINE)+AVRG_ONLINE*(1 - AVRG_ONLINE)**2*(1 - 2*BASE_REWARDS_PROPOTIONAL_TO_VALIDATORS_ONLINE)));
    online_per_validator_reward_per_epoch = step1 + step2;
    # print("online: " , online_per_validator_reward_per_epoch)
    ## Offline validator penalty
    offline_per_validator_penalty_per_epoch = baseReward * BASE_REWARDS_PER_EPOCH
    # print("offline: " , offline_per_validator_penalty_per_epoch)

    return (online_per_validator_reward_per_epoch*validator_count*AVRG_ONLINE - offline_per_validator_penalty_per_epoch*validator_count*(1-AVRG_ONLINE)) * EPOCHS_PER_YEAR / GWEI

def generated_coin_per_day(total_staked, deposit_amount, validator_count):
    return generated_coin_per_year(total_staked, deposit_amount, validator_count) / 365;

def network_issuance(total_staked, deposit_amount, validator_count):
    return generated_coin_per_year(total_staked, deposit_amount, validator_count) / CIRRCULATING_SUPPLY * 100

def supply_with_simple_interest(cirrculating_supply_t0, interest_rate, years):
    # A = P (1 + rt)
    return (cirrculating_supply_t0 * (1 + interest_rate * years))

# def supply_with_compounding_effect(cirrculating_supply_t0, interest_rate, years):
#     # A = P(1 + r/n)^(nt)
#     # n -> number of interest applied per period
#     n = 365
#     return (cirrculating_supply_t0 * (1 + interest_rate/n)**(years*n))

# def supply_with_generated_annual_coin(cirrculating_supply_t0, total_staked, deposit_amount, validator_count, years):
#     annualGenerated = generated_coin_per_year(total_staked, deposit_amount, validator_count)
#     return (cirrculating_supply_t0 + years*annualGenerated)
print("Estimated Price: ", ESTIMATED_PRICE)
print("Validator Count: ", VALIDATOR_COUNT)

print("Rewards with Vitalik's simple formula: %" , calc_annual_reward(TOTAL_STAKED_SUPPLY))
print("Rewards with protocol parameters: %" , calc_validator_interest(TOTAL_STAKED_SUPPLY, DEPOSIT_REQ))
print("Generated coin per year with this model: " , generated_coin_per_year(TOTAL_STAKED_SUPPLY, DEPOSIT_REQ, VALIDATOR_COUNT))
print("Generated coin per day with this model: " , generated_coin_per_day(TOTAL_STAKED_SUPPLY, DEPOSIT_REQ, VALIDATOR_COUNT))
print("Annual network issuance: " , network_issuance(TOTAL_STAKED_SUPPLY, DEPOSIT_REQ, VALIDATOR_COUNT))
print("Supply with simple effect: " , supply_with_simple_interest(CIRRCULATING_SUPPLY, network_issuance(TOTAL_STAKED_SUPPLY, DEPOSIT_REQ, VALIDATOR_COUNT), 10))

# print("Supply according to annual coin issuance: " , supply_with_generated_annual_coin(CIRRCULATING_SUPPLY, TOTAL_STAKED_SUPPLY, 32, VALIDATOR_COUNT, 10))
# print("Supply with compounding effect: " , supply_with_compounding_effect(CIRRCULATING_SUPPLY, network_issuance(TOTAL_STAKED_SUPPLY, DEPOSIT_REQ, VALIDATOR_COUNT), 10))






