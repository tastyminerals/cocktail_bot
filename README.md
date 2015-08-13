# chatbotty
This is a small chatbot created in order to try out AIML markup language for dialog modelling.
This chatbot attempts to imitate a cocktail advisor, it tries to make an intelligble advice based on the information the user provides.

### Installation
You don't need to install it, just make sure you have **python3**.
Before running chatbotty also check if you have the following python3 modules installed.
* **nltk** (Wordnet, SnowballStemmer)
* **numpy**

Once you installed the above start with `./chatbotty.py`, or if your default python is python2 `python3 chatbotty.py`

### What does it do?
As mentioned above, the chatbot attempts to imitate a cocktail advisor and a casual chatbot. The chat topics are of course limited to just one, cocktails. In order to get an advice about which cocktail to drink the user has to ask the chatbot about it by basically saying "I want ..." or whaterver suits the conversation context. After that the chatbot analyzes user query and returns the recipe for the cocktail that best matches the query.

### How it works?
There are two similarity strategies used in order to analyze the query TFIDF and WORDNET. By default the chatbot uses TFIDF but you can change it during conversation by issuing the following commands: `Hanna use wordnet`, `Hanna use tfidf`. You can check which strategy is used currently by asking `Hanna what do you use?` (available after greeting).
The chatbot uses a small cocktails database `cocktails.xml` to run its similarity comparisons. The database contains cocktail descriptions, history and some trivia facts. Once the user asks/replies to system with "I want ..." or any other phrase suitable in context the system takes the query and runs similarity analysis. For example:
```
$ ./chatbotty.py 
Loading cocktail_brains.aiml... done (0.29 seconds)
Hi there! I am Hanna and I shall be your favourite cocktail adviser :)
What's on your mind?
> hi
Hola!
> How are you?
Doing fine.
> I want a cocktail
Cocktails! I love them! What will you drink?
> I want something blue
I found the one you might like! "Mai Tai"
 The Mai Tai is an alcoholic cocktail based on rum, Curacao liqueur, and lime juice, 
 associated with Polynesian-style settings. (...)
> awesome thanks
You are welcome.
```
Obviously you don't have to straight away ask the chatbot for a cocktail advice but the final result of the conversation is the recipe.

### Cocktails database


### WORDNET similarity
I shall omit TFIDF description since you can read about it on wikipedia. WORDNET however is a custom similarity search. Before running wordnet comparisons the user query gets expanded with wordnet adjective definitions. Every adjective in user query is expanded with most semantically close adjectives according to wordnet, non-contentful (there is a filter) words are removed. For example: `I want something blue` is converted into `clear intermediate green similar blue sky`. The database is called with all the available fields. We iterate through every word in the expanded query and match it against the cocktail database. The number of matched words is divided by the number of words in the field and multiplied by the multiplier. Every cocktail entry has several different fields in the database `<description>, <history>, <ingredients>, ...`. If the match is found in "description" it is multiplied by 2 since the words from "description" field have more weight than the ones from "history", thus every field has a multiplier. When we caclulate the scores for every cocktail in the database and return the one with the highest value.
WORDNET strategy is not as accurate as TFIDF but it certainly suffers less because of a small query or a small database (tbh I think it just needs some tuning).

