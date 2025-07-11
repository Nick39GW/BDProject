from nick_api_utils import search_movies, get_watchmode_id_by_imdb, get_streaming_sources
import streamlit as st
import base64


def set_background(image_file: str):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

        st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(
                rgba(0, 0, 0, 0.75), 
                rgba(0, 0, 0, 0.75)
            ),
            url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


st.set_page_config(layout="wide", page_title="Movie Explorer", page_icon="🎬")
set_background("app/background_picture.png")

st.title("🎬 Movie Explorer")

title = st.text_input("Enter a movie title")

GENRES = ["Action", "Adventure", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller"]
PLATFORMS = ["Netflix", "Amazon Prime", "Disney+", "HBO Max", "Apple TV+"]

selected_genres = st.multiselect("🎭 Select genre(s)", GENRES)
selected_platforms = st.multiselect("📺 Select streaming platform(s)", PLATFORMS)

if st.button("Search"):
    query = title.strip()

    if not query and not selected_genres and not selected_platforms:
        st.warning("Please enter a movie title or choose at least one filter.")
    else:
        st.markdown(f"🔎 Searching for: **{query if query else 'Popular Movies'}**...")
        with st.spinner("Searching..."):
            if query:
                results = search_movies(query)
            else:
                default_titles = ["Inception", "The Matrix", "Avengers", "Titanic", "Interstellar"]
                results = []
                for name in default_titles:
                    results.extend(search_movies(name))

        if not results:
            st.error("❌ No results found.")
        else:
            st.success(f"✅ Found following result(s):")

            sorted_results = sorted(
                results,
                key=lambda x: (x.get("numVotes") or 0, x.get("averageRating") or 0),
                reverse=True
            )

            shown = 0

            for movie in sorted_results:
                genres_list = movie.get("genres") or []

                # If genres selected and no match → skip
                if selected_genres and not any(g in selected_genres for g in genres_list):
                    continue

                # Check streaming platforms
                watchmode_id = get_watchmode_id_by_imdb(movie.get("id"))
                sources = get_streaming_sources(watchmode_id) if watchmode_id else []
                sub_sources = [s for s in sources if s.get("type") == "sub"]
                source_names = [s.get("name") for s in sub_sources if s.get("name")]

                # If platforms selected and no match → skip
                if selected_platforms and not any(p in source_names for p in selected_platforms):
                    continue

                # --- Passed all filters, display movie ---
                movie_title = movie.get('primaryTitle', 'Unknown')
                year = movie.get('startYear', 'N/A')
                st.markdown(f"### 🎬 {movie_title} ({year})")

                img_data = movie.get("primaryImage")
                img_url = img_data.get("url") if isinstance(img_data, dict) else img_data

                col1, col2 = st.columns([1, 3])
                with col1:
                    if img_url:
                        st.image(img_url, width=220)

                with col2:
                    genres = ", ".join(genres_list) if genres_list else "N/A"
                    st.markdown(f"**Genres:** {genres}")
                    rating = movie.get("averageRating", "N/A")
                    votes = movie.get("numVotes")
                    vote_text = f"{votes:,} votes" if isinstance(votes, int) else "No votes"
                    st.markdown(f"**Rating:** {rating} ⭐ ({vote_text})")
                    description = movie.get("description") or "No description available."
                    st.markdown(f"**Description:** {description}")
                    imdb_url = movie.get("url")
                    if imdb_url:
                        st.markdown(f"🔗 [IMDb Page]({imdb_url})")

                    if sub_sources:
                        st.markdown("📺 **Available on:**")
                        platform_logos = {
                            "Netflix": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
                            "Amazon Prime": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Prime_Video.png",
                            "Disney+": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg",
                            "HBO Max": "https://upload.wikimedia.org/wikipedia/commons/1/17/HBO_Max_Logo.svg",
                            "Apple TV+": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Apple_TV_Plus_Logo.svg",
                        }

                        unique_platforms = {}
                        for s in sub_sources:
                            name = s.get("name")
                            if name not in unique_platforms:
                                unique_platforms[name] = platform_logos.get(name)

                        cols = st.columns(min(len(unique_platforms), 5))
                        for i, (name, logo) in enumerate(unique_platforms.items()):
                            with cols[i % len(cols)]:
                                if logo:
                                    st.image(logo, width=80)
                                else:
                                    st.markdown(f"- {name}")

                shown += 1
                st.markdown("---")

            if shown == 0:
                st.info("No results matched your filters. Try adjusting your genre or platform selections.")
