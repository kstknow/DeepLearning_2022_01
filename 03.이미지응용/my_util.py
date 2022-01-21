from sre_constants import FAILURE, SUCCESS
import urllib3, json, base64, requests
import matplotlib as mpl
from PIL import Image , ImageDraw, ImageFont
import matplotlib.pyplot as plt
RESPONSE_OK = 200



def detect_image(img_file, return_file):
    with open('API_KEY.txt') as f:
        ai_key = f.read()

    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
    http = urllib3.PoolManager() # 프로그램 안에서 한번만 실행하면 됨
    img_type = img_file.split('.')[-1]
    img_type = 'jpg' if img_type == 'jfif' else img_type
    with open(img_file, "rb") as file: 
        img_contents = base64.b64encode(file.read()).decode("utf8")  
        
        request_json = {
            "access_key": ai_key,
            "argument": {
                "type": img_type,
                "file": img_contents
            }
        }
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(request_json)
        )
        if response.status != RESPONSE_OK:
            return FAILURE

        result = json.loads(response.data)
        obj_list = result['return_object']['data']
        img = Image.open(img_file)
        draw = ImageDraw.Draw(img)
        for obj in obj_list:
            name = obj['class']
            x = int(obj['x'])
            y = int(obj['y'])
            w = int(obj['width'])
            h = int(obj['height'])
            draw.rectangle(((x, y), (x+w, y+h)), outline=(255,0,0), width=2)
            draw.text((x+10, y-20), name, font=ImageFont.truetype('malgun.ttf',20), fill=(0,0,255))


        img.save(return_file)
        return SUCCESS