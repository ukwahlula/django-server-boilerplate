#!/bin/bash

# Exit on any error
set -ex

GIT_TAG="${GITHUB_REF##refs/tags/}"
GIT_BRANCH="${GITHUB_REF##refs/heads/}"

if [ "$GIT_BRANCH" == "develop" ]; then
    mkdir ~/.ssh
    echo -e "Host *\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
    echo "$TESTING_SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
    chmod 700 ~/.ssh/id_rsa
    fab deploytesting
elif [ "$GIT_BRANCH" == "master" ]; then
    fab deploystaging
elif [[ $GITHUB_REF != $GIT_TAG ]]; then
    fab deployprod
fi
