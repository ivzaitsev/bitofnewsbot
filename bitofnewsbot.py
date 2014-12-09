import praw
import time
import datetime
import pyteaser

toadd = []


submissions_limit = 10 #number of top subissions to check during each cron period
thresh_max = 500 #karma threshholds for commenting
thresh_min = 10
username="username"#reddit login details
password="password"
comments_per_run = 10 #comments per cron period
sentences_per_summary = 4 #sentences per summary
subreddits = "subreddit1+subreddit2"
agent = "u/agent"
filestore = "done.txt" #to store submission ids of ones that are commented

def main():
	submissions = getSubmissions()
	done = getDone()
	counts=0 #how many comments made this round	
	for submission in submissions:
		#print submission
		if counts>=comments_per_run:
				break
		id = submission.id
		point = submission.ups - submission.downs
		#print id
		if id not in done:
			putDone(submission.id)
			sentences = pyteaser.SummarizeUrl(submission.url);
			#print sentences
			if (sentences != None):
				counts+=1
				comment = formComment(sentences, submission)		
				submission.add_comment(comment);
			##print(comment)	

def getDone():
	with open(filestore) as f:
		return f.read().splitlines()

def putDone(id):
	with open(filestore, "a") as text_file:
		text_file.write(id+"\n")

def getSubmissions():
	r = praw.Reddit(user_agent=agent)
	r.login(username, password)
	return r.get_subreddit(subreddits).get_hot(limit=1000)

def formComment(sentences, submission):
	#print(submission.title+": "+submission.url)

	comment = "**"+submission.title+"**:\n"
	count = 0
	if (sentences is None or len(sentences)<3):
		return None
	for sentence in sentences:
			if count < sentences_per_summary:
				sentence.replace('\n', ' ')
				comment += ("\n>* " + sentence + "\n")
				count = count + 1
	comment += u'\n Это [мой](http://reddit.com/user/user) бот. \n\n**Заголовки могут отбражаться некорректно**'
	return comment.encode('utf8')

if __name__ == "__main__":
	main()
