### 環境構築方法
* npm install -g serverless
* git clone https://github.com/koty/glnagano-lambda-bot.git
* cd glnagano-lambda-bot
* npm install
* ~/.aws/config および ~/.aws/credentials を設定

### deploy方法
* serverless deploy --aws-profile some_profile でdeploy

今のところ手動で

* CONSUMER_KEY
* CONSUMER_SECRET
* ACCESS_TOKEN
* ACCESS_TOKEN_SECRET

を環境変数に設定。