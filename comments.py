import praw
import re
import operator
import words

wordcount = {}

def ready_file():
    with open('words.py', 'w'):
        pass

    f = open('words.py', 'w')
    f.write('bad_words = {} \n good_words = {}')

def count_words(comment):
    global wordcount
    match = re.split(r' ', str(comment))
    if match:
        for word in match:
            if word == '' or word == '[deleted]':
                continue
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    return

def build_dictionary(search, attitude):
    print 'Building ' + attitude + ' dictionary ...'
    submissions = reddit.search(search)
    stop = 0
    for submission in submissions:
        if stop > 2:
            break
        stop += 1
        for comment in submission.comments:
            count_words(comment)
            if hasattr(comment, 'replies'):
                for reply in comment.replies:
                    count_words(reply)

        for k, v in wordcount.items():
            if v > 10:
                if attitude == 'good':
                    if k not in words.good_words:
                        words.good_words[k] = v
                    else:
                        words.good_words[k] += v
                elif attitude == 'bad':
                    if k not in words.bad_words:
                        words.bad_words[k] = v
                    else:
                        words.bad_words[k] += v

    word_file = open('words.py', 'w')
    word_file.write(str('bad_words = ' + str(words.bad_words)) + '\n')
    word_file.write(str('good_words = ' + str(words.good_words)))
    print('Done with ' + attitude + ' dictionary')

reddit = praw.Reddit(user_agent='CommentLurker')

if len(words.good_words) > 0 and len(words.bad_words) > 0:
    build_yes_or_no = ''
    while build_yes_or_no != 'y' and build_yes_or_no != 'n':
        build_yes_or_no = raw_input('Do you want to build dictionaries? (y/n)  ')
        build_yes_or_no = build_yes_or_no.lower()

    if build_yes_or_no == 'y':
        ready_file()
        bad_word = raw_input('Bad word: ')
        good_word = raw_input('Good word: ')

        build_dictionary(bad_word, 'bad')
        build_dictionary(good_word, 'good')
else:
    ready_file()
    bad_word = raw_input('Bad word: ')
    good_word = raw_input('Good word: ')

    build_dictionary(bad_word, 'bad')
    build_dictionary(good_word, 'good')

url = raw_input('Submission URL: ')
submission = reddit.get_submission(url)
score = 0

print 'Deciding if the submission is positive or negative'
for comment in submission.comments:
    match = re.split(r' ', str(comment))
    if match:
        for word in match:
            if word == '' or word == '[deleted]':
                continue
            if word in words.good_words and word in words.bad_words:
                if words.good_words[word] > words.bad_words[word]:
                    score += 1
                elif words.good_words[word] < words.good_words[word]:
                    score -= 1
            elif word in words.good_words:
                score += 1
            elif word in words.bad_words:
                score -= 1

print submission
print submission.url

score -= 100

if score > 0:
    print (str(submission) + ' has a positive tone! (' + str(score) + ')')
elif score < 0:
    print (str(submission) + ' has a negative tone! (' + str(score) + ')')
else:
    print ':('