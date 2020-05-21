from flask import Flask, render_template, redirect, url_for, session, request, jsonify, make_response
from service.controller import bp_review
# 디비
from service.model import dbHelper
from service import config
from service.controller.hbTypeCal import HBFormula
app = Flask(__name__)


@bp_review.route('/review/<rest_id>/<user_id>/<user_hbType>/<tasteScore>/<moodScore>/<restSize>/<restSound>/<num>')
def review(rest_id,user_id,user_hbType,tasteScore,moodScore,restSize,restSound,num): 
    tmp = HBFormula(tasteScore,moodScore,user_hbType)
    cnt = tmp.getHBFormulaResult()
    print(cnt)
    if num == '1':
        result = dbHelper.insertReview(rest_id,user_id,tasteScore,moodScore,restSize,restSound)
        return jsonify(result)    
    else:
        return jsonify(cnt)
        
        

if __name__ == '__main__':
    app.run(debug = True)
        

