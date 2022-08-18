import pandas as pd
from validator import schema
import joblib
import schedule

def load_data(yesterday, today):
    data = pd.read_sql(f'SELECT * FROM yellow_tripdata WHERE tpep_pickup_datetime >= "{yesterday}" AND tpep_pickup_datetime < "{today}"', 'sqlite:///data.db')
    return data

def create_features(data):
    data["fare_amount_per_person"] = data["fare_amount"] / (data["passenger_count"] + 1)
    return data

def make_predictions():
    #today = pd.to_datetime("today").strftime("%Y-%m-%d")
    #yesterday = pd.to_datetime("today") - pd.Timedelta(days=1)
    #yesterday = yesterday.strftime("%Y-%m-%d")
    today = "2022-01-05"
    yesterday = "2022-01-04"

    data = load_data(yesterday, today)
    data = create_features(data)

    validated_data = schema.validate(data)

    #print(data.columns)

    #print("validado", validated_data.columns)

    model = joblib.load("model.joblib")
    predictions = model.predict(validated_data)

    predictions_df = pd.DataFrame(predictions, columns=["prediction"], index=data["index"])
    predictions_df.to_sql("predictions", "sqlite:///data.db", if_exists="append")


if __name__ == '__main__':
    schedule.every().day.at("00:00").do(make_predictions)
    print("Rodando")
    while True:
        schedule.run_pending()