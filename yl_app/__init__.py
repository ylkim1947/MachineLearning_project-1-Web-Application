import flask
from flask import Flask, request, render_template
#from sklearn.externals 
import joblib
import numpy as np
from imageio import imread
from yl_app.ml.model import export_model
from flask_restful import Resource, Api
import pandas as pd
import pickle


# from sklearn.compose import ColumnTransformer
# #from sklearn.ensemble import RandomForestRegressor
# from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier
# from category_encoders import OrdinalEncoder
# from category_encoders import TargetEncoder
# from category_encoders import BinaryEncoder
# from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.metrics import accuracy_score


app = Flask(__name__)
api = Api(app)


# 메인 페이지 라우팅
@app.route("/")
@app.route("/index")
def index():
    # breakpoint()
    return flask.render_template('index4.html')


# 데이터 예측 처리
@app.route('/predict', methods=['POST'])
def make_prediction():

    if request.method == 'POST':
        #breakpoint()
        # 업로드 파일 처리 분기
        #val = request.form['']
        HE_wc=request.form['HE_wc']
        HE_BMI=request.form['HE_BMI']
        HE_wt=request.form['HE_wt']
        HE_ht=request.form['HE_ht']
        BE3_31=request.form['BE3_31']
        BD2=request.form['BD2']
        BO1_1=request.form['BO1_1']
        BP16=request.form['BP16']
        L_OUT_FQ=request.form['L_OUT_FQ']
        BE8_1=request.form['BE8_1']


        #breakpoint()
        #if not val: return render_template('index4.html', ml_result="No results")



        # -- 입력값 예시 --
        HE_DM_HbA1c=1.0
        HE_wc=68.2
        HE_BMI=50
        HE_wt=60
        HE_ht=160.0
        BE3_31=7.0
        BD2=19.0
        BO1_1=1.0
        BP16=8
        L_OUT_FQ=3.0
        BE8_1=5
        # # # 입력 받은 데이터 예측
        inputdata = { 
                      #'HE_DM_HbA1c':HE_DM_HbA1c,
                      'HE_wc':[HE_wc],
                      'HE_BMI':[HE_BMI],
                      'HE_wt':[HE_wt],
                      'HE_ht':[HE_ht],
                      'BE3_31':[BE3_31],
                      'BD2':[BD2],
                      'BO1_1':[BO1_1],
                      'BP16':[BP16],
                      'L_OUT_FQ':[L_OUT_FQ],
                      'BE8_1':[BE8_1] }
        df = pd.DataFrame(inputdata)
        model = joblib.load('yl_app/model/xg_model1.pkl')

        prediction = model.best_estimator_.named_steps['estimator'].predict(df) # array([1. or 2.])
        val =+ int(np.squeeze(prediction))
        
        #prediction = 0 
        # 예측 값을 1차원 배열로부터 확인 가능한 문자열로 변환


        # 숫자가 10일 경우 0으로 처리
        #if label == '10': label = '0'

        # 결과 리턴
        return render_template('index4.html', ml_result=val)


# # 데이터 모델 재학습
# @app.route('/retrain', methods=['POST'])
# def make_model():
#     if request.method == 'POST':
#         # 모델 재 생성
#         export_model('R')
#         return render_template('index3.html', md_label='모델 재생성 완료')


# # 데이터 모델 재학습(RestApi)
# class RestMl(Resource):
#     def get(self):
#         export_model('R')
#         return {'result': True, 'modelName': 'model.pkl'}

#prc_column= ['HE_DM_HbA1c','HE_wc','HE_BMI','HE_wt','HE_ht','BE3_31','BD2','BO1_1','BP16','L_OUT_FQ','BE8_1']
#data =[1.0,68.2,19.722233,52.4,163.0,5.0,19.0,1.0,8,3.0,5]

    # Rest 등록
#api.add_resource(RestMl, '/retrainModel')

if __name__ == '__main__':
    # 모델 로드
    # ml/model.py 선 실행 후 생성
    model = joblib.load('yl_app/model/rf_model1.pkl')
    # Flask 서비스 스타트
#    app.run(host='0.0.0.0', port=8000, debug=True)
    app.run()