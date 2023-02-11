# [PHP - Unserialize overflow](https://www.root-me.org/fr/Challenges/Web-Serveur/PHP-Unserialize-overflow)

## Source code

```php
<?php
include 'flag.php';

ini_set('display_errors', 1);
error_reporting(E_ALL);

class User
{
    protected $_username;
    protected $_password;
    protected $_logged = false;
    protected $_email = '';

    public function __construct($username, $password)
    {
        $this->_username = $username;
        $this->_password = $password;
        $this->_logged = false;
    }

    public function setLogged($logged)
    {
        $this->_logged = $logged;
    }

    public function isLogged()
    {
        return $this->_logged;
    }

    public function getUsername()
    {
        return $this->_username;
    }

    public function getPassword()
    {
        return $this->_password;
    }
}

function storeUserSession($user)
{
    $serialized_value = serialize($user);
    // avoid the storage of null byte, replace it with \0 just in case some session storage don't support it
    // this is done because protected object are prefixed by \x00\x2a\x00 in php serialisation
    $data = str_replace(chr(0) . '*' . chr(0), '\0\0\0', $serialized_value);
    $_SESSION['user'] = $data;
}

function getUserSession()
{
    $user = null;
    if (isset($_SESSION['user'])) {
        $data = $_SESSION['user'];
        $serialized_user = str_replace('\0\0\0', chr(0) . '*' . chr(0), $data);
        $user = unserialize($serialized_user);
    } else {
        $user = new User('guest', '');
    }
    return $user;
}

session_start();
$errorMsg = "";
$currentUser = null;

// keep entered values :
if (isset($_POST['submit'])) {
    $currentUser = new User($_POST['username'], $_POST['password']);
    $isLogged = $currentUser->getUsername() === 'admin' && 
        hash('sha512',$currentUser->getPassword()) === 'b3b7b663909f8e9b4e2a581337159e8a5e468c088ec802cb99a027c1dcbefb7d617fcab66ab4402d4617cde33f7fce93ae3c4e8f77aec2bb5f8c7c8aec3bbc82'; // don't try to bruteforce me this is useless
    $currentUser->setLogged($isLogged);
    $errorMsg = ($isLogged) ? '' : 'Invalid username or password.';
    storeUserSession($currentUser);
} else {
    $currentUser = getUserSession();
}

if ($currentUser->isLogged()) {
    echo 'you are logged in! congratz, the flag is: ' . $FLAG;
    die();
}

if (isset($_GET['source'])) {
    show_source(__FILE__);
    die();
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8"/>
    <title>Login Page</title>
</head>
<body>
<div class="error"><?= $errorMsg ?></div>
<form name="input" action="" method="post">
    <label for="username">Username:</label><input type="text" value="<?php echo htmlspecialchars($currentUser->getUsername(), ENT_QUOTES, 'UTF-8'); ?>"
                                                  id="username" name="username"/>
    <label for="password">Password:</label><input type="password" value="<?php echo htmlspecialchars($currentUser->getPassword(), ENT_QUOTES, 'UTF-8'); ?>"
                                                  id="password" name="password"/>
    <input type="submit" value="login" name="submit"/>
</form>
<p><em><a href="index.php?source">source code</a></em></p>
</body>
</html>
```

## Solutions
