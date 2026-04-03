import streamlit as st
import random
import json
from datetime import datetime

# Movie database (simplified for demo)
MOVIES = {
    "Action": [
        {"title": "Avengers: Endgame", "year": 2019, "rating": 8.4, "description": "The Avengers assemble for the ultimate battle against Thanos."},
        {"title": "John Wick: Chapter 4", "year": 2023, "rating": 7.7, "description": "John Wick uncovers a path to defeat the High Table."},
        {"title": "Mission: Impossible - Dead Reckoning", "year": 2023, "rating": 7.7, "description": "Ethan Hunt races against time to stop a rogue AI."}
    ],
    "Comedy": [
        {"title": "Superbad", "year": 2007, "rating": 7.6, "description": "Two co-dependent high school guys navigate their last night before college."},
        {"title": "The Hangover", "year": 2009, "rating": 7.7, "description": "Three groomsmen lose their about-to-be-wedded pal in Las Vegas."},
        {"title": "Deadpool", "year": 2016, "rating": 8.0, "description": "A wise-cracking mercenary comes back from the dead."}
    ],
    "Drama": [
        {"title": "The Shawshank Redemption", "year": 1994, "rating": 9.3, "description": "Two imprisoned men bond over decades in Shawshank prison."},
        {"title": "Forrest Gump", "year": 1994, "rating": 8.8, "description": "The history of the US from the perspective of an Alabama man."},
        {"title": "The Pursuit of Happyness", "year": 2006, "rating": 8.0, "description": "A struggling salesman takes custody of his son as he's poised to begin a life-changing professional career."}
    ],
    "Sci-Fi": [
        {"title": "Dune", "year": 2021, "rating": 8.0, "description": "A young nobleman must survive on the desert planet Arrakis."},
        {"title": "Interstellar", "year": 2014, "rating": 8.7, "description": "A team of explorers travel through a wormhole in space."},
        {"title": "The Matrix", "year": 1999, "rating": 8.7, "description": "A computer hacker learns from mysterious rebels about the true nature of his reality."}
    ],
    "Horror": [
        {"title": "Hereditary", "year": 2018, "rating": 7.3, "description": "A family's unsettling reunion leads to dark secrets."},
        {"title": "The Conjuring", "year": 2013, "rating": 7.5, "description": "Paranormal investigators Lorraine and Ed Warren confront a powerful entity."},
        {"title": "Get Out", "year": 2017, "rating": 7.8, "description": "A young African-American man uncovers shocking secrets when he meets his girlfriend's family."}
    ]
}

# Session state to maintain conversation
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_stage" not in st.session_state:
    st.session_state.conversation_stage = "greeting"
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {}
if "recommendations_shown" not in st.session_state:
    st.session_state.recommendations_shown = False

# Streamlit app title
st.title("🎬 MovieBot - Your Personal Movie Recommender")
st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What kind of movies are you in the mood for?"):

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response based on conversation stage
    response = generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)

def generate_response(user_input):
    user_input_lower = user_input.lower()
    
    if st.session_state.conversation_stage == "greeting":
        st.session_state.conversation_stage = "genre_selection"
        return """🎉 Hi there, movie lover! I'm MovieBot, your personal movie recommendation assistant!

I can help you find the perfect movie based on:
- **Genre** (Action, Comedy, Drama, Sci-Fi, Horror, etc.)
- **Mood** (funny, thrilling, emotional, etc.) 
- **Actors/Directors**
- **Recent releases** or **classics**

**What kind of movies are you in the mood for today?** 🎥"""

    elif st.session_state.conversation_stage == "genre_selection":
        # Detect genre or mood
        genre_keywords = {
            "action": "Action", "thriller": "Action", "exciting": "Action", "intense": "Action",
            "comedy": "Comedy", "funny": "Comedy", "hilarious": "Comedy", "laugh": "Comedy",
            "drama": "Drama", "emotional": "Drama", "sad": "Drama", "touching": "Drama",
            "sci-fi": "Sci-Fi", "science fiction": "Sci-Fi", "space": "Sci-Fi", "futuristic": "Sci-Fi",
            "horror": "Horror", "scary": "Horror", "creepy": "Horror", "spooky": "Horror"
        }
        
        detected_genre = None
        for keyword, genre in genre_keywords.items():
            if keyword in user_input_lower:
                detected_genre = genre
                break
        
        if detected_genre and detected_genre in MOVIES:
            st.session_state.user_preferences["genre"] = detected_genre
            st.session_state.conversation_stage = "recommendations"
            return f"🎬 Perfect choice! I love **{detected_genre}** movies too! Here are my top 3 recommendations for you:\n\n" + format_recommendations(get_recommendations(detected_genre))
        
        else:
            # Ask for clarification
            return """Hmm, I'm not sure about that genre yet! 😅 

I have these genres available:
🎭 **Action** | 😂 **Comedy** | 😢 **Drama** | 🚀 **Sci-Fi** | 👻 **Horror**

**Could you pick one of these, or tell me your mood?** (funny, scary, emotional, etc.)"""

    elif st.session_state.conversation_stage == "recommendations":
        if "like" in user_input_lower or "love" in user_input_lower:
            return "🎉 Awesome! Glad you found something you like! Want more recommendations in this genre or try something different?"
        elif "dislike" in user_input_lower or "not" in user_input_lower:
            return "😕 No worries! Taste is personal. Want to try a different genre or tell me more about what you like?"
        elif any(word in user_input_lower for word in ["another", "more", "next"]):
            genre = st.session_state.user_preferences.get("genre", "Action")
            return f"Here are {len(MOVIES[genre])} more {genre} recommendations:\n\n" + format_recommendations(get_recommendations(genre))
        else:
            return """What did you think of those recommendations? 
- Say **"I like [movie]"** or **"Show me more"**
- Say **"Try another genre"** or **"Something different"**
- Or tell me about your favorite movies/actors! 🎥"""

def get_recommendations(genre):
    """Get 3 random recommendations from the specified genre"""
    return random.sample(MOVIES[genre], min(3, len(MOVIES[genre])))

def format_recommendations(movies):
    """Format movie recommendations nicely"""
    formatted = ""
    for i, movie in enumerate(movies, 1):
        formatted += f"""
**{i}. {movie['title']} ({movie['year']})** ⭐{movie['rating']}
{movie['description']}

🔗 *Watch on: Netflix, Amazon Prime, or your local cinema*
---
"""
    formatted += "\n**Which one sounds good? Or say 'more' for additional suggestions!** 🎬"
    return formatted

# Sidebar with conversation info
with st.sidebar:
    st.header("🤖 MovieBot Status")
    st.write(f"**Stage:** {st.session_state.conversation_stage.replace('_', ' ').title()}")
    st.write(f"**Genre Preference:** {st.session_state.user_preferences.get('genre', 'Not set')}")
    st.write(f"**Messages:** {len(st.session_state.messages)}")
    
    if st.button("🆕 New Conversation"):
        st.session_state.messages = []
        st.session_state.conversation_stage = "greeting"
        st.session_state.user_preferences = {}
        st.session_state.recommendations_shown = False
        st.rerun()

# Footer
st.markdown("---")
st.markdown("*Powered by Blackbox AI - Movie Recommendation Chatbot*")
