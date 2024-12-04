## GET User Info

```
GET /drive/v3/about/?fields=kind,user,storageQuota HTTP/1.1
Host: www.googleapis.com
Content-length: 0
Authorization: Bearer ya29.a0AeDClZCIu9hWOCGFiuGbLngpPnL380LN98nkF6FL_QLGU-no54P9oSMpYdL7zQ9fcd7KBT8_dm4kMtDnKXlbytdGWrIWd-ANkIVmZNU4i8xmq2lIoNFNIHTVmdbjtpovJO71Pwu7juEnnax_Y9MsnHLQKkNvT7glUcgZnAsPaCgYKAbASARASFQHGX2MixpBO6jUjNoNXohA1HnOasg0175
```

```
HTTP/1.1 200 OK
Content-length: 462
X-xss-protection: 0
Content-location: https://www.googleapis.com/drive/v3/about/?fields=kind,user,storageQuota
X-content-type-options: nosniff
Transfer-encoding: chunked
Expires: Mon, 01 Jan 1990 00:00:00 GMT
Vary: Origin, X-Origin
Server: ESF
-content-encoding: gzip
Pragma: no-cache
Cache-control: no-cache, no-store, max-age=0, must-revalidate
Date: Wed, 04 Dec 2024 06:40:28 GMT
X-frame-options: SAMEORIGIN
Alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
Content-type: application/json; charset=UTF-8

{
  "storageQuota": {
    "usage": "326725084", 
    "usageInDrive": "2090815", 
    "usageInDriveTrash": "0", 
    "limit": "16106127360"
  }, 
  "kind": "drive#about", 
  "user": {
    "me": true, 
    "kind": "drive#user", 
    "displayName": "Jon Snow", 
    "permissionId": "01197440981747165698", 
    "emailAddress": "happychitresh@gmail.com", 
    "photoLink": "https://lh3.googleusercontent.com/a/ACg8ocLCeb1rsn8wDpVbkacYfy65aMezciTVMYZDoOTPd1yFXpLM8g=s64"
  }
}
```
## More fields can be found here
https://developers.google.com/drive/api/reference/rest/v3/about#About
