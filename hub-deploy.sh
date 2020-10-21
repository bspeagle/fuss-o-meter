#!/bin/bash
set -e

PI_IP=192.168.1.178
ZIP_EXPORT=fom-hub.zip
HOME_DIR=/home/pi
PI_DIR=fom

echo "Adding files to ZIP export"
zip -r $ZIP_EXPORT src/hub/. -x '*__pycache__*' '*deploy.sh'
zip -g $ZIP_EXPORT ".env"
zip -g $ZIP_EXPORT src/hub/requirements.txt

trap "rm $ZIP_EXPORT" INT

echo "Checking if Pi 0 is up..."
if ping -c 1 $PI_IP
then
    if ssh pi@$PI_IP "[ -d $HOME_DIR/$PI_DIR ]"
    then
        echo "Clearing out directory on Pi"
        ssh pi@$PI_IP rm -R $HOME_DIR/$PI_DIR
    else
        echo "Creating directory on Pi"
        ssh pi@$PI_IP mkdir $HOME_DIR/$PI_DIR
    fi

    echo "Copying ZIP to Pi"
    scp $ZIP_EXPORT pi@$PI_IP:$HOME_DIR

    echo "Unzipping export"
    ssh pi@$PI_IP unzip $HOME_DIR/$ZIP_EXPORT -d $HOME_DIR/$PI_DIR

    echo "Deleting ZIP $ZIP_EXPORT on Pi"
    ssh pi@$PI_IP rm $ZIP_EXPORT

    echo "Deleting local export ZIP file: $ZIP_EXPORT"
    rm $ZIP_EXPORT

    # echo "Installing Python requirements..."
    # ssh pi@$PI_IP pip3 install -r $HOME_DIR/$PI_DIR/src/hub/requirements.txt
else
    rm $ZIP_EXPORT
    exit 0
fi
