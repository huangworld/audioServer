import requests
BASE = "http://127.0.0.1:5000/"
TEST_AUDIO = "test/audios/"
with open(TEST_AUDIO + "CantinaBand3.wav", 'rb') as file:
    data = {'uuid': ''}
    files = {'file': file}
    response = requests.post(BASE + "upload", files=files, json=data)
    print(response)
# input()
# response = requests.get(BASE + "video/2")
# print(response.json())