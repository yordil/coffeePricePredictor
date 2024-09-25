from flask import Flask, jsonify, request
import pandas as pd
from prophet import Prophet
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load and fix column names for the datasets
coffee_data1 = pd.read_excel("./extracted_files/Coffee-2019.xlsx", header=[1, 2])
coffee_data1.columns = [
    " ".join([str(i) for i in col if pd.notna(i)]) for col in coffee_data1.columns
]

coffee_data2 = pd.read_excel("./extracted_files/Coffee-2019.xlsx", header=[1, 2])
coffee_data2.columns = [
    " ".join([str(i) for i in col if pd.notna(i)]) for col in coffee_data2.columns
]

# Rename columns to clean up and match expected names
rename_columns = {
    "Unnamed: 0_level_0 Trade Date": "Trade Date",
    "Unnamed: 1_level_0 Symbol": "Symbol",
    "Unnamed: 2_level_0 Warehouse": "Warehouse",
    "Unnamed: 3_level_0 Production Year": "Production Year",
    "Unnamed: 4_level_0 Opening Price": "Opening Price",
    "Unnamed: 5_level_0 Closing Price": "Closing Price",
    "Unnamed: 6_level_0 High": "High",
    "Unnamed: 7_level_0 Low": "Low",
    "Unnamed: 8_level_0 Change": "Change",
    "Unnamed: 9_level_0 Persetntage Change": "Percentage Change",
    "Unnamed: 10_level_0 Volume (Ton)": "Volume (Ton)",
}

coffee_data1.rename(columns=rename_columns, inplace=True)
coffee_data2.rename(columns=rename_columns, inplace=True)

# Merge on 'Trade Date'
merged_data = pd.merge(coffee_data1, coffee_data2, on="Trade Date", how="inner")

# Remove commas and convert to numeric values
merged_data["Closing Price_x"] = pd.to_numeric(
    merged_data["Closing Price_x"].str.replace(",", ""), errors="coerce"
)
merged_data["Opening Price_x"] = pd.to_numeric(
    merged_data["Opening Price_x"].str.replace(",", ""), errors="coerce"
)

# Prepare data for Prophet model
merged_data["ds"] = pd.to_datetime(merged_data["Trade Date"])
merged_data["y"] = merged_data[
    "Closing Price_x"
]  # Assuming you want to use 'Closing Price_x'

# Drop any rows with missing values after conversion
merged_data = merged_data.dropna(subset=["y"])

# Train the Prophet model
model = Prophet()
model.fit(merged_data[["ds", "y"]])




@app.route("/predict", methods=["POST"])
def predict():
    # Get the number of days to predict from the request
    days = request.json.get("days", 15)

    # Create future dataframe and predict
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    # Return predicted values for the requested days
    predictions = forecast[["ds", "yhat"]].tail(days).to_dict(orient="records")
    return jsonify(predictions)


if __name__ == "__main__":
    app.run(debug=True)
