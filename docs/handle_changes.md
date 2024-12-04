# Handle Changes for Drive

https://developers.google.com/drive/api/reference/rest/v3/changes

To start watching changes for a drive or a file, you need to get a start page token

## GET Start Page Token

```
GET /drive/v3/changes/startPageToken HTTP/1.1
Host: www.googleapis.com
Content-length: 0
Authorization: Bearer ya29.a0AeDClZDccNCLXUA21qTRslYLxDYGes1Csz04E7eN9hgVo1BgpYwFrZgbUKNpYOh04Br18DLmkUMaRWbr66Vug5gzE6MMSo7EFVOTEIAM86kxa8eOB72QSuNICbhtSDXU8f4_UmzNnNwnkVZSKejStZDQw3Os13u_-Wi66SQbaCgYKAbkSARASFQHGX2MiG8RzEQEK2IhlT5Kb7O1NcA0175
```

```
HTTP/1.1 200 OK
Content-length: 64
X-xss-protection: 0
Content-location: https://www.googleapis.com/drive/v3/changes/startPageToken
X-content-type-options: nosniff
Transfer-encoding: chunked
Expires: Mon, 01 Jan 1990 00:00:00 GMT
Vary: Origin, X-Origin
Server: ESF
-content-encoding: gzip
Pragma: no-cache
Cache-control: no-cache, no-store, max-age=0, must-revalidate
Date: Mon, 02 Dec 2024 07:54:22 GMT
X-frame-options: SAMEORIGIN
Alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
Content-type: application/json; charset=UTF-8
{
  "kind": "drive#startPageToken", 
  "startPageToken": "660"
}
```

Once you've a start page token, you can either simply list the changes or watch for the change

## List Changes
```
GET /drive/v3/changes?pageToken=671 HTTP/1.1
Host: www.googleapis.com
Content-length: 0
Authorization: Bearer ya29.a0AeDClZCIu9hWOCGFiuGbLngpPnL380LN98nkF6FL_QLGU-no54P9oSMpYdL7zQ9fcd7KBT8_dm4kMtDnKXlbytdGWrIWd-ANkIVmZNU4i8xmq2lIoNFNIHTVmdbjtpovJO71Pwu7juEnnax_Y9MsnHLQKkNvT7glUcgZnAsPaCgYKAbASARASFQHGX2MixpBO6jUjNoNXohA1HnOasg0175
```

```
HTTP/1.1 200 OK
Content-length: 80
X-xss-protection: 0
Content-location: https://www.googleapis.com/drive/v3/changes?pageToken=671
X-content-type-options: nosniff
Transfer-encoding: chunked
Expires: Mon, 01 Jan 1990 00:00:00 GMT
Vary: Origin, X-Origin
Server: ESF
-content-encoding: gzip
Pragma: no-cache
Cache-control: no-cache, no-store, max-age=0, must-revalidate
Date: Wed, 04 Dec 2024 06:54:05 GMT
X-frame-options: SAMEORIGIN
Alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
Content-type: application/json; charset=UTF-8
{
  "kind": "drive#changeList", 
  "changes": [], 
  "newStartPageToken": "671"
}
```

## Watch Changes
You may register to listen to changes using following call

```
POST /drive/v3/changes/watch?pageToken=671 HTTP/1.1
Host: www.googleapis.com
Content-length: 134
Content-type: application/json
Authorization: Bearer ya29.a0AeDClZCIu9hWOCGFiuGbLngpPnL380LN98nkF6FL_QLGU-no54P9oSMpYdL7zQ9fcd7KBT8_dm4kMtDnKXlbytdGWrIWd-ANkIVmZNU4i8xmq2lIoNFNIHTVmdbjtpovJO71Pwu7juEnnax_Y9MsnHLQKkNvT7glUcgZnAsPaCgYKAbASARASFQHGX2MixpBO6jUjNoNXohA1HnOasg0175
{
  "payload": true,
  "id": "asxasx",
  "type": "webhook",
  "address": "https://webhook.site/9ff7ae9f-3c9a-4f7a-9835-edec6863519b"
}
```

```
HTTP/1.1 200 OK
Content-length: 213
X-xss-protection: 0
X-content-type-options: nosniff
Transfer-encoding: chunked
Expires: Mon, 01 Jan 1990 00:00:00 GMT
Vary: Origin, X-Origin
Server: ESF
-content-encoding: gzip
Pragma: no-cache
Cache-control: no-cache, no-store, max-age=0, must-revalidate
Date: Wed, 04 Dec 2024 06:56:08 GMT
X-frame-options: SAMEORIGIN
Alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
Content-type: application/json; charset=UTF-8
{
  "resourceId": "7axk6UsP7NfD81YqDzjDL1t7Gqs", 
  "kind": "api#channel", 
  "expiration": "1733298968000", 
  "id": "asxasx", 
  "resourceUri": "https://www.googleapis.com/drive/v3/changes?alt=json&pageToken=671"
}
```

Here's a sample notification you will receive on your callback URL. 

_The request details are stored as json, as webhooks.site didnt give me an easier format to store_

```json
{
  "log": {
    "version": "1.2",
    "creator": {
      "name": "Webhook.site",
      "version": "1.0"
    },
    "entries": [
      {
        "startedDateTime": "2024-12-04 06:56:08",
        "request": {
          "method": "POST",
          "url": "https://webhook.site/9ff7ae9f-3c9a-4f7a-9835-edec6863519b",
          "headers": [
            {
              "name": "accept-encoding",
              "value": "gzip, deflate, br"
            },
            {
              "name": "user-agent",
              "value": "APIs-Google; (+https://developers.google.com/webmasters/APIs-Google.html)"
            },
            {
              "name": "content-length",
              "value": "0"
            },
            {
              "name": "x-goog-resource-uri",
              "value": "https://www.googleapis.com/drive/v3/changes?alt=json&pageToken=671"
            },
            {
              "name": "x-goog-resource-id",
              "value": "7axk6UsP7NfD81YqDzjDL1t7Gqs"
            },
            {
              "name": "x-goog-message-number",
              "value": "1"
            },
            {
              "name": "x-goog-resource-state",
              "value": "sync"
            },
            {
              "name": "x-goog-channel-expiration",
              "value": "Wed, 04 Dec 2024 07:56:08 GMT"
            },
            {
              "name": "x-goog-channel-id",
              "value": "asxasx"
            },
            {
              "name": "accept",
              "value": "*/*"
            },
            {
              "name": "host",
              "value": "webhook.site"
            },
            {
              "name": "content-type",
              "value": ""
            }
          ],
          "bodySize": 0,
          "postData": {
            "mimeType": "application/json",
            "text": ""
          }
        },
        "response": {
          "status": 200,
          "httpVersion": "HTTP/1.1",
          "headers": [
            {
              "name": "Content-Type",
              "value": "text/html"
            }
          ],
          "content": {
            "size": 145,
            "text": "This URL has no default content configured. <a href=\"https://webhook.site/#!/view/9ff7ae9f-3c9a-4f7a-9835-edec6863519b\">View in Webhook.site</a>.",
            "mimeType": "text/html"
          }
        }
      }
    ]
  }
}
```