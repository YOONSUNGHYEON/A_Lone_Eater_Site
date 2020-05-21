# blueprint 정의
from flask import Blueprint

# ~/user
bp_user = Blueprint('userbp', 
                    __name__, 
                    template_folder='../templates',
                    static_folder='../static')

# ~/join
bp_join  = Blueprint('joinbp',
                    __name__, 
                    template_folder='../templates',
                    static_folder='../static')

# ~/bbs
bp_review  = Blueprint('reviewbp',
                    __name__, 
                    template_folder='../templates',
                    static_folder='../static')

# ~/mypage
bp_mypage  = Blueprint('mypagebp',
                    __name__, 
                    template_folder='../templates',
                    static_folder='../static')