# parse-email
This project is used for extracting email address in certain domain.

```
pip install scrapy
pip install Twisted==13.2.0
pip install selenium
```

You also have to download chrome dirver.

Download from http://chromedriver.storage.googleapis.com/index.html?path=2.16/

Copy it to /usr/bin

After cloning the project, run parser with domain and output file name.
```
python run_email_parse.py jana.com result
```

Email result will be save to the output file.
