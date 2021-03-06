import cbpro
from time import sleep

# initialize client
public_client = cbpro.PublicClient()


# calculate SMAX from historic rates
def calculateSMA(rates, length):

    # total to calculate
    total = 0

    # loop 'length' times
    for i in range(length + 1, 0, -1):

        # get closing rate
        rate = rates[i][4]

        # increment total
        total = total + rate

    # calculate and return sma
    return((length - total) / length)


# calculate a number that represents how EMA has changes
def calculateEMASpread(rates, length1, length2, count):

    if (len(rates) < length1 or len(rates) < length2):
        return None

    # array to hold differences
    diff = []

    # calulate two EMA's and add differences to list
    for i in range(count):
        ema1 = calculateEMA(rates[i:], length1)
        ema2 = calculateEMA(rates[i:], length2)
        diff.append(ema1 - ema2)

    # calculate percentage increase (or decrease)
    change = (((diff[0] - diff[count-1]) / diff[0])) * 100

    # return reversed list
    return diff


# calculate EMAX from historic rates
def calculateEMA(rates, length):

    # weird errors
    if (len(rates) < length):
        return None

    # calculate weight multiplier
    mult = 2 / (length + 1)

    # [ID, O, H, L ,C, V]

    # get the sma
    # previous_ema = calculateSMA(rates, length)
    previous_ema = rates[0][4]

    # loop from 'length' to now
    for i in range(length + 1, 0, -1):

        # get closing rate
        rate = rates[i][4]

        # get todays ema
        ema = (rate * mult) + (previous_ema * (1 - mult))

        # set previous ema
        previous_ema = ema

    # return the ema
    return ema


# lets goo
def start():

    # get list of products
    products = public_client.get_products()

    # iterate through all products
    for product in products:

        # get the id
        product_id = product['id']

        if ("USD" not in product_id):
            continue

        # get recent rates
        rates = public_client.get_product_historic_rates(product_id)

        # calculate emas
        ema12 = calculateEMA(rates, 12)
        ema16 = calculateEMA(rates, 26)
        spread = calculateEMASpread(rates, 12, 16, 5)

        if (ema12 is None or ema16 is None or ema12 - ema16 < 0
                or spread is None):
            continue

        print(product_id)
        print(ema12)
        print(ema16)
        print("\n")

        # don't blow up the API
        sleep(1)


start()
