import pymysql as my
from DBUtils.PooledDB import PooledDB


class PostModel:
    mem_id          = None
    mem_nickname    = None
    mem_password    = None
    mem_gender      = None
    mem_age         = None
    hb_id           = None
    sido_no         = None
    sgg_no          = None
    def __init__(self, mem_id, mem_nickname, mem_password, mem_gender, mem_age, hb_id, sido_no, sgg_no ):
        self.mem_id         = mem_id
        self.mem_nickname   = mem_nickname
        self.mem_password   = mem_password
        self.mem_gender     = mem_gender
        self.mem_age        = mem_age
        self.hb_id          = hb_id
        self.sido_no        = sido_no
        self.sgg_no         = sgg_no

class RestaurantModel:
    rest_id             = None
    restName            = None
    menu                = None
    score               = None
    imgLink             = None
    link                = None
    sgg_no              = None
    sido_no             = None
    content             = None
    arr                 = None
    num                 = None
    restTime            = None
    rest_normal_score   = None
    rest_taste_score    = None
    rest_mood_score     = None
    def __init__(self, rest_id, restName, menu, score, imgLink, link, sido_no, sgg_no, content, arr, num, restTime, rest_normal_score, rest_taste_score , rest_mood_score):
        self.rest_id            = rest_id
        self.restName           = restName
        self.menu               = menu
        self.score              = score
        self.imgLink            = imgLink
        self.link               = link
        self.sido_no            = sido_no
        self.sgg_no             = sgg_no
        self.content            = content
        self.arr                = arr
        self.num                = num
        self.restTime           = restTime
        self.rest_normal_score  = rest_normal_score
        self.rest_taste_score   = rest_taste_score
        self.rest_mood_score    = rest_mood_score


DB_URL          = 'pythondb.clfc3vrmyheu.ap-northeast-2.rds.amazonaws.com'
DB_PORT         =  3306 
DB_USER         = 'root'
DB_PASSWORD     = 'yu989898'
DB_DATABASE     = 'pythondb'
DB_CHARSET      = 'utf8'
MAX_POOL        = 100

class DBHelper:
    # 맴버 변수
    app = None
    # 풀링객체(디비와 연결된 커넥션을 가지고 있는 객체)
    connectionPool = None    
    # 생성자
    def __init__(self, application=None):
        self.app = application
        if self.app:# Flask 객체가 존재하면 -> 환경변수에서 뽑아서 세팅
            DB_URL          = self.app.config['DB_URL']
            #DB_PORT         = 3306#, 포트가 다른 사람을 변경
            DB_USER         = self.app.config['DB_USER']
            DB_PASSWORD     = self.app.config['DB_PASSWORD']
            DB_DATABASE     = self.app.config['DB_DATABASE']
            DB_CHARSET      = self.app.config['DB_CHARSET']
            MAX_POOL        = self.app.config['MAX_POOL']

        self.initPool()
    # 소멸자
    # del 객체명
    def __del__(self):
        self.freePool()
    # 맴버 함수
    # 커넥션 풀생성
    def initPool(self):
        self.connectionPool = PooledDB( creator=my,
                                        host=DB_URL,
                                        user=DB_USER,
                                        password=DB_PASSWORD,
                                        database=DB_DATABASE,
                                        autocommit=False,
                                        charset=DB_CHARSET,
                                        cursorclass=my.cursors.DictCursor,
                                        blocking=False,
                                        maxconnections=MAX_POOL )
    # 커넥션 풀해제
    def freePool(self):
        # 디비와 연결된 모든 커넥션을 닫는다
        self.connectionPool.close()
    # 개별쿼리

    # 회원가입할 때 입력한 정보 디비에 넣기
    def join( self, pm ):
        result = None
        try:
            # 디비 오픈
            conn = self.connectionPool.connection()
            # 쿼리
            cursor = conn.cursor()
            sql = '''
            insert into tbl_mem
            ( mem_id, mem_nickname, mem_password, mem_gender, mem_age, hb_id, sido_no, sgg_no ) 
            values 
            ( %s, %s, %s, %s, %s, %s, %s, %s );
            '''
            cursor.execute( sql, ( pm.mem_id, pm.mem_nickname, pm.mem_password, pm.mem_gender, pm.mem_age, pm.hb_id, pm.sido_no, pm.sgg_no ) )                
            cursor.close()
            conn.commit()
            result = conn.affected_rows()
            conn.close()
        except Exception as e:
            print( e )
            result = None
        return result


    # 로그인 처리
    def loginSql( self, mem_id, mem_password ):
        rows = None
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            sql = '''
                select
                    mem_id, mem_password
                from
                    tbl_mem
                where
                    mem_id=%s and mem_password=%s;
            '''
            cursor.execute( sql, (mem_id, mem_password) )
            rows = cursor.fetchone()
            cursor.close()     
            conn.close()
        except Exception as e:
            print(e)
            rows = None
        return rows

    # 멤버의 아이디 정보 뽑아와서 아이디 중복 체크
    def idCheck(self, mem_id):
        try:
            # 커넥션을 풀링에서 빌려온다
            conn = self.connectionPool.connection()
            # 쿼리 수행 ========================
            cursor = conn.cursor()
            sql = '''
                select
                    count(*) cnt 
                from
                    tbl_mem
                where
                    mem_id=%s
            '''
            cursor.execute( sql, (mem_id,) )
            cnt = cursor.fetchone()
            cursor.close()
            # =================================        
            # 풀링에 반납한다
            conn.close()
        except Exception as e:
            cnt = None
        return cnt
    # 멤버의 닉네임 정보 뽑아와서 닉네임 중복 체크
    def nicknameCheck(self, mem_nickname):
        try:
            # 커넥션을 풀링에서 빌려온다
            conn = self.connectionPool.connection()
            # 쿼리 수행 
            cursor = conn.cursor()
            sql = '''
                select
                    count(*) cnt 
                from
                    tbl_mem
                where
                    mem_nickname=%s
            '''
            cursor.execute( sql, (mem_nickname,) )
            cnt = cursor.fetchone()
            cursor.close()  
            # 풀링에 반납한다
            conn.close()
        except Exception as e:
            cnt = None
        return cnt
    
    #회원정보 수정된 것 데이터베이스에 업데이트
    def updateMyInfo(self, mem_id, mem_password, mem_age, hb_id, sgg_no, sido_no):
        updateInfo = None    #수정결과
        # 디비 오픈
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            #2. sql준비
            sql = '''
            update 
                tbl_mem 
            set 
                mem_password=%s, mem_age=%s, hb_id=%s, sgg_no=%s, sido_no=%s 
            where 
                mem_id=%s;'''
            print( mem_password, mem_age, hb_id, sgg_no, sido_no )
            #3. 쿼리수행
            updateInfo = cursor.execute( sql, (mem_password, mem_age, hb_id, sgg_no, sido_no, mem_id) ) 
            print('updateInfo=', updateInfo)
            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            updateInfo = None
        return updateInfo
        
    #회원정보 데이터베이스에서 가져오기 (->마이페이지와 마이페이지 수정첫페이지에 쓸 것)     
    def getInfo(self, mem_id):
        rows = None
        try:
            # 디비 오픈
            conn = self.connectionPool.connection()
            # 쿼리
            cursor = conn.cursor()
            sql = "select * from tbl_mem where mem_id=%s;"
            cursor.execute( sql, (mem_id,) )
            # fetchone() 1개만 가져온다 -> 리스트 형태 제외됨
            gettinginfo = cursor.fetchone()
            cursor.close()
            # 디비 닫기
            conn.close()
        except Exception as e:
            gettinginfo = None
        return gettinginfo

    # 회원 평점을 데이터베이스에서 가져와서 마이페이지에 데이터뿌리기
    # 회원 평점을 데이터베이스에서 가져와서 마이페이지에 데이터뿌리기
    def getVisit(self, mem_id):
        rows = None
        try:
            # 디비 오픈
            conn = self.connectionPool.connection()
            # 쿼리
            cursor = conn.cursor()
            sql = "select visit_regdate, mem_id, tv.visit_taste_score, tv.visit_mood_score, tv.visit_size, tv.visit_sound,tr.restName from tbl_visit tv left join tbl_rest tr on tv.rest_id = tr.rest_id where mem_id=%s;"
            cursor.execute( sql, (mem_id,) )
            # fetchone() 1개만 가져온다 -> 리스트 형태 제외됨
            gettingvisit = cursor.fetchall()
            cursor.close()
            # 디비 닫기
            conn.close()
        except Exception as e:
            gettingvisit = None
        return gettingvisit

    # 시도 획득
    def get_sido(self):
        sidos = None
        try:
            conn =self.connectionPool.connection()
            cursor = conn.cursor()
            sql = '''
            select *
            from sido; 
            '''
            cursor.execute( sql )
            sidos = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print('오류발생')
            print(e)
            # sidos = None
        finally :
            return sidos
    # sido의 이름 가져오기
    
    def get_sigungu(self, sido_number):
        sigungus = None
        try:
            conn =self.connectionPool.connection()
            cursor = conn.cursor()
            sql = '''
            select * 
            from sigungu 
            where sido_no=%s;
            '''
            cursor.execute( sql , sido_number)
            sigungus = cursor.fetchall()
            print(sigungus)
            cursor.close()
            conn.close()
        except Exception as e:
            print('오류발생')
            print(e)
            sigungus = None
        finally :
            return sigungus 



    def getRestInfo3(self, rest_id):
        restInfo = None    #수정결과
        # 디비 오픈
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            #2. sql준비
            sql = '''
                    select rest_id,restName, score, imgLink, rest_normal_score, rest_taste_score, rest_mood_score, sd.sido_name, sg.sgg_name,umdong_no,restTime,menu,num 
                    from tbl_rest tr 
                    left join sigungu sg on tr.sgg_no = sg.sgg_no
                    left join sido sd on tr.sido_no = sd.sido_no
                    where  rest_id=%s;
                '''
            #3. 쿼리수행
            cursor.execute( sql, rest_id) 
            restInfo = cursor.fetchone()
            # print(restInfo) #영향 받은 row의 개수가 1개
            cursor.close()
            conn.close()
        except Exception as e:
            restInfo = None
        return restInfo     

    def getRestInfo(self, sido_no, sgg_no):
        
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            #2. sql준비
            sql = '''
            select 
                rest_id, restName, score, imgLink, sido_no, sgg_no, rest_normal_score, rest_taste_score, rest_mood_score
            from
                tbl_rest 
            where
                sido_no=%s and sgg_no=%s
                '''
            #3. 쿼리수행
            cursor.execute( sql, ( sido_no, sgg_no) )
            restInfo = cursor.fetchall()
            # print(restInfo)
            # print(restInfo) #영향 받은 row의 개수가 1개
            cursor.close()
            conn.close()
        except Exception as e:
            restInfo = None
        return restInfo  
    def getRestInfo2(self, sido_no):
        
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            #2. sql준비
            sql = '''
            select 
                rest_id, restName, score, imgLink, sido_no, sgg_no, rest_normal_score, rest_taste_score, rest_mood_score
            from
                tbl_rest 
            where
                sido_no=%s
                '''
            #3. 쿼리수행
            cursor.execute( sql, ( sido_no, ) )
            restInfo = cursor.fetchall()
            # print(restInfo)
            # print(restInfo) #영향 받은 row의 개수가 1개
            cursor.close()
            conn.close()
        except Exception as e:
            restInfo = None
        return restInfo  

    # 일반인파 기준으로 정렬한 식당 랭킹
    def getRestInfo_normal(self, sido_no, sgg_no):
        
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            #2. sql준비
            sql = '''
            select 
                rest_id, restName, score, imgLink, sido_no, sgg_no, rest_normal_score, rest_taste_score, rest_mood_score, sido_no, sgg_no
            from
                tbl_rest 
            where
                sido_no=%s and sgg_no=%s
            order by
                rest_normal_score desc
                '''
            #3. 쿼리수행
            cursor.execute( sql, ( sido_no, sgg_no) )
            restInfo = cursor.fetchall()
            # print(restInfo)
            # print(restInfo) #영향 받은 row의 개수가 1개
            cursor.close()
            conn.close()
        except Exception as e:
            restInfo = None
        return restInfo  

    # 미식가파 기준으로 정렬한 식당 랭킹
    def getRestInfo_taste(self, sido_no, sgg_no):
        
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            #2. sql준비
            sql = '''
            select 
                rest_id, restName, score, imgLink, sido_no, sgg_no, rest_normal_score, rest_taste_score, rest_mood_score
            from
                tbl_rest 
            where
                sido_no=%s and sgg_no=%s
            order by
                rest_taste_score desc
                '''
            #3. 쿼리수행
            cursor.execute( sql, ( sido_no, sgg_no) )
            restInfo = cursor.fetchall()
            # print(restInfo)
            # print(restInfo) #영향 받은 row의 개수가 1개
            cursor.close()
            conn.close()
        except Exception as e:
            restInfo = None
        return restInfo      

    # 분위기파 기준으로 정렬한 식당 랭킹
    def getRestInfo_mood(self, sido_no, sgg_no):
        
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            #2. sql준비
            sql = '''
            select 
                rest_id, restName, score, imgLink, sido_no, sgg_no, rest_normal_score, rest_taste_score, rest_mood_score
            from
                tbl_rest 
            where
                sido_no=%s and sgg_no=%s
            order by
                rest_mood_score desc
                '''
            #3. 쿼리수행
            cursor.execute( sql, ( sido_no, sgg_no) )
            restInfo = cursor.fetchall()
            # print(restInfo)
            # print(restInfo) #영향 받은 row의 개수가 1개
            cursor.close()
            conn.close()
        except Exception as e:
            restInfo = None
        return restInfo    

        # 식당정보 획득
    
    def getHbtype(self, mem_id):
        # 디비 오픈
        try:
            conn = self.connectionPool.connection()
            cursor = conn.cursor()
            #2. sql준비
            sql = '''
            select 
                mem_id, hb_id
            from
                tbl_mem
            where
                mem_id=%s
                '''
            #3. 쿼리수행
            cursor.execute( sql, (mem_id,) )
            hb_type = cursor.fetchone()

            # print(restInfo) #영향 받은 row의 개수가 1개
            cursor.close()
            conn.close()
        except Exception as e:
            hb_type = None
        return hb_type   


        #식당 소리, 크기 정보 가져오기    
    def getSize(self, rest_id, word):
        rows = None
        try:
            # 디비 오픈
            conn = self.connectionPool.connection()
            # 쿼리
            cursor = conn.cursor()
            sql = "select count(visit_size) as %s from tbl_visit where rest_id=%s and visit_size=%s;"
            print(sql)
            cursor.execute( sql, (word,rest_id,word))
            # fetchone() 1개만 가져온다 -> 리스트 형태 제외됨
            rows = cursor.fetchone()
            cursor.close()
            # 디비 닫기
            conn.close()
        except Exception as e:
            rows = None
        print(rows)
        return rows


            #식당 소리, 크기 정보 가져오기    
    def getSound(self, rest_id, word):
        rows = None
        try:
            # 디비 오픈
            conn = self.connectionPool.connection()
            # 쿼리
            cursor = conn.cursor()
            sql = "select count(visit_sound) as %s from tbl_visit where rest_id=%s and visit_sound=%s;"
            print(sql)
            cursor.execute( sql, (word,rest_id,word))
            # fetchone() 1개만 가져온다 -> 리스트 형태 제외됨
            rows = cursor.fetchone()
            cursor.close()
            # 디비 닫기
            conn.close()
        except Exception as e:
            rows = None
        print(rows)
        return rows





    # 회원 혼밥유형 가져오기
    def get_hbType(self, mem_id):
        hbType = None
        try:
            conn =self.connectionPool.connection()
            cursor = conn.cursor()
            sql = '''
            select m.mem_id, m.mem_nickname, hb.hb_name from tbl_mem m left join tbl_HBtype hb on m.hb_id  = hb.hb_id  where m.mem_id = %s;
            '''
            cursor.execute( sql , mem_id)
            hbType = cursor.fetchone()
            print(hbType)
            cursor.close()
            conn.close()
        except Exception as e:
            print('오류발생')
            print(e)
            hbType = None
        finally :
            return hbType   

        # 리뷰 등록
    def insertReview( self, rest_id,user_id,tasteScore,moodScore,restSize,restSound ):
        result = '평점을 남겨주셔서 감사합니다!'
        try:
            # 디비 오픈
            conn = self.connectionPool.connection()
            # 쿼리
            cursor = conn.cursor()
            sql = '''
            insert into tbl_visit 
            (rest_id, mem_id, visit_taste_score, visit_mood_score, visit_size, visit_sound) 
            values 
            (%s, %s, %s, %s, %s, %s);
            '''
            cursor.execute( sql, (rest_id,user_id,tasteScore,moodScore,restSize,restSound) )            
            cursor.close()
            # 커밋(디비에 실제 반영)
            conn.commit()
            # 영향받은 로의수로 설정 = 수정된 row의 수
            #result = conn.affected_rows()
            # 디비 닫기
            conn.close()
        except Exception as e:
            print( e )
            result = "이미 리뷰를 작성한 식당입니다."
        return result

    # sido의 이름 가져오기
    def get_sido_name(self, sido_number):
        try:
            conn =self.connectionPool.connection()
            cursor = conn.cursor()
            sql = '''
            select *
            from sido
            where sido_no=%s; 
            '''
            cursor.execute( sql, sido_number )
            sidoName = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            print('오류발생')
            print(e)
            # sidos = None
        finally :
            return sidoName

    def get_sigungu_name(self, sigungu_number):
        sigungus = None
        try:
            conn =self.connectionPool.connection()
            cursor = conn.cursor()
            sql = '''
            select sgg_name 
            from sigungu 
            where sgg_no=%s;
            '''
            cursor.execute( sql , sigungu_number)
            sigungName = cursor.fetchone()
            # print(sigungus)
            cursor.close()
            conn.close()
        except Exception as e:
            print('오류발생')
            print(e)
            sigungName = None
        finally :
            return sigungName 


# 테스트 코드는 if문 이하로 이동:모듈화 처리중 불필요한 코드이동
if __name__ == '__main__':

    obj = DBHelper()
    result = obj.get_sigungu(11)
    print('--------------------------------------------------')
    # print( '결과출력', result )
    print(obj.getRestInfo_normal(11, 11090))
    # print(obj.getRestInfo(2))
    # print(type(obj.getRestInfo(2)))
    print(obj.getHbtype(1))
    print(obj.get_sigungu(11))
    tmp = []
    for i in obj.get_sido():
        tmp.append(i['sido_no'])
    print(tmp)
    print(obj.getRestInfo_normal(11, 11090))
    print(obj.getHbtype(1))
    print(obj.getInfo())
