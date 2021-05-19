import urllib.request
import re


def GetVidId(query):
    query = str(query)
    A = query.replace(" ", "+")
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={A}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v="+ video_ids[0]


