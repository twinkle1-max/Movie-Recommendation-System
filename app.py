from flask import Flask, request, render_template
import requests
import pandas as pd 
from patsy import dmatrices
import pickle

movies = pickle.load(open('model/movies_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances =sorted(list(enumerate(similarity[index])), reverse = True, key=lambda x: x[1])

    recommended_movies_name=[]
    

    for i in distances [1:7]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name




app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route ('/recommendation' , methods = ['GET', 'POST'])
def recommendation():
    movie_list = movies['title'].values

    status = False

    if request .method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)

                recommended_movies_name = recommend(movies_name)
                print(recommended_movies_name)
            
                status = True


                return render_template('recommendation.html', movies_name = recommended_movies_name, movie_list = movie_list, status =  status)
                
                

        except Exception as e:
            error = {'error': e}
            return render_template('recommendation.html', error = error, movie_list= movie_list, status =  status)
        
    else:
        return render_template('recommendation.html', movie_list= movie_list, status =  status)


    
    

@app.route('/contact')
def contact():
    return render_template('contact.html')





if __name__ == "__main__":
    app.debug= True
    app.run()


