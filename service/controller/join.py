import json
from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response
from service.controller import bp_join
# 디비
from service.model import dbHelper, PostModel
from service import config
from service.model.dbMgr import DBHelper

obj = DBHelper()

# /join/
@bp_join.route('/', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        sido_number=11  # 임시기본값
        sidos = obj.get_sido() # 시도 전체의 sido_no, sido_name 가져옴
        sigungus = obj.get_sigungu( sido_number ) # sigungus에는 서울시 구의 sgg_name 자료 존재
        # return redirect(url_for('joinbp.repeat_check'))
        return render_template('join.html', sidos=sidos, sigungus=sigungus, config=config )
    else:
        mem_id          = request.form['mem_id']
        mem_nickname    = request.form['mem_nickname']
        mem_password    = request.form['mem_password']
        mem_gender      = request.form['mem_gender']
        mem_age         = request.form['mem_age']
        hb_id           = request.form['hb_id']
        sido_no         = request.form['sido_no']
        sgg_no          = request.form['sgg_no']
        param = PostModel( mem_id, mem_nickname, mem_password, mem_gender, mem_age, hb_id, sido_no, sgg_no )
        dbHelper.join(param)
        return render_template('common/alert_join.html', msg='%s님 슬기로운 혼밥러가 되신 것을 환영합니다 ♡'%(mem_id))


# id 중복확인 버튼 클릭하여 함수 호출 후 넘어가는 url
@bp_join.route('/id_check/<mem_id>')
def id_check(mem_id):
    cnt = obj.idCheck(mem_id)
    # 결과 => {'cnt' : 0 또는 1 }
    return jsonify(cnt)

# 닉네임 중복체크
@bp_join.route('/nickname_check/<mem_nickname>')
def nickname_check(mem_nickname):
    cnt = obj.nicknameCheck(mem_nickname)
    return jsonify(cnt)