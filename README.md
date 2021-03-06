# Detecting Cyberbullying with NLP

**Author**: Greg Burgess

![cyberbully image](images/Cyberprzemoc.png)

****

## Overview

Parents find it extremely difficult to monitor their children's social media interactions for cyberbullying and toxic comments. I trained several machine learning models to detect toxic comments in over 500,000 social media comments. The best machine learning model could be used to provide alerts to parents when these issues arise online. Ultimately, these parental alerts could ameliorate some of the risks that children experience online.

Please review my [presentation](./Presentation.pdf) for a quick overview of this project.

****

## Business Problem

According to a surveys from the CDC, nearly 16 percent of students in grades 9–12 reported experiencing cyberbullying. The percentage was twice as large for females (20.4%) as males (10.9%), and nearly twice as large for students identifying as gay, lesbian, or bisexual (26.6%) as those identifying as heterosexual (14.1%). [source](http://nces.ed.gov/programs/coe/indicator/a10#6)

However, these may be underestimates of the prevalence of cyberbullying. In 2021, Bark (a parental control app) analyzed 3.4 billion messages and found that 85% of teens experienced or witnessed cyberbullying at some point during 2021. [source](https://www.bark.us/annual-report-2021/)

[![Bark annual survey](images/bark_annual_survey.png)](https://www.bark.us/annual-report-2021/)
[source: Bark annual survey](https://www.bark.us/annual-report-2021/)

Parents struggle to keep their kids and teens safe, especially online. Very few products that monitor internet usage can also monitor the *content* teens see while they are online. There are some products being developed that offer APIs to moderators and service providers to monitor for dangerous content posted by their users. But those products only provide feedback to moderators, not to the parents of children that were exposed to those comments.

I developed a machine learning model that can identify cyberbullying and other toxic comments in online text comments. This service could be utilized to protect children from toxic comments by alerting parents to these occurrences, thereby enabling them to discuss these issues with their children.

****

## Data

The data I used to train the model came from a set of roughly two million comments collected by the [Civil Comments](https://medium.com/@aja_15265/saying-goodbye-to-civil-comments-41859d3a2b1d) platform. [Jigsaw](https://jigsaw.google.com), a subsidiary of Google that explores various threats across the internet, provided human ratings of different subtypes of toxicity in those comments. The comments and rating labels were released in csv format on [Kaggle](https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/data)

### Data Download

To download these data, visit the Kaggle competition site [data page](https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/data). You must sign in with your Kaggle account and agree to the "Competition Rules" before you can click on the "Download All" button to download the data. Clicking "Download All" should save a file named `jigsaw-unintended-bias-in-toxicity-classification.zip` into your default download location. Move this zip file into the data/ directory in this repository. Unzip / extract the zip file into the data/ directory, which should create a new `jigsaw-unintended-bias-in-toxicity-classification` directory containing the needed `all_data.csv` file.

### Comment Ratings

All comments were rated by up to 10 human raters, who were asked whether the comment contained several different subtypes of toxicity. These categories include:
- `toxicity`
- `severe_toxicity`
- `obscene`
- `threat`
- `insult`
- `identity_attack`
- `sexual_explicit`

The values for each category label reflect the proportion of human raters who assessed that subtype of toxicity in the comment. I created a single binary `target` variable by reviewing comments, determining appropriate thresholds for each category, and flagged comments containing any subtype of toxicity above those thresholds.

****

## Methods

The comment text and ratings are stored in csv files, and I read the data into a Pandas DataFrame. 

The ratings labels are floating point values ranging from 0.0 to 1.0, reflecting the proportion of human raters who determined the comment included that subtype of toxicity. I engineered a binary target for classification. Specifically, the `target` label flagged comments that exceeded thresholds (chosen by me) for any of the subsets of toxicity that were included. Using these criteria, roughly 17% of the posts are considered positive targets. Although the proportion of toxic posts is small, the total number of toxic posts is approaching 340,000. Consequently, I chose to undersample the negative class in order to avoid class imbalance while training the model.

![class imbalance](images/class_imbalance.jpg)

The `comment_text` feature is stored as a single continuous text string for each record, which required standard "Bag of Words" preprocessing techniques for NLP. This includes text cleaning, removing stop words, tokenization, lemmatization, and vectorization. Using the CountVectorizer method in sci-kit learn, we get a set of features representing a the number of occurrences of words in each comment.

I trained several different models to use these features to predict the target label. Specifically, I tested the performance of multinomial naive bayes and logistic regression algorithms to distinguish the positive and negative target classes.

For this classification problem, there are costs for both false positives and false negatives. False negatives (i.e., labeling toxic posts as non-toxic) are cases of cyberbullying that were missed, and negative effects of that cyberbullying will be unaddressed. On the other hand, false positives (i.e., labeling non-toxic posts as toxic) can reduce trust in the predictive model and result in parents choosing to ignore potential warnings. To balance sensitivity to both types of errors, during both training and evaluation, I used the F1-score as the metric for model performance.

****

## Results

### Most-common words across all comments
After removing the most common stopwords, there are still certain words that are common across toxic and non-toxic classes, but do not seem to distinguish between those classes.
![most frequent terms](images/FreqDist.jpg)


### Terms more common in toxic comments

Other words are more common in the toxic comment class than the non-toxic comment class.

![bully specific words](images/bully_wordcloud.png)


### Terms more common in non-toxic comments

Still other words appear more often in the non-toxic class than toxic class.

![nonbully specific words](images/nonbully_wordcloud.png)



****

## Conclusions

The final model achieved a F1 score of 80%. This was the best performance, in terms of F1 score, from the multinomial naive bayes and logistic regression models that I tested.

By choosing F1 scores as the optimization metric, there should be some degree of balance between the proportion of false positives and false negatives. 

### Confusion matrix

Reviewing the confusion matrix, it seems that the proportion of false positives (15%) and false negatives (23%) are relatively balanced. I sought this balance because of the concern that both false positives and false negatives carried costs. False positives could result in parents choosing to ignore potential warnings, while false negatives reflect cases of toxic content that were missed.

![final model confusion matrix](images/final_model_confusion_matrix.png)


### Strongest predictors from Logistic Regression model

The following terms have the coefficients with the highest magnitude (absolute value). 

Some of these words were in the list of words that were more common in the toxic class than non-toxic class. But many were not. Perhaps those words were also predictive due to the relative frequency of their usage in the toxic class compared to non-toxic class.

![logistic regression coefficients](images/logistic_regression_coefs.jpg)


### Predictions

An app with the deployed model is running on [Streamlit](https://share.streamlit.io/gcburgess/cyberbullying_detector/main/cyberbullying_detector_app.py).

The model is able to classify comment text as 'toxic' or 'non-toxic'. Here are a few examples.

A comment that should be classified as 'toxic' by using some of the terms with the strongest coefficients in the logistic regression.


```python
detect("You're a stupid idiot")
```

    toxic comment


Another comment that, on its face, should be classified as 'non-toxic'


```python
detect('You are awesome and I love you')
```

    not a toxic comment


Lastly, a comment that was created to be intentionally ambiguous.


```python
detect('I am a cereal killer!')
```

    toxic comment


****

## Future Work / Recommendations

The development of this predictive model represents an early stage in the creation of a project that can help parents monitor the safety of their children's online activity. Given the opportunity, I would like to improve upon this model, and develop it into a product capable of reviewing texts and social media content. Most social media companies follow GDPR regulations for all users, which includes the data portability requirement allowing users to download their personal data, or import them to other apps.

Future work
- Acquire more diverse data, such as comments specifically from teenaged users
- Perform additional feature engineering, such as using bigrams and trigrams
- Develop an API to interface with users' social media accounts and highlight potential toxic comments (either made or received)

****

## Repository Navigation

Please check out my [presentation](./Presentation.pdf) for a quick overview.

For the full analysis, review my Jupyter notebooks: 
- [Data exploration](./01-data-understanding.ipynb)
- [NLP preprocessing](./02-data-preprocessing.ipynb)
- [Pipelines and model selection](./03-pipelines-and-models.ipynb)

To run the notebooks in this repository, you should re-create the `nlp-env` environment from the `nlp-env.yml` file using `conda`. Check the [conda docs](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) for installation instructions.



For any additional questions, please [email](mailto:gcburgess@gmail.com) or connect via [LinkedIn](https://www.linkedin.com/in/Greg-Burgess).



```
├── README.md					<- The top-level README for reviewers of this project
├── Presentation.pdf				<- PDF version of project presentation
├── 01-data-understanding.ipynb			<- Notebook containing data exploration
├── 02-data-preprocessing.ipynb			<- Notebook containing NLP preprocessing
├── 03-pipelines-and-models.ipynb		<- Notebook containing pipelines and model selection
├── .gitignore					<- exclude certain files from repository
├── nlp-env.yml					<- environment file for notebooks in this repository
├── cyberbullying_detector_app.py		<- streamlit app code to deploy final model
├── requirements.txt				<- requirements file for streamlit app
├── data					<- Both sourced externally and generated from code
│   └── final_model_pipe.pkl			<- File containing final model for deployment
└── images					<- Both sourced externally and generated from code
```
