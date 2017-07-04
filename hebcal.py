import math as _math
import datetime as _datetime
import time
data = {
100 : 36501 ,
200 : 73029 ,
300 : 109560 ,
400 : 146088 ,
500 : 182619 ,
600 : 219147 ,
700 : 255647 ,
800 : 292176 ,
900 : 328706 ,
1000 : 365235 ,
1100 : 401765 ,
1200 : 438294 ,
1300 : 474822 ,
1400 : 511322 ,
1500 : 547853 ,
1600 : 584381 ,
1700 : 620910 ,
1800 : 657440 ,
1900 : 693969 ,
2000 : 730469 ,
2100 : 766998 ,
2200 : 803528 ,
2300 : 840057 ,
2400 : 876587 ,
2500 : 913116 ,
2600 : 949616 ,
2700 : 986146 ,
2800 : 1022675 ,
2900 : 1059203 ,
3000 : 1095734 ,
3100 : 1132262 ,
3200 : 1168793 ,
3300 : 1205291 ,
3400 : 1241821 ,
3500 : 1278350 ,
3600 : 1314880 ,
3700 : 1351409 ,
3800 : 1387939 ,
3900 : 1424438 ,
4000 : 1460968 ,
4100 : 1497496 ,
4200 : 1534027 ,
4300 : 1570555 ,
4400 : 1607084 ,
4500 : 1643584 ,
4600 : 1680115 ,
4700 : 1716643 ,
4800 : 1753174 ,
4900 : 1789702 ,
5000 : 1826231 ,
5100 : 1862761 ,
5200 : 1899261 ,
5300 : 1935790 ,
5400 : 1972320 ,
5500 : 2008849 ,
5600 : 2045379 ,
5700 : 2081908 ,
5800 : 2118408 ,
5900 : 2154936 ,
6000 : 2191465}


def _get_molad(year):
    # gets a year, returns the day on which aleph tishrey is on

    a = (7 * (year - 1) + 1) % 19.0
    n = (235 * (year - 1) - a + 1) / 19

    s = 1.5305941358
    b = 2.2162037

    molad = (s * n + b) % 7

    # lo adu rosh
    if 1 < molad < 2:
        molad = 2
    elif 4 < molad < 5:
        molad = 5
    elif 6 < molad < 7:
        molad = 0

    # molad zaken
    elif 2.75 < molad < 3:
        molad = 3
    elif molad > 3.75 and molad < 4:
        molad = 5
    elif molad > 5.75 and molad < 6:
        molad = 0
    elif molad > 0.75 and molad < 1:
        molad = 2

    # gatrad
    elif not _is_meuberet(year) and 3.38287 < molad < 3.75:
        molad = 5

    # btu-takpat
    elif not _is_meuberet(year) and _is_meuberet(year - 1) and 2.64772 < molad < 2.75:
        molad = 3

    else:
        molad = int(molad)

    return molad


def _is_meuberet(year):
    a = year % 19
    m = [0, 3, 6, 8, 11, 14, 17]
    return a in m


def _day_count(year):
    current_molad = _get_molad(year)
    next_molad = _get_molad(year + 1)

    if _is_meuberet(year):
        if (current_molad + 383) % 7 == next_molad:
            return 383
        if (current_molad + 384) % 7 == next_molad:
            return 384
        if (current_molad + 385) % 7 == next_molad:
            return 385
    else:
        if (current_molad + 353) % 7 == next_molad:
            return 353
        if (current_molad + 354) % 7 == next_molad:
            return 354
        if (current_molad + 355) % 7 == next_molad:
            return 355


def _get_pesach(year):
    return (_get_molad(year + 1) - 2) % 7


def _print_year_info(year):
    print(_get_molad(year))
    print(_is_meuberet(year))
    print(_day_count(year))
    print(_get_pesach(year))


def _date_to_days(year, month, day):
    total = 0
    for i in range(1, year):
        total += _day_count(i)

    day_counts = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
    day_num = _day_count(year)
    if _is_meuberet(year):
        day_counts.insert(5, 30)
    if day_num == 353 or day_num == 383:
        day_counts[2] -= 1
    if day_num == 355 or day_num == 385:
        day_counts[1] += 1

    total += sum(day_counts[:month-1])
    total += day

    return total


def _days_to_date(num):
    year = 1
    # print(num)
    while _day_count(year+1) <= num:
        # print(num)
        num -= _day_count(year+1)
        year += 1
    # print(num)
    day_counts = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
    day_num = _day_count(year)
    if _is_meuberet(year):
        day_counts.insert(5, 30)
    if day_num == 353 or day_num == 383:
        day_counts[2] -= 1
    if day_num == 355 or day_num == 385:
        day_counts[1] += 1

    month = 1
    # print('num', num)
    # print(day_counts)
    for i in day_counts:
        # print('i',i)
        if i <= num:
            num -= i
            month += 1
        else:
            break
    # print(num)
    return (year,month,num-2)

def _days_to_date2(num):
    _datetime.timedelta(days=num)
    c = _date_to_days(3761, 4, 18)

# print(_days_to_date(_date_to_days(2,5,26)), (2,5,26))
# print(_days_to_date(_date_to_days(1000,2,26)), (1000,2,26))
# print(_days_to_date(_date_to_days(2000,6,26)), (2000,6,26))
# print(_days_to_date(_date_to_days(5777,5,26)), (5777,5,26))

# print('h')
print(_days_to_date(_date_to_days(777, 5, 26)))
# d = _date_to_days(5778, 5, 26)
# f = _date_to_days(5778, 1, 1)


# print(d-f)


def _heb_to_greg(year, month, day):
    d1 = _date_to_days(year, month, day)
    c = _date_to_days(3761, 4, 18)
    td = _datetime.timedelta(days=d1-c)
    return _datetime.date(year=1, day=1,month=1)+td



class TimeDelta:
    def __init__(self, weeks=0, days=0, hours=0, minutes=0):
        if minutes > 60:
            self.minutes = minutes % 60
            hours += minutes // 60
        else:
            self.minutes = minutes
        if hours > 24:
            self.hours = hours % 24
            days += hours // 24
        else:
            self.hours = hours
        if days > 7:
            self.days = days % 7
            weeks = days // 7
        else:
            self.days = days
        self.weeks = weeks

    def __str__(self):
        return 'TimeDelta<{}-{}  {}:{}>'.format(self.weeks,self.days,self.hours,self.minutes)

    def __neg__(self):
        # for CPython compatibility, we cannot use
        # our __class__ here, but need a real timedelta
        return TimeDelta(weeks= -self.weeks,
                         days= -self.days,
                         hours= -self.hours,
                         minutes= -self.minutes)

    def __add__(self, other):
        if isinstance(other, TimeDelta):
            return TimeDelta(weeks=self.weeks + other.weeks,
                             days=self.days + other.days,
                             hours=self.hours + other.hours,
                             minutes=self.minutes+self.minutes)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, TimeDelta):
            return TimeDelta(weeks=self.weeks - other.weeks,
                             days=self.days - other.days,
                             hours=self.hours - other.hours,
                             minutes=self.minutes - self.minutes)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, TimeDelta):
            return - self + other
        return NotImplemented


class DateTime:
    def __init__(self, year=5777, month=1, day=1):
        self.year = year
        self.month = month
        self.day = day

    def __add__(self, other):
        if isinstance(other, TimeDelta):



            return DateTime(weeks=self.weeks + other.weeks,
                             days=self.days + other.days,
                             hours=self.hours + other.hours,
                             minutes=self.minutes+self.minutes)
        return NotImplemented


    # implement __add__, __sub__ with timedelta

    def day_of_week(self):
        day_counts = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        day_num = _day_count(self.year)
        if _is_meuberet(self.year):
            day_counts.insert(5, 30)
        if day_num == 353 or day_num == 383:
            day_counts[2] -= 1
        if day_num == 355 or day_num == 385:
            day_counts[1] += 1

        total = sum(day_counts[:self.month-1])
        total += self.day
        total = total % 7
        total += _get_molad(self.year)
        return (total-1) % 7

    def gauss(self):
        # returns the date of pesach on self.year .
        # ladies and gentlemen, Carl Friedrich Gauss:
        A = self.year
        a = (12*A + 17) % 19
        b = A % 4
        res = 32 + (4343 / 98496) + (1 + (272953 / 492480)) * a + (b / 4) - ((313 / 98496) * A)
        april = 0
        M = int(res)
        c1 = False
        if M > 31:
            c1 = True
            M -= 31
            april = 1
        m = res - M
        c = (3*A + 5*b + M + 5) % 7
        c2 = False
        if c == 2 or c == 4 or c == 6:
            c2 = True
            p = M + 1
        if c == 1 and a > 6 and m >= 1367/2160:
            p = M+2
        if c == 0 and a > 11 and m >= 23269/25920:
            c2 = True
            p = M+1
        p = M

        julian = _datetime.date(A-3760, 3+ april, p)

        d = _datetime.timedelta(days=(A-3760)//100 - 2 - (A-3760)//400)
        gregorian = julian + d
        if (c1 and not c2) or (not c1 and c2):
            gregorian += _datetime.timedelta(days=1)
        return gregorian

    def to_gregorian(self):
        pass


# for i in range(10):
#     d = DateTime(5777+i, 10, 9)
#     print(d.gauss())


# d1 = _date_to_days(5777,6,3)
# c = _date_to_days(3761,4,18)
# d = d1-c
# td = _datetime.timedelta(days=d)
# first = _datetime.date(year=1,day=1,month=1)
# print(first+td)

# for i in range(300):
#     print(_days_to_date(_date_to_days(4777+i,5,26)), (4777+i,5,26))



#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# class Month:
#     def __init__(self, first_day=1, day_num=30, name=None):
#         self.first_day = first_day
#         self.day_num = day_num
#         self.name = name
#
#     def print_month(self):
#         print('         Month:   {}'.format(self.name))
#         print('Sunday{}Monday{}Tuesday{}Wednesday{}Thursday{}Friday{}Saturday'.format(' '*4,' '*4,' '*3,' '*1,' '*2,' '*4,' '*2))
#         for i in range((self.first_day-1)%7):
#             print('          ',end='')
#         for day in range(self.day_num):
#             print(day+1,end=' '*(10-len(str(day+1))))
#             if (day+self.first_day)%7==0:
#                 print()
#         print('\n'*4)
#
# class Year:
#     def __init__(self, year):
#         self.meuberet = _is_meuberet(year)
#         self.day_num = _day_count(year)
#         self.molad = _get_molad(year)
#         self.pesach = _get_pesach(year)
#         self.day_counts = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
#         self.months = ['Tishrei', 'Cheshvan', 'Kislev', 'Tevet',
#                        'Shevat', 'Adar', 'Nissan', 'Iyar', 'Sivan', 'Tammuz', 'Av', 'Elul']
#         if self.meuberet:
#             self.day_counts.insert(5, 30)
#             self.months[5] = 'Adar B'
#             self.months.insert(5, 'Adar A')
#
#         if self.day_num == 353 or self.day_num == 383:
#             self.day_counts[2] -= 1
#         if self.day_num == 355 or self.day_num == 385:
#             self.day_counts[1] += 1
#
#     def print_calendar(self):
#         first = self.molad
#         for i in range(12):
#             m = Month(first,self.day_counts[i],self.months[i])
#             m.print_month()
#             first = (first+m.day_num)%7
#
#
#
#
#
# # y = Year(5779)
# # y.print_calendar()
