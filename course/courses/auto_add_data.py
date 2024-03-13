import googleapiclient.discovery
from .models import CourseSection, Course

def get_playlist_videos(playlist_id):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyAGYAvoPAdYqdAX4BnFt5LBJGwq6nJg7e0"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    # Request playlist items
    request = youtube.playlistItems().list(
        part="contentDetails,snippet",  # Include snippet part to get video titles
        playlistId=playlist_id,
        maxResults=50  # Maximum number of results per request, adjust as needed
    )
    response = request.execute()

    videos_info = [(item['contentDetails']['videoId'], item['snippet']['title']) for item in response['items']]

    return videos_info

def generate_embedded_links(videos_info):
    embedded_links = [f"https://www.youtube.com/embed/{video_id}" for video_id, _ in videos_info]
    return embedded_links

def main():
    playlist_id = "PLZPZq0r_RZOMQArzyI32mVndGBZ3D99XQ"
    videos_info = get_playlist_videos(playlist_id)
    embedded_links = generate_embedded_links(videos_info)
    
    course_id = Course.objects.get(pk=1)
    for video_info, embedded_link in zip(videos_info, embedded_links):
        video_id, video_title = video_info
        try:
            obj = CourseSection.objects.create(course=course_id, section=video_title, pointer=embedded_link)
            print(obj)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()

#just use this in shell. import lil by lil