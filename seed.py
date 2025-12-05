import asyncio
import pandas as pd
from prisma import Prisma
from decimal import Decimal

async def main():
    print("Connecting to Database...")
    db = Prisma()
    await db.connect()

    print("Reading CSV file...")
    try:
        df = pd.read_csv('data.csv') # provide data as data.csv
    except FileNotFoundError:
        print("ERROR: Could not find 'data.csv'. Try again")
        await db.disconnect()
        return

    df.columns = [c.strip().lower() for c in df.columns]
    

    df['datetime'] = pd.to_datetime(df['datetime'])

    print(f"Found {len(df)} records. Inserting data (this may take a moment)...")

    count = 0
    
    for index, row in df.iterrows():
        exists = await db.candle.find_unique(
            where={'datetime': row['datetime']}
        )
        
        if not exists:
            await db.candle.create(
                data={
                    'datetime': row['datetime'],
                    # Convert float -> string -> Decimal to preserve precision
                    'open': Decimal(str(row['open'])),
                    'high': Decimal(str(row['high'])),
                    'low': Decimal(str(row['low']),),
                    'close': Decimal(str(row['close'])),
                    'volume': int(row['volume']) # Python int handles BigInt
                }
            )
            count += 1
            if count % 100 == 0:
                print(f"   Inserted {count} records...")

    print(f"SUCCESS: Inserted {count} new candles.")
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())