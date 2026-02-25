class Grid:

    @staticmethod
    def getx(x,ops=False):
        if ops:
            return x  * 70 // 100
        return x * 30 // 100


    @staticmethod
    def gety(y,ops=False):
        if ops:
            return y * 70 // 100 
        return y * 30 // 100
    
    @staticmethod
    def getSqt(y,x):
        return(Grid.gety(y),Grid.getx(x))