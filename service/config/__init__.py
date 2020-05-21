class FlaskConfig(object):
    DB_URL          = 'localhost'
    DB_PORT         =  3306
    DB_USER         = 'root'
    DB_PASSWORD     = '1234'
    DB_DATABASE     = 'pythondb' 
    DB_CHARSET      = 'utf8'
    MAX_POOL        =  100 

class WebConfig:
    # 이거 수정해야 할 사항
    
    title       = '슬기로운 혼밥생활 : 전국 혼밥 맛집 지도'
    site_name   = '슬기로운 혼밥생활'
    version     = 'v1.0.0'
    debug       = True
    page_title  = { 'HBTYPE_EXPLAIN':'혼밥 유형 설명', 'MAP_1':'전국', 'MAP_2':'서울' }
    cookie_uid  = None
    # 생성자
    def __init__(self):
        print('환경설정 생성자 호출')
    # 맴버 함수

if __name__=='__main__':
    obj = WebConfig()
    print( obj.site_name )