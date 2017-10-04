import requests
import argparse
import sys
import os
import platform
import random

BASE_URL = 'https://source.unsplash.com/'
USER_URL = BASE_URL+'user/'
COLLECTION_URL = BASE_URL + 'collection/'

WIDTH = '1440'
HEIGHT = '900'

CATEGORY_LIST = ['nature', 'people']
CATEGORY_NAME = random.choice(CATEGORY_LIST).lower()

WALLPAPER_NAME = ''

def parse_args():
    parser = argparse.ArgumentParser(description = 'arguments of how to change wallpaper')
    subparsers = parser.add_subparsers(help = 'type of photo you want', dest = 'command')
    
    parser_unsplash = subparsers.add_parser('unsplash', description = 'will search for entire unsplash')
    parser_unsplash.add_argument('time',nargs='?',type=str.lower,default=None,choices=['daily','weekly'],help = 'fixed image of the day')
    parser_unsplash.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_unsplash.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')
    

    parser_user = subparsers.add_parser('user')
    parser_user.add_argument('username',type=str,help='username of the user')
    parser_user.add_argument('time',nargs='?',type=str.lower,default=None,choices=['daily','weekly'],help = 'fixed image of the time frame')
    parser_user.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_user.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')

    parser_likes = subparsers.add_parser('likes')
    parser_likes.add_argument('username',type=str,help='username of the user')
    parser_likes.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_likes.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')

    parser_collection = subparsers.add_parser('collection')
    parser_collection.add_argument('collection_id',type=str,help='ID of the collection')
    parser_collection.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_collection.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')

    parser_search_category = subparsers.add_parser('search_category', description = 'subparser to search photo by category', help='search a photo by category')
    parser_search_category.add_argument('category',type=str.lower,nargs='?',default=CATEGORY_NAME,help='name of the category you want to search in')
    parser_search_category.add_argument('-f',action='store_true',default=False,help='filters by searching in curated collections')
    parser_search_category.add_argument('-time',type=str.lower,default='',choices=['daily','weekly'],help='fixed image of the time frame')
    parser_search_category.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_search_category.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')
    parser_search_category.add_argument('-terms',nargs = '+',default='')

    parser_search_size = subparsers.add_parser('search_size', description = 'subparser to search photo by size', help='search a photo by given size')
    parser_search_size.add_argument('-f',action='store_true',default=False,help='filters by searching in curated collections')
    parser_search_size.add_argument('-time',type=str.lower,default='',choices=['daily','weekly'],help='fixed image of the time frame')
    parser_search_size.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_search_size.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')
    parser_search_size.add_argument('-terms',nargs = '+',default='')

    parser_photo = subparsers.add_parser('photo')
    parser_photo.add_argument('photo_id',type=str, help='id of the photo')
    parser_photo.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_photo.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')


    parser.add_argument('-d','--display', type = int, default = 0,
                        help = 'Desktop display number on OS X (0: all displays, 1: main display, etc')
    
    return parser.parse_args()

def get_response(url):
    r = requests.get(url)
    if r.status_code != 200 or r.url == 'https://images.unsplash.com/photo-1446704477871-62a4972035cd?fit=crop&fm=jpg&h=800&q=50&w=1200':
        sys.exit("Couldn't find that photo")
    return r

def name():
    import datetime
    now = datetime.datetime.now()
    return '-'.join(map(str,[now.month,now.day,now.year]))+'_'+'.'.join(map(str,[now.hour, now.minute, now.second]))+'.jpg'

def save_photo(photo_response, filename):
    with open(filename, 'wb') as f:
        for chunk in photo_response:
            f.write(chunk)

def change_wallpaper(save_location, display):
    platform_name = platform.system()
    if platform_name.startswith('Win'):
        #Python 3.x
        if sys.version_info >= (3, 0):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, save_location, 3)
        #Python 2.x
        else:
            ctypes.windll.user32.SystemParametersInfoA(20, 0, save_location, 3)
            
    if platform_name.startswith('Darwin'):
        if display == 0:
            cmd = """
                            osascript -e 'tell application "System Events"
                                set desktopCount to count of desktops
                                repeat with desktopNumber from 1 to desktopCount
                                    tell desktop desktopNumber
                                        set picture to "{save_location}"
                                    end tell
                                end repeat
                            end tell'
                            """.format(save_location=save_location)
        else:
            cmd = """osascript -e 'tell application "System Events"
                                        set desktopCount to count of desktops
                                        tell desktop {display}
                                            set picture to "{save_location}"
                                        end tell
                                    end tell'""".format(display = display, save_location=save_location)
        
        os.system(cmd)

def get_image(url):
    photo_response = get_response(url)
    global WALLPAPER_NAME
    WALLPAPER_NAME = name()
    save_photo(photo_response, WALLPAPER_NAME)

def default():
    get_image(BASE_URL+'featured/'+WIDTH+'x'+HEIGHT+'/?')

def main():
    import time
    s = time.time()
    args = parse_args()
    if args.command is None:
        default()
    if args.command == 'unsplash':
        if args.time is None:
            get_image(BASE_URL+'random/'+args.width+'x'+args.height)
        else:
            get_image(BASE_URL+args.time)
    elif args.command == 'user':
        if args.time is None:
            get_image(USER_URL+args.username+'/'+args.width+'x'+args.height)
        else:
            get_image(USER_URL+args.username+'/'+args.time)
    elif args.command == 'likes':
        get_image(USER_URL+args.username+'/likes/'+args.width+'x'+args.height)
    
    elif args.command == 'collection':
        get_image(COLLECTION_URL+args.collection_id+'/'+args.width+'x'+args.height)
    
    elif args.command == 'search_category':
        if args.f:    
            get_image(BASE_URL+'category/'+args.category+'/featured/'+args.width+'x'+args.height+'/'+args.time+'?'+','.join(args.terms))
        else:
            get_image(BASE_URL+'category/'+args.category+'/'+args.width+'x'+args.height+'/'+args.time+'?'+','.join(args.terms))
    elif args.command == 'search_size':
        if args.f:    
            get_image(BASE_URL+'featured/'+args.width+'x'+args.height+'/'+args.time+'?'+','.join(args.terms))
        else:
            get_image(BASE_URL+'/'+args.width+'x'+args.height+'/'+args.time+'?'+','.join(args.terms))

    elif args.command == 'photo':
        get_image(BASE_URL+args.photo_id+'/'+args.width+'x'+args.height)

    change_wallpaper(os.getcwd()+r'/'+WALLPAPER_NAME, args.display)


if __name__ == '__main__':
    main()