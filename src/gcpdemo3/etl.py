from google.cloud import translate


def process_book(in_path, out_path):
    """

    :param in_path:
    :param out_path:
    :return:
    """

    with open(out_path, 'w+', encoding='utf8') as out_file:
        with open(in_path, 'r', encoding='utf8') as in_file:

            # skip first 15 header lines
            lines = in_file.readlines()[15:]

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
            out_file.writelines(lines)


def translate_book(credentials, in_path, out_path, source, target, chunk_size):
    """

    :param credentials:
    :param in_path:
    :param out_path:
    :param source:
    :param target:
    :param chunk_size:
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

            break  # TODO remove

    with open(out_path, 'w+', encoding='utf8') as out_file:

        # add newline to each line and write to file
        translated_lines = list(map(
            lambda line: f'{line}\n',
            translated_lines
        ))
        out_file.writelines(translated_lines)


def concat_label_files(in_paths, out_path, label):
    """

    :param in_paths:
    :param out_path:
    :param label:
    :return:
    """

    with open(out_path, 'w+', encoding='utf8') as out_file:

        # iterate through files and concatenate
        for in_path in in_paths:
            with open(in_path, 'r', encoding='utf8') as in_file:
                lines = in_file.readlines()

                # add label to each line and write to file
                lines = list(map(
                    lambda line: line.replace('\n', f',{label}\n'),
                    lines
                ))

                out_file.writelines(lines)
