from service import create_app, config

# 플라스크 어플리케이션 서버 생성
application = create_app()

# 구동
if __name__=='__main__':
    
    host = None
    port = None
    if application.config['ENV'] == 'production':# 상용
        host = application.config['REAL_URL']
        port = application.config['REAL_PORT']
    else:# 개발, 테스트
        host = application.config['TEST_URL']
        port = application.config['TEST_PORT']
    application.run(
        host=host,
        port=port,
        debug=application.config['SERVER_RUN_MODE_DEBUG'])
    print('호스트는',host)
    print(port)