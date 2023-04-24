import praw
import json
import os

def open_connection (file_credentials):
    with open(file_credentials, 'r') as jsonfile:
        credentials = json.load(jsonfile)

    client_id = credentials["client_id"]
    client_secret = credentials["client_secret"]
    user_agent = "Comment Extraction (by u/"+credentials["username"]+")"
    username = credentials["username"]
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         user_agent=user_agent, username=username,
                         check_for_async=False)
    return reddit

def recursive_coments (submission):
    recursive = []
    upvote, downvote = "**UPVOTE**", "**DOWNVOTE**"
    if (len(submission.comments) > 0):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments:
            if ((upvote not in comment.body)and
                (downvote not in comment.body)):
                point = len(recursive)
                recursive.append(comment.body)
                try:
                    for reply in comment.replies:
                        reply_result = recursive_coments(reply)
                        if (len(reply_result) > 0):
                            if ("comments" not in result.keys):
                                recursive.append({})
                                recursive[point]["body"] = comment.body
                            recursive[point]["comments"] = reply_result
                except: continue
    return recursive

def write_data (data, dir, topic, count):
    path = ""
    if (count < 10): path = dir+"reddit_"+topic+"_00"+str(count)+".json"
    elif (count < 100): path = dir+"reddit_"+topic+"_0"+str(count)+".json"
    else: path = dir+"reddit_"+topic+"_"+str(count)+".json"
    with open(path, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def generate_count (dir, topic):
    for i in range(1000):
        path = ""
        if (i < 10): path = dir+"reddit_"+topic+"_00"+str(i)+".json"
        elif (i < 100): path = dir+"reddit_"+topic+"_0"+str(i)+".json"
        else: path = dir+"reddit_"+topic+"_"+str(i)+".json"
        if (not os.path.isfile(path)): return i

def extract (reddit, topic, subreddit, limit, dir):
    if (dir[:-1] != "/"): dir = dir+"/"
    posts = {"posts": []}
    post_topic = reddit.subreddit(subreddit)
    count = generate_count (dir, topic)
    for post in post_topic.new(limit=limit):
        dict_post = {}
        dict_post["title"] = post.title
        dict_post["selftext"] = post.selftext
        dict_post["subreddit"] = post.subreddit.display_name
        dict_post["topic"] = topic
        dict_post["id"] = post.id
        dict_post["num_comments"] = post.num_comments
        try:
            comm_url = 'https://www.reddit.com/r/'+dict_post["subreddit"]+'/comments/'+post.id+'/'
            comm_result = recursive_coments(reddit.submission(url=comm_url))
            if (len(comm_result) > 0): dict_post["comments"] = comm_result
        except: continue
        posts["posts"].append(dict_post)

        if (len(posts["posts"])%10 == 0):
            write_data(posts, dir, topic, count)
        if (len(posts["posts"]) == 100):
            count += 1
            posts = {"posts": []}
    write_data(posts, dir, topic, count)

if __name__ == '__main__':
    file_credentials = str(input("Directory for Credentials: "))
    dir_results = str(input("Directory for Extracted Data: "))
    reddit = open_connection(file_credentials)

    exit_comand = ""
    while (exit_comand != "x"):
        topic = str(input("Data Topic: "))
        subreddit = str(input("Subreddit: "))
        limit = int(input("Limit of Posts: "))
        extract(reddit, topic, subreddit, limit, dir_results)
        print(topic.upper()+" Data from "+subreddit.upper()+" Subreddit are extracted!")
        exit_comand = str(input("Clik on 'x' to exit: "))