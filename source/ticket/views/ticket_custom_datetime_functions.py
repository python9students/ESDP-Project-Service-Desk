import datetime
from dateutil.rrule import *
from datetime import datetime, timedelta

def find_working_day_after(start_date, days_to_add):
    # 0 - Sunday and 6 Saturday are to be skipped
    workingDayCount = 0
    while workingDayCount < days_to_add:
        start_date += datetime.timedelta(days=1)
        weekday = int(start_date.strftime('%w'))
        print(weekday)
        if (weekday != 0 and weekday != 6):
            workingDayCount += 1

    return start_date


# startDate = datetime.datetime(2022, 5, 21)
# daysToAdd = 10
# print(find_working_day_after(startDate, daysToAdd))

def convert_hour_to_sec(time):
    h, m, s = time.split(":")
    return (int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds()))


def add_weekday_seconds(start, x):
    rr = rrule(SECONDLY, byweekday=(MO, TU, WE, TH, FR), dtstart=start, interval=x)
    return rr.after(start)


# def clamp(t, start, end):
#     "Return `t` clamped to the range [`start`, `end`]."
#     return max(start, min(end, t))
#
#
# def day_part(t):
#     "Return timedelta between midnight and `t`."
#     return t - t.replace(hour = 0, minute = 0, second = 0)
#
#
# def office_time_between(a, b, start = timedelta(hours = 8),
#                         stop = timedelta(hours = 17)):
#
#     """
#     Return the total office time between `a` and `b` as a timedelta
#     object. Office time consists of weekdays from `start` to `stop`
#     (default: 08:00 to 17:00).
#     """
#     zero = timedelta(0)
#     assert(zero <= start <= stop <= timedelta(1))
#     office_day = stop - start
#     days = (b - a).days + 1
#     weeks = days // 7
#
#     if a.weekday() == 0 and (b.weekday() == 4 or b.weekday() == 5):
#         extra = 5
#     else:
#         extra = (max(0, 5 - a.weekday()) + min(5, 1 + b.weekday())) % 5
#     weekdays = weeks * 5 + extra
#     total = office_day * weekdays
#     if a.weekday() < 5:
#         total -= clamp(day_part(a) - start, zero, office_day)
#     if b.weekday() < 5:
#         total -= clamp(stop - day_part(b), zero, office_day)
#     return total