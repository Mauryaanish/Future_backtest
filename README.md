# Future Backtest with 100 SL

This repository contains a Python program to perform a backtest on historical future data for the 'banknifty' and 'nifty' indices, applying a strategy involving stop-loss (SL) and profit-taking targets. The program retrieves data from a MongoDB database, processes the data, and saves the results to a CSV file.

Table of Contents
- Usage
- Program Details



Usage

1. Prepare your MongoDB data:
   - Ensure that your MongoDB databases and collections follow the naming convention used in the code. The databases should be named in the format `{index_name}_option_data_{date}` and should contain a `weekly` collection with the required data.

2. Run the program:
   python main.py
   - You will be prompted to enter the start and end dates in `ddmmyyyy` format.

Program Details
---------------
Data Retrieval (`data` function)
- Purpose: Retrieve historical data for a specified index and date range from MongoDB.
- Inputs:
  - `index_name`: Name of the index ('banknifty' or 'nifty').
  - `start_date`: Start date for data retrieval in `ddmmyyyy` format.
  - `end_date`: End date for data retrieval in `ddmmyyyy` format.
- Outputs: A list of MongoDB collections containing the historical data.

Process:
1. Connects to a MongoDB server at `localhost:27017`.
2. Converts the start and end dates to `datetime` objects.
3. Iterates through each day in the specified date range.
4. Constructs the database name based on the index and date.
5. Fetches the 'weekly' collection from each database and stores it in a list if data exists for that date.

Backtest Execution (`future_backtest_with_100_sl` function)
- Purpose: Perform a backtest on historical future data, applying a strategy involving stop-loss (SL) and profit-taking targets, and save the results to a CSV file.
- Inputs:
  - `collection_data`: List of MongoDB collections containing the historical data.
  - `index_name`: Name of the index ('banknifty' or 'nifty').
- Outputs: CSV file with backtest results.

Process:
1. Determines the file path and quantity (`qty`) based on the index name.
2. Reads historical data from a predefined CSV file.
3. Iterates over each collection in `collection_data`.
4. For each collection:
   - Fetches the entry price at 9:20 AM and sets the exit time to 3:00 PM.
   - Calculates stop-loss and target prices for both buy and sell trades.
   - Queries the collection to find the first occurrence of prices hitting the stop-loss or target, or reaching the exit time.
   - Records the entry and exit times and prices for both buy and sell trades.
5. Creates a DataFrame from the recorded data and calculates PnL (Profit and Loss) for both buy and sell trades.
6. Combines the new backtest data with historical data and saves it to a CSV file.


Output Details:
- CSV Report File: Contains the following columns:
  - `Entry_time`: The time when the trade was entered.
  - `Entry_price`: The price at the time of trade entry.
  - `buy_exit_time`: The time when the buy trade was exited.
  - `buy_exit_price`: The price at the time of buy trade exit.
  - `sell_exit_time`: The time when the sell trade was exited.
  - `sell_exit_price`: The price at the time of sell trade exit.
  - `buy_pnl`: Profit and Loss for the buy trade.
  - `sell_pnl`: Profit and Loss for the sell trade.
  - `buy_net_pnl`: Net Profit and Loss for the buy trade (considering quantity).
  - `sell_net_pnl`: Net Profit and Loss for the sell trade (considering quantity).

Example Output:
The results are saved to:
- `Y:\Future_backtest\Bank_nifty_100_sl_future_report.csv`
- `Y:\Future_backtest\nifty_100_sl_future_report.csv`

Each report file contains detailed trade information and PnL calculations based on the backtest strategy applied to the historical data.


