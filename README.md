

🎬 AI Movie Recommendation System
📌 Overview

The AI Movie Recommendation System is a content-based recommendation engine that suggests movies based on similarity in movie overviews.
The system uses TF-IDF Vectorization and Cosine Similarity to compute similarity scores and recommend relevant movies.
The web interface is built using Streamlit and integrates movie posters using the TMDB API.

🚀 Features

🎥 Movie-based recommendations
🎭 Genre filtering
⭐ Movie ratings display
🖼️ Dynamic poster fetching via TMDB API
⚡ Fast similarity computation using TF-IDF
🌐 Clean interactive UI

🧠 How It Works
1. Movie metadata is preprocessed and stored in movies.pkl
2. Overview text is converted into TF-IDF vectors
3. Cosine similarity is calculated dynamically
4. Top similar movies are displayed with:
Poster
Title
Rating

------------------

🛠️ Tech Stack

Technology	Purpose

Python	Core Programming
Pandas	Data Handling
NumPy	Numerical Operations
Scikit-learn	TF-IDF & Similarity
Streamlit	Web Interface
TMDB API	Movie Posters



---

📂 Project Structure

AI-Movie-Recommendation-System/
│
├── app.py
├── movies.pkl
├── requirements.txt
└── README.md


---

▶️ Installation & Setup

1️⃣ Clone the Repository

git clone https://aaditya2411-gkybhjbexgydyxpxtbymbf.streamlit.app/

2️⃣ Navigate to Project Folder

cd AI-Movie-Recommendation-System

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Run the App

streamlit run app.py


---

🔐 API Key Setup

To fetch movie posters:

1. Create an account on TMDB
2. Generate your API key
3. Replace in app.py:
TMDB_API_KEY = "your_api_key_here"
--------------

🌍 Deployment

This project is fully compatible with:

Streamlit Cloud

Render

Railway

Localhost



---

👨‍💻 Author

Aaditya Kumar Singh
Naveen Kumar @Tf141Naveen
Keti Aditya @Keti23Aditya
Nikhil Raj @nikhilraj475
Madhusmita Behera @madhusmita1042
Samridhi Sinha @samridhi5-cmd

B.Tech CSE (AI & DS)


---

📈 Future Improvements

Add collaborative filtering

Add user login system

Save watch history

Improve UI with animations

Add search bar



---

📜 License

This project is developed for educational and academic purposes.


