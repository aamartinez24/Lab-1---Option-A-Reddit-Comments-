# CS2302, Airam A Martinez, Lab1(Option A), Diego Aguirre, Gerardo Barraza, 9/8/2019
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='e3Ib50QHVQn7Iw',
                     client_secret='cV6Vqp4kPp8zgnFtkFIgrAsL6Bo',
                     user_agent='my user agent'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# returns number value that determines if text is negative.
def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']

# returns number value that determines if text is neutral.
def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']

# returns number value that determines if text is positive.
def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']

# Returns all comments and replies of that specific post as a tree.
def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()
    
    return submission.comments

"""
In order to iterate through the tree of all the comments on the reddit post I created a method called process_comments
where I start with an index of zero as a parameter.
After that we move through the list by iterating through the main comments first. ex. comments[i].body
Then we check if there’s no more main comments by comparing the range of the list to the index. If that’s the case, then we
start to iterate through the replies of the main comment, and repeat the same process to the replies of the replies by 
calling the same method this time with comment[i].replies and starting again with an index of zero.
In order to check if my recursion was working, I made it for the method to print each comment that I was passing,
if all the comments printed then it worked.
I the end I implemented three lists to the method, one for neutral comments, another list for negative comments, and 
lastly for positive comments.
In my process method I call all the get_text_proba passing with the comment and compare the number given to determine
the greatest number then add that comment to the appropriate list.
I tested my code by implementing different URLs for different reddit post.
I first did it with a reddit post without any comments which in return gave me empty lists.
Then I implemented another reddit post that had little amount of comments and checked if it worked.
At the very end I implemented the URL that I was given and checked if it also works.
In the end I concluded that my code worked.
"""

# Iterate through the comments list
def process_comments(comments, i, neg_list, neu_list, pos_list):
    if i not in range(len(comments)):   # Checks if theres no more comments in a list.
        return None
    else:
        curr_comment = comments[i]
        # Get all three connotation values for a comment.
        neg = get_text_negative_proba(curr_comment.body)
        neu = get_text_neutral_proba(curr_comment.body)
        pos = get_text_positive_proba(curr_comment.body)
        # Compare the three values and if it has a greater value for a specific connotation then add the comment to the
        # appropriate list.
        if neg >= neu and neg >= pos:
            neg_list.append(curr_comment.body)
        elif neu >= pos and neu >= neg:
            neu_list.append(curr_comment.body)
        else:
            pos_list.append(curr_comment.body)
        # Call method again and update the index by 1 to iterate through the comment list.
        process_comments(comments, i+1, neg_list, neu_list, pos_list)
        i=0
        # Call method again, this time with the comment replies, and starting again with index zero.
        process_comments(curr_comment.replies, i, neg_list, neu_list, pos_list)
        
        return neg_list, neu_list, pos_list     # Return the three lists.

def main():
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    i = 0           # Index starting at zero that will help iterate the tree.
    neg_list = []   # Three lists that will save the comments according to the SentimentIntensityAnalyzer.
    neu_list = []
    pos_list = []
    # Call process_comments method with above variables as parameters and set it equal to a list that contains all three lists.
    all_list = process_comments(comments[:], i, neg_list, neu_list, pos_list)
    neg_list, neu_list, pos_list = all_list     # Divide the return list into three list.
    
    
main()
