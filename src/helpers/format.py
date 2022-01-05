import datetime

def returnFormat(message:str='', data:dict={}, status:int=200) -> tuple:
    return {
        'message': message,
        'data': data
    }, status

def toCsv(labels:list, data:list):
    csv = ', '.join(labels) + '\n'
    for row in data:
        csv_row = ', '.join(row) + '\n'
        csv+=csv_row
    return csv


def folioFormat(date:datetime, number:int, name:str, first_lastname:str = '', second_lastnmae:str = '') -> str:
    year = twoDigitFormat(date.year)
    month = twoDigitFormat(date.month)
    day = twoDigitFormat(date.day)
    count = twoDigitFormat(number)
    name_initials = getInitials(name)
    first_lastname_initials = getInitials(first_lastname)
    second_lastnmae_initials = getInitials(second_lastnmae)

    return day + month + year + count + name_initials + first_lastname_initials + second_lastnmae_initials

def twoDigitFormat(number:int) -> str:
    if number >= 10:
        return str(number)[-2:]
    else:
        return str(0) + str(number)[-2:]

def getInitials(name:str) -> str:
    names = name.split(' ')
    initials = ''
    for n in names:
        initials += n[0].upper()
    return initials

