# importing necessary libraries
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math


# function to load data
def load_data():
    tcs_data = pd.read_csv('data/TCS.csv')
    tcs_data['Date'] = pd.to_datetime(tcs_data['Date'], dayfirst=True)
    tcs_data['Price'] = tcs_data['Price'].replace(',', '', regex=True).astype(float)

    holidays = pd.read_excel('data/holidays_list.xlsx')
    holidays['Date'] = pd.to_datetime(holidays['Date'], dayfirst=True)

    return tcs_data, holidays


# function to get planned date
def get_planned_date(current_date):
    return current_date.replace(day=1)


# function to get actual investment date
def get_actual_date(planned_date, holidays):
    actual_date = planned_date

    while (
        actual_date.weekday() >= 5 or
        actual_date in holidays['Date'].values
    ):
        actual_date = actual_date + timedelta(days=1)

    return actual_date

# function to get price on actual investment date
def get_price(actual_date, tcs_data):
    row = tcs_data[tcs_data['Date'] == actual_date]
    
    price = row['Price'].values[0]
    
    return price

# function to simulate the investment
def simulate_investment(tcs_data, holidays):
    
    # starting with an initial investment of 1000 and incrementing it by 1000 every April (after the first year)
    start_date = pd.to_datetime('2005-04-01')
    end_date = tcs_data['Date'].max()

    investment_amount = 1000
    leftover_amount = 0
    total_shares = 0

    current_date = start_date
    start_year = start_date.year

    results = []

    while current_date <= end_date:
        
        # increment every April (after first year)
        if current_date.month == 4 and current_date.year > start_year:
            investment_amount += 1000

        planned_date = get_planned_date(current_date)

        current_date = current_date + relativedelta(months=1)

        actual_date = get_actual_date(planned_date, holidays)

        price = get_price(actual_date, tcs_data)

        total_money = investment_amount + leftover_amount

        shares = math.floor(total_money / price)

        leftover_amount = round(total_money - (shares * price), 2)
        total_shares += shares

    

        results.append({
            "Date": actual_date,
            "Investment": investment_amount,
            "total money": total_money,
            "Price": price,
            "Shares": shares,
            "Leftover": leftover_amount,
            "Total Shares": total_shares
        })
        
    df = pd.DataFrame(results)
    df.to_csv("output.csv", index=False)

    latest_date = tcs_data['Date'].max()
    latest_price = tcs_data[tcs_data['Date'] == latest_date]['Price'].values[0]
    portfolio_value = total_shares * latest_price
    print("\nFINAL OUTPUT")
    print("Total Shares:", total_shares)
    print("Portfolio Value:", round(portfolio_value, 2))

if __name__ == "__main__":
    tcs_data, holidays = load_data()
    simulate_investment(tcs_data, holidays)