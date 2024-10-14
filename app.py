import pickle
import streamlit as st
import numpy as np

st.header('📚  Book Recommender System Using Machine Learning')

# Load your pickled data
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_names.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))

# Fetch poster function
def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url

# Recommend books function
def recommend_book(book_name, sort_by):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    poster_url = fetch_poster(suggestion)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)

    # Apply sorting criteria
    if sort_by == "Alphabetical":
        books_list.sort()
    elif sort_by == "Year of Publication":
        # Sort by year by fetching the year of each book from final_rating
        books_list.sort(key=lambda x: final_rating[final_rating['title'] == x]['year'].values[0])

    return books_list, poster_url

# Add sorting options
sort_by = st.selectbox(
    "Sort recommendations by:",
    ["Default", "Alphabetical", "Year of Publication"]
)

# Select a book from the dropdown
selected_books = st.selectbox("Type or select a book from the dropdown", book_names)

# Show recommendations on button click
if st.button('Show Recommendation'):
    recommended_books, poster_url = recommend_book(selected_books, sort_by)
    
    # Create columns to display books and their images
    col1, col2, col3, col4, col5 = st.columns(5)

    # Function to create Amazon link for each book
    def get_amazon_link(book_name):
        search_query = book_name.replace(" ", "+")
        return f"https://www.amazon.com/s?k={search_query}&i=stripbooks"

    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
        st.markdown(f'<a href="{get_amazon_link(recommended_books[1])}" target="_blank">Buy on Amazon</a>', unsafe_allow_html=True)

    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])
        st.markdown(f'<a href="{get_amazon_link(recommended_books[2])}" target="_blank">Buy on Amazon</a>', unsafe_allow_html=True)

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
        st.markdown(f'<a href="{get_amazon_link(recommended_books[3])}" target="_blank">Buy on Amazon</a>', unsafe_allow_html=True)

    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
        st.markdown(f'<a href="{get_amazon_link(recommended_books[4])}" target="_blank">Buy on Amazon</a>', unsafe_allow_html=True)

    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])
        st.markdown(f'<a href="{get_amazon_link(recommended_books[5])}" target="_blank">Buy on Amazon</a>', unsafe_allow_html=True)
