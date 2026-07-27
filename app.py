import streamlit as st
from backend import generate_trip
from towns import towns

# Page Configuration
st.set_page_config(
    page_title="ExploreLK AI",
    page_icon="🌿",
    layout="wide"
)

# Sidebar
with st.sidebar:

    st.markdown("""
<div style="text-align:center;">

<h1>🌿 ExploreLK</h1>

<h4>Hidden Gems Planner</h4>

</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📊 Project Overview")

    st.success("""
📄 Knowledge Base

29 PDF Documents
""")
    st.info("""
🤖 AI Agents

4 Intelligent Agents
""")
    st.warning("""
🧠 RAG

Enabled
""")
    st.success("""
⚡ Language Model

Groq Llama 3.3
""")

    st.markdown("---")

    st.subheader("🗺️ About")

    st.write(
        """
        ExploreLK helps travelers discover hidden destinations
        across Sri Lanka and generates personalized travel
        recommendations using LangGraph and Retrieval-Augmented
        Generation (RAG).
        """
    )

    st.markdown("---")

    st.info("🇱🇰 Explore Sri Lanka like never before!")
    st.markdown("---")

# Header
st.markdown("""
<div style="
    background: linear-gradient(135deg,#0f5132,#2e8b57);
    padding:30px;
    border-radius:18px;
    color:white;
    text-align:center;
    box-shadow:0px 4px 12px rgba(0,0,0,0.2);
">

<h1>🌿 ExploreLK</h1>

<h3>Discover Sri Lanka's Hidden Gems</h3>

<p style="font-size:17px;">
Plan unforgettable journeys to breathtaking waterfalls,
mountains, forests, villages, beaches, and other unique
destinations across Sri Lanka.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# User Inputs
with st.container(border=True):

    st.subheader("✈️ Plan Your Journey")

    col1, col2 = st.columns(2)

    with col1:
        budget = st.selectbox(
            "💰 Budget",
            ["Low", "Medium", "High"]
        )

    with col2:
        days = st.selectbox(
            "🗓️ Days",
            ["1", "2", "3", "4", "5+"]
        )

    location = st.selectbox(
    "📍 Starting Location",
    options=towns,
    index=None,
    placeholder="Type or select your town..."
    )

    interests = st.multiselect(
        "🎯 Select Your Interests",
        [
            "Waterfalls",
            "Hiking",
            "Nature",
            "Wildlife",
            "Camping",
            "Photography",
            "Historical Places",
            "Beaches",
            "Villages"
        ]
    )

    generate = st.button(
        "🚀 Generate My Travel Plan",
        use_container_width=True,
        type="primary"
    )

# Generate Travel Plan
if generate:

    if location.strip() == "":
        st.warning("⚠️ Please enter your starting location.")
        st.stop()

    if len(interests) == 0:
        st.warning("⚠️ Please select at least one interest.")
        st.stop()

    with st.spinner("🌿 Generating your personalized travel plan..."):

        try:

            result = generate_trip(
                budget=budget,
                days=days,
                location=location,
                interests=", ".join(interests)
            )

            st.success("✅ Your travel plan is ready!")

            # Recommended Destinations
            st.markdown("## 🌍 Recommended Destinations")

            destinations = result.get("destinations", "")

            with st.container(border=True):
                st.success("📍 Hidden Gems Recommended For You")
                st.markdown(destinations)

            st.write("")

            # Travel Information
            st.markdown("## 📚 Travel Information")

            travel_info = result.get("travel_info", "")

            with st.container(border=True):
                st.info("📖 Travel Guide")
                st.markdown(travel_info)

            st.write("")

            # Suggested Itinerary
            st.markdown("## 🗓️ Suggested Itinerary")

            itinerary = result.get("itinerary", "")

            with st.container(border=True):
                st.warning("🧭 Your Personalized Itinerary")
                st.markdown(itinerary)

        except Exception as e:
            st.error("❌ An error occurred while generating the travel plan.")
            st.exception(e)
