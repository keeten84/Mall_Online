# _*_ coding: utf-8 _*_
# @File  : weibo_access.py
# @Author: Keeten_Qiu
# @Date  : 2018/11/16
# @Desc  :

def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_url = 'http://118.24.144.159:8000/complete/weibo/'
    auth_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={re_url}".format(client_id=3200328026,re_url=redirect_url)
    print(auth_url)


def get_access_token(code="43a2deff6cf70cb33b5ffc3e33402d56"):
    access_token_url =  'https://api.weibo.com/oauth2/access_token'
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id" : 3200328026,
        "client_secret" :"6c4b438078e40d3cc8a0e581f594beb0",
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://118.24.144.159:8000/complete/weibo/"
    })
    pass



if __name__ == '__main__':
    get_auth_url()
    get_access_token(code="43a2deff6cf70cb33b5ffc3e33402d56")