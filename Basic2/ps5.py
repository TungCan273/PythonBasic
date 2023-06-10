"""
Name: Luong Minh Tung 
Collaborators: 
Time:
"""

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
from datetime import datetime, timezone
from pytz import timezone as tz

# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)
        try:
            description = translate_html(entry.description)
        except AttributeError:
            description = ""
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1

# TODO: NewsStory
class NewsStory: 
    def __init__(self, guid, title, description, link, pubdate):
        """
        guid: String,  A globally unique identifier for this news story
        title: String, The new story's headline 
        description: String, A paragraph or so summarizing the news story
        link: String, A link to a website with was published
        pubdate: Datetime, Date the new was published

        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description 
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate

# ======================
# Triggers
# ======================


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        """
        phrase: String
        Convert the phrase to lowercase letters
        """
        #self.phrase = phrase.lower()
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        """ 
        Convert text in to lowercase
        Returns True if the phare is present in text, False otherwise.
        Then, Remove punctuation and split into words
        The last, Join words into phrases and check if the given phrase is present
        """ 
        text = text.lower()
        # Remove punctuation and split into words
        text = "".join([c.lower() if c not in string.punctuation else " " for c in text])
        words = text.split() # Convert text to list  
        phrase_words = self.phrase.split()
        if all(word in words for word in phrase_words):
            phrase_indices = [words.index(word) for word in phrase_words]
            if all(phrase_indices[i] == phrase_indices[i-1] + 1 for i in range(1, len(phrase_indices))):
                return True
        return False

    def evaluate(self, story):
        """
        PhraseTrigger inherit its evaluate method from Trigger.
        """
        return self.is_phrase_in(story.get_title()) or self.is_phrase_in(story.get_description())

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        #PhraseTrigger.__init__(self, phrase)
        #super().__init__(phrase) 
        self.phrase = phrase

    def evaluate(self, story):
        """ 
        TitleTrigger inherit title from Trigger and 
        evaluate method is_phrase_in from PhraseTrigger
        """
        return self.is_phrase_in(story.get_title())
        #return self.phrase.lower() in story.get_title().lowe()

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)
        
    def evaluate(self, story):
        """
        DescriptionTrigger inherit description from Trigger and 
        evaluate is_phrase_in from PhraseTrigger
        """
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time): 
        """ 
        Make time to be in EST and format it to "%d %b %Y %H:%M:%S"
        """
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        time = time.replace(tzinfo=pytz.timezone("EST"))
        self.time = time

    def evaluate(self, time):
        """ 
        Convert time to string before saving it as an attribute
        """
        return str(time.get_pubdate().replace(tzinfo=pytz.timezone("EST")))


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        """ 
        Return strictly before the trigger's time 
        """
        #return story.get_pubdate() < self.time
        
        pubdate = story.get_pubdate()
        if pubdate.tzinfo is None:
            pubdate = pubdate.replace(tzinfo=timezone.utc)
        return pubdate < self.time.astimezone(timezone.utc)
    
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        """ 
        Return strictly after the trigger's time
        """
        #return story.get_pubdate() > self.time
        pubdate = story.get_pubdate()
        if pubdate.tzinfo is None:
            pubdate = self.time.astimezone(timezone.utc)
        return pubdate > self.time.astimezone(timezone.utc)

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, new_item):
        return not self.trigger.evaluate(new_item)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, new_item):
        return self.trigger1.evaluate(new_item) and self.trigger2.evaluate(new_item)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, new_item):
        return self.trigger1.evaluate(new_item) or self.trigger2.evaluate(new_item)

# ======================
# Filtering
# ======================


# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return [story for story in stories if any(trigger.evaluate(story) for trigger in triggerlist)]


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    returns: a list of trigger objects specified by the trigger configuration
    file.
    """
    # we give you the code to read in the file and eliminate blank lines and
    # comments. you don't need to know how it works for now!
    trigger_file = open(filename, "r")
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith("//")):
            lines.append(line)

    # todo: problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    all_triggers = {}
    added_triggers = []

    for line in lines:
        arguments = line.split(',')
        # Trigger definitions.
        if arguments[0] != 'ADD':
            if arguments[1] == 'DESCRIPTION':
                trigger_name = arguments[0]
                trigger_phrase = arguments[2]
                all_triggers[trigger_name] = DescriptionTrigger(trigger_phrase)
            if arguments[1] == 'TITLE':
                trigger_name = arguments[0]
                trigger_phrase = arguments[2]
                all_triggers[trigger_name] = TitleTrigger(trigger_phrase)
            if arguments[1] == 'BEFORE':
                trigger_name = arguments[0]
                trigger_time = arguments[2]
                all_triggers[trigger_name] = BeforeTrigger(trigger_time)
            if arguments[1] == 'AFTER':
                trigger_name = arguments[0]
                trigger_time = arguments[2]
                all_triggers[trigger_name] = AfterTrigger(trigger_time)
            if arguments[1] == 'NOT':
                trigger_name = arguments[0]
                trigger_phrase = arguments[2]
                all_triggers[trigger_name] = NotTrigger(trigger_phrase)
            if arguments[1] == 'AND':
                trigger_name = arguments[0]
                first_composed_trigger = all_triggers[arguments[2]]
                second_composed_trigger = all_triggers[arguments[3]]
                all_triggers[trigger_name] = AndTrigger(first_composed_trigger, second_composed_trigger)
            if arguments[1] == 'OR':
                trigger_name = arguments[0]
                first_composed_trigger = all_triggers[arguments[2]]
                second_composed_trigger = all_triggers[arguments[3]]
                all_triggers[trigger_name] = OrTrigger(first_composed_trigger, second_composed_trigger)
        # Trigger addition.
        else:
            for i in range(1, len(arguments)):
                added_triggers.append(all_triggers[arguments[i]])

    return added_triggers
#print(lines)  # for now, print it so you see what it contains!


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config("triggers.txt")

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify="center")
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=" ")
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
