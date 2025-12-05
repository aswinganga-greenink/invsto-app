import pandas as pd
from decimal import Decimal
from prisma import Prisma
from validation.schema import StratPerf

async def calc_strat(db: Prisma) -> StratPerf:
    candles = await db.candle.find_many(order={"datetime":"asc"})

    #edge case : no data
    if not candles:
        return StratPerf(
            strategy="No Data",
            total_ret_perc=Decimal(0),
            buy_signals=0,
            sell_signals=0
        )
    
    #extracing just the closing price and date
    data = [
        {"datetime":c.datetime, "close":float(c.close)} for c in candles
    ]

    df = pd.DataFrame(data=data)

    # short moving average with 10 candles and long moving avg with 50 candles
    df['short_mavg'] = df['close'].rolling(window=10).mean()
    df['long_mavg'] = df['close'].rolling(window=50).mean()

    buy_signals = 0
    sell_signals = 0
    position = None # None, 'LONG'
    entry_price = 0.0
    total_profit_pct = 0.0

    for i in range(50, len(df)):
        short = df['short_mavg'].iloc[i]
        long = df['long_mavg'].iloc[i]

        price = df['close'].iloc[i]

        prev_short = df['short_mavg'].iloc[i-1]
        prev_long = df['long_mavg'].iloc[i-1]

        if prev_short <= prev_long and short > long:
            if position != 'LONG':
                position = 'LONG'
                entry_price = price
                buy_signals += 1

        elif prev_short >= prev_long and short < long:
            if position == 'LONG':
                position = None
                trade_profit = (price - entry_price)/entry_price
                total_profit_pct += trade_profit 
                sell_signals += 1

    return StratPerf(
        strategy='Moving Average Crossover (10/50)',
        total_ret_perc=Decimal(total_profit_pct * 100).quantize(Decimal("0.01")),
        buy_signals=buy_signals,
        sell_signals=sell_signals
    )