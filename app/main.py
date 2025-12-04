from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from typing import List
from prisma import Prisma
from validation.schema import CandleCreate, CandleResponse

db = Prisma()

# lifespan to avoid any unexpected crashes or halfbaked process before db starts up.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # starting up db

    print("Connecting to DB...")
    await db.connect()
    yield

    # disconnecting from db

    print("Disconnecting from DB...")
    await db.disconnect()

app = FastAPI(lifespan=lifespan, title="Invsto trading api")

#Post req from /data - create new candle
@app.post("/data", response_model=CandleResponse)
async def create_candle(candle: CandleCreate):
    try:
        data = candle.model_dump()

        new_record = await db.candle.create(data=data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_record


#get req from /data - fetch all candles
@app.get("/data", response_model=List[CandleResponse])
async def get_candle():
    records = await db.candle.find_many(order={'datetime':'asc'}) #retrive data in ascending order by date

    return records