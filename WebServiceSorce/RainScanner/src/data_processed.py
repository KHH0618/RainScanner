import pandas as pd
import numpy as np
import ssl
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

class WeatherPrediction:
    def __init__(self, api_key, stn=108):
        self.api_key = api_key
        self.stn = stn
        self.label_encoding_dict = {"no_clouds": 0,"Sc": 1,"Ci": 2,"ScAs": 3,"StNs": 4,"Ac": 5,"As": 6,"ScAc": 7,
        "ScCi": 8,"CuSc": 9,"AcCi": 10,"StAs": 11,"StSc": 12,"St": 13,"Cu": 14,"Cs": 15,"CuCi": 16,
        "ScNs": 17,"AsCi": 18,"CuAc": 19,"StCi": 20,"AcCs": 21,"ScCs": 22,"Cc": 23,"ScAcCi": 24,
        "CuAs": 25,"CsCi": 26,"AsAc": 27,"CbSt": 28,"CuSt": 29,"CbStNs": 30,"AcCc": 31,"AsCs": 32,
        "CbSc": 33,"CbCu": 34,"CbNs": 35,"Ns": 36,"ScCc": 37,"CuScCi": 38,"StAc": 39,"CcCi": 40,
        "CuScAs": 41,"CbAs": 42,"CuScAc": 43,"ScAcCs": 44,"Cb": 45,"CuScAcCi": 46,"CuScCc": 47,"CuCs": 48,"CbCi": 49,
        "CuAcCi": 50,"CuCc": 51,"ScAcCc": 52,"CuScCs": 53,"AsCc": 54,"ScCcCi": 55,"CbAc": 56,"CbCuNs": 57,
        "CuNs": 58,"CuScAsCi": 59,"ScAsCi": 60,"AcCcCi": 61,"CuScNs": 62,"AsSc": 63,"ScCu": 64,"CuScAcCc": 65,
        "CbScNs": 66,"CuScCcCi": 67,"CbScCs": 68,"CuCcCi": 69,"CuAcCc": 70,"StAsCi": 71,"CbScAs": 72,"ScAsCs": 73
        }
        self.column_names = [
            "TM", "STN", "WD", "WS", "GST_WD", "GST_WS", "GST_TM", "PA", "PS", "PT",
            "PR", "TA", "TD", "HM", "PV", "RN", "RN_DAY", "RN_JUN", "RN_INT",
            "SD_HR3", "SD_DAY", "SD_TOT", "WC", "WP", "WW", "CA_TOT", "CA_MID",
            "CH_MIN", "CT", "CT_TOP", "CT_MID", "CT_LOW", "VS", "SS", "SI", "ST_GD",
            "TS", "TE_005", "TE_01", "TE_02", "TE_03", "ST_SEA", "WH", "BF", "IR", "IX"
        ]
        self.dnn_model_paths = [
            '../static/models/DNN/3h_dnn.h5',
            '../static/models/DNN/6h_dnn.h5',
            '../static/models/DNN/12h_dnn.h5',
            '../static/models/DNN/24h_dnn.h5'
        ]
        self. lstm_model_paths = [
            '../static/models/LSTM/3h_lstm.h5',
            '../static/models/LSTM/6h_lstm.h5',
            '../static/models/LSTM/12h_lstm.h5',
            '../static/models/LSTM/24h_lstm.h5'
        ]
        ssl._create_default_https_context = ssl._create_unverified_context

    def fetch_data(self):
        start_day = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d%H00")
        end_day = datetime.now().strftime("%Y%m%d%H00")
        url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm3.php?tm1={start_day}&tm2={end_day}&stn=108&help=1&authKey=1tZQKilfR2iWUCopX3do8g'
        predict_data = pd.read_csv(url, encoding='cp949', comment='#', sep=r'\s+', header=None, names=self.column_names)[
            ['TM', 'HM', 'PV', 'TD', 'PA', 'TE_005', 'TE_01', 'TE_02', 'TE_03', 'CT', 'CH_MIN']]
        return predict_data

    def no_clouds_chmin(slef, row):
        if row['CT'] == 'no_clouds':
            row['CH_MIN'] = 0.0
        return row

    def data_processe(self, data):
        data.loc[:, 'CT'] = data['CT'].map(lambda x: 'no_clouds' if x.strip() == '-' else x) # 데이터가 없는경우 no_clouds
        data.loc[:, ['CT', 'CH_MIN']] = data[['CT', 'CH_MIN']].apply(lambda x: self.no_clouds_chmin(x),axis=1) # 운형과 최저운고가 없을시 no_clouds
        data['CT'] = data['CT'].map(lambda x: self.label_encoding_dict[x]) # 운형 라벨링
        return data

    def scale_data(self, data):
        scaler = MinMaxScaler()
        lstm_predict_X = scaler.fit_transform(np.array(
            data.loc[1:, ['HM', 'TD', 'PA', 'TE_005', 'TE_01', 'TE_02', 'TE_03', 'CT', 'CH_MIN']]).reshape(-1,9)).reshape(-1, 24, 9)
        dnn_predict_X = scaler.fit_transform(np.array(
            data.loc[:, ['HM', 'PV', 'TD', 'PA', 'TE_005', 'TE_01', 'TE_02', 'TE_03', 'CT', 'CH_MIN']]).reshape(-1, 1)).reshape(-1, 10)
        return lstm_predict_X, dnn_predict_X

    def load_models(self, model_paths):
        """모델 로드"""
        return [load_model(path) for path in model_paths]

    def predict_with_models(self, models, input_data):
        """모델로 예측 수행"""
        return [model.predict(input_data)[0][0] for model in models]

    def get_predictions(self):
        """전체 프로세스를 실행하여 예측 값 반환"""
        raw_data = self.fetch_data()
        processed_data = self.data_processe(raw_data)
        lstm_X, dnn_X = self.scale_data(processed_data)
        dnn_models = self.load_models(self.dnn_model_paths)
        dnn_predictions = self.predict_with_models(dnn_models, dnn_X[-1].reshape(-1, 10))
        lstm_models = self.load_models(self.lstm_model_paths)
        lstm_predictions = self.predict_with_models(lstm_models, lstm_X)

        return dnn_predictions, lstm_predictions

if __name__ == '__main__':
    api_key = '1tZQKilfR2iWUCopX3do8g'
    predictor = WeatherPrediction(api_key)  # 클래스 인스턴스 생성
    print(predictor.get_predictions())  # 인스턴스 메서드 호출