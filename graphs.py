from base_reward_model import calc_annual_reward, calc_validator_interest, network_issuance, supply_with_simple_interest #, supply_with_compounding_effect, supply_with_generated_annual_coin
import math
import matplotlib.pyplot as plt
import numpy as np

CIRRCULATING_SUPPLY = 122500000
TOTAL_STAKED_SUPPLY = 14602000
DEPOSIT_REQ = 32
VALIDATOR_COUNT = TOTAL_STAKED_SUPPLY/DEPOSIT_REQ


#  Inputs
total_stake_in = np.linspace(500000, 20000000, 1000000)

y = np.vectorize(calc_annual_reward)
y2 = np.vectorize(calc_validator_interest)
y3 = np.vectorize(network_issuance)
y4 = np.vectorize(supply_with_simple_interest)
# y5 = np.vectorize(supply_with_compounding_effect)
# y6 = np.vectorize(supply_with_generated_annual_coin)

figure, axis = plt.subplots(2, 2)

# ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%1.2e'))

# plt.ylim(1, 25)
# plt.xlim(500000, 25000000)
# x_tick = range(500000, 20000000, 1000000)
# y_tick = range(25, 1, -1)
# plt.xticks(x_tick, rotation ='vertical')
# plt.yticks(y_tick)
# plt.xlabel('Total staked amount')
# plt.ylabel('Validator interest %')
axis[0, 0].set_title('Annual Validator Interest')
axis[0, 0].plot(total_stake_in, y(total_stake_in))
# plt.plot(total_stake_in, y(total_stake_in))

# plt.show()

#  2
# plt.ylim(1, 25)
# plt.xlim(500000, 25000000)
# x_tick = range(500000, 20000000, 1000000)
# y_tick = range(25, 1, -1)
# plt.xticks(x_tick, rotation ='vertical')
# plt.yticks(y_tick)
# plt.xlabel('Total staked amount')
# plt.ylabel('Validator interest %')
# plt.title('Annual Validator Interest (Protocol)')

axis[0, 1].set_title('Annual Validator Interest (Protocol)')
axis[0, 1].plot(total_stake_in, y2(total_stake_in, 32), 'tab:green')

# for ax in axis.flat:
#     ax.set(xlabel='Total Staked', ylabel='Validator Interest %')

axis[1, 0].set_title("Network Issuance vs Total Staked Supply")
axis[1, 0].plot(total_stake_in, y3(
    total_stake_in, DEPOSIT_REQ, total_stake_in/DEPOSIT_REQ))

##
years = range(1, 30)
cirrculating_supply_t0 = 122500000
issuance_rate = 0.48331688444290744

axis[1, 1].set_title("Total Supply vs Years")
axis[1, 1].plot(years, y4(122500000, issuance_rate, years))


plt.show()
