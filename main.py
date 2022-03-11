import os
import requests
import datetime
from tqdm import tqdm
from time import sleep
from pprint import pprint


def get_token_vk():
    with open(os.path.join(os.getcwd(), 'token_VK.txt'), 'r') as file:
        token = file.read().strip()
        return token


def get_token_yandex():
    with open(os.path.join(os.getcwd(), 'token_YaDisc.txt'), 'r') as file_object:
        token_ya = file_object.read().strip()
        return token_ya


class VkUser:

    def __init__(self, token, version='5.131'):
        self.token = get_token_vk()
        self.id = vk_id
        self.version = version
        self.base_params = {'access_token': self.token,
                            'v': self.version}
        self.json, self.export_dict = self.get_output()

    def get_photo(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1,
                  'count': photo_qty,
                  'fields': 'screen_name'}
        response = requests.get(url, params={**self.base_params, **params}).json()['response']
        return response['count'], response['items']

    def get_largest_photo(self, dict_response):
        largest_photo = 0
        for each in range(len(dict_response)):
            photo_size = dict_response[each].get('width') * dict_response[each].get('height')
            if photo_size > largest_photo:
                largest_photo = photo_size
            needed_item = each
            largest_photo_url = dict_response[needed_item].get('url')
            largest_photo_type = dict_response[needed_item].get('type')
            return largest_photo_url, largest_photo_type

    def convert_time(self, unix_format):
        time_unix = datetime.datetime.fromtimestamp(unix_format)
        time_converted = time_unix.strftime('%Y-%m-%d time %H-%M-%S')
        return time_converted

    def get_photo_info(self):
        photo_count, response = self.get_photo()
        result = {}
        for each in tqdm(range(photo_qty), desc='Downloading...', unit=' pic', dynamic_ncols=True, colour='green'):
            sleep(.1)
            if photo_qty > photo_count:
                print(f'\nYou exceeded the maximum amount of {photo_count} photos.')
                break
            else:
                likes_count = response[each]['likes']['count']
                url_download, picture_size = self.get_largest_photo(response[each]['sizes'])
                date = self.convert_time(response[each]['date'])
                photo_dict = result.get(likes_count, [])
                photo_dict.append({'add_name': date,
                                   'url_picture': url_download,
                                   'size': picture_size})
                result[likes_count] = photo_dict
        return result

    def get_output(self):
        json_list = []
        name_url_dict = {}
        photo_dict = self.get_photo_info()
        for name in photo_dict.keys():
            for size in photo_dict[name]:
                if len(photo_dict[name]) == 1:
                    file_name = f'{name}.jpeg'
                else:
                    file_name = f'{name} {size["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': size["size"]})
                name_url_dict[file_name] = photo_dict[name][0]['url_picture']
        return json_list, name_url_dict


class YaDisc:
    def __init__(self, folder_name, token):
        self.token = get_token_yandex()
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        self.folder = self.create_folder(folder_name)

    def create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f"\nFolder '{folder_name}' created successfully\n")
        else:
            print(f"\nFolder '{folder_name}' already exists.\n")
        return folder_name

    def get_photo_names(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        response = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        photo_list = []
        for name in response:
            photo_list.append(name['name'])
        return photo_list

    def upload_photo_to_disc(self, name_url_dict):
        photo_list = self.get_photo_names(self.folder)
        total_files_added = 0
        for key in name_url_dict.keys():
            if key not in photo_list:
                params = {'path': self.folder + '/' + key,
                          'url': name_url_dict[key],
                          'overwrite': 'false'}
                requests.post(self.url, headers=self.headers, params=params)
                print(f"Picture {key} added successfully to folder '{self.folder}'.")
                total_files_added += 1
            else:
                print(f"Picture {key} already in folder '{self.folder}'.")
        print(f'\nTotal files added: {total_files_added}')


if __name__ == '__main__':
    print('Welcome to PY-cloud!')
    vk_id = input('Please enter you ID vk.com: ')
    user_folder_name = input('Please enter the name of the folder: /')
    photo_qty = int(input(f'How many pictures you would like to upload? '))

    vk_user = VkUser(get_token_vk())
    pprint(vk_user.json)

    ya = YaDisc(user_folder_name, get_token_yandex())
    ya.upload_photo_to_disc(vk_user.export_dict)
