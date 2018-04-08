
def pretty_time_delta(seconds):
    sign_string = '-' if seconds < 0 else ''
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '{0}д. {1}ч. {2}м.'.format(days, hours, minutes)
    elif hours > 0:
        return '{0}ч. {1}м.'.format(hours, minutes)
    elif minutes > 0:
        return '{0}м.'.format(minutes)
    else:
        return '{0}с.'.format(seconds)