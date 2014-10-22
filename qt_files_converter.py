import os
import re
import argparse

TIME_CODE_PATTERN = re.compile(r'^\[\d+:\d+:\d+\.\d+\]$', re.M)
QT_FILENAME_PATTERN = re.compile(r'^Job_(.*)\.mp4.*$')
TEMPLATE_PATTERN = re.compile(r'\{file_name\}')
BLANK_AUDIO_PATTERN = re.compile(r'\[BLANK_AUDIO\]')


def get_smil_template(path):
    """
    Returns content of template.smil file
    """
    with open(os.path.join(path, 'template.smil'), 'r') as template:
        return template.read()


def converter(path):
    """
    Creates .smil file from template.smil and replaces all '{file_name}'
    string with file_id in .smil file
    Creates .qt.text file with needed modifications
    """
    smil_template = get_smil_template(path)

    for filename in os.listdir(path):
        if not filename.endswith('.qt'):
            continue

        match = QT_FILENAME_PATTERN.search(filename)
        if match:
            file_id = match.groups()[0]
            smil_file = os.path.join(path, '{}{}'.format(file_id, '.smil'))

            with open(smil_file, 'w') as smil:
                smil.write(TEMPLATE_PATTERN.sub(file_id, smil_template))

            qt_file_path = os.path.join(path, filename)
            caption_file_path = os.path.join(
                path,
                '{}{}'.format(file_id, '.qt.text')
            )
            is_caption_text = False
            output = []

            with open(qt_file_path, 'r') as qt_file:
                for line in qt_file:
                    line = BLANK_AUDIO_PATTERN.sub('', line)
                    is_time_code = TIME_CODE_PATTERN.search(line)
                    if is_time_code:
                        is_caption_text = not is_caption_text
                        if not is_caption_text:
                            continue
                    elif is_caption_text:
                        line = line.replace('[', '(').replace(']', ')')

                    output.append(line)

            with open(caption_file_path, 'w') as caption_file:
                caption_file.writelines(output)
            os.remove(qt_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Enter path to your .qt files')
    args = parser.parse_args()
    converter(args.path)
