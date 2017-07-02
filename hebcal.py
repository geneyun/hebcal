import math

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
        self.days = day_count(year)
        self.molad = get_molad(year)
        self.pesach = get_pesach(year)

    def print_calendar(self):
        if not self.meuberet:
            month_names = ['t','h','c','t','s','a','n','i','s','t','a','e']
            month_days = [30,29,30,29,30,29,30,29,30,29,30,29]
            if self.days==353:
                month_days[2] = 29
            if self.days==355:
                month_days[1] = 30
            first = self.molad
            for i in range(12):
                m = Month(first,month_days[i],month_names[i])
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
    return (get_molad(year+1)-2)%7

def print_year_info(year):
    print(get_molad(year))
    print(is_meuberet(year))
    print(day_count(year))
    print(get_pesach(year))
