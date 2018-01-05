# Lob Take Home Project

LobTakeHome is a simple command line program that sends a letter to your legislator with Lob. 

### Getting Started

The only external program needed to run LobTakeHome is requests.

Before you install requests, LobTakeHome suggests that you install pipenv (a popular python packaging tool). This can be installed with pip.

```
pip install pipenv
```

After installing pipenv, it should be simple to install requests. To install Requests, run this command in your terminal of choice:

```
pipenv install requests
```

After this, you're ready to use LobTakeHome.

### How to Use

LobTakeHome is run entirely from the command line. Your input must follow the format of name, address line 1, address line 2 (this should be set to an empty string when n/a), city, state, zip code, and a maximum of 500 character message to send. Any additional inputs will be ignored. This program **does not** take a file as the input for the 500 character message. 

An example input looks something like this.

```
 python LobTakeHome.py "Aurash Jalalian" "545 East 14th Street" "" "New York" "NY" "US" "10009" "Hello World"
```

This yields the corresponding output in the form of a url in your console.

![Sample Output Image](https://user-images.githubusercontent.com/25331886/34631685-6eb916b0-f226-11e7-8011-a80d60f40c36.png)

**Errors:**
All errors will be printed to the console with the corresponding API, Error Code, and Error Message.

## Built With

* [Google Civic Information API](https://developers.google.com/civic-information/) - For Gathering Legislator Information
* [Lob API](https://lob.com/docs/python#intro) - For Creating Letter PDF
* [Requests](http://docs.python-requests.org/en/master/) - For GET and POST requests

## Authors

* **Aurash Jalalian** - *Initial work*
