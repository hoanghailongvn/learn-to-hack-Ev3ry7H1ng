# [Directory traversal](https://www.root-me.org/en/Challenges/Web-Server/Directory-traversal)

## Solutions

- Khi ta ấn vào `emotes`, `apps` hoặc `devices`, ... Ta thấy có query parameter `galerie=emotes`
- Thay đổi thành `galerie=.`, response hiển thị các folder có chứa trong galerie. Tương tự thay đổi query parameter để tìm password trong folder `galerie`

Kết quả:

- Tìm được file password.txt tại `galerie/86hwnX2r/password.txt`: `kcb$!Bx@v4Gs9Ez`

## Questions

- Vì sao truy cập trực tiếp vào folder galerie thì được phản hồi 403 còn galerie/86hwnX2r/password.txt thì lại được
