import os
import time


def format_file_size(size):

    for unit in ['B','KB','MB', 'GB', "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

def get_file_type(filename):

    extension = filename.split('.')[-1].lower()

    image_types = [
        'png',
        'jpg',
        'jpeg',
        'gif',
        'webp'
    ]

    video_types = [
        'mp4',
        'webm',
        'ogg'
    ]

    pdf_types = ['pdf']

    text_types = [
        'txt',
        'py',
        'js',
        'html',
        'css',
        'json'
    ]

    if extension in image_types:
        return 'image'

    elif extension in video_types:
        return 'video'

    elif extension in pdf_types:
        return 'pdf'

    elif extension in text_types:
        return 'text'

    return 'other'

def get_file_data(shared_folder):
    file_data=[]
    for file in os.listdir(shared_folder):
        path = os.path.join(shared_folder, file)
        if os.path.isfile(path):
            size = os.path.getsize(path)
            file_data.append({
                'id': file.split('_',1)[0],
                'name': file.split('_',1)[1],
                'stored_name': file,
                'size': format_file_size(size),
                'type': get_file_type(file.split('_',1)[1])
            })
    return file_data

def detect_device(user_agent):

    ua = user_agent.lower()

    if 'iphone' in ua:
        return 'iPhone'

    elif 'android' in ua:
        return 'Android'

    elif 'windows' in ua:
        return 'Windows'

    elif 'linux' in ua:
        return 'Linux'

    return 'Unknown'


# def cleanup_expired_files(shared_folder, file_expiry):

#     current = time.time()

#     expired = []

#     for file, expiry in file_expiry.items():

#         if current > expiry:

#             expired.append(file)

#     for file in expired:

#         path = os.path.join(
#             shared_folder,
#             file
#         )

#         if os.path.exists(path):

#             os.remove(path)

#         del file_expiry[file]