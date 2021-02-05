# Created By  : hclim
# Created Date: 2021-02-04
#---------------------------------------------------------
from datetime import date, datetime, timedelta
from enum import Enum
# from engine_modules.PrepareData import *
import calendar
#---------------------------------------------------------

class TimeUnit(str, Enum):
    ```
    TimeUnit 필요함 
    ```
    Days = "D"
    Weeks = "W"
    Months = "M"
    Years = "Y"
    Minutes = "MI"
    Seconds = "SE"

class BusConv(str, Enum):
    Following = "F"
    ModifiedFollowing = "MF"
    Preceding = "P"
    ModifiedPreceding = "MP"
    Unadjusted = "U"
    Nearest = "NE"

class EGCalendar(object):
    class __EGCalendar(object):
        def __init__(self, name, arg={'Weekdays':{5,6}, 'Hol':[]}):
            self.name_ = name
            self.holidays_ = arg['Hol']
            self.weekdays_ = set(arg['Weekdays'])

        def __str__(self):
            return repr(self) + self.name_

        def set_weekdays(self, wds={5, 6}):
            #self.weekdays_ = set()
            if not hasattr(wds, '__iter__'):
                wds = {wds}
            self.weekdays_ = set(wds)

        def get_weekdays(self):
            return self.weekdays_

        def get_holidays(self):
            return list(self.holidays_)

        def set_holidays(self, h):
            return self.addholiday(h)

        def busdate(self, d, dire=1):
            sgn = 1
            if dire < 0:
                sgn = -1
            elif dire == 0:
                raise('0 direction')

            d2 = d+timedelta(days=dire)
            while not self.is_busday(d2):
                d2 += timedelta(days=sgn)
            return d2

        def is_busday(self, d):
            if d.weekday() in self.weekdays_:
                return False
            elif d in self.holidays_:
                return False
            return True

        def is_holiday(self, d):
            return not self.is_busday(d)

        def is_weekend(self, d):
            if d.weekday() in self.weekdays_:
                return True
            else:
                return False

        def add_holiday(self, dd):
            if hasattr(dd, '__iter__'):
                for d in dd:
                    self.add_holiday1(d)
            else:
                self.add_holiday1(d)

        def add_holiday1(self, d):
            if isinstance(d, str):
                d = dparser(d).date()
            if isinstance(d, date):
                self.holidays_.add(d)
            else:
                raise "wrong date"

        def remove_holiday(self, d):
            self.holidays_.discard(d)

        def adjust(self, d, conv="F"):
            #f: following, mf: modified-following, p:precedings, mp:mod-p
            if self.is_busday(d):
                return d
            if conv == 'F':
                return self.busdate(d, 1)
            elif conv == 'MF':
                d2 = self.busdate(d, 1)
                if d2.month != d.month:
                    return self.busdate(d, -1)
                else:
                    return d2
            elif conv == 'P':
                return self.busdate(d, -1)
            elif conv == 'MP':
                d2 = self.busdate(d)
                if d2.month != d.month:
                    return self.busdate(d, 1)
                else:
                    return d2
            elif conv == 'U':
                return d
            else:
                raise('invalid bizconv {}'.format(conv))

        def advance(self, d, period, conv="F", eom=False):
            n = period.n_
            unit = period.unit_

            if n == 0:
                return self.adjust(d, conv)
            elif unit == "D":
                d1 = d
                if n > 0:
                    while n > 0:
                        d1 = d1+timedelta(days=1)
                        if self.is_holiday(d1):
                            d1 = d1+timedelta(days=1)
                        n -= 1
                else:
                    while n < 0:
                        d1 = d1+timedelta(days=-1)
                        if self.is_holiday(d1):
                            d1 = d1+timedelta(days=-1)
                        n += 1
                return d1
            elif unit == "W":
                d1 = d.addtodate(d, period)
                return self.adjust(d1, conv)
            else:  # M,Y
                d1 = d.addtodate(d, period)
                if eom and self.is_eom(d):
                    return calendar.mdays[d1.month]
                return self.adjust(d1, conv)

        def busdaysbetween(self, d1, d2, isd1=True, isd2=False):
            s = 0 if isd1 else 1
            e = 1 if isd2 else 0
            dd = [d1 + timedelta(days=x) for x in range(s, (d2-d1).days+e)]
            busdates = []
            for d in dd:
                if self.is_busday(d):
                    busdates.append(d)
            return busdates

        def clear(self):
            self.holidays_ = set()

    instances_ = {}

    def reset_instances():
        EGCalendar.instances_ = {}

    def get_instances():
        return EGCalendar.instances_

    def clear_instance(name):
        EGCalendar.instances_.pop(name, None)

    def __new__(cls, name, arg={'Weekdays':{5,6}, 'Hol':[]}):
        if not isinstance(name, str):
            raise "wrong or empty calendar name"
        if len(name) == 0:
            name = "NULL"

        name = name.upper()
        if not EGCalendar.instances_.get(name):
            EGCalendar.instances_[name] = EGCalendar.__EGCalendar(name)
        return EGCalendar.instances_[name]

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


