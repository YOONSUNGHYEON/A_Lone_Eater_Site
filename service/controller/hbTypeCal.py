from service.model import dbHelper

class HBFormula:
    user_hptype = ''
    tasteScore = 0
    moodScore = 0

    def __init__(self,tasteScore=None,moodScore=None, user_hptype=None):
        self.user_hptype = user_hptype
        self.tasteScore = tasteScore
        self.moodScore = moodScore

    def getHBFormulaResult(self):     
        if self.user_hptype=='일반인파':
            visit_total_score = (int(self.tasteScore) + int(self.moodScore))/2
        elif self.user_hptype=='분위기파':
            visit_total_score = (int(self.tasteScore)* 0.2) + (int(self.moodScore)* 0.8)   
        else:
            visit_total_score = (int(self.tasteScore)* 0.8 )+ (int(self.moodScore) * 0.2 )
        return visit_total_score

    def getSizePercent(self, cate1, cate2):
        len = cate1['big']+cate2['small']
        bigPercent = (cate1['big']/len)*100
        smallPercent = (cate2['small']/len)*100
        return bigPercent,smallPercent
        
    def getSoundPercent(self, cate1, cate2):
        len = cate1['noisy']+cate2['silent']
        noisyPercent = (cate1['noisy']/len)*100
        silentPercent = (cate2['silent']/len)*100
        return noisyPercent,silentPercent
        
       
        