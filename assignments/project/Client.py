import requests
import os

def send_data_to_server(request, image_path):
    
    url = 'http://127.0.0.1:5000/'
    test_url = url + 'imageProcessor'

    headers = {"Accept":"*/*"}
    payload = {'requests' : request}

    image_filename = os.path.basename(image_path)
    multipart_form_data = {
        'file': (image_filename, open(image_path, 'rb'))
    }
 
    response = requests.post(test_url, headers=headers, files=multipart_form_data, data=payload)
    
    if response.status_code != 200:
        print('Status:', response.status_code)
        exit()
    print(response.status_code)
    print('Content-Type: ', response.headers['Content-Type'])  
    print('Date: ', response.headers['Date'])  

if __name__ == '__main__':
    send_data_to_server("flip_h,rotate_360,grayscale,w_400,h_500,rotate_left", "Images/test_image.jpeg")
