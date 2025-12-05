import unittest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi.testclient import TestClient
from datetime import datetime
from decimal import Decimal

from app.main import app
from logic.startegy import calc_strat
from validation.schema import StratPerf

class TestTradingApp(unittest.IsolatedAsyncioTestCase):

    #Testing async functions

    def setUp(self):
        self.client = TestClient(app)
        #Test Client for sending fake api calls

    def test_case_candle_invalid_type(self):
        payload = {
            "datetime": "2023-01-01T10:00:00",
            "open": "invalid-price", # invalid type ( decimal value ) status code 422
            "high": 105.0,
            "low": 99.0,
            "close": 101.0,
            "volume": 1000
        }

        response = self.client.post("/data", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_candle_negative_price(self):

        payload = {
            "datetime": "2023-01-01T10:00:00",
            "open": -100.00, # Negative price
            "high": 105.0,
            "low": 99.0,
            "close": 101.0,
            "volume": 1000
        }
        response = self.client.post("/data", json=payload)
        self.assertEqual(response.status_code, 422)



    async def test_get_candles(self):
        """
        Requirement: Fetch all records.
        We mock the database to return one candle and ensure the API returns 200 OK.
        """
        # Mock the DB response
        mock_db = MagicMock()
        mock_candle = MagicMock()
        mock_candle.id = 1
        mock_candle.open = Decimal("100.00")
        mock_candle.high = Decimal("105.00")
        mock_candle.low = Decimal("99.00")
        mock_candle.close = Decimal("102.00")
        mock_candle.volume = 1000
        mock_candle.datetime = datetime.now()
        

        mock_db.candle.find_many = AsyncMock(return_value=[mock_candle])


        with patch("app.main.db", mock_db):
            response = self.client.get("/data")
            

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)





    
    
    async def test_strategy_logic_calculation(self):
        mock_db = MagicMock()
        # fake test db

        mock_candles = []

        for i in range(60):
            candle = MagicMock()
            candle.datetime = datetime(2025, 1, 1)
            candle.close = Decimal(100+i)
            mock_candles.append(candle)

        mock_db.candle.find_many = AsyncMock(return_value=mock_candles)

        result = await calc_strat(mock_db)

        self.assertIsInstance(result, StratPerf)
        self.assertEqual(result.strategy, "Moving Average Crossover (10/50)")

        print(f"\nTest Result - Buy Signals: {result.buy_signals}, Return: {result.total_ret_perc}%")

if __name__ == "__main__":
    unittest.main()
