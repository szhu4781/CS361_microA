import requests

# Base URL for local microservice
BASE_URL = "https://cs-361-micro-3jmwiqz28-szhu4781s-projects.vercel.app/"

# Upload image case
def upload_image():
    url = f"{BASE_URL}/upload_image"
    image_path = "C:/Users/Shengwei (OSU)/Downloads/google-drive-logo.png"
    try:
        with open(image_path, 'rb') as file:
            files = {'image': file}
            data = {'event_id': 'event123'}

            response = requests.post(url, files=files, data=data)
            print("Status Code:", response.status_code)
            print("Response Content:", response.text)  # Debugging

            if response.status_code == 200:
                try:
                    print("Image uploaded successfully. URL:", response.json().get('image_url'))
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

    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Response Content:", response.text)  # Debugging

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

    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
    print("Response Content:", response.text)  # Debugging

    if response.status_code == 200:
        try:
            print("Image removed successfully.")
        except ValueError:
            print("Error: Server returned non-JSON response.")
    else:
        print("Error removing image:", response.text)

# Run test cases in main
if __name__ == "__main__":
    print("Testing upload image...")
    upload_image()

    print("Testing getting image...")
    get_image()

    print("Testing removing image...")
    remove_image()