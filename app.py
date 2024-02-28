# 플라스크 서버 *채팅 값*

import pymysql
from flask import Flask
import datetime, json
import setting

conn = pymysql.connect(host='localhost', user=setting.userName, password=setting.password, db=setting.database, charset='utf8') # mysql 연결
curs = conn.cursor() # sql문을 입력할 cursor 생성

if conn.open: # DB 연결 여부 확인
    print('connected')
try:
    app = Flask(__name__) 
    # flask 메인 
    # __name__: 현재 이 파일을 실행하고 있는 파일의 이름이 들어감(원본과 같은 파일 일 경우 '__main__')

    # route() : 외부 웹브라우져에서 웹서버로 접근 시 해당 주소로 입력을 하게 되면 특정 함수가 실행되게 도와줌('/test': /test 주소에 접근하면 아래 함수 실행)
    @app.route('/test',methods=['POST','GET']) 
    def dbToWeb(): # db -> web (python)
            sql = "select * from chat"
            curs.execute(sql)
            rows = curs.fetchall()
            return json.dumps(rows) 
            # fetch한 데이터 json형식으로 변환 후 string으로 바꿔서 return

finally:
    app.run(host='0.0.0.0', port= 5000) # 웹서버 호스트, 포트 지정
    conn.close() # DB 연결 해제
