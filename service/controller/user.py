from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response
from service.controller import bp_user
from service.controller.hbTypeCal import HBFormula
# 디비
from service.model import dbHelper, RestaurantModel
from service.model.dbMgr import DBHelper
from service import config
import datetime


obj = DBHelper()
# 라우팅
# ~/user

@bp_user.route('/')


# /user/login
@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        mem_id          = request.form['mem_id']
        mem_password    = request.form['mem_password']
        row             = dbHelper.loginSql( mem_id, mem_password )
        if row:
            # 세션 처리 (필요한 정보를 세션으로 저장한다)
            # 사용자 아이디를 저장하겠다
            session['user_id'] = mem_id
            return redirect( url_for('home') )
        else:
            return render_template('common/alert2.html', msg='회원이 아닙니다')

# 로그아웃
# # ~/user/logout

@bp_user.route('/logout')
def logout():
    if not 'user_id' in session:# 세션없으면 false ->부정->참
        return redirect( url_for('userbp.login') )

    # 세션 종료
    print( session )
    if 'user_id' in session:
        session.pop('user_id', None)

    print( '세션제거후->', session )
    # 페이지 요청을 리다이렉트-> 홈페이지
    return redirect( url_for('home') )

# 지도 1의 버튼에서 값 받아서 오기
@bp_user.route('/map1')
def map_1():
    if 'user_id' in session:
        sidos = obj.get_sido()
        # 여기서 config는 위에서 config=Webconfig => config폴더의 __init__.py 참고
        return render_template('map_1.html', config=config, sidos=sidos)
    else:
        return redirect(url_for('userbp.login'))

@bp_user.route('/map2/<sido_no>')
def map_2( sido_no ):
    if 'user_id' in session:
        sigungus = obj.get_sigungu( sido_no )
        # sigungus = [11, 21, 22, 23, 24, 25, 26, 29, 31, 32, 33, 34, 35, 36, 37, 38, 39]
        return render_template('map_2.html', config=config, sigungus=sigungus, sido_no=sido_no)
    else:
        return redirect(url_for('userbp.login'))
    

# @bp_user.route('/ranking/<sido_no>/<sgg_no>')
# def ranking_seoul(sido_no, sgg_no):
#     if 'user_id' in session:

#         mem_id = session['user_id']

#         hb_id = obj.getHbtype(mem_id)

#         rest_info = obj.getRestInfo(sido_no, sgg_no)
#         return render_template('ranking_normal.html', restInfo = rest_info)
#     else:
#         return redirect(url_for('userbp.login'))
@bp_user.route('/ranking/<sido_no>/<sgg_no>')
def ranking_seoul(sido_no, sgg_no):
    if 'user_id' in session:
        # session['user_id'] = mem_id로 저장했었음. 
        # 따라서 (여기서 받는 인자 mem_id)=session['user_id']=(사용자가 입력한 mem_id)
        mem_id = session['user_id']

        # mem_id에 따른 혼밥유형 가져오기
        a = obj.getHbtype(mem_id)
        sido = obj.get_sido_name(sido_no)
        sigungu = obj.get_sigungu_name(sgg_no)

        if a['hb_id'] == 1: # 일반인파
            rest_info_normal = obj.getRestInfo_normal(sido_no, sgg_no)
            print(sigungu)
            return render_template('ranking_normal.html', restInfo = rest_info_normal, sido=sido, sigungu=sigungu)
        if a['hb_id'] == 2: # 미식가파
            rest_info_taste = obj.getRestInfo_taste(sido_no, sgg_no)
            return render_template('ranking_taste.html', restInfo = rest_info_taste, sido=sido, sigungu=sigungu)
        if a['hb_id'] == 3: # 분위기파
            rest_info_mood = obj.getRestInfo_mood(sido_no, sgg_no)
            print(rest_info_mood)
            return render_template('ranking_mood.html', restInfo = rest_info_mood, sido=sido, sigungu=sigungu)
        # return render_template('ranking_normal.html', restInfo = rest_info)
    else:
        return redirect(url_for('userbp.login'))

@bp_user.route('/ranking/<sido_no>/')
def ranking_others(sido_no):
    if 'user_id' in session:
        return render_template('alert3.html') 
    else:
        return redirect(url_for('userbp.login'))

@bp_user.route('/restaurantDetail/<rest_id>')
def restaurantDetail(rest_id):
    if 'user_id' in session:
        user= dbHelper.get_hbType(session['user_id'])
        rest = dbHelper.getRestInfo3(rest_id)
        obj = HBFormula()
        try:
            sizeCount = obj.getSizePercent(dbHelper.getSize(rest_id,'big'),dbHelper.getSize(rest_id,'small'))
            soundCount = obj.getSoundPercent(dbHelper.getSound(rest_id,'noisy'),dbHelper.getSound(rest_id,'silent'))
        except Exception as e1:
            sizeCount = None
            soundCount =None
        return render_template('restaurantDetail.html', user = user, rest=rest,sizeCount=sizeCount,soundCount=soundCount)
    else:
        return redirect(url_for('userbp.login'))



if __name__ == '__main__':
    obj = DBHelper()
    print(obj.getRestInfo())
    print(session['user_id'])



