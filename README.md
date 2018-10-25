# Single Page Apps


### Object
- Input form
- Serverless Architecture
- Send Email



### How to Build.

```
$ python-lambda-local --function lambda_handler --timeout 5 lambda_function.py event.json  
$ lambda-uploader
$ aws lambda update-function-configuration --function-name spa_action  --runtime "python3.6"
```