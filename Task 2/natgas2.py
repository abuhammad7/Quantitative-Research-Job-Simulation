import pandas as pd
from scipy.interpolate import interp1d

#Load the CSV File
gas_data = pd.read_csv("Nat_Gas (1).csv")

#Convert dates column to datetime
gas_data["Dates"] = pd.to_datetime(
    gas_data["Dates"],
    format="%m/%d/%y"
)

# Create interpolation function
price_function = interp1d(
    gas_data["Dates"].astype("int64"),
    gas_data["Prices"],
    kind="linear",
    fill_value="extrapolate"                       
)

#Pricing Function

def price_storage_contract(
    injection_dates,
    withdrawal_dates,
    volumes,
    max_storage,
    injection_rate,
    withdrawal_rate,
    storage_cost_per_day
): 
    total_profit = 0 
    current_storage = 0
    
    for inj_date, wd_date, volume in zip(
        injection_dates,
        withdrawal_dates,
        volumes
    ): 
        
        inj_date = pd.to_datetime(inj_date)
        wd_date = pd.to_datetime(wd_date)
        
        if volume > injection_rate:
            raise ValueError("Injection rate exceeded")
        
        if volume > withdrawal_rate:
            raise ValueError("Withdrawal rate exceeded")
        
        if current_storage + volume > max_storage:
            raise ValueError("Storage capacity exceeded")
        
        buy_price = float(price_function(inj_date.value))
        sell_price = float(price_function(wd_date.value))
        
        days = (wd_date - inj_date).days
        
        purchase_cost = buy_price * volume
        sale_revenue = sell_price * volume
        storage_cost = storage_cost_per_day * volume * days
        
        profit = sale_revenue - purchase_cost - storage_cost
        
        total_profit += profit
        current_storage += volume
        
    return total_profit    

#Test Example

injection_dates = [
    "2021-06-30",
    "2021-08-31"
]

withdrawal_dates = [
    "2021-12-31",
    "2022-02-28"
]

volumes = [
    500000,
    300000
]

contract_value = price_storage_contract(
     injection_dates=injection_dates,
     withdrawal_dates=withdrawal_dates,
     volumes=volumes,
     max_storage=1000000,
     injection_rate=600000,
     withdrawal_rate=600000,
     storage_cost_per_day=0.0005
     
)

print("Estimated Contract Value: ${:.2f}".format(contract_value))
 

input()