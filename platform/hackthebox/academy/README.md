# [academy.Hack The Box](https://academy.hackthebox.com/)

my student id: HTB-215FE1EF25

## Notes

vpn problem - signature digest algorithm too weak:

- Insert the following line in the client's config.ovpn file: `tls-cipher "DEFAULT:@SECLEVEL=0"`
- references: [link](https://www.snbforums.com/threads/openvpn-2-4-5-cannot-connect-because-of-weak-algorithm.45428/)
