import numpy as np
from numpy import array as a_
#from dateutil.relativedelta import relativedelta  
# used in yearfrac, addtodate
from enum import Enum, IntEnum
import scipy.interpolate
from scipy.optimize import least_squares as LeastSquares
from engine.common.instrument import IInstrument
from engine.common.eg_date import EGDate
from engine.common.eg_daycounter import Actual365
#---------------------------------------------------------

class Compounding(str, Enum):
    Simple = "SIMPLE"
    Compounded = "COMPOUNDED"
    Continuous = "CONTINUOUS"
    SimpleThenCompounded = "SIMPLECOMP"
    CompoundedThenSimple = "COMPSIMPLE"

class ZeroCurve(IInstrument):
    """tenor와 이자율을 입력받아 필요 이자율을 생성하는 클래스 
    :param date refdate: 
    :param date[] dates:
    :parma float[] times:
    :parma float[] zeros:
    """

    def __init__(self, arg={}):
        self.arg_ = arg
        self.zinterp_ = None
        self.zspread_ = 0.0
        self.setup_argument(arg)

    def setup_argument(self, arg):
        self.arg_ = arg
        self.refdate_ = arg.get('refdate', EGDate.today())
        self.calendar_ = arg.get('calendar', None) #needs for spotdays
        self.daycounter_ = arg.get('daycounter', None)
        self.spotdays_ = arg.get('spotdays', 0)
        self.dates_ = arg.get('dates', [])
        self.zeros_ = arg.get('zeros', [])
        self.times_ = arg.get('times', [])
        if not self.daycounter_:
            self.daycounter_ = Actual365.Actual365()
        self.set_zeros(self.times_, self.zeros_)
        
    def set_zeros(self, times, zeros, comp=Compounding.Continuous):
        """time tenor와 zero rate을 이용하여 이자율 커브를 생성 ."""

        #if not times: #<--0, [], None checking
        #    return #do nothing
        self.times_ = times
        self.zeros_ = zeros
        if isinstance(self.times_, (int, float)):
            self.times_ = [0.0, np.finfo(float).max]
            self.zeros_ = [self.zeros_, self.zeros_]
        elif hasattr(self.times_, '__iter__'):
            if len(self.times_)==1:
                self.times_ = self.times_+ self.times
                self.zeros_ = self.zeros_+ self.zeros_
            elif len(self.times_)==0:
                return #do nothing
        #sorted_by_second = sorted(data, key=lambda tup: tup[1])
        self.zinterp_ = scipy.interpolate.interp1d( \
                        self.times_, 
                        self.zeros_, 
                        bounds_error=False,
                        fill_value=(self.zeros_[0], self.zeros_[-1]))
    
    def set_zspread(self, zspr):
        self.zspread_ = zspr
    
    def get_time1(self, t):
        """테너 기간 을 return """

        if isinstance(t, EGDate):
            return self.daycounter_.yearfraction(self.refdate_, t)
        else:
            return t

    def get_time(self, t):
        if hasattr(t, '__iter__'):
            tt = []
            for t_ in t:
                tt.append(self.get_time1(t_))
            return tt
        else:
            return self.get_time1(t)

    def get_discount(self, t):
        t = self.get_time(t)
        z = self.get_zerorate(t)
        return np.exp(-z*t)
    
    def get_zerorate(self, t):
        t = self.get_time(t)
        if self.zinterp_:
            return self.zinterp_(t)+self.zspread_
        else:
            raise "empty zero data"
            
    def get_fwdrate(self, times, dt=0.001):
        #(1)piecewise flat forward rates
        if isinstance(times,(int,float)):
            times = a_([times, times+dt])

        if hasattr(times, '__iter__'): 
            discs = self.get_discount(times)
            fdiscs = discs[1:]/discs[:-1]
            dtimes = np.diff(times)
            fwds = -np.log(fdiscs)/dtimes
            return fwds
        else:
            raise( "invalid times")
