import os
import requests


SUPABASE_URL = "https://prnnymcaxwytzxnqhxxo.supabase.co"
SUPABASE_REST_URL = SUPABASE_URL + "/rest/v1"
SUPABASE_PUBLISHABLE_KEY = "sb_publishable_B0Pc0up_thPRxp-M30wD-Q_3NHau0bJ"

TIMEOUT = 20


class SupabaseClient:

    def __init__(self):
        self.headers = {
            "apikey": SUPABASE_PUBLISHABLE_KEY,
            "Authorization": "Bearer " + SUPABASE_PUBLISHABLE_KEY,
        }

    def _json_headers(self):
        headers = dict(self.headers)
        headers["Content-Type"] = "application/json"
        return headers

    def upsert_profile(self, profile_id, name=""):
        response = requests.post(
            SUPABASE_REST_URL + "/profiles",
            headers={
                **self._json_headers(),
                "Prefer": "resolution=merge-duplicates,return=minimal",
            },
            json={
                "profile_id": profile_id,
                "name": name or "",
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()

    def upload_file(self, local_path, remote_path):
        with open(local_path, "rb") as file:
            data = file.read()

        response = requests.post(
            SUPABASE_URL + "/storage/v1/object/items/" + remote_path,
            headers={
                **self.headers,
                "Content-Type": "application/octet-stream",
                "x-upsert": "true",
            },
            data=data,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return remote_path

    def download_file(self, remote_path, local_path):
        response = requests.get(
            SUPABASE_URL + "/storage/v1/object/items/" + remote_path,
            headers=self.headers,
            timeout=TIMEOUT,
        )
        response.raise_for_status()

        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with open(local_path, "wb") as file:
            file.write(response.content)

        return local_path

    def create_transfer(
        self,
        transfer_id,
        sender_profile_id,
        recipient_profile_id,
        name,
        category,
        location,
        description,
        image_path,
    ):
        response = requests.post(
            SUPABASE_REST_URL + "/item_transfers",
            headers={
                **self._json_headers(),
                "Prefer": "return=minimal",
            },
            json={
                "transfer_id": transfer_id,
                "sender_profile_id": sender_profile_id,
                "recipient_profile_id": recipient_profile_id,
                "name": name,
                "category": category or "",
                "location": location or "",
                "description": description or "",
                "image_path": image_path or "",
                "status": "sent",
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()

    def get_pending_transfers(self, recipient_profile_id):
        response = requests.get(
            SUPABASE_REST_URL + "/item_transfers",
            headers=self.headers,
            params={
                "recipient_profile_id": "eq." + recipient_profile_id,
                "status": "eq.sent",
                "order": "created_at.asc",
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def mark_transfer_received(self, transfer_id):
        response = requests.patch(
            SUPABASE_REST_URL + "/item_transfers",
            headers={
                **self._json_headers(),
                "Prefer": "return=minimal",
            },
            params={
                "transfer_id": "eq." + transfer_id,
            },
            json={
                "status": "received",
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()
