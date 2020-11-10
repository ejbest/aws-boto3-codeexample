#!/bin/bash

echo "Script Started ..."

echo "creating key-foo-bar-tmp directory ..."
rm -Rf key-foo-bar-tmp
mkdir -p key-foo-bar-tmp

echo "Generating key-foo-bar-tmp for user1 ..."
ssh-keygen -t rsa -f key-foo-bar-tmp/user1 -q -P "" -C user1

echo "Generating key-foo-bar-tmp for user2 ..."
ssh-keygen -t rsa -f key-foo-bar-tmp/user2 -q -P "" -C user2

echo "Setting up permissions ..."
chmod 400 key-foo-bar-tmp/user1
chmod 400 key-foo-bar-tmp/user2

echo "Running server.py ..."
python3 server.py
rm -Rf key-foo-bar-tmp

