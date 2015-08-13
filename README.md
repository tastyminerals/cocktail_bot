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
There are two similarity strategies used in order to analyze the query TFIDF and WORDNET. By default the chatbot uses TFIDF but you can change it during converstation by issuing the following commands: `Hanna use wordnet`, `Hanna use tfidf`. You can check which strategy is used currently by asking `Hanna what do you use?` (after greeting).
The chatbot uses small cocktails database `cocktails.xml` to run its similarity comparisons. The database contains cocktail descriptions, history and some trivia facts.

