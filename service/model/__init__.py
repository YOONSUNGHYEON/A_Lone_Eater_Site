from service.model.dbMgr import DBHelper
dbHelper = None

# DBHelper 객체를 생성하는 역할만 담당
def createDBHelper( app ):
    global dbHelper
    dbHelper = DBHelper( app )

class PostModel:
    mem_id          = None
    mem_nickname    = None
    mem_password    = None
    mem_gender      = None
    mem_age         = None
    hb_id           = None
    sido_no         = None
    sgg_no          = None
    def __init__(self, mem_id, mem_nickname, mem_password, mem_gender, mem_age, hb_id, sido_no, sgg_no):
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