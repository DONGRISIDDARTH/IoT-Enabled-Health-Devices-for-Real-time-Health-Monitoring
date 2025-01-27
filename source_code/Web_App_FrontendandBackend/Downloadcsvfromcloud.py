#Code to download csv file from the object storage in Google cloud

from google.cloud import storage

# Replace 'path/to/service_account.json' with the path to your service account key file
client = storage.Client.from_service_account_json('centering-sweep-420320-9a1744a337f8.json')

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Google Cloud Storage bucket."""
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name}.')

upload_blob('rfid_project', 'C:\\Users\\VB\\Documents\\vscode_workspace\\MTech CSE\\IOT Project\\all_readers_data.csv', 'RFID_Data_28thApril_2024/10pm_28April.csv')