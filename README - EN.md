# You need to write a programm which will copy photos from vk.com to cloud storage on Yandex.disc

## Requirements:
1. Get photos using REST API [photos.get](https://vk.com/dev/photos.get).
2. Save max size pictures (width/height in px) on Yandex.disc.
3. For photo name you shoud use quantity of likes, if quantity of likes are the same, upload date should be added to the name.  
4. All info should be stored in json file.
5. Create new folder for the pictures.
6. Save any amount of pictures (default 5).
7. Progress bar for tracking the progress of the programm.

### Input:
1. user id vk.com;
2. token for Yandex.disc (https://yandex.ru/dev/disk/poligon/).

### Output:
1. json-file:
```javascript
    [{
    "file_name": "34.jpg",
    "size": "z"
    }]
```

![](result.gif)

