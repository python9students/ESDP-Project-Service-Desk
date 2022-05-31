import datetime, businesstimedelta, pytz



# def find_working_day_after(start_date, days_to_add):
#     # 0 - Sunday and 6 Saturday are to be skipped
#     workingDayCount = 0
#     while workingDayCount < days_to_add:
#         start_date += datetime.timedelta(days=1)
#         weekday = int(start_date.strftime('%w'))
#         print(weekday)
#         if (weekday != 0 and weekday != 6):
#             workingDayCount += 1
#
#     return start_date
#
#
#
# def convert_hour_to_sec(time):
#     h, m, s = time.split(":")
#     return (int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds()))
#
#
# def add_weekday_seconds(start, x):
#     rr = rrule(SECONDLY, byweekday=(MO, TU, WE, TH, FR), dtstart=start, interval=x)
#     return rr.after(start)

def buisnesstimedelta_function(object_):
    workday = businesstimedelta.WorkDayRule(
        start_time=datetime.time(9),
        end_time=datetime.time(18),
        working_days=[0, 1, 2, 3, 4],
        tz=pytz.timezone('Asia/Bishkek'))
    businesshrs = businesstimedelta.Rules([workday])
    expected_time_to_finish = object_.expected_finish_date
    time_difference = businesshrs.difference(datetime.datetime.now(), expected_time_to_finish)
    return time_difference