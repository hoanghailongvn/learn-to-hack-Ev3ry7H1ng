# [Illumination](https://app.hackthebox.com/challenges/illumination)

## CHALLENGE DESCRIPTION

A Junior Developer just switched to a new source control platform. Can you find the secret token?

## Analysis

```bash
┌──(realkali㉿kali)-[~]
└─$ tree -a Illumination.JS/
Illumination.JS/
├── bot.js
├── config.json
└── .git
```

## Solutions

get the token from `.git`

```bash
>git log
commit edc5aabf933f6bb161ceca6cf7d0d2160ce333ec (HEAD -> master)
Author: SherlockSec <dan@lights.htb>
Date:   Fri May 31 14:16:43 2019 +0100

    Added some whitespace for readability!

commit 47241a47f62ada864ec74bd6dedc4d33f4374699
Author: SherlockSec <dan@lights.htb>
Date:   Fri May 31 12:00:54 2019 +0100

    Thanks to contributors, I removed the unique token as it was a security risk. Thanks for reporting responsibly!

commit ddc606f8fa05c363ea4de20f31834e97dd527381
Author: SherlockSec <dan@lights.htb>
Date:   Fri May 31 09:14:04 2019 +0100

    Added some more comments for the lovely contributors! Thanks for helping out!

commit 335d6cfe3cdc25b89cae81c50ffb957b86bf5a4a
Author: SherlockSec <dan@lights.htb>
Date:   Thu May 30 22:16:02 2019 +0100

    Moving to Git, first time using it. First Commit!

>git diff 47241a..ddc606
diff --git a/config.json b/config.json
index 6735aa6..316dc21 100644
--- a/config.json
+++ b/config.json
@@ -1,6 +1,6 @@
 {

-       "token": "Replace me with token when in use! Security Risk!",
+       "token": "SFRCe3YzcnNpMG5fYzBudHIwbF9hbV9JX3JpZ2h0P30=",
        "prefix": "~",
        "lightNum": "1337",
        "username": "UmVkIEhlcnJpbmcsIHJlYWQgdGhlIEpTIGNhcmVmdWxseQ==",

```
