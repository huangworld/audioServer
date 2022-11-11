# AudioServer

This is a simple audio server with a few APIs.

## List of APIs
1) /: home page, renders a menu of actions
2) /upload: uploads a .wav audio file to the server
3) /download?name=myfile.wav: retrieves the audio file specified by name
4) /list?maxduration=val: gives a list of audio files whose metadata satisfies the query parameter. The retuned value is a list of JSON objects. Currently only the duration of the audio file is kept as the metadata and only maxduration is supported in /list.
5) /info?name=myFile.wav: displays the metadata of the audio file indicated by the name.

## How to run it with a simple front end.
1) Clone this repository
2) Go to the local directory containing the server
3) Run pip install -r requirements.txt to make sure the packages are installed
3.5) Run pip install SoundFile or pip3 install SoundFile
4) Run python3 audioServer.py
5) Go to http://localhost:5000/ in browser 

## Here are some design choices for reference:
1) Every time we stop the server and run again (Reboot), it cleans the uploads folder. Here is why: currently whether a file already exists is checked by looking in a global variable containing all the metadata. This global variable is cleared when the server reboots however the actual files in the uploads folder are not cleared. This may lead to a discrepancy about states of the server.
2) For simplicity, we restrict allowed extension types to only .wav, but it can be easily extended to other types such as .mp3.
3) Secure path is used to prevent user passes adversarial filenames.

## Future improvements:
1) Incorporate other key APIs such as /delete
2) More interactive ui: /list now displays stringified list of json objects, I wish to display each audio as a clickable item that goes to the display mode when it’s clicked.
3) More robust robooting behavior to avoid losing all stored files when the server restarts (which is inevitable). I can potentially read in the uploads folder and load its information into the global variable (metadata) during the reboot process.
4) Currently it uses memory to store audio files and metadata. When it scale up, databases is needed. Since both the data and metadata would have defined schemas, we can use relational database (i.e. mySQL) to store both the data and metadata for ACID compliance. They can be further partitioned for better scalability in the future.
5) Currently every one has both read and write access for any audio file on the server. In the future, we can ask users to sign in to their account and send a token (cookie session) to each request to the server. Therefore, the server can check this user's permissions and validate each request.
6) Depending on users' use patterns, we can introduce caching. If a user always plays the audio right after uploading, we can cache it to avoid one lookup in the database.
7) Rate limiting: For each user or ip address, we can set an upper limit of the number of requests per minute to avoid potential ddos attacks.
