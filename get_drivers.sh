#!/bin/bash
mkdir ./app/drivers
cd ./app/drivers

echo 'Downloading chromedriver-linux64'
wget https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chromedriver-linux64.zip
echo 'Unziping files'
unzip ./chromedriver-linux64.zip

wget https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chrome-linux64.zip
echo 'Unziping files'
unzip ./chrome-linux64.zip

echo 'Complete!'