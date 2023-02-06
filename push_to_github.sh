#!/bin/bash

# Get file name
full_name=$1
file_name=`echo $full_name | cut -d "/" -f2`
c_message=$2

if [ -e $full_name ] 
then
    # Add file with git
    git add $full_name

    # Commit the file
    if [ "$c_message" ]
    then
        git commit -m "$c_message"
    else
        git commit -m "Added $file_name assignment."
    fi

    # push to github
    git push origin main

    echo "Your file $file_name pushed to github."
else
    echo "Your entered file does not exists."
fi