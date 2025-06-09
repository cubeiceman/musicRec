import pandas
import numpy
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



try:
    df = pandas.read_csv("./archive/Music Info.csv")
except FileNotFoundError:
    print("Error: file not found. Please check the file path.")
    exit()

df.rename(columns={
    'track_id': 'track_id',
    'artist': 'artist',
    'name': 'song_name',
    'spotify_preview_url': 'spotify_preview_url',
    'spotify_id': 'spotify_id',
    'tags': 'tags',
    'genre': 'genre',
    '# year': 'year_published',
    '# duration_ms': 'duration_ms',
    '# danceability': 'danceability'
}, inplace=True)

for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].replace(r'(?i)^nan$', numpy.nan, regex=True)
    if col in ['danceability', 'duration_ms']:
        df[col] = pandas.to_numeric(df[col], errors='coerce')

initial_rows = len(df)
df.dropna(subset=['track_id', 'artist', 'song_name', 'tags', 'duration_ms', 'danceability'], inplace=True)

numerical_features_for_scaling = ['danceability', 'duration_ms']
existing_numerical_features = [col for col in numerical_features_for_scaling if col in df.columns]

for col in existing_numerical_features:
    if df[col].isnull().any():
        df[col].fillna(df[col].mean(), inplace=True)
        print(f"Filled missing values in '{col}' with its mean.")

if 'tags' in df.columns:
    df['tags'] = df['tags'].astype(str).fillna('')
else:
    df['tags'] = ''
if 'genre' in df.columns:
    df['genre'] = df['genre'].astype(str).fillna('')
else:
    df['genre'] = ''

df['combined_text_features'] = (df['tags'].str.lower().str.replace(',', ' ').str.replace('  ', ' ') +
                                ' ' + df['genre'].str.lower())

scaler = MinMaxScaler()
for col in existing_numerical_features:
    df[f'{col}_scaled'] = scaler.fit_transform(df[[col]])

scaled_numerical_cols = [f'{col}_scaled' for col in existing_numerical_features]
print("\nData preprocessing complete.")

tfidf_vectorizer = TfidfVectorizer(stop_words='english', min_df=5)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_text_features'])
print(f"\nTF-IDF matrix shape: {tfidf_matrix.shape}")

numerical_features_array = df[scaled_numerical_cols].values

if tfidf_matrix.shape[0] != numerical_features_array.shape[0]:
    print("Error: Mismatch in number of rows between TF-IDF matrix and numerical features. Exiting.")
    exit()

features_matrix = numpy.hstack((tfidf_matrix.toarray(), numerical_features_array))
print(f"Combined features matrix shape: {features_matrix.shape}")

cosine_sim_matrix = cosine_similarity(features_matrix)
cosine_sim_df = pandas.DataFrame(cosine_sim_matrix)
print("\nCosine similarity matrix calculated!")


def get_similar_songs(song_name_input, df_original, cosine_sim_df, top_n=4):
    # Find all indices of songs matching the input (case-insensitive, partial match)
    song_indices = df_original[
        df_original['song_name'].str.contains(song_name_input, case=False, na=False)].index.tolist()

    if not song_indices:
        print(f"Song '{song_name_input}' not found in the dataset. Please try a different title or a more precise one.")
        return pandas.DataFrame()

    # If multiple songs match, choose the first one for demonstration.
    # In a user-facing app, you might ask the user to pick from a list.
    if len(song_indices) > 1:
        print(f"Multiple songs found matching '{song_name_input}'. Using the first match:")
        for i, idx in enumerate(song_indices):
            print(f"  {i + 1}. '{df_original.loc[idx]['song_name']}' by {df_original.loc[idx]['artist']}")
        song_idx = song_indices[0]  # Select the first match
        print(f"Selected: '{df_original.loc[song_idx]['song_name']}' by {df_original.loc[song_idx]['artist']}")
    else:
        song_idx = song_indices[0]

    original_song_info = df_original.loc[song_idx]

    print(
        f"\n--- Finding similar songs for: '{original_song_info['song_name']}' by "
        f"{original_song_info['artist']} ---")

    # Get similarity scores for the chosen song from the pre-calculated matrix
    sim_scores = cosine_sim_df[song_idx].sort_values(ascending=False)

    # Exclude the song itself from the recommendations (similarity score will be 1.0)
    sim_scores = sim_scores.drop(song_idx)

    # Get the top_n most similar songs by their indices
    top_similar_songs_indices = sim_scores.head(top_n).index

    # Retrieve the full song details for the recommended songs from the original DataFrame
    # Use .copy() to ensure we're working on a copy and avoid SettingWithCopyWarning
    recommended_songs = df_original.loc[top_similar_songs_indices].copy()

    # Add the similarity score as a new column to the recommended songs DataFrame
    recommended_songs['similarity_score'] = sim_scores.head(top_n).values

    # Define the columns to display in the output, in a readable order
    display_cols = [
        'song_name', 'artist', 'genre', 'tags', 'danceability',
        'duration_ms', 'similarity_score', 'spotify_preview_url'
    ]
    # Filter display_cols to ensure only existing columns are included
    display_cols = [col for col in display_cols if col in recommended_songs.columns]

    return recommended_songs


# --- Example Usage ---
# You can change this song name to test different recommendations from your dataset
def recommendations(song_name, dataframe=df, cosine_sim_df=cosine_sim_df):
    recommended = get_similar_songs(song_name, dataframe, cosine_sim_df)

    if not recommended.empty:
        return {"song_name": recommended["song_name"].tolist(),
                "artist": recommended["artist"].tolist(),
                "preview": recommended["spotify_preview_url"].tolist()}
    else:
        return "No recommendations found."
