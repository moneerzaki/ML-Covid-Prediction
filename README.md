# ML-Covid-Prediction
a machine learning model that could predict the severity of a Covid patient depending on some personal details including age, sex, other diseases like: Asthma and obesity. and finally some sex-specific cases like pregnancy ...etc. 

# This is the website homepage 
![image](https://github.com/moneerzaki/ML-Covid-Prediction/assets/78418503/c31bf672-edeb-43e4-97b7-a986904e990a | width=50)

Based on the fact that most people need a fast response to their own case if they are covid holders or not and that there is no need for a whole profile for each user, then we decided there is no need for registering to our page to be able to use the model. 
Once, the user click on the button "Predict My Covido State" a form is presented infront of the user to fill and submit. 

![image](https://github.com/moneerzaki/ML-Covid-Prediction/assets/78418503/69ab6653-b5be-432c-b609-df62c26d0898)


Based on the chosen options from the form the model predicts the state of the patient based on the pretrained data from hugging face [[link](https://www.kaggle.com/datasets/meirnizri/covid19-dataset)](COVID-19 Dataset). The prediction should be only one of two options, whether the patient is or is not a covid holder. ![image](https://github.com/moneerzaki/ML-Covid-Prediction/assets/78418503/bd9dbbf4-eefb-4202-98ae-182829d2d6e5)

There is 1 more option if the user already knows his/her own case he can provide feedback to the system and then this instance of that user will be saved in the database to be retrained on from the same model. Otherwise, the instance of the user with the person's own prediction will not be saved in our database. 

to access to dataset of the model in the admin page. 
username: moneerzaki or mario
password: MMMCF#332


![image](https://github.com/moneerzaki/ML-Covid-Prediction/assets/78418503/d6dd0ddb-5369-4ae5-866d-b6ce6ffc0359)

There you could find all instances of patients that were used for the system to train on and those new instances that were recently added to the database by new users that the model will retrain on later. 


Retraining of the model on the new instances will happen after some time interval, set to 7 days in this model version. It will automatically take place in the backend every 7 days also after making sure there are enough instances to retrain on which is estimated to be a minimum number of 10 instances. 


