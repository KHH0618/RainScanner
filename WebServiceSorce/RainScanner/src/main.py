from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from data_processed import WeatherPrediction
from weather_crawler_kma import weather_crawler
import os

api_key = '1tZQKilfR2iWUCopX3do8g'
predictor = WeatherPrediction(api_key)
dnn_predict_list, lstm_predict_list = predictor.get_predictions()
weather_list, kma_rain_prob = weather_crawler()
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 현 폴더의 절대경로
app.mount('/static',
          StaticFiles(directory=os.path.join(BASE_DIR, '../static')),
          name='static')
templates = Jinja2Templates(directory=os.path.join(BASE_DIR,
                                                   '../templates'))

@app.get("/")
def read_root(request: Request):
    dnn_data = [
        {"time": "3시간 뒤", "precipitation": ('맑음' if dnn_predict_list[0] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(dnn_predict_list[0]*100))},
        {"time": "6시간 뒤", "precipitation": ('맑음' if dnn_predict_list[1] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(dnn_predict_list[1]*100))},
        {"time": "12시간 뒤", "precipitation": ('맑음' if dnn_predict_list[2] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(dnn_predict_list[2]*100))},
        {"time": "24시간 뒤", "precipitation": ('맑음' if dnn_predict_list[3] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(dnn_predict_list[3]*100))},
    ]
    lstm_data = [
        {"time": "3시간 뒤", "precipitation": ('맑음' if lstm_predict_list[0] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(lstm_predict_list[0] * 100))},
        {"time": "6시간 뒤", "precipitation": ('맑음' if lstm_predict_list[1] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(lstm_predict_list[1] * 100))},
        {"time": "12시간 뒤", "precipitation": ('맑음' if lstm_predict_list[2] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(lstm_predict_list[2] * 100))},
        {"time": "24시간 뒤", "precipitation": ('맑음' if lstm_predict_list[3] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(lstm_predict_list[3] * 100))},
    ]
    kma_data = [{"time": "3시간 뒤", "precipitation": weather_list[0], "rain_prob":kma_rain_prob[0]},
        {"time": "6시간 뒤", "precipitation": weather_list[1], "rain_prob":kma_rain_prob[1]},
        {"time": "12시간 뒤", "precipitation": weather_list[2], "rain_prob":kma_rain_prob[2]},
        {"time": "24시간 뒤", "precipitation": weather_list[3], "rain_prob":kma_rain_prob[3]},]
    return templates.TemplateResponse("home.html", {"request": request, "dnn_data": dnn_data, 'lstm_data':lstm_data, 'kma_data':kma_data})


@app.get("/dnn")
def read_root(request: Request):
    dnn_data = [
        {"time": "3시간 뒤", "precipitation": ('맑음' if dnn_predict_list[0] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(dnn_predict_list[0]*100))},
        {"time": "6시간 뒤", "precipitation": ('맑음' if dnn_predict_list[1] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(dnn_predict_list[1]*100))},
        {"time": "12시간 뒤", "precipitation": ('맑음' if dnn_predict_list[2] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(dnn_predict_list[2]*100))},
        {"time": "24시간 뒤", "precipitation": ('맑음' if dnn_predict_list[3] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(dnn_predict_list[3]*100))},
    ]
    kma_data = [{"time": "3시간 뒤", "precipitation": weather_list[0], "rain_prob":kma_rain_prob[0]},
        {"time": "6시간 뒤", "precipitation": weather_list[1], "rain_prob":kma_rain_prob[1]},
        {"time": "12시간 뒤", "precipitation": weather_list[2], "rain_prob":kma_rain_prob[2]},
        {"time": "24시간 뒤", "precipitation": weather_list[3], "rain_prob":kma_rain_prob[3]},]
    return templates.TemplateResponse("dnn.html", {"request": request, "dnn_data": dnn_data, 'kma_data':kma_data})

@app.get("/lstm")
def read_root(request: Request):
    lstm_data = [
        {"time": "3시간 뒤", "precipitation": ('맑음' if lstm_predict_list[0] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(lstm_predict_list[0] * 100))},
        {"time": "6시간 뒤", "precipitation": ('맑음' if lstm_predict_list[1] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(lstm_predict_list[1] * 100))},
        {"time": "12시간 뒤", "precipitation": ('맑음' if lstm_predict_list[2] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(lstm_predict_list[2] * 100))},
        {"time": "24시간 뒤", "precipitation": ('맑음' if lstm_predict_list[3] < 0.5 else '비'),
         "rain_prob": "{:.2f}%".format(round(lstm_predict_list[3] * 100))},
    ]
    kma_data = [{"time": "3시간 뒤", "precipitation": weather_list[0], "rain_prob":kma_rain_prob[0]},
        {"time": "6시간 뒤", "precipitation": weather_list[1], "rain_prob":kma_rain_prob[1]},
        {"time": "12시간 뒤", "precipitation": weather_list[2], "rain_prob":kma_rain_prob[2]},
        {"time": "24시간 뒤", "precipitation": weather_list[3], "rain_prob":kma_rain_prob[3]},]
    return templates.TemplateResponse("lstm.html", {"request": request, 'lstm_data':lstm_data, 'kma_data':kma_data})

