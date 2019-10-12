# Author : Kim Hangon (Daniel, 金漢坤)
# Khan academy video downloader
# No copyright, freely use and modify code

import urllib3
import json
import pprint
import os

SERVER_URL = "https://www.khanacademy.org"
HTTP = urllib3.PoolManager()

# This function will return API request result
def request_topic_slug(topic_slug):
    response = HTTP.request("GET", SERVER_URL + '/api/v1/topic/' + topic_slug)
    json_object = json.loads(response.data.decode("utf-8"))
    return(json_object)

# Check type of children nodes
# Return True if it can recusively go to another topic
# Return False if is not
def check_children_kind(json_object):
    for i in range(len(json_object['children'])):
        if json_object['children'][i]['kind'] != 'Topic':
            return False
        else:
            return True
    return True

def filter_invalid_char(string):
    # Simple function to filter Windows' invalid filename characters
    for invalid_char in ['<', '>', ':', "\\", "|", "/", "?", "*", '"']:
        if string.find(invalid_char) is not -1:
            string = string.replace(invalid_char, '')
    return string
    
def create_folder(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        # Notify to user and ignore existing folder
        print("Folder\t{}\tis already exists".format(path))
    print("\nFolder created: {}".format(path))
    return
    
def download_video(name, path, index, url):
    name = "({}) {}".format(index, name)
    path = path + '/' + name + '.mp4'
    
    # Ignore if the file is already exists
    if os.path.isfile(path):
        print("File {} is exist, and ignored".format(path))
        return
   
    # Download and save the video
    print("Downloaded as {}\nURL is\t{}".format(path, url))
    request = HTTP.request("GET", url)
    open(path, 'wb').write(request.data)
    print("Succeessfully downloaded\n")
    return

# When KeyError raised, (no .mp4 link for the video)
# We will save JSON file as a name of the lecture
# So the user can manually download it from YouTube
def write_json(json_video, path, index):
    path = path + "/({}) {}.json".format(index, json_video['title'])
    open(path, 'w').write(pprint.pformat(json_video))
    print("\nThere are no download_urls for this video." +
    "\nYou should check saved 'JSON' file and try to get YouTube link of the video" +
    "\nThe file saved at {}".format(path))
    input("Press Enter to continue...")

# Recursively check for all children videos
# If no videos for a topic, than just make a folder
# and recursively continue to topic's children
def find_all_sub_videos(json_object, path):
    #Get Topic's JSON
    response = HTTP.request("GET", SERVER_URL + 
    '/api/v1/topic/{}'.format(json_object['node_slug']))
    json_object = json.loads(response.data.decode("utf-8"))
    
    # Get all video URLs for topic
    response = HTTP.request("GET", SERVER_URL + 
    '/api/v1/topic/{}/videos'.format(json_object['node_slug']))
    json_videos = json.loads(response.data.decode("utf-8"))
    
    # Create the folder
    create_folder(path)
    
    # Filter invalid title
    json_object['title'] = filter_invalid_char(json_object['title'])
    
    # If there are any videos for topic, download it
    for index, json_video in enumerate(json_videos, 1):
        json_video['title'] = filter_invalid_char(json_video['title'])
        try:
            download_video(json_video['title'], path, index, json_video['download_urls']['mp4'])
        except KeyError:
            write_json(json_video, path, index)
        
    if check_children_kind(json_object) is True:
        for index, json_object in enumerate(json_object['children'], 1):
            json_object['title'] = filter_invalid_char(json_object['title'])
            newpath = path + "/(" + str(index) + ") " + json_object['title']
            find_all_sub_videos(json_object, newpath.strip())
    
def show_and_select(json_object):
    # Check if kind of children is not a 'Topic'
    # If true, than download its videos
    if check_children_kind(json_object) is False:
        print("This topic's title is: {}".format(json_object['title']))
        print("There are no more following children. Enter to download videos")
        input()
        find_all_sub_videos(json_object, json_object['title'])
        return
    
    # If there are children kind of topic
    # than should ask if use wants to download all sub-topics
    # or continue to move sub-topic
    if len(json_object['children']) is not 0:
        print("\nThis topic's title is:\n   (0) {}\n\nChildren topics are following:".format(json_object['title']))
        for i in range(len(json_object['children'])):
            print("   ({}) {}".format(str(i+1), json_object['children'][i]['title']))
        print("\nChoose 0 if you want to download all videos for {}".format(json_object['title']))
        print("Choose 1~{} if you want to continue choose topic you wish".format(str(len(json_object['children']))))
        choice = int(input('\nChoose option you wish : '))
        if choice is 0:
            find_all_sub_videos(json_object, json_object['title'])
        else:
            show_and_select(request_topic_slug(json_object['children'][choice-1]['node_slug']))

def main():
    # Usage introduction
    print("\nWelcome to Khan Academy Lecture Downloader!")
    print("Topic slug can be found by looking at URL of each topic")
    print("For example, URL of High School Geometry is:")
    print("""https://www.khanacademy.org/math/geometry""")
    print("So the topic slug of High School Geometry is 'geometry'")
    topic_slug = input("Please input topic slug (ex. 'differential-calculus') : ")
    json_object = request_topic_slug(topic_slug)
    show_and_select(json_object)
    # Done
    input("Seems your program is successfully finished!\nPress Enter to terminate this program")
    
if __name__ == "__main__":
    main()
