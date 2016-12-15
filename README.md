# Stock-AI

This application is Stock analytics using AI (Artificial Intelligence).
It aims to help users make more accurate judgments when trading stocks.
This application will be able to perform fundamental analysis and help to predict the stock price using artificial intelligence.
To run this application, follow the steps below.

## Preparation

* Create Procfile with `web: gunicorn -b 0.0.0.0:$PORT app:app`
* Run `virtualenv venv`
* VirtualEnv for Python3: `virtualenv -p python3 venv`
* Run `source venv/bin/activate`
* Run `pip freeze > requirements.txt`
* Run `heroku create --stack cedar`

## Result
```
{
  'price': str(price),
  'grade': grade,
  'critical': {
      'score': str(sum(criticals)),
      'total': str(len(criticals))
  },
  'score': {
      'score': str(sum(scores)),
      'total': str(len(scores))
  }
}
```
## License

[MIT License](https://github.com/jongha/stock-ai/blob/master/LICENSE.txt)