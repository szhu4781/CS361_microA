import requests
import time

# Base URL for Vercel-hosted microservice
BASE_URL = "https://cs-361-micro-a.vercel.app/"

# Upload image case
def upload_image():
    url = f"{BASE_URL}/upload_image"

    # Image path is hard-coded for testing purposes
    image_path = "C:/Users/Shengwei (OSU)/Downloads/google-drive-logo.png"

    # Attempt to open file path to locate image
    try:
        with open(image_path, 'rb') as file:
            files = {'image': file}
            data = {'event_id': 'event123'}

            # If the image exists, send its url, file, and event_id 
            # to the server to find it
            response = requests.post(url, files=files, data=data)

            # Return the status code
            print("Status Code:", response.status_code)
            print("Response Content:", response.text)

            # 200 means the operation was succesful, else return something like 404
            if response.status_code == 200:
                try:
                    print("Operation successfully. URL:", response.json().get('image_url'))
                except ValueError:
                    print("Error: Server returned non-JSON response.")
            else:
                print(f"Error uploading image: Status code {response.status_code}")
    
    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

# Get image case
def get_image():
    event_id = 'event123'
    url = f"{BASE_URL}/get_image?event_id={event_id}"

    # Fetch the url
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Response Content:", response.text) 

    if response.status_code == 200:
        try:
            print("Image found. URL:", response.json().get('image_url'))
        except ValueError:
            print("Error: Server returned non-JSON response.")
    else:
        print("Error retrieving data:", response.text)

# Remove image case
def remove_image():
    url = f"{BASE_URL}/remove_image"
    data = {'event_id': 'event123'}

    # Sends the data to the server to remove the image
    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
    print("Response Content:", response.text) 

    if response.status_code == 200:
        try:
            print("Image removed successfully.")
        except ValueError:
            print("Error: Server returned non-JSON response.")
    else:
        print("Error removing image:", response.text)

# Run test cases in main
if __name__ == "__main__":
    print("Testing upload image...\n")
    upload_image()
    time.sleep(10)

    print("Testing getting image...\n")
    get_image()
    time.sleep(10)

    print("Testing removing image...\n")
    remove_image()
    time.sleep(10)