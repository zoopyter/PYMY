#EGPeriod
#egpricing_python_project
#---------------------------------------------------------
import numpy as np
from numpy import array as a_
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta  # used in yearfrac, addtodate
from enum import Enum
from engine.common.eg_date import EGDate
#---------------------------------------------------------

class DayCounter:
    class Basis(str, Enum):
        BondCoupon = "BONDCOUPON"
        Thirty360EU = "THIRTY360EU"
        Thirty360US = "THIRTY360US"
        Actual360 = "ACTUAL360"
        ActualActualISDA = "ACTUALACTUAL"
        Actual365 = "ACTUAL365"

    #name_ = DayCounter.Name.ACT365<--static member
    instance_ = None
    def __init__(self, basis):
        if not isinstance(basis, str):
            basis = ""
        self.instance_ = DayCounter.create(basis)
        #print(self.instance_)

    def yearfraction(self, date1, date2):
        return self.instance_.yearfraction(date1, date2)

    @staticmethod
    def yearfraction_raw(basis, date1, date2):
        y1 = date1.year
        m1 = date1.month
        d1 = date1.day
        y2 = date2.year
        m2 = date2.month
        d2 = date2.day

        if basis == DayCounter.Basis.BondCoupon:
            if m1 == 2 and d1 > 27:
                d1 = 30
            if m2 == 2 and d2 > 27:
                d2 = 30
            t = 360.0*(y2-y1)+30*(m2-m1-1) + \
                np.maximum(30-d1, 0)+np.minimum(30, d2)
            t /= 360.0
        elif basis == DayCounter.Basis.Actual360:
            t = (date2-date1).days/360.0
        elif basis == DayCounter.Basis.ActualActualISDA:
            t1 = 365.0
            t2 = 365.0
            if EGDate.is_leap(y1):
                t1 = 366.0
            if EGDate.is_leap(y2):
                t2 = 366.0
            t = y2 - y1 - 1
            t = t + (date(y1 + 1, 1, 1) - d1) / t1
            t = t + (date2 - date(y2, 1, 1)) / t2
        else:
            t = (date2-date1).days/365.0
        return t

    @staticmethod
    def create(basis):
        basis = basis.upper()
        if basis == DayCounter.Basis.Actual360:
            return Actual360()
        elif basis == DayCounter.Basis.Actual365:
            return Actual365()
        elif basis == DayCounter.Basis.ActualActualISDA:
            return ActualActualISDA()
        elif basis == DayCounter.Basis.Thirty360EU:
            return Thirty360EU()
        elif basis == DayCounter.Basis.Thirty360US:
            return Thirty360US()
        elif basis == DayCounter.Basis.BondCoupon:
            return BondCouponDayCounter()
        else:
            return Actual365()


class BondCouponDayCounter(object):
    class __BondCouponDayCounter(DayCounter):
        def __init__(self):
            self.basis_ = "BONDCOUPON"

        def __str__(self):
            return repr(self) + self.basis_

        def yearfraction(self, date1, date2):
            y1 = date1.year
            m1 = date1.month
            d1 = date1.day
            y2 = date2.year
            m2 = date2.month
            d2 = date2.day
            if m1 == 2 and d1 > 27:
                d1 = 30
            if m2 == 2 and d2 > 27:
                d2 = 30
            t = 360.0*(y2-y1)+30*(m2-m1-1) + \
                np.maximum(30-d1, 0)+np.minimum(30, d2)
            t /= 360.0
            return t
    instance = None

    def __new__(cls):  # __new__ always a classmethod
        if not BondCouponDayCounter.instance:
            BondCouponDayCounter.instance = BondCouponDayCounter.__BondCouponDayCounter()
        return BondCouponDayCounter.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class Actual360(object):
    class __Actual360(DayCounter):
        def __init__(self):
            self.basis_ = "ACTUAL360"

        def __str__(self):
            return repr(self) + self.basis_

        def daycount(self, date1, date2):
            return (date2-date1).days

        def yeardays(self):
            return 360.0

        def yearfraction(self, date1, date2):
            return (date2-date1).days/360.0
    instance = None

    def __new__(cls):
        if not Actual360.instance:
            Actual360.instance = Actual360.__Actual360()
        return Actual360.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class Actual365(object):
    class __Actual365(DayCounter):
        def __init__(self):
            self.basis_ = "Actual365".upper()

        def __str__(self):
            return repr(self) + self.basis_

        def daycount(self, date1, date2):
            return (date2-date1).days

        def yeardays(self):
            return 365.0

        def yearfraction(self, date1, date2):
            return (date2-date1).days/365.0
    instance = None

    def __new__(cls):  # __new__ always a classmethod
        if not Actual365.instance:
            Actual365.instance = Actual365.__Actual365()
        return Actual365.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class ActualActualISDA(object):
    class __ActualActualISDA(DayCounter):
        def __init__(self):
            self.basis_ = "ActualActualISDA".upper()

        def __str__(self):
            return repr(self) + self.basis_

        def daycount(self, date1, date2):
            return (date2-date1).days

        def yeardays(self):
            return 365.0

        def yearfraction(self, date1, date2):
            return (date2-date1).days/365.0
    instance = None

    def __new__(cls):  # __new__ always a classmethod
        if not ActualActualISDA.instance:
            ActualActualISDA.instance = ActualActualISDA.__ActualActualISDA()
        return ActualActualISDA.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class Thirty360EU(object):
    class __Thirty360EU(DayCounter):
        def __init__(self):
            self.basis_ = "Thirty360EU".upper()

        def __str__(self):
            return repr(self) + self.basis_

        def daycount(self, date1, date2):
            y1 = date1.year
            m1 = date1.month
            d1 = date1.day
            y2 = date2.year
            m2 = date2.month
            d2 = date2.day
            if m1 == 2 and d1 > 27:
                d1 = 30
            if m2 == 2 and d2 > 27:
                d2 = 30
            d = 360.0*(y2-y1)+30*(m2-m1-1) + \
                np.maximum(30-d1, 0)+np.minimum(30, d2)
            return d

        def yeardays(self):
            return 360.0

        def yearfraction(self, date1, date2):
            return self.daycount(date1, date2)/self.yeardays()

    instance = None

    def __new__(cls):
        if not Thirty360EU.instance:
            Thirty360EU.instance = Thirty360EU.__Thirty360EU()
        return Thirty360EU.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class Thirty360US(object):
    class __Thirty360US(DayCounter):
        def __init__(self):
            self.basis_ = "Thirty360US".upper()

        def __str__(self):
            return repr(self) + self.basis_

        def daycount(self, date1, date2):
            y1 = date1.year
            m1 = date1.month
            d1 = date1.day
            y2 = date2.year
            m2 = date2.month
            d2 = date2.day
            #if m1==2 and d1>27: d1 = 30
            #if m2==2 and d2>27: d2 = 30
            d = 360.0*(y2-y1)+30*(m2-m1-1) + \
                np.maximum(30-d1, 0)+np.minimum(30, d2)
            return d

        def yeardays(self):
            return 360.0

        def yearfraction(self, date1, date2):
            return self.daycount(date1, date2)/self.yeardays()

    instance = None

    def __new__(cls):
        if not Thirty360US.instance:
            Thirty360US.instance = Thirty360US.__Thirty360US()
        return Thirty360US.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

