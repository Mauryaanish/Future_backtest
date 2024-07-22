import pandas as pd
from datetime import datetime, time, timedelta
import pymongo

def data(index_name, start_date, end_date):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    collection_list = []
    
    try:
        start_date = pd.to_datetime(start_date, format='%d%m%Y')
        end_date = pd.to_datetime(end_date, format='%d%m%Y')
        
        # Fetch data in monthly batches for efficiency
        delta = end_date - start_date
        
        for i in range(delta.days + 1):
            current_date = start_date + timedelta(days=i)
            current_date_str = current_date.strftime("%d%m%Y")
            database_name = f'{index_name}_option_data_{current_date_str}'
            print(f"Processing data for: {database_name}")
            
            db = client[database_name]
            collection = db['weekly']
            
            # Fetch only necessary fields for efficiency
            first_record = collection.find_one()
            if first_record:
                collection_list.append(collection)
            else:
                print(f"No data found for {current_date}")
    
    except Exception as e:
        print(f"Error in data function: {e}")
    
    return collection_list

def future_backtest_with_100_sl(collection_data, index_name):
    try:
        if index_name == 'banknifty':
            file_path = r'Y:\Future_backtest\Bank_nifty_100_sl_future_report.csv'  # Use raw string for Windows paths
            qty = 15
        elif index_name == 'nifty':
            file_path = r'Y:\Future_backtest\nifty_100_sl_future_report.csv'  # Use raw string for Windows paths
            qty = 25
        
        historical_data = pd.read_csv(file_path)
        report_list = []
        
        for collection in collection_data:
            first_data = collection.find_one({})
            current_date = first_data['time_entry'].date()
            entry_time = datetime.combine(current_date, time(9, 20))
            exit_time = datetime.combine(current_date, time(15, 0))

            future_price_entry_price = collection.find_one({'time_entry' : {'$gt' : entry_time}})['future_price']
            future_price_entry_time = collection.find_one({'time_entry' : {'$gt' : entry_time}})['time_entry']

            buy_sl = future_price_entry_price - 100
            sell_sl = future_price_entry_price + 100
            
            # Efficient query to find buy and sell details
            buy_details = collection.find_one({
                '$or': [
                    {'future_price': {'$lt': buy_sl}, 'time_entry': {'$gt': entry_time}},
                    {'time_entry': {'$gt': exit_time}}
                ]
            })
            
            sell_details = collection.find_one({
                '$or': [
                    {'future_price': {'$gt': sell_sl}, 'time_entry': {'$gt': entry_time}},
                    {'time_entry': {'$gt': exit_time}}
                ]
            })
            
            # Extract relevant data for the report
            buy_exit_time = buy_details['time_entry']
            buy_exit_price = buy_details['future_price']
            sell_exit_time = sell_details['time_entry']
            sell_exit_price = sell_details['future_price']
            
            data = {
                'Entry_time': entry_time,
                'Entry_price': future_price_entry_price,
                'buy_exit_time': buy_exit_time,
                'buy_exit_price': buy_exit_price,
                'sell_exit_time': sell_exit_time,
                'sell_exit_price': sell_exit_price
            }
            
            report_list.append(data)
        
        # Create report DataFrame and calculate PnL
        report_df = pd.DataFrame(report_list)
        report_df['buy_pnl'] = report_df['buy_exit_price'] - report_df['Entry_price']
        report_df['sell_pnl'] = report_df['Entry_price'] - report_df['sell_exit_price']
        report_df['buy_net_pnl'] = report_df['buy_pnl'] * qty
        report_df['sell_net_pnl'] = report_df['sell_pnl'] * qty
        
        # Concatenate historical data and current report data
        final_report = pd.concat([historical_data, report_df], ignore_index=True)

        # Save final report to CSV
        final_report.to_csv(file_path, index=False)
        print(f"Backtest Report saved: {file_path}")
    
    except Exception as e:
        print(f"Error in future_backtest_with_100_sl function: {e}")

if __name__ == '__main__':
    index_list = ['banknifty', 'nifty']
    start_date = input('Enter Data Start Date (12052024 format): ')
    end_date = input('Enter Data End Date (12052024 format): ')
    
    for index_name in index_list:
        print(f'{index_name} Backtest start: ')
        collection_data = data(index_name=index_name, start_date=start_date, end_date=end_date)
        future_backtest_with_100_sl(collection_data=collection_data, index_name=index_name)
        print(f'{index_name} Backtest End And Data save: ')
