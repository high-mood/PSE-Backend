"""For the first week sprint, we want a very basic analysis of spotify song 'mood'/'emotion'
The spotify API audio-features request for a track gives us the following:
{
  "danceability" : 0.588,
  "energy" : 0.352,
  "key" : 6,
  "loudness" : -13.197,
  "mode" : 0,
  "speechiness" : 0.0546,
  "acousticness" : 0.566,
  "instrumentalness" : 0.924,
  "liveness" : 0.111,
  "valence" : 0.581,
  "tempo" : 170.710,
  "type" : "audio_features",
  "id" : "0Sual1ICmnvv1bZ8IEZsS5",
  "uri" : "spotify:track:0Sual1ICmnvv1bZ8IEZsS5",
  "track_href" : "https://api.spotify.com/v1/tracks/0Sual1ICmnvv1bZ8IEZsS5",
  "analysis_url" : "https://api.spotify.com/v1/audio-analysis/0Sual1ICmnvv1bZ8IEZsS5",
  "duration_ms" : 89438,
  "time_signature" : 4
}
For a very basic model of mood we make direct use of some of these parameters.
The most important will be: valence, energy, danceability
Less important (but still usable): loudness, speechiness, acousticness, instrumentalness, liveness, tempo
(Energy, Positivity) Will be relative (+ or -) to:
Energy: +energy, +loudness, +tempo, +danceability, -speechiness
Positivity: +valence, -speechiness, +-mode(1=major, 0=minor)

For this model, I will assume the audio-features to be delivered in a dict data-type, we will have to see
how exactly we can extract the data from the prometheus database, and then possibly change the implementation
a to suit the eventual format."""
# import spotipy

# spotify = spotipy.Spotify(auth="BQAvltxhcFX1Df5ieXYG6GXfxhI9rsaxabYWIRv-KY9CEpAa9DnVL8vAqottjTItcthZ-F1YrpolSRfj8ql00PjIb8Ofdm4WlpcjtoQmDv40k-judIMNHJYAOf41e4dwh6sZ3DEwEj2pEyrxlSJwTRU")


# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])

#Audio-features 1 (Song: Jinsang - Bliss)
af1 = {"danceability" : 0.588,
       "energy" : 0.352,
       "key" : 6,
       "loudness" : -13.197,
       "mode" : 0,
       "speechiness" : 0.0546,
       "acousticness" : 0.566,
       "instrumentalness" : 0.924,
       "liveness" : 0.111,
       "valence" : 0.581,
       "tempo" : 170.710}

# Example weights for the different parameters for energy and positivity,
# perhaps we should use some kind of ML-implementation to get ideal weights
def get_energy(af):
    return 3*af['energy'] + af['danceability'] + (af['tempo']-130)/60 - af['speechiness'] + 1

def get_positivity(af):
    return 4*af['valence'] + 2*af['mode'] - af['speechiness'] - 1
                

def analyse_mood(af):
    energy = get_energy(af)
    positivity = get_positivity(af)
    return (energy, positivity)

print(analyse_mood(af1))

