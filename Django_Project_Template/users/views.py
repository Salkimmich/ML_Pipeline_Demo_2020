from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
# import sklearn.cluster.k_means_
from wordcloud import WordCloud, STOPWORDS
import pickle
#sentiments
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import uuid

from wsgiref.util import FileWrapper

from .forms import SignUpForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
import glob
from io import BytesIO
import base64

dir_path = os.path.dirname(os.path.realpath(__file__))


def signup_view(request):
	if request.user.is_authenticated:
		return redirect('users:dashboard')
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('users:dashboard')
		else:
			messages.error(request, 'Correct the errors below')
	else:
		form = SignUpForm()

	return render(request, 'app/signup.html', {'form': form})

vectorizer = pickle.load(open(os.path.join(dir_path, "machinelearningmodel/tfidf.pickle"), 'rb'))


tagged_vectors = {0: "Staff Capacity(Helping, good services and friendly)",
                  1: "Service quality and friendliness",
                  2: "Food quality and variety",
                  3: "Helping, meeting needs",
                  4: "Staff Capacity(Helping, good services and friendly)",
                  5: "Satisfied/Dissatisfied overall",
                  6: "No comment",
                  7: "Food quality and variety",
                  8: "Helping, meeting needs",
                  9: "Time management and processes",
                  10: "Supporting teens",
                  11: "Staff Capacity(Helping, good services and friendly)",
                  12: "Satisfied/Dissatisfied overall",
                  13: "Quality of care",
                  14: "Homework support",
                  15: "neutral"}


def tagging_system(txt):

    try:
        global vectorizer, tagged_vectors
        Y = vectorizer.transform([txt])
        loaded_model = pickle.load(open(os.path.join(dir_path,"machinelearningmodel/finalized_kmean_model.sav"), 'rb'))
        prediction = loaded_model.predict(Y)
        return tagged_vectors[prediction[0]]

    except Exception as err:
        return "error"



def sentiment_text(txt):
    sid = SentimentIntensityAnalyzer()
    neg = 0.0
    pos = 0.0
    neu = 0.0
    cop = 0.0
    sentiment = dict(sid.polarity_scores(txt))
    #         print(sentiment)
    cop += sentiment["compound"]
    neg += sentiment["neg"]
    neu += sentiment["neu"]
    pos += sentiment["pos"]

    labels = ['Negative', 'Positive', 'Neutral']

    values = [int(neg * 100), int(pos * 100), int(neu * 100)]
    return [labels, values]


# Display the generated image:
def plot_wordcloud(data):
    # d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='black', width=800, height=360).generate(data)
    return wc.to_image()



def make_image(data):
    img = BytesIO()
    plot_wordcloud(data=data).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())



def data_filter_issue(dataframe, val, col):
    return dataframe[dataframe[col] == val]

def gen_filter(dataframe, male, female, other):
   filter_list = list()
   if male == "on":
     filter_list.append("Male")
   if female == "on":
     filter_list.append("Female")
   if other == "on":
     filter_list.append("Other")

   return dataframe[dataframe["Gender"].isin(filter_list)]


def nps_filter(dataframe, nps_val):
    return dataframe[dataframe["NPS_type"]==nps_val]






@login_required
def download_view(request):
    path = os.path.join(dir_path, "./DataPredictionTagging/" + str(request.user) + "/eaf9047f-e1ef-4bf8-b4c2-3c7a2a752f9d.csv")
    #find latest
    list_of_files = glob.glob(os.path.join(dir_path, "./DataPredictionTagging/" + str(request.user) + '/*'))  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getmtime)
    print(latest_file)
    response = HttpResponse(open(latest_file, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=DownloadedFile.csv'
    return response


@login_required
def dashboard_view(request):
    user = request.user  # get the current login user details
    if user:
        if request.method == 'POST':
            if request.FILES:
                try:
                    file_input = request.FILES['employeefile'].file
                    file_name = request.FILES['employeefile'].name
                    startval = int(request.POST.get('startval'))
                    endval = int(request.POST.get('endval'))

                    startageval = int(request.POST.get('startageval'))
                    endageval = int(request.POST.get('endageval'))
                    rcval = int(request.POST.get('rcval'))

                    rcbool = str(request.POST.get('rcbool'))
                    print(rcbool, rcval)
                    print(startageval, endageval)


                    # return None

                    # Issue Area Filter
                    issue_area_coll1 = str(request.POST.get('IssueAreal1'))
                    issue_area_coll2 = str(request.POST.get('IssueAreal2'))
                    issue_area_coll3 = str(request.POST.get('IssueAreal3'))
                    # issue_area_value = str(request.POST.get('IssueFilterValue'))
                    
                    # gender
                    
                    gender_male = str(request.POST.get('genderM'))
                    gender_female = str(request.POST.get('genderF'))
                    gender_other = str(request.POST.get('genderO'))

                    # NPS_type
                    NPS_type = str(request.POST.get('NPS_type'))

                    # budget_range
                    budget_range = str(request.POST.get('budget_range'))

                    print(gender_male, gender_female, gender_other)

                    # print(file_name)
                    dataframe = None
                    if file_name.endswith(".xlsx"):
                        dataframe = pd.read_excel(file_input)
                    elif file_name.endswith(".csv"):
                        dataframe = pd.read_csv(file_input, skiprows=range(1, startval), nrows=endval)
                    list_of_dict = list()



                    # Gender Insights
                    gender = dict(dataframe["Gender"].value_counts())
                    nps_type = dict(dataframe["NPS_type"].value_counts())
                    race_ethnicity = dict(dataframe["Race/Ethnicity"].value_counts())


                    dataframe["data_sen"] = dataframe['Q2_What is org GOOD AT'] + ' ' + dataframe['Q3_What could org DO BETTER']

                    # prediction tagging
                    dataframe["Theme"] = dataframe["data_sen"].apply(lambda x: tagging_system(str(x)))
                    final_text = " ".join(str(txt) if isinstance(txt, str) else "" for txt in dataframe["data_sen"][:10])
                    sentiment_analysis = sentiment_text(final_text)

                    wordcloud_img = make_image(final_text)

                    # # Issue Filteration
                    if issue_area_coll1 != "Not":
                        dataframe = dataframe[dataframe["Issue Area_SL1"]==issue_area_coll1]
                        
                    if issue_area_coll2 != "Not":
                        dataframe = dataframe[dataframe["Issue Area_SL2"]==issue_area_coll2]

                    if issue_area_coll3 != "Not":
                        dataframe = dataframe[dataframe["Issue Area_SL3"]==issue_area_coll3]


                    # gen_filter
                    if gender_male=="on" or gender_female  =="on" or gender_other =="on":
                        print("done")
                        dataframe = gen_filter(dataframe, gender_male, gender_female, gender_other)
                    

                    # NPS_type
                    if NPS_type != "Not":
                        print(NPS_type)
                        dataframe = nps_filter(dataframe, NPS_type)
                        print(dataframe["NPS_type"])

                                  
                    def age_group_filter(row):
                            try:
                                nonlocal startageval, endageval

                                age_group_list = str(row).split(" ")
                                if len(age_group_list) == 3:
                                    final_val = age_group_list[0].split("-")
                                    start_val = int(final_val[0])
                                    end_val = int(final_val[1])
                                    # print(start_val, end_val)
                                    if start_val >= startageval and end_val <= endageval:
                                        return True;
                                print(len(age_group_list))
                                return False
                            except Exception as err:
                                return False


                    # Age filter on frame
                    dataframe = dataframe[dataframe["Age_groups"].apply(age_group_filter)]

                    # remove column
                    dataframe.pop('data_sen')

                    dataframe.insert(0, 'Theme', dataframe.pop('Theme'))


                    # Region/Community
                    if rcbool=="on":
                        dataframe["Region/Community"] = pd.to_numeric(dataframe["Region/Community"], errors='coerce')
                        dataframe = dataframe[dataframe["Region/Community"] == rcval]

                    
                    if budget_range != "Not":
                        print(budget_range)
                        dataframe = dataframe[dataframe["Annual Budget Range"]==budget_range]
                        
                    header = None
                    for row in dataframe.sample(n=30).to_dict('records'):
                        list_of_dict.append(row.values())
                        header = row.keys()



                    # Tagging Pie Chart data
                    tagg_piechart = dict(dataframe["Theme"].value_counts(normalize=True))






                    content = {
                        "header": header, "row": list_of_dict, "gender": gender, "NPS_type": nps_type,
                        "race_ethnicity": race_ethnicity, "data_sentiment": sentiment_analysis[1],
                        "data_label_sentiment": sentiment_analysis[0],"tag_label":list(tagg_piechart.keys()), "tag_values": list(list(map(lambda num:int(num*100),tagg_piechart.values()))), "wordcloud_img":wordcloud_img
                    }
                    # save user data
                    # mode

                    # print(content["tag_label"], content["tag_values"])


                    # save results put on hold for now.

                    try:
                        path_t = os.path.join(dir_path, "DataPredictionTagging/"+ str(request.user))
                        if not (os.path.exists(path_t) and os.path.isdir(path_t)):
                            os.mkdir(path_t)
                    except Exception as err:
                        pass
                    data_path = os.path.join(dir_path, "DataPredictionTagging/"+ str(request.user) + '/' +str(uuid.uuid4()) + '.csv')
                    dataframe.to_csv(data_path, index=False)
                    return render(request, 'app/dashboard.html', {'content': content})

                except Exception as e:
                    print(e)
                    return render(request, 'app/error.html', {})

    return render(request, 'app/dashboard.html')


def home_view(request):
    return render(request, 'app/home.html')
