from lib.youtube.api_types.video_meta import VideoMeta
from lib.youtube.api_types.video_live import VideoLive
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import http.client as httplib
import httplib2
import os
import random
import time

class YoutubeAPI:
    def __init__(self, secrets_path: str, credential_path: str):
        self.secrets_path = secrets_path
        self.credential_path = credential_path
        args = argparser.parse_args()
        self.youtube = self.__get_authenticated_service(args)

    def __get_authenticated_service(self, args):
        flow = flow_from_clientsecrets(self.secrets_path,
            scope="https://www.googleapis.com/auth/youtube.upload",
            message="Client secrets file missing!")

        storage = Storage(self.credential_path)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage, args)

        return build("youtube", "v3",
            http=credentials.authorize(httplib2.Http()))
    
    def upload_video(self, video_meta: VideoMeta) -> VideoLive:
        valid_visibilities = ("public", "private", "unlisted")
        if video_meta.visibility not in valid_visibilities:
            print("[WARN] Invalid video visibility, setting to private")
            video_meta.visibility = "private"
            
        body=dict(
            snippet=dict(
            title=video_meta.title,
            description=video_meta.description,
            tags=video_meta.tags,
            defaultLanguage=video_meta.default_language
            ),
            status=dict(
            privacyStatus=video_meta.visibility,
            embeddable=video_meta.embeddable,
            publicStatsViewable=video_meta.public_stats
            )
        )

        insert_request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(video_meta.video_path, chunksize=-1, resumable=True)
        )
        return self.resumable_upload(insert_request)

    def resumable_upload(self, insert_request) -> VideoLive:
        httplib2.RETRIES = 1
        max_retries = 10
        retriable_exceptions = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                                httplib.IncompleteRead, httplib.ImproperConnectionState,
                                httplib.CannotSendRequest, httplib.CannotSendHeader,
                                httplib.ResponseNotReady, httplib.BadStatusLine)
        retriable_status_codes = [500, 502, 503, 504]

        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print(f"Video was successfully uploaded.")
                    else:
                        exit(f"The upload failed with an unexpected response: {response}")
            except HttpError as e:
                if e.resp.status in retriable_status_codes:
                    error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
                else:
                    raise
            except retriable_exceptions as e:
                error = f"A retriable error occurred: {e}"

            if error is not None:
                print(error)
                retry += 1
                if retry > max_retries:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print(f"Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)
        return VideoLive(response)
