#!/usr/bin/bash

curl -L -k -s -o /dev/null -w "%{http_code}\n"  https://example.com
