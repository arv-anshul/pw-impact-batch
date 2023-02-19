# PW Impact Batch - Hindi

This repo contains all the **assignments** present in the Impact batch. There is also some **quizzes** in the batch but it was emmbedded in the website.

This repo also contains a [_automation script_](./utils/make_assingment_folder.py) which helps you to make [_new assignment folder_](#automate-the-assignment-folder-creation-🤖) in **no time**.

Also, automate the `git add && git commit` command with pyhton. [Script Here](./utils/commit_assignment.py). This script add and commit the assignment and then provide you the _github repo link_\* also.

> \* For this feature you have to modify the script.

## Assignment Leaderboard 🥇

<img src="./img/1.png" height=100>
<img src="./img/2.png" height=100>
<img src="./img/3.png" height=100>

## Repo Structure 📁

```mermaid
flowchart LR

repo{pw-impact-batch}

repo  --> ut[utils]
repo --> month-f[Months Folders]
repo --> repo-sh([push_to_github.sh])
repo --> repo-md([README.md])

ut --> ut1{{make_assingment_folder.py}}
ut --> ut2{{commit_assignment.py}}

month-f --> date-f[Dates Folders]
date-f --> 1{{Answer.ipynb}}
date-f --> 2{{Question.pdf}}
```

## Additional 📌

### Automate the assignment folder creation 🤖

I created a [`python script`](./utils/make_assingment_folder.py) to automate the downloading of the **pdf** file from the website and add to a new folder.

```python
from utils.make_assingment_folder import new_assignment_folder

# Add new assignment
url = 'https://drive.google.com/file/d/1dJiiIdeT3mk6REVQgTZRj_bWuJ7NwEOL/view?usp=sharing'

new_assignment_folder(url=url, date=7, month_name='February')
```

### Automate git commit shell command 🤖

I also created another [`python script`](./utils/commit_assignment.py) to **automate the git commands** to commit the **solved** assignment.

```bash
# Provide fliename and commit message
python3 utils/commit_assignment.py --file-name February/07\ Feb --commit-message "Added 07 Feb assignment."
```

You can skip the commit message. _Only applicable for assignment files_.

```bash
python3 utils/commit_assignment.py --file-name February/07\ Feb

# Note:
    # The default commit messsage is "Added <<file_name>> assignment."
```

## Created by [arv-anshul](https://github.com/arv-anshul)

#### Check my other works 📎

- Dashboard of **PW Skills Experience Portal** with `streamlit` and `python`. [Check here](https://github.com/arv-anshul/pw-experience-portal)

- Dashboard of **PW Skills Courses** with `streamlit` and `python`. [Check here](https://github.com/arv-anshul/pw-courses-scrapper-app)
