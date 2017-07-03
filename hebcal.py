import math as _math
import datetime as _datetime

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
        molad = 7
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
    def __init__(self, year=5777, month=1, day=1, hour=0, minute=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute




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
        M = int(res)
        m = res - M
        c = (3*A + 5*b + M + 5) % 7
        if c == 2 or c == 4 or c == 6:
            p = M + 1
        if c == 1 and a > 6 and m >= 1367/2160:
            p = M+2
        if c == 0 and a > 11 and m >= 23269/25920:
            p = M+1
        p = M
        if p > 31:
            julian = _datetime.date(A-3760, 4, p-31)
        else:
            julian = _datetime.date(A - 3760, 3, p)
        d = _datetime.timedelta(days=(A-3760)//100 - 2 - (A-3760)//400)
        gregorian = julian + d
        return gregorian




for i in range(10):
    d = DateTime(5777+i, 10, 9)
    print(d.gauss())



















class Month:
    def __init__(self, first_day=1, day_num=30, name=None):
        self.first_day = first_day
        self.day_num = day_num
        self.name = name

    def print_month(self):
        print('         Month:   {}'.format(self.name))
        print('Sunday{}Monday{}Tuesday{}Wednesday{}Thursday{}Friday{}Saturday'.format(' '*4,' '*4,' '*3,' '*1,' '*2,' '*4,' '*2))
        for i in range((self.first_day-1)%7):
            print('          ',end='')
        for day in range(self.day_num):
            print(day+1,end=' '*(10-len(str(day+1))))
            if (day+self.first_day)%7==0:
                print()
        print('\n'*4)

class Year:
    def __init__(self, year):
        self.meuberet = _is_meuberet(year)
        self.day_num = _day_count(year)
        self.molad = _get_molad(year)
        self.pesach = _get_pesach(year)
        self.day_counts = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        self.months = ['Tishrei', 'Cheshvan', 'Kislev', 'Tevet',
                       'Shevat', 'Adar', 'Nissan', 'Iyar', 'Sivan', 'Tammuz', 'Av', 'Elul']
        if self.meuberet:
            self.day_counts.insert(5, 30)
            self.months[5] = 'Adar B'
            self.months.insert(5, 'Adar A')

        if self.day_num == 353 or self.day_num == 383:
            self.day_counts[2] -= 1
        if self.day_num == 355 or self.day_num == 385:
            self.day_counts[1] += 1

    def print_calendar(self):
        first = self.molad
        for i in range(12):
            m = Month(first,self.day_counts[i],self.months[i])
            m.print_month()
            first = (first+m.day_num)%7





# y = Year(5779)
# y.print_calendar()
