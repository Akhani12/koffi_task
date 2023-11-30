from datetime import datetime, timedelta
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/profit")
def calculate_profit(scheme_code: str, start_date: str, end_date: str, capital: int = 1000000.0 or None) -> float:
    profit = 0.0
    r_data = requests.get(f"https://api.mfapi.in/mf/{scheme_code}")
    if r_data.status_code == 200:
        mutual_data = r_data.json()
        mf_data = mutual_data["data"]
        while True:
            start_date_nav = [i["nav"] for i in mf_data if i["date"] == start_date]  # Get Starting date value ...
            if not start_date_nav:
                myday = datetime.strptime(start_date, '%d-%m-%Y')
                start_date = myday + timedelta(days=1)
                start_date = start_date.strftime('%d-%m-%Y')
            else:
                start_date_nav = float(start_date_nav[0])
                break

        while True:
            end_date_nav = [i["nav"] for i in mf_data if i["date"] == end_date]  # Get Ending  date value ...
            if not end_date_nav:
                myday = datetime.strptime(end_date, '%d-%m-%Y')
                end_date = myday + timedelta(days=1)
                end_date = end_date.strftime('%d-%m-%Y')
            else:
                end_date_nav = float(end_date_nav[0])
                break
        number_units = capital / start_date_nav # Calculate units we got based on capital with current price
        end_date_value = number_units * end_date_nav  # Calculate last day valuation based on units purchased
        profit = end_date_value - capital  # Calculating the profit we got in end date

    return profit


if __name__ == "__main__":
    uvicorn.run("app:app", port=4500)
