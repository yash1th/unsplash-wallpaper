'''testing name function'''
import datetime
from unsplash_wallpaper import name

def test_name():
    '''test whether the name returned is as expected or not'''
    now = datetime.datetime.now()
    assert name() == '-'.join(map(str, [now.month, now.day, now.year]))+'_'+'.'.join(map(str, [now.hour, now.minute, now.second]))+'.jpg'
    