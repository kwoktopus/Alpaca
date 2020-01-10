class Market:

    def __init__(self, api):
        self.api = api
        self.watchList = []


    
    def getMovingAverage(self, stock, timePeriod, nPeriods):
        avg = 0

        bars = self.api.get_barset(stock, timePeriod, limit=nPeriods)[stock]

        for bar in bars:
            avg += bar.o
        
        return avg/nPeriods
        
    

    def addWatchList(self, stock):
        self.watchList.append(stock)




    