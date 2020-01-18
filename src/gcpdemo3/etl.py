import io
from typing import List
from google.cloud import translate_v2 as translate
from google.cloud import storage
from google.cloud.storage import Bucket

def authenticate_gcs() -> storage.Client:
    """Creates Python Client Object to access GCS API
    Returns:
      Object representing GCS Client
    """
    return storage.Client()

def get_gcs_object(gcs_client: storage.Client,
                   bucket_name: str,
                   file_name: str) -> io.StringIO:
    """Downloads object file from GCS.
    Args:
        gcs_client: google.cloud.storage.Client
        bucket_name: String representing bucket name.
        file_name: String representing file name.
    Returns:
        file like object 
    """
    bucket = gcs_client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_name)
    return io.StringIO(blob.download_as_string())

def put_gcs_object(gcs_client: storage.Client,
                   bucket_name: str,
                   file_name: str,
                   lines: List[str]):
    """Put object file from GCS.
    Args:
        gcs_client: google.cloud.storage.Client
        bucket_name: String representing bucket name.
        file_name: String representing file name.
    """
    bucket = gcs_client.get_bucket(bucket_name)
    object = bucket.blob(file_name)
    object.upload_from_string(lines, content_type='text/plain')

def process_book(bucket, in_file_name, out_file_name):
    """
    Process a single book file and write process file
    Args:
        bucket: GCS bucket name
        in_file_name: input file name for the book file
        out_file_name: output file name for the processed book
    Returns:
    """
    # fetch file from GCS
    gcs_client = authenticate_gcs()
    downloaded_file = get_gcs_object(gcs_client, bucket, in_file_name)

    # skip first 15 header lines
    lines = downloaded_file.readlines()[15:]

    # get rid of head, tail, underscores, commas, and quotation marks
    lines = list(map(
        lambda line: line.strip().split('>')[1].split('<')[0].replace('_', '').replace(',', '').replace('"',
                                                                                                        ''),
        lines
    ))

    # filter out lines less than 10 words and greater than 25 words
    lines = list(filter(
        lambda line: (len(line.split()) > 10) & (len(line.split()) < 25),
        lines
    ))

    # add newline to each line and write to file
    lines = list(map(
        lambda line: f'{line}\n',
        lines
    ))
    put_gcs_object(gcs_client, bucket, out_file_name, lines)


def translate_book(credentials, bucket, in_file_name, out_file_name, source, target, chunk_size):
    """
    Translate pre-processed book file
    Args:
        credentials: credential object for AutoML
        bucket: GCS bucket name
        in_file_name: input file name for the book file
        out_file_name: output file name for the processed book
        source: source language
        target: target language
        chunk_size: chunk size to translate text in
    Returns:
    """
    # fetch file from GCS
    gcs_client = authenticate_gcs()
    downloaded_file = get_gcs_object(gcs_client, bucket, in_file_name)

    # remove newline characters
    lines = list(map(
        lambda line: line.replace('\n', ''),
        downloaded_file.readlines()
    ))

    idx = 0
    translated_lines = []
    for jdx in range(chunk_size, len(lines) + 300, chunk_size):

        # chunk lines for translation
        if jdx > len(lines):
            chunk = lines[idx:]
        else:
            chunk = lines[idx:jdx]
            idx = jdx

        # add @ delimeter to separate sentences and join chunk
        chunk = '@'.join(chunk)

        # translate chunk
        client = translate.Client(credentials=credentials)
        translated = client.translate(
            chunk,
            source_language=source,
            target_language=target
        )
        translated = translated['translatedText']

        # separate at the @ delimeter and strip white space
        translated = list(map(
            lambda sentence: sentence.strip(),
            translated.split('@')
        ))

        # append to final translated lines
        translated_lines += translated

    # add newline to each line and write to file
    translated_lines = list(map(
        lambda line: f'{line}\n',
        translated_lines
    ))
        
    put_gcs_object(gcs_client, bucket, out_file_name, translated_lines)


def concat_label_files(bucket, in_file_names, out_file_name, label):
    """
    Concatenate csv files and add labels
    Args:
        bucket: GCS bucket name
        in_file_names: csv files to concatenate
        out_file_name: concatenated csv file
    Returns:
    """
    
    # fetch file from GCS
    gcs_client = authenticate_gcs()
    all_lines = []

    for in_file_name in in_file_names:
        downloaded_file = get_gcs_object(gcs_client, bucket, in_file_name)
        lines = downloaded_file.readlines()
        # add label to each line and write to file
        lines = list(map(
            lambda line: line.replace(',', '').replace('\n', f',{label}\n'),
            lines
        ))
        all_lines.append(lines)
    
    put_gcs_object(gcs_client, bucket, out_file_name, all_lines)

def create_data_sets(bucket, in_file_names, train_file_name, predict_file_name):
    """
    Concatenate csv files and split up into training sets and testing sets
    Args:
        bucket: GCS bucket name
        in_file_names: csv files to concatenate
        train_file_name: file name for the training set
        predict_file_name: file name for the testing set
    Returns:
    """
    # fetch file from GCS
    gcs_client = authenticate_gcs()
    train_lines = []
    test_lines = []

    for in_file_name in in_file_names:
        downloaded_file = get_gcs_object(gcs_client, bucket, in_file_name)
        lines = downloaded_file.readlines()
        # split into training or testing sets
        train_lines.append(lines[:-50])
        test_lines.append(lines[-50:])
    
    put_gcs_object(gcs_client, bucket, train_file_name, train_lines)
    put_gcs_object(gcs_client, bucket, predict_file_name, test_lines)


    

   




