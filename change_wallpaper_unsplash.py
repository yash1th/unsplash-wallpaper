import requests
import argparse
import sys
import os
import platform

BASE_URL = 'https://source.unsplash.com/'
USER_URL = BASE_URL+'user/'
COLLECTION_URL = BASE_URL + 'collection/'

def parse_args():
    parser = argparse.ArgumentParser(description = 'arguments of how to change wallpaper')
    parser.add_argument('-d','--display', type = int, default = 0,
                        help = 'Desktop display number on OS X (0: all displays, 1: main display, etc') 
    subparsers = parser.add_subparsers(help = 'mode of result fixed or random or photo_id', dest = 'command')
    parser_random = subparsers.add_parser('random')
    parser_random.add_argument('A',type = str)

    parser_fixed = subparsers.add_parser('fixed')
    #parser_fixed.add_argument('-t','--time', type = str.lower, choices = ['daily','weekly'], help = 'time period')


    parser_specific_photo = subparsers.add_parser('specific_photo')
    parser_specific_photo.add_argument('photo_id',type = str, help = 'id of the photo')
    parser_specific_photo.add_argument('-w','--width',type = str, default = '1600',help = 'width of the photo you need')
    parser_specific_photo.add_argument('-e','--height',type = str, default = '900',help = 'height of the photo you need')
    return parser.parse_args()

def random_image():
    pass

def debug_request(r):
    print('status code = ',r.status_code)
    print('url = ',r.url)
    print('type of r = ',type(r.content))

def get_response(url):
    r = requests.get(url)
    if r.status_code != 200 or r.url == 'https://images.unsplash.com/photo-1446704477871-62a4972035cd?fit=crop&fm=jpg&h=800&q=50&w=1200':
        sys.exit("Couldn't find that photo")
    return r

def specific_photo(photo_id, display, width = '1600', height = '900'):
    photo_response = get_response(BASE_URL+photo_id+'/'+width+'x'+height)
    save_photo(photo_response)
    change_wallpaper(os.getcwd()+r'/wallpaper.jpg', display)

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

def main():
    args = parse_args()
    #print(args)
    if args.command == 'specific_photo':
        specific_photo(args.photo_id, args.display, width = args.width, height = args.height)

if __name__ == '__main__':
    main()
