#!/usr/env/python
import os
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Recursively search directory and sub-directories files with given extension for keywords (exact matches).',
                                     epilog="Examples:\n"
                                            "\t(1) Search for '# TODO:' and '# NOTE:' keywords in current\n"
                                            "\t    and all subdirectories to current directory,\n"
                                            "\t    and save them to a file 'todo.csv' in csv format:\n\n"
                                            "\t    python3 todo.py -d '.' -e '.py' -k '# TODO:' '# NOTE:' -f csv -o todo.csv\n\n"
                                            "\t(2) Search for '# TODO:' and print to screen, but exclude\n"
                                            "\t    folder 'venv' and file 'todo.py':\n\n"
                                            "\t    python3 todo.py -s 'venv' 'todo.py'\n\n"
                                            "\t(3) Find '# TODO:' keywords in todo.py:\n\n"
                                            "\t    python3 todo.py -f markdown | grep todo.py\n\n"
                                            "\t(4) Similar grep command for searching for '# TODO:' keyword:\n\n"
                                            "\t    grep -rnw './' -e '# TODO:'",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d', '--dir', default='.', help='Absolute path to the root directory (defaults to ".").')
    parser.add_argument('-e', '--ext', default='.py', nargs='*', help='List of file extensions to search in.')
    parser.add_argument('-s', '--skip', default='', nargs='*', help='List of directories or files to skip. Can be both parent and subdirectories.')
    parser.add_argument('-o', '--output', default='', help='Name of output file.')
    parser.add_argument('-k', '--keywords', default='# TODO:', nargs='*', help='List of keywords to search for (exact match). Defaults to "# TODO:".')
    parser.add_argument('-f', '--format', default='', help='Output format. Either markdown table, csv. or json (default).')
    args = parser.parse_args()

    root = args.dir
    extensions = args.ext if type(args.ext) == list else [args.ext]
    skip = args.skip if type(args.skip) == list else [args.skip]
    filename = args.output  # TODO: Check for file extension
    keywords = args.keywords if type(args.keywords) == list else [args.keywords]
    format = args.format

    logs = []

    for dirpath, dirnames, files in os.walk(root, topdown=True):
        # look for dirs we want to skip. By removing them from the list in place, os.walk will skip them
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in files:
            _, extension = os.path.splitext(name)
            # skip this file if its not the correct extension or marked to be skipped
            if extension not in extensions or name in skip:
                continue
            with open(dirpath + '/' + name, 'r') as cur_file:
                try:
                    # open the file and search each line for keywords
                    for line_num, line in enumerate(cur_file):
                        for keyword in keywords:
                            # check if there is a keyword in the current line
                            if keyword in line:
                                # remove the keyword from the line, and remove leading whitespace
                                line = line.replace(keyword, '')
                                line = line.lstrip()
                                line = line.replace('\n', '')

                                entrance = {
                                    'index': str(len(logs)+1),
                                    'keyword': keyword,
                                    'line_number': str(line_num+1),
                                    'link': 'None',
                                    'line_text': line,
                                    'file_path': dirpath+'/'+name
                                }

                                logs.append(entrance)
                except UnicodeDecodeError:
                    print('UnicodeDecodeError in file {}'.format(dirpath + '/' + name))

    if format.upper() == 'CSV':
        to_file = 'index,keyword,file path,line number,line text,link\n'
        for log in logs:
            to_file += log['index'] + ',' + log['keyword'] + ',' + log['file_path'] + ',' + log['line_number'] + ',' + log['line_text'] + ',' + log['link'] + '\n'

        if filename == '':
            print(to_file)
        else:
            with open(filename, 'wb') as output_file:
                output_file.write(bytes(to_file, 'utf-8'))

    elif format.upper() == 'JSON':
        import json
        with open(filename, 'wb') as output_file:
            json.dump(logs, output_file)

    elif format.upper() == 'MARKDOWN':
        # add content to the table
        to_file =  '|Index|Keyword|File path|Line number|Comment|Link|\n'
        to_file += '|-----|-------|---------|-----------|-------|----|\n'
        for log in logs:
            to_file += '|' + log['index'] + '|' + log['keyword'] + '|' + log['file_path'] + '|' + log['line_number'] + '|' + log['line_text'] + '|' + log['link'] + '|\n'

        if filename == '':
            print(to_file)
        else:
            with open(filename, 'wb') as output_file:
                output_file.write(bytes(to_file, 'utf-8'))

    else:
        import json
        print(json.dumps(logs, indent=4))
