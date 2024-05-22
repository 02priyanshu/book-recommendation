from flask import Flask, render_template, request, session
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

try:
    popular_df = pd.read_pickle(open("C:\\Users\\Priyanshul\\OneDrive\\Desktop\\Recommender_system\\popular.pkl", 'rb'))
    pt = pd.read_pickle(open("C:\\Users\\Priyanshul\\OneDrive\\Desktop\\Recommender_system\\pt.pkl", 'rb'))
    books = pd.read_pickle(open("C:\\Users\\Priyanshul\\OneDrive\\Desktop\\Recommender_system\\books.pkl", 'rb'))
    similarity_scores = pd.read_pickle(
        open("C:\\Users\\Priyanshul\\OneDrive\\Desktop\\Recommender_system\\similarity_scores.pkl", 'rb'))
except FileNotFoundError as e:
    print("One or more files not found:", e)




def get_random_books():
    # Select 8 random books
    random_books = random.sample(popular_df, 8)
    return random_books

@app.route('/')
def user():
    return render_template('user.html')

@app.route('/index')
def index():
    if 'recommendations' in session:
        books_to_display = session['recommendations']
    else:
        # Replace this with your code to select 4 random books
        books_to_display = get_random_books()

    return render_template('index.html', books=books_to_display,
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )




@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')

    try:
        index = np.where(pt.index == user_input)[0][0]
    except IndexError:
        # Handle the case where the user input is not found in the dataset
        error_message = "Sorry, the book you entered is not available in our database."
        return render_template('recommend.html', error_message=error_message)

    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    similar_items1 = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    data1 = []
    for i in similar_items1:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data1.append(item)

    print(data1)
    session['recommendations'] = data1
    return render_template('recommend.html', data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
