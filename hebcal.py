import math as _math


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







td = TimeDelta(weeks=3, days=56)
td2 = TimeDelta(days=5, hours=2)
print(td)
print(td2)
print(td+td2)




















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
        self.meuberet = is_meuberet(year)
        self.day_num = day_count(year)
        self.molad = get_molad(year)
        self.pesach = get_pesach(year)
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



def get_molad(year):
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
    elif not is_meuberet(year) and 3.38287 < molad < 3.75:
        molad = 5

    # btu-takpat
    elif not is_meuberet(year) and is_meuberet(year - 1) and 2.64772 < molad < 2.75:
        molad = 3

    else:
        molad = int(molad)

    return molad


def is_meuberet(year):
    a = year % 19
    m = [0, 3, 6, 8, 11, 14, 17]
    return a in m


def day_count(year):
    current_molad = get_molad(year)
    next_molad = get_molad(year + 1)

    if is_meuberet(year):
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

def get_pesach(year):
    return (get_molad(year + 1) - 2) % 7

def print_year_info(year):
    print(get_molad(year))
    print(is_meuberet(year))
    print(day_count(year))
    print(get_pesach(year))

# y = Year(5779)
# y.print_calendar()
