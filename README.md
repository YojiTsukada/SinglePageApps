# Single Page Apps


### Object
- Input form
- Serverless Architecture
- Send Email



### How to Build.

spa_action
```
$ python-lambda-local --function lambda_handler --timeout 5 lambda_function.py event.json  
$ lambda-uploader
$ aws lambda update-function-configuration --function-name sendmail  --runtime "python3.6"
```

sendmail
```
$ python-lambda-local --function lambda_handler --timeout 5 lambda_function.py event.json  
$ lambda-uploader --variables '{"MAIL_ADDR": メールアドレスを設定}'
$ aws lambda update-function-configuration --function-name sendmail  --runtime "python3.6"
```
