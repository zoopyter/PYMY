import engine_modules
import engine
from engine.common.eg_calendar import EGCalendar
from engine.common.eg_date import EGDate
def test_eg_calendar():

    value = {'Weekdays':{1,7}}
    code = 'SS'
    calendar = EGCalendar(code, value)
    print(calendar)
    print(calendar.get_holidays())


def test_eg_date():
    date1 = EGDate('2020-11-30')
    print(date1)

# def test_get_bondcfdates():
#     issue=EGDate(2020,9,25)
#     maturity=EGDate(2025,9,25)
#     period=EGPeriod('3M')
#     bus_conv='MF'
#     mat_conv='UN'
#     date_gen='FW'
#     eom=True
#     start = timeit.default_timer()
#     # hol=get_Hol('KR',datetime(2020,1,1),datetime(2025,9,30))
#     hol = new_Calendar('KR')
#     stop = timeit.default_timer()
#     print('hol Time: ', stop - start)
#     first=''
#     nexttolast=''
    
#     start = timeit.default_timer()
#     schedule = EGSchedule(issue, maturity, period, hol, bus_conv, mat_conv, date_gen, eom, first, nexttolast)
#     print(schedule)


if __name__ == "__main__":
    #test_eg_calendar()
    test_eg_date()

