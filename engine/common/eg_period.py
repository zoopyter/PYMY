# Created By  : hclim
# Created Date: 2021-02-04
"""The Module Has Been Build for..."""
from dateutil.relativedelta import relativedelta  # used in yearfrac, addtodate

class EGPeriod:
    def __init__(self, temp1, temp2=None, temp3=None):
        if isinstance(temp1, str):
            self.years, self.months, self.days = \
                EGPeriod.conv_tenor(temp1)
        elif isinstance(temp1, relativedelta):
            self.years, self.months, self.days = \
                temp1.years, temp1.months, temp1.days
            if self.years is None:
                self.years = 0
            if self.months is None:
                self.months = 0
            if self.days is None:
                self.days = 0
        elif isinstance(temp1, int) and \
                isinstance(temp2, int) and \
                isinstance(temp3, int):
            self.years = temp1
            self.months = temp2
            self.days = temp3
        else:
            raise "invalid period input"

    def __add__(self, temp):  # obj o = o + x
        if isinstance(temp, EGPeriod):
            years = self.years + temp.years
            months = self.months + temp.months
            days = self.days + temp.days
            return EGPeriod(years, months, days)
        else:
            raise "invalid period add input"

    def __radd__(self, temp):  # obj o = x + o
        return self.__add__(temp)

    def __sub__(self, temp):  # obj o = o + x
        if isinstance(temp, EGPeriod):
            years = self.years - temp.years
            months = self.months - temp.months
            days = self.days - temp.days
            return EGPeriod(years, months, days)
        else:
            raise "invalid period add input"

    def to_relativedelta(self):
        return relativedelta(years=self.years, months=self.months, days=self.days)

    def get_periodmonth(self):
        periodmonth = self.years*12 + self.months
        return periodmonth

    @staticmethod
    def conv_tenor(period):
        period = period.upper()
        num = period.find('Y')
        years = 0
        months = 0
        days = 0
        if num > -1:
            years = int(period.split('Y')[0])
            period = period[num+1:]
        num = period.find('M')
        if num > -1:
            months = int(period.split('M')[0])
            period = period[num+1:]
        num = period.find('D')
        if num > -1:
            days = int(period.split('D')[0])
        return years, months, days


if __name__ == "__main__":
    period1 = EGPeriod('3M')
    period2 = period1.__add__(period1)
    period3 = period1.__radd__(period1)
    list_test = [1, 2, 2, 2]
    #print(__radd__(1, 2))
