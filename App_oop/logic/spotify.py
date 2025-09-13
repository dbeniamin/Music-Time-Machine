import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
from ..config.settings import get_app_data_dir
from ..logic.billboard import get_songs

class SpotifyClient:
    def __init__(self, client_id, client_secret, app_instance=None):
        cache_path = str(get_app_data_dir() / "token.txt")
        if not client_id or not client_secret:
            raise ValueError("Spotify credentials are required")

        self.redirect_uri = "https://example.com/callback"
        self.app = app_instance

        self.auth_manager = SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri=self.redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            cache_path=cache_path,
            show_dialog=True,
        )

        # Use cached token if available
        token_info = self.auth_manager.get_cached_token()
        if token_info and not self.auth_manager.is_token_expired(token_info):
            self.sp = spotipy.Spotify(auth=token_info["access_token"])
        else:
            # Prompt user only if no valid cached token
            auth_url = self.auth_manager.get_authorize_url()
            webbrowser.open(auth_url)

            if self.app:
                redirect_response = self.app.get_oauth_url_from_user(auth_url)
            else:
                redirect_response = input(
                    "Paste the full redirect URL after Spotify login: "
                ).strip()

            code = self.auth_manager.parse_response_code(redirect_response)
            token_info = self.auth_manager.get_access_token(code, as_dict=True)
            self.sp = spotipy.Spotify(auth=token_info["access_token"])

    # ---------------------------
    # Create playlist from Billboard (titles-only)
    # ---------------------------
    def create_playlist_from_billboard(self, date: str):
        songs = get_songs(date)  # list of titles
        year = date.split("-")[0]
        user_id = self.sp.me()["id"]

        playlist = self.sp.user_playlist_create(
            user=user_id,
            name=f"Billboard Hot 100 - {date}",
            public=False,
            description=f"Top 100 songs from Billboard on {date}"
        )

        track_uris = []
        not_found = []

        for title in songs:
            query = f"track:{title} year:{year}"
            result = self.sp.search(q=query, type="track", limit=1)
            items = result.get("tracks", {}).get("items")
            if items:
                track_uris.append(items[0]["uri"])
            else:
                not_found.append(title)

        if not track_uris:
            raise Exception("No songs found on Spotify")

        # Add in batches of 100
        for i in range(0, len(track_uris), 100):
            self.sp.playlist_add_items(playlist["id"], track_uris[i:i+100])

        print(f"{len(not_found)} songs were not found on Spotify.")  # optional log
        return len(track_uris)
