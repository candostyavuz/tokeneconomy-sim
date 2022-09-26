BLOCK_TIME = 10 # seconds
EPOCH_SIZE = 30 # blocks

TARGET_MONTHLY_MINT_AMOUNT = 2_500_000 # subject to halving

MINTUES_PER_MONTH = 43200

def mint_per_epoch():
    epochPerMonth = MINTUES_PER_MONTH / (EPOCH_SIZE * BLOCK_TIME / 60);
    return TARGET_MONTHLY_MINT_AMOUNT / epochPerMonth

print("Mint per epoch = ", mint_per_epoch())