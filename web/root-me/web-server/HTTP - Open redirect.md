# [HTTP - Open redirect](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Open-redirect)

## Solutions

- Thay đổi Request Query Parameters của request khi ấn vào một trong 3 nút:
  - url = <https://faceook.com>
  - h = b094bbedbac7a4c62e27cfe5f45bb45b

  - Trong đó h = md5(url)

- Flag xuất hiện trong response: `e6f8a530811d5a479812d7b82fc1a5c5`
