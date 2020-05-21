import json
from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response
# 환경설정 클레스 모듈 가져오기
from service.config import WebConfig
#from service.model.dbMgr import loginSql, searchSql,selectAllEplList
from service.model import createDBHelper
from service.model.dbMgr import DBHelper


config = WebConfig()
obj = DBHelper()
# dbHelper= None

def create_app(config_path='resource/config.cfg'):    
    app = Flask(__name__)
    # 세션생성에 필요한 세션키(중복되지 않는 해쉬값)를 정의
    app.secret_key = 'sdkjfelifnweldqldfkwefdjlsdl'
    #######################################################
    # 환경변수 로드 (파일에서, 클레스에서)
    # 프로그램에 사용되는 고정된 정보(디비접속, 운용수치등)
    # 등은 외부파일에서 관리하는것이 일반적(소스에 고정하지 않음)
    # 통상 상수값임(변수명 대문자)
    app.config.from_pyfile(config_path, silent=True)

    from service.config import FlaskConfig
    app.config.from_object(FlaskConfig)
    print( '환경변수 사용->', app.config['DB_URL'] )
    configCheckTest( app.config.items() )
    ######################################################
    # 디비 로드 -> 웹서비스든 어플리케이션서버든 -> 요청할대마다
    # 디비에 접속->쿼리->닫기 이렇게 작업하지 않는다!!
    # 동접 천단위로 가면 -> 서비스가 셛다운됨. 살아도 응답이 느리다.
    # 풀링을 기술을 이용하여 디비 커넥션, 연결닫음 미리 준비해둔다
    # 요청 -> 커넥션 빌림 -> 쿼리 -> 반납 -> 응답
    # 접속과 닫기 라는 시간이 세이브가된다
    # dbHelper = DBHelper( app )
    createDBHelper( app )
    # Flask 객체가 생성된 이후에 라우트 진행되야 한다
    # 회원쪽 URL : ~/users/login, ~/users/logout, ~/users/join
    # epl URL : ~/epl/allList, ~/epl/search,
    # URL에 prefix를 부여하여 업무를 분할하고 api 분류할수 있는 방식
    # blueprint(블루프린트)
    from service.controller import user, join, review, mypage
    from service.controller import bp_user, bp_join, bp_review, bp_mypage

    app.register_blueprint(bp_user, url_prefix='/user')
    app.register_blueprint(bp_join, url_prefix='/join')
    app.register_blueprint(bp_review, url_prefix='/review')
    app.register_blueprint(bp_mypage, url_prefix='/mypage')
    
    initRoute( app )  
    # 에러핸들러 등록
    return app

def initRoute(app):
    # 요청과 응답 전후로 이런 이벤트를 감지하여 전처리, 후처리
    # 를 수행하는 이미 정해져있는 함수들
    @app.before_first_request
    def before_first_request():
        print('서버가 가동하고 최초 요청시 반응 단한번')
    
    @app.before_request
    def before_request():

        print('요청할때마다 무조건 여기를 거친다:전처리')
    
    @app.after_request
    def after_request( res ):
        print('매 요청 처리되고나서 실행됨, 응답이 지나가는 곳')
        return res
    
    @app.teardown_request
    def teardown_request(exception):
        print('브라우저가 응답하고 나서 실행')
        return '브라우저가 응답하고 나서 실행'
    
    @app.teardown_appcontext
    def teardown_appcontext(exception):
        print('http 요청 어플리케이션 컨텍스트 종료되고 실행')

        # 홈페이지
    @app.route('/')
    def home():
        resp = make_response( render_template('home_page.html', config=config) )
        return resp
    
    @app.route('/hbtype_explain')
    def hbtype_explain():
        return render_template('hbtype_explain.html', config=config)

    @app.route('/sigungu/<sido_no>')
    def sigungu(sido_no):
        print(sido_no)
        sigungus = obj.get_sigungu(sido_no)
        print(jsonify(sigungus))
        return jsonify(sigungus)

# 환경 변수 체크하는 함수
# configCheckTest( app.config.items() )
def configCheckTest(config):
    for key, value in config:
        print( '%s : %s ' % (key, value) )
