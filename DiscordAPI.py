import requests
import random
import time

def get_nonce():
    dt = str(hash(str(random.randint(0,1000000))))
    if len(dt)>25:
        return dt[:25]
    return dt


API_URL = 'https://discordapp.com/api/v6/'


def get_region():
    return requests.get('https://best.discord.media/region').text


class User:
    def __init__(self,id,username,discriminator,avatar):
        self.id = id
        self.username = username
        self.discriminator = discriminator
        self.avatar = ''

    def get_photo(self,size=128):
        return requests.get('https://cdn.discordapp.com/avatars/'+self.avatar+f'?size={size}').content






class API:
    def __init__(self,token=''):
        
        self.token = token
        self.user_settings = {}
        self.username = ''
        self.password = ''
        self.session = requests.session()
        self.counter = 0

    def login(self,username,password):
        self.username = username
        self.password = password
        headers = {'origin':'https://discordapp.com',
                   'referer':'https://discordapp.com/login',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   }

        payload = {'captcha_key': None,
                    'email': self.username,
                    'gift_code_sku_id': None,
                    'login_source': None,
                    'password': self.password,
                    'undelete': False
                    }

        response = self.session.post('https://discordapp.com/api/v6/auth/login',
                                     json=payload,headers=headers).json()

        self.token = response['token']
        self.user_settings = response['user_settings']
        return response

    def get_guilds(self):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }

        data = self.session.get(API_URL+'users/@me/affinities/guilds',headers=headers)
        return data.json()

    def get_library(self):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+'users/@me/library',headers=headers)
        return data.json()


    def get_detectable(self):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+'applications/detectable',headers=headers)
        return data.json()

    def get_users(self):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+'users/@me/affinities/users',headers=headers)
        return data.json()

    def get_user(self,id:str,obj=True):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+f'users/{id}',headers=headers).json()
        if obj:
            return User(data['id'],data['username'],data['discriminator'],data['avatar'])
        else:
            return data.json()

    def get_guilds(self):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+'/users/@me/guilds',headers=headers)
        return data.json()

    def leave_guild(self,guild_id):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+f'/users/@me/guilds/{guild_id}',headers=headers)
        return data

    def post_message(self,channel,message,tts=False):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }

        payload = {'content':message,
                   'nonce':get_nonce(),
                   'tts':tts}

        #if self.counter == 9:
        #    time.sleep(0.5)
        #    self.counter = 0

        while True:
            data = self.session.post(API_URL+f'channels/{channel}/messages',json=payload,headers=headers)
            if data.status_code == 429:
                time.sleep(data.json()['retry_after']/1000)
                #time.sleep(float('0.'+str(data.json()['retry_after'])))
                continue
            break

        #self.counter += 1
        return data.json()

    def get_guild_info(self,guild_id):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+f'guilds/{guild_id}',headers=headers)
        return data.json()

    def get_guild_preview(self,guild_id):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+f'guilds/{guild_id}/preview',headers=headers)
        return data.json()

    def get_guild_channels(self,guild_id):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+f'guilds/{guild_id}/channels',headers=headers)
        return data.json()

    def get_channel(self,channel_id):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+f'channels/{channel_id}',headers=headers)
        return data.json()

    def get_channel_messages(self,channel_id,around=None,before=None,after=None,limit=50):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }

        url = API_URL+f'/channels/{channel_id}/messages?limit={limit}'
        if around != None:
            url += f'&around={around}'
        if before != None:
            url += f'&before={before}'
        if after != None:
            url += f'&after={after}'
        data = self.session.get(url,headers=headers)
        return data.json()

    def get_channel_message(self,channel_id,message_id):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.get(API_URL+f'channels/{channel_id}/messages/{message_id}',headers=headers)
        return data.json()

    def trigger_typing_indicator(self,channel_id):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        data = self.session.post(API_URL+f'channels/{channel_id}/typing',headers=headers)
        return data

    def delete_message(self,channel_id,message_id):
        headers = {'authorization':self.token,
                   'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.307 Chrome/78.0.3904.130 Electron/7.3.2 Safari/537.36',
                   'sec-fetch-mode':'cors',
                   'sec-fetch-site':'same-origin',
                   }
        ret = self.session.delete(API_URL+f'channels/{channel_id}/messages/{message_id}',headers = headers)
        if ret.status_code == 429:
            raise Exception('Time limit')
        #if not ret.status_code == 204:
        #    print('')
        return ret.status_code == 204

    



if __name__ == '__main__':

    data = get_region()

    api = API()
    api.login('','')
    import time
    while True:
        api.post_message(1,'2')
     