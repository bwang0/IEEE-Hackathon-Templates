#!/usr/bin/python

# This is a simple guessing game based on the images from reddit.com/r/pics
# Player has to guess the title of a randomly selected image by answering a multiple choice question
# This code is provided as a basic example of a Flask app. Read http://flask.pocoo.org/docs/quickstart/ to learn about Flask

# Author: Daeyun Shin
# Sept 7, 2012

from flask import Flask,url_for,render_template,Markup
import urllib2, re, random, htmllib

# this function is used to correctly display the parsed title ( replace &amp; with & and etc. ). not important
def unescape(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()

app = Flask(__name__)


# about() is called when the requested url is "example.com/about"
@app.route('/about')
def about():
    # get the appropriate html string by rendering template.html
    return render_template('template.html', about_text="This is a simple guessing game based on the images from reddit.com/r/pics. Player has to guess the title of a randomly selected image by answering a multiple choice qusetion. Read the comments in the source code for details.")

# play() is called when the requested url is "example.com"
@app.route('/')
def play():
    # download the html content of the front page of /r/pics (top 100 links)
    f = urllib2.urlopen('http://www.reddit.com/r/pics?limit=100')
    html=f.read()
    # parse the html using regular expression. matched pattern inside the parentheses can be referred as group(1), group(2), group(3), respectively
    iterator=re.finditer(r'<a class="title " href="([^" ]+)" >([^<]+)<[^\t]+?class="comments" href="([^"]+)"',html)
    # initialise the lists
    link=[]
    title=[]
    comments_link=[]

    for match in iterator:
        l=match.group(1)
        # unless the 4th character from the end of the url is a '.' (example.com/image.jpg, for example), skip.
        # this is a lazy trick to filter out links that are not images (a page containing the actual image, for example)
        if l[-4:-3] !='.':
            # ignore the rest of the loop and continue
            continue

        link.append(l)
        # reddit's default encoding is utf-8.
        title.append(unescape(match.group(2)).decode('utf-8'))
        comments_link.append(match.group(3))

    # number of collected images
    count = len(link)

    # random image selection
    rand=random.randint(0,count-1)
    thelink = link[rand]
    comments = comments_link[rand]
    # title of the selected image. it will be the correct answer of the multiple choice question
    answer = title[rand]
    # remove the correct title
    title.pop(rand)

    # a list containing randomly selected titles (wrong answers)
    titles = random.sample(title,4)
    answer_index = random.randint(0,4)
    # insert the correct answer in the middle of the list
    titles.insert(answer_index,answer)

    # generate the html code based on the result
    return render_template('template.html', imgurl=thelink, titles=titles, comments=comments, answer=answer_index)

if __name__ == '__main__':
    # print error message when available
    app.debug = True
    # the current file is the executed file (not imported)
    app.run()
