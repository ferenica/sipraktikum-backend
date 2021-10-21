import datetime


def parse_time_custom(datetime_inp):
    '''
    CUSTOM PARSER FOR TIME DD-MM-YY hh:mm
    '''
    return datetime.strptime(datetime_inp, '%d-%m-%Y %H:%M')
