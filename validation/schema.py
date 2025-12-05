from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from decimal import Decimal

# Base model definition
class CandleBase(BaseModel):
    datetime : datetime

    open: Decimal = Field(..., gt=0, description='Opening price') #Greater than 0 only
    high : Decimal = Field(..., gt=0, description='Highest price possible') #Same
    low: Decimal = Field(..., gt=0, description='Lowest price possible') #Same
    close: Decimal = Field(..., gt=0, description='Closing price') #Same

    volume: int = Field(..., ge=0, description='Volume') # Greater than or equal to 0

    # ConfigDict to accpet both dict i/p and obj i/p
    model_config = ConfigDict(populate_by_name=True)


# POST call validation model
class CandleCreate(CandleBase):

    #ensure the value is a number
    @field_validator('high')
    @classmethod
    def valid_high(cls, v, info):
        return v

#GET call validation model
class CandleResponse(CandleBase):
    id: int #extra attr

    model_config = ConfigDict(from_attributes=True) #Read only from db obj

    
class StratPerf(BaseModel):
    strategy : str
    total_ret_perc : Decimal
    buy_signals : int
    sell_signals : int