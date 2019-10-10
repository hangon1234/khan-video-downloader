# khan-video-downloader
Simple Python3 script for downloading Khan Academy videos
***
This script is written in Python.

For my personal reason, I need .mp4 files for some topic in Khan Academy.
In Khan Academy's own FAQ, they recommended us to use YouTube downloader to download videos but this is time-consuming and error prone.
This Python code will use Khan Academy's API v1 and recursively find topic and their related videos. You don't need to worry about directory's naming, sequence of video, topics and its sub topics, videos related in each topic.

I am a student and code was written in last few hours, so the code is incomplete and errors are not properly handled. Tomorrow is the end of my annual leave so I have to go back to military service and will be not here for most of the time. (I'm korean and still needs to be there for 6 months 😊)

Since I have no time to revise the code, if someone wants to download Khan Academy's videos into mp4 and knows Python, please improve my code.

Of course, there are some iOS/Android apps that can download videos easily. However, someone might need pure .mp4 files for some cases like me. I can use smartphone/PC only for 3 hours per day. Except for that time, I can only use PMP(Portable Media Player, Windows CE device) to play Khan Academy's videos. Hope that someone find it useful.

# Usage
***
1. Install Python 3 Interpreter (https://www.python.org)
2. Install urllib3 library
```
pip install urllib3
```
3. Download 'khanLectureDownloader.py'
4. Run the script.
```
python khanLectureDownloader.py

Welcome to Khan Academy Lecture Downloader!
Topic slug can be found by looking at URL of each topic
For example, URL of High School Geometry is:
https://www.khanacademy.org/math/geometry
So the topic slug of High School Geometry is 'geometry'
Please input topic slug (ex. 'differential-calculus') : differential-calculus

This topic's title is:
   (0) Differential Calculus

Children topics are following:
   (1) Limits and continuity
   ...
   (6) Parametric equations, polar coordinates, and vector-valued functions

Choose 0 if you want to download all videos for Differential Calculus
Choose 1~6 if you want to continue choose topic you wish

Choose option you wish : 1

This topic's title is:
   (0) Limits and continuity

Children topics are following:
   (1) Limits intro
   (2) Estimating limits from graphs
   ...
   (16) Intermediate value theorem

Choose 0 if you want to download all videos for Limits and continuity
Choose 1~16 if you want to continue choose topic you wish

Choose option you wish : 1
This topic's title is: Limits intro
There are no more following children. Enter to download videos


Folder created: Limits intro
Downloaded as Limits intro/(1) Limits intro.mp4
URL is  https://cdn.kastatic.org/ka-youtube-converted/riXcZT2ICjA.mp4/riXcZT2ICjA.mp4
Succeessfully downloaded

There are no download_urls for this video.
You should check saved 'JSON' file and try to get YouTube link of the video
The file saved at Differential Calculus/(1) Limits and continuity/(15) Limits at infinity/(1) Introduction to limits at infinity.json
Press Enter to continue...

Seems your program is successfully finished!
Press Enter to terminate this program
```
5. Open the folder where you saved khanLectureDownloader.py and you should be able to find videos.
6. If the API response doesn't have proper download_urls, as you noticed the script will pause and let you know where the responed JSON file is. You have to look into that file and find another way to download the video. (There will be YouTube ID, Khan Academy URL, etc)

Enjoy!
