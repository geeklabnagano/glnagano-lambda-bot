### 環境構築方法
* npm install -g serverless
* git clone https://github.com/koty/glnagano-lambda-bot.git
* cd glnagano-lambda-bot
* npm install
* ~/.aws/config および ~/.aws/credentials を設定
* serverless.env.yml.templateをコピーしてserverless.env.ymlにし内容を設定

### deploy方法
* serverless deploy --aws-profile some_profile でdeploy
