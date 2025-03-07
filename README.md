# CS361 Microservice A: Image Upload, Retreival, and Removal Service

**Author**: Shengwei Zhu <br>
**Designed for**: JinHui Zhen

This microservice allows users to upload, retreive, and remove images associated with events. It is hosted on Vercel and uses Rest API to communicate over HTTP. Responses for requests will be in JSON format.

## Communication Contract

**Base URL:** https://cs-361-micro-a.vercel.app/ <br>
Note: Accessing root URL in Vercel will return a 404 error since there's no route defined for it. This should not have any overall impact on the main program.

### Instructions

To interact with the microservice, your program must send HTTP requests to the appropriate endpoints.

1. Clone repository into your project folder
   ```
    git clone https://github.com/szhu4781/CS361_microA.git
    cd project_folder
   ```
2. Install dependencies
   ```
    pip install -r requirements.txt
   ```
3. Start the app
   ```
    python index.py
   ```

#### Endpoints
**Image Upload** <br>
* Method: POST <br>
* URL: /upload_image <br>
* Parameters: event_id - Unique identifier for the event; image - Image file to upload <br>
> Example Request using Python: <br>
```index.py
  import requests

  url = "https://cs-361-micro-a.vercel.app/upload_image"
  files = {'image': open('path/to/image.png', 'rb')}
  data = {'event_id': 'event123'}
  response = requests.post(url, files=files, data=data)
  print(response.json())
```
> Expected Response: 
```
{
"image_url": "https://cs-361-micro-a.vercel.app/get_image?event_id=event123"
}
```

**Retreive Image** <br>
* Method: GET <br>
* URL: /get_image <br>
* Parameters: event_id - Unique identifier for the event <br>
> Example Request using Python: <br>
```index.py
  import requests

  url = "https://cs-361-micro-a.vercel.app/get_image"
  params = {'event_id': 'event123'}
  response = requests.post(url, params=params)
  print(response.json())
```
> Expected Response: <br>
```
{ 
  "image_url": "https://cs-361-micro-a.vercel.app/get_image?event_id=event123"
} 
```

**Remove Image** <br>
* Method: POST <br>
* URL: /remove_image <br>
* Parameters: event_id - Unique identifier for the event <br>
> Example Request using Python: <br>
```index.py
  import requests

  url = "https://cs-361-micro-a.vercel.app/remove_image"
  data = {'event_id': 'event123'}
  response = requests.post(url, data=data)
  print(response.json())
```
> Expected Response: <br>
```
{
  "message": "Image removed successfully"
}
```

## UML Diagram

![Flowchart](https://github.com/user-attachments/assets/a8cd150b-ccf4-4831-818d-c4ff85b167ad)

