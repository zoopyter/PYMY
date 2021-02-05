# Created By  : hclim
# Created Date: 2021-02-04
import engine.common.eg_period import EGPeriod
import engine.common.eg_calendar import EGCalendar

class EGSchedule(object):
    def __new__(cls, effect_date, mat_date, period, hol=EGCalendar(''), bus_conv='MF', mat_conv='MF', date_gen='FW', eom=True, first_date='', nexttolast_date=''):
        dates=[]
        start_date = effect_date
        end_date = mat_date
        eom = True if effect_date.is_eom() and eom else False

        #n = int(np.floor((mat_date-settle).days/30.0/tenor+1))
        if date_gen=='FW':
            dates.append(start_date)
            if first_date!='':
                dates.append(first_date)
                start_date = first_date
            if nexttolast_date!='':
                end_date=nexttolast_date

            # print(start_date<=(end_date.addtodate(-10,'d')))
            while start_date<end_date:
                start_date = start_date.addtodate(period)
                start_date = start_date.eom() if eom else start_date
                if start_date<=(end_date.addtodate(EGPeriod('-10d'))):
                    dates.append(start_date)
                else:
                    dates.append(end_date)
                    if nexttolast_date!='':
                        dates.append(mat_date)

        elif date_gen=='BW':
            dates.append(end_date)
            if first_date!='':
                start_date = first_date
            if nexttolast_date!='':
                dates.append(nexttolast_date)
                end_date=nexttolast_date

            while start_date<end_date:
                end_date = end_date.addtodate(-period)
                end_date = end_date.eom if eom else end_date
                if start_date<=(end_date.addtodate(EGPeriod('-10d'))):
                    dates.append(end_date)
                else:
                    dates.append(start_date)
                    if first_date!='':
                        dates.append(effect_date)

        elif date_gen=='ZO':
            dates.append(mat_date) 

        dates = sorted(dates)
        schedule = [hol.adjust(d,bus_conv) for d in dates[:-1]]
        
        schedule.append(dates[-1])
        if mat_conv!='UN':
            schedule[-1]=hol.adjust(schedule[-1],mat_conv)

        return schedule

    def __str__(self):
        return repr(self)