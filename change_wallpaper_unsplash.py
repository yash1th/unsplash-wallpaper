
import requests
import argparse
import sys
import os
import platform

BASE_URL = 'https://source.unsplash.com/'
USER_URL = BASE_URL+'user/'
COLLECTION_URL = BASE_URL + 'collection/'

WIDTH = '1600'
HEIGHT = '900'

def parse_args():
    parser = argparse.ArgumentParser(description = 'arguments of how to change wallpaper')
    subparsers = parser.add_subparsers(help = 'type of photo you want', dest = 'command')
    
    parser_unsplash = subparsers.add_parser('unsplash', description = 'will search for entire unsplash')
    parser_unsplash.add_argument('time',nargs='?',type=str.lower,default=None,choices=['daily','weekly'],help = 'fixed image of the day')
    parser_unsplash.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_unsplash.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')
    

    parser_user = subparsers.add_parser('user')
    parser_user.add_argument('username',type=str,help='username of the user')
    parser_user.add_argument('time',nargs='?',type=str.lower,default=None,choices=['daily','weekly'],help = 'fixed image of the day')
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

    parser_search = subparsers.add_parser('search')
    parser_search.add_argument('--category',type=str.lower,default='',help='searches full database by a category')
    parser_search.add_argument('-f',action='store_true',default=False,help='filters by searching in curated collections')
    parser_search.add_argument('-terms',nargs = '+',default='')

    parser_photo = subparsers.add_parser('photo')
    parser_photo.add_argument('photo_id',type=str, help='id of the photo')
    parser_photo.add_argument('-w','--width',type = str,default = WIDTH, help = 'width of the photo you need')
    parser_photo.add_argument('-e','--height',type = str,default = HEIGHT, help = 'height of the photo you need')


    parser.add_argument('-d','--display', type = int, default = 0,
                        help = 'Desktop display number on OS X (0: all displays, 1: main display, etc')
    # #parser.add_argument('-t','--time', type=str.lower, default='daily', choices = ['daily','weekly'], help = 'time period')
    return parser.parse_args()

def get_response(url):
    r = requests.get(url)
    if r.status_code != 200 or r.url == 'https://images.unsplash.com/photo-1446704477871-62a4972035cd?fit=crop&fm=jpg&h=800&q=50&w=1200':
        sys.exit("Couldn't find that photo")
    return r

def save_photo(photo_response):
    with open('wallpaper.jpg', 'wb') as f:
        for chunk in photo_response:
            f.write(chunk)

def change_wallpaper(save_location, display):
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
    print('url = ',url)
    #sys.exit()
    photo_response = get_response(url)
    save_photo(photo_response)

def main():
    args = parse_args()
    print(args)
    #sys.exit('exiting main')
    if args.command == 'unsplash':
        if args.time is None:
            get_image(BASE_URL+'random/'+args.width+'x'+args.height)
        else:
            get_image(BASE_URL+args.time)
    elif args.command == 'user':
        print('user parser is called')
        if args.time is None:
            get_image(USER_URL+args.username+'/'+args.width+'x'+args.height)
        else:
            get_image(USER_URL+args.username+'/'+args.time)
    elif args.command == 'likes':
        print('likes parser is called')
        get_image(USER_URL+args.username+'/likes/'+args.width+'x'+args.height)
    
    elif args.command == 'collection':
        print('collection parser is called')
        get_image(COLLECTION_URL+args.collection_id+'/'+args.width+'x'+args.height)
    
    elif args.command == 'search':
        print('search parser is called')
        if args.category:
            url = BASE_URL+'category/'+args.category+'/'
        else:
            url = BASE_URL
        if args.f:
            url += 'featured/'
        get_image(url+'?'+','.join(args.terms))
            #BASE_URL+'category/'+args.category+'/?'+','.join(args.terms)

            
            #get_image(BASE_URL+args.width+'x'+args.height)
            #https://source.unsplash.com/featured/1600x900/?nature,water -- working
            #https://source.unsplash.com/category/buildings/featured/1600x900/?montreal -- working


    elif args.command == 'photo':
        print('photo parser is called')
        get_image(BASE_URL+args.photo_id+'/'+args.width+'x'+args.height)

    sys.exit()
    os.system('open wallpaper.jpg')
    #change_wallpaper(os.getcwd()+r'/wallpaper.jpg', args.display)
    
if __name__ == '__main__':
    main()
