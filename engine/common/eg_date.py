#EGDate
#egpricing_python_project
#---------------------------------------------------------
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta  # used in yearfrac, addtodate
from engine.common.eg_period import EGPeriod
import calendar
#---------------------------------------------------------

class EGDate(date):
    def __new__(self, temp1, temp2=None, temp3=None, date_format='%Y%m%d'):
        if isinstance(temp1, date):
            d = temp1
        elif isinstance(temp1, datetime):
            d = temp1.date()
        elif isinstance(temp1, str):
            d = datetime.strptime(temp1.replace('-', ''), date_format).date()
        elif isinstance(temp1, int) and \
                isinstance(temp2, int) and \
                isinstance(temp3, int):
            d = date(temp1, temp2, temp3)
        else:
            print(type(temp1))
            raise "invalid date input"
        self.date_format = date_format
        return super().__new__(self, year=d.year, month=d.month, day=d.day)

    def __str__(self):
        return f"{self.year:04d}{self.month:02d}{self.day:02d}"

    def __add__(self, num):  # obj o = o + x
        return EGDate(self.__add(num))

    def __radd__(self, num):  # obj o = x + o
        return EGDate(self.__add(num))

    def __iadd__(self, num):  # obj o += x
        return EGDate(self.__add(num))

    def __sub__(self, num):  # obj o = o + x
        return self.__sub(num)

    def __rsub__(self, num):  # obj o = o + x
        return self.__sub(num)

    def __isub__(self, num):  # obj o += x
        return self.__sub(num)

    def __add(self, x):
        if isinstance(x, (int, float)):
            return super(EGDate, self).__add__(timedelta(days=int(x)))
        elif isinstance(x, EGPeriod) or isinstance(x, relativedelta):
            d: date = self.to_date()  # date(self.year, self.month, self.day)
            d = d+relativedelta(years=x.years)
            d = d+relativedelta(months=x.months)
            d = d+relativedelta(days=x.days)
            return d
        else:
            return super(EGDate, self).__add__(x)

    def __sub(self, x):
        if isinstance(x, (int, float)):
            return super(EGDate, self).__sub__(timedelta(days=int(x)))
        elif isinstance(x, EGPeriod) or isinstance(x, relativedelta):
            d = date(self.year, self.month, self.day)
            d = d-relativedelta(years=x.years)
            d = d-relativedelta(months=x.months)
            d = d-relativedelta(days=x.days)
            return d
        else:
            return super(EGDate, self).__sub__(x)

    def add(self, x):
        self = EGDate(self.__add(x))

    def clone(self):
        return EGDate(self)

    def to_date(self):
        return date(self.year, self.month, self.day)

    def is_leapself(self):
        y = self.year
        if y % 400 == 0:
            return True
        if y % 100 == 0:
            return False
        if y % 4 == 0:
            return True
        else:
            return False

    def eom(self):
        return EGDate(self.year, self.month, calendar.mdays[self.month])

    def is_eom(self):
        return calendar.mdays[self.month] == self.day

    # next_weekday: d의 다음주 w(요일) 산출
    # d: EQDate
    # w: weekday
    def next_weekday(self, w):
        gap = w - self.weekday()
        if gap <= 0:
            gap += 7
        return self + timedelta(days=gap)
        #return EGDate(d.year,d.month,d.day)

    # nth_weekday: d의 해당 월의 n번째 w(요일) 산출
    # d: EQDate
    # w: weekday
    def nth_weekday(self, nw, w):
        d = EGDate(self.year, self.month, 1)
        adj = (w - d.weekday()) % 7
        d += timedelta(days=adj)
        d += timedelta(weeks=nw-1)
        return d

    @staticmethod
    def pydate(d, fmt='%Y%m%d'):
        if isinstance(d, datetime):
            return d
        elif isinstance(d, str):
            return datetime.strptime(d.replace('-', ''), fmt)
        elif isinstance(d, (int, float)):
            return datetime(1900, 1, 1)+timedelta(int(d))
        else:
            raise('invalid data')

    @staticmethod
    def xldate(d, fmt='%Y%m%d'):
        if isinstance(d, datetime):
            return (d-datetime(1900, 1, 1)).days
        elif isinstance(d, str):
            return xldate(datetime.strptime(d.replace('-', ''), fmt))
        elif isinstance(d, (int, float)):
            return int(d)
        else:
            raise('invalid data')
