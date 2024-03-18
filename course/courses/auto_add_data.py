import googleapiclient.discovery
from courses.models import CourseSection, Course

def get_playlist_videos(playlist_id):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyAGYAvoPAdYqdAX4BnFt5LBJGwq6nJg7e0"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    videos_info = []
    next_page_token = None

    # Loop until all pages are fetched
    while True:
        # Request playlist items with optional page token
        request = youtube.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=playlist_id,
            maxResults=50,  # Set your desired maximum results per page
            pageToken=next_page_token
        )
        response = request.execute()

        # Append video info from current page
        videos_info.extend([(item['contentDetails']['videoId'], item['snippet']['title']) for item in response['items']])

        # Check if there are more pages
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break  # No more pages to fetch

    return videos_info

def generate_embedded_links(videos_info):
    embedded_links = [f"https://www.youtube.com/embed/{video_id}" for video_id, _ in videos_info]
    return embedded_links

def main(playlist_id, course_id):
    videos_info = get_playlist_videos(playlist_id)
    embedded_links = generate_embedded_links(videos_info)
    
    course = Course.objects.get(pk=course_id)
    for video_info, embedded_link in zip(videos_info, embedded_links):
        video_id, video_title = video_info
        try:
            obj = CourseSection.objects.create(course=course, section=video_title, pointer=embedded_link)
            print(obj)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()