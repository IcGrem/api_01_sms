import time, os, requests
from twilio.rest import Client
from dotenv import load_dotenv 
load_dotenv()


def get_status(user_id):
    user_id = int(user_id)
    params = {
        'user_ids':user_id,
        'fields':'online',
        'v':'5.92',
        'access_token':os.getenv("VK_AUTH_TOKEN")
    }
    r = requests.post(url = 'https://api.vk.com/method/users.get', params = params).json()
    user_status = r.get("response")[0].get("online")
    return user_status


def sms_sender(sms_text):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=os.getenv("NUMBER_TO"),
        from_=os.getenv("NUMBER_FROM"),
        body=sms_text
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
