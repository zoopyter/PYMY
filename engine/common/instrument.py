#---------------------------------------------------------
from numpy import array as a_
from dateutil.relativedelta import relativedelta
#---------------------------------------------------------
class IInstrument:
    def __init__(self):
        self.name_ = ""
        self.code_ = ""
        self.arg_ = {}
        self.res_ = {}
        self.pricer_ = None

    def calculate(self):
        if isinstance(self.pricer_, IInstrument):
            self.pricer_.calculate()
            self.res_ = self.pricer_.res_
            
    def get_value(self, tag, defval=None):
        return self.res_.get(tag, defval)
        
    def get_argvalue(self, tag, defval=None):
        return self.arg_.get(tag, defval)
    
    def get_maturity(self):
        pass
#---------------------------------------------------------
class IPricer:
    instrument_ = None
    evaldate_ = None
    price_ = None
    res_ = {}
    def calculate(self):
        pass
#---------------------------------------------------------
