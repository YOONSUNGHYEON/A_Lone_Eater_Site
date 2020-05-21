import json
from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response
from service.controller import bp_mypage
# 디비
from service.model import dbHelper, PostModel
from service import config
from service.model.dbMgr import DBHelper

obj = DBHelper()

# /mypage/ -> 그냥 마이페이지
@bp_mypage.route('/')
def mypage():
    if 'user_id' in session:
        row = obj.getInfo(session['user_id'])
        visit = obj.getVisit(session['user_id'])
        print('mypage row=', row)
        print('mypage visit=', visit)
        sidos = obj.get_sido()
        sigungus = obj.get_sigungu( row['sido_no'] )
        return render_template('mypage.html', row=row, visit=visit, sidos=sidos, sigungus=sigungus)
    else:
        return redirect(url_for('userbp.login'))
        

#mypage/revise -> 마이페이지 수정 전 화면
@bp_mypage.route('/revise', methods=['GET', 'POST'])
def mypage_revise():
    if 'user_id' in session: 
        if request.method == 'GET':
            row = obj.getInfo(session['user_id'])
            sidos = obj.get_sido()
            sigungus = obj.get_sigungu( row['sido_no'] )
            return render_template('mypage_revise.html', row=row, sidos=sidos, sigungus=sigungus)
        print('1')
    else:
        return redirect(url_for('userbp.login'))
    


#mypage/revise2 -> 마이페이지 수정후화면
@bp_mypage.route('/revise2', methods=['GET', 'POST'])
def myRevise():
    if request.method == 'GET':
        sido_number=11 # 임시기본값
        sidos = obj.get_sido() # 시도 전체의 sido_no, sido_name 가져옴
        sigungus = obj.get_sigungu( sido_number ) # sigungus에는 서울시 구의 sgg_name 자료 존재
        # return redirect(url_for('joinbp.repeat_check'))
        return render_template('mypage.html', sidos=sidos, sigungus=sigungus, config=config )
    else:
        mem_id          = request.form['mem_id']
        mem_nickname    = request.form['mem_nickname']
        mem_password    = request.form['mem_password']
        mem_gender      = request.form['mem_gender']
        mem_age         = request.form['mem_age']
        hb_id           = request.form['hb_id']
        sido_no         = request.form['sido_no']
        sgg_no          = request.form['sgg_no']
        obj.updateMyInfo(mem_id, mem_password, mem_age, hb_id, sgg_no, sido_no)
        return redirect(url_for('mypagebp.mypage'))
        


