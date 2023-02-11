""" Add the completed assignment to github repository. """

import os
from argparse import ArgumentParser


def git_commit(message):
    os.system(f'git commit -m "{message}"')


def git_add(filename: str):
    os.system(f'git add "{filename}"')


def commit_assignment(filename: str | None, commit_message: str | None):
    # If filename not given
    if filename is None:
        exit()

    # Check the file path
    if os.path.exists(filename):
        git_add(filename)
    else:
        exit()

    # Check commit message
    if commit_message:
        git_commit(commit_message)
    else:
        git_commit(f"Added {filename.split('/')[-1]} assignment.")


def get_link_to_submit(filename: str) -> str:
    github_link = 'https://github.com/arv-anshul/pw-impact-batch/blob/main/'

    MONTH, DATE = filename.split('/')
    link_to_answer_sheet = f'{MONTH}/{DATE}/{DATE} - Answer.ipynb'

    return github_link + link_to_answer_sheet.replace(' ', r'%20')


def main():
    parser = ArgumentParser()

    parser.add_argument('--file-name', type=str, default=None,
                        help='Get the filename to add & commit.')
    parser.add_argument('--commit-message', type=str, default=None,
                        help='Get commit message.')

    # Get passed args
    args = parser.parse_args()

    # Finally commit the file
    commit_assignment(filename=args.file_name,
                      commit_message=args.commit_message)

    os.system('echo ' + get_link_to_submit(filename=args.file_name))


if __name__ == '__main__':
    main()
