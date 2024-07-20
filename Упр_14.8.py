bday = int(input('Введите день:'))
bmonth = int(input('Введите месяц:'))
byear = int(input('Введите год:'))
# bday=1
# bmonth=1
# byear=2000
delta = int(input('Введите количество дней:'))
delta_year_cel=delta//365
delta_year_ost = delta%365
delta_month_cel=delta_year_ost//30
delta_day=delta_year_ost%30
print(delta_year_cel,delta_month_cel,delta_day)
new_byear = byear+delta_year_cel
new_bmonth = bmonth+delta_month_cel
if new_bmonth>12:
    x=new_bmonth//12
    y=new_bmonth%12
    new_byear = new_byear+x
    new_bmonth=new_bmonth-12+y
new_bday = bday+delta_day
if new_bday>30:
    x=new_bday//30
    y=new_bday%30
    new_bday=new_bday-30+y
print('Ваш ', delta, '-ный день жизни будет', '{:02d}'.format(new_bday),'.','{:02d}'.format(new_bmonth), '.', '{:04d}'.format(new_byear))
