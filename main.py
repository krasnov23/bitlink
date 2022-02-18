from dotenv import load_dotenv
import requests
import os
from urllib.parse import urlparse
import argparse
load_dotenv()

parser = argparse.ArgumentParser(description='Get bitlink and its amount clicks')
parser.add_argument('link',help='Insert and check link')
args = parser.parse_args()

AUTH_TOKEN = {
    "Authorization": os.getenv("BITLY_TOKEN")
}

def check_bitlink(user_input):
    user_input_parse = urlparse(user_input)
    input_cut = user_input_parse.netloc + user_input_parse.path
    body = f'https://api-ssl.bitly.com/v4/bitlinks/{input_cut}'
    response = requests.get(body,headers=AUTH_TOKEN)
    response.raise_for_status()
    return input_cut


def count_click_link(user_input):
    parameters = {
        "units": -1
    }
    user_input_parse = urlparse(user_input)
    input_cut = user_input_parse.netloc + user_input_parse.path
    count_click_apilink = f'https://api-ssl.bitly.com/v4/bitlinks/{input_cut}/clicks/summary'
    response_amount_click = requests.get(count_click_apilink, params=parameters, headers=AUTH_TOKEN)
    response_amount_click.raise_for_status()
    total_clicks = response_amount_click.json()['total_clicks']
    return total_clicks



def shorten_link(url):
    json_parameters = {"long_url": url}
    make_shortlink = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(make_shortlink,json=json_parameters,headers = AUTH_TOKEN)
    response.raise_for_status()
    short_link = response.json()['link']
    return short_link


if __name__ == '__main__':
    user_input = args.link
    try:
        check_bitlink(user_input)
    except requests.exceptions.HTTPError:
        try:
            print(shorten_link(user_input))
        except requests.exceptions.HTTPError:
            print('Incorrect Insert')
    else:
        try:
          print(count_click_link(user_input))
        except requests.exceptions.HTTPError:
          print('No connection with server')
