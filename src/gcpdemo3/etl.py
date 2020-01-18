from google.cloud import translate_v2 as translate
from google.cloud import storage


def process_book(bucket, path):
    """
    Process a single book file and write process file
    :param bucket: bucket name
    :param path: raw book file
    :return:
    """

    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.get_blob(path)
    fn = blob.filename  # lookup actual
    downloaded_file = blob.download_as_file()

    # skip first 15 header lines
    lines = downloaded_file.readlines()[15:]

    # get rid of head, tail, underscores, commas, and quotation marks
    lines = list(map(
        lambda line: line.strip().split('>')[1].split('<')[0].replace(
            '_', '').replace(',', '').replace('"', ''),
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
    blob = bucket.blob('{}_processed'.format(fn), lines))
    blob.upload_from_string(lines,content_type='text/plain')


def translate_book(credentials, in_path, out_path, source, target, chunk_size):
    """
    Translate pre-processed book file
    :param credentials: credential object for AutoML
    :param in_path: processed book file
    :param out_path: translated book file
    :param source: source language
    :param target: target language
    :param chunk_size: chunk size to translate text in
    :return:
    """

    with open(in_path, 'r', encoding='utf8') as in_file:

        # remove newline characters
        lines = list(map(
            lambda line: line.replace('\n', ''),
            in_file.readlines()
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

    with open(out_path, 'w+', encoding='utf8') as out_file:

        # add newline to each line and write to file
        translated_lines = list(map(
            lambda line: f'{line}\n',
            translated_lines
        ))
        out_file.writelines(translated_lines)


def concat_label_files(in_paths, out_path, label):
    """
    Concatenate csv files and add labels
    :param in_paths: csv files to concatenate
    :param out_path: concatenated csv file
    :param label: label to add to end of each line
    :return:
    """

    with open(out_path, 'w+', encoding='utf8') as out_file:

        # iterate through files and concatenate
        for in_path in in_paths:
            with open(in_path, 'r', encoding='utf8') as in_file:
                lines = in_file.readlines()

                # add label to each line and write to file
                lines = list(map(
                    lambda line: line.replace(',', '').replace('\n', f',{label}\n'),
                    lines
                ))

                out_file.writelines(lines)
