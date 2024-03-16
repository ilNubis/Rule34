from urllib.request import Request, urlopen
from timeit import default_timer as timer
import ssl

def loading_bar(current: int, end: int, length: int) -> str:
    slot_potential = end//length
    full_slot = current // slot_potential
    return f"[{'#'*full_slot}>{'-'*(length-full_slot-1)}]" if full_slot != length else f"[{'#'*full_slot}{'-'*(length-full_slot)}]"

def scale_data(data: int) -> tuple[int, str]:
    type_data = "bit"

    # from bit to byte
    if data >= 8:
        data = data / 8
        type_data = "byte"

    # from byte to kilobyte
    if data >= 1024:
        data = data / 1024
        type_data = "kb"

    # from kilobyte to megabyte
    if data >= 1024:
        data = data / 1024
        type_data = "mb"

    # from megabyte to gigabyte
    if data >= 1024:
        data = data / 1024
        type_data = "gb"

    return int(data), type_data

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
context = ssl._create_unverified_context()

def download(filename: str, url: str):
    # Path Manager
    if '/' in filename:
        *path, filename = filename.split('/')
        path = "/".join(path)
    elif '\\' in filename:
        *path, filename = filename.split('\\')
        path = "/".join(path)
    else:
        path = ""

    # Donwload Area
    req = Request(url, headers=headers)
    uopen = urlopen(req, context=context)

    dl_content = 0

    file_size = int(uopen.info()['Content-Length']) # file_size is in bytes

    scale_size, type_data = scale_data(file_size*8)

    print(f'Start downloading: {filename} Size: {scale_size}{type_data}  ') # scale_data richiede il dato in Bit

    # Create/Write File
    with open(f'{filename}', 'wb') as f:
        download_speed = 10

        while dl_content != file_size:
            # Manage for a maximum download speed
            start = timer()
            buffer = uopen.read(int(download_speed))
            end = timer()

            # Calculate max speed on a second
            download_speed = download_speed//(end - start)

            # Manage error
            if download_speed > file_size:
                download_speed = 10

            # Manage for ultimate part of file
            if file_size - dl_content <= download_speed:
                download_speed = file_size - dl_content

            # Esclude None content
            if buffer:
                # Count downloaded Byte
                dl_content += len(buffer)
                # Write buffer on file
                f.write(buffer)
                yield file_size, dl_content, download_speed

if __name__ == "__main__":
    for file_size, dl_content, download_speed in download(filename="test.mp4", url="https://clips-media-assets2.twitch.tv/AvtQo2sZJ_eqgEafqgTOfA/39560787301-offset-3740.mp4"):
        download_speed, type_data = scale_data(download_speed*8)
        print(f'Downloaded: {loading_bar(dl_content, file_size, 20)} {dl_content//(file_size//100)}% Speed: {download_speed} {type_data}/s     ', end='\r')
