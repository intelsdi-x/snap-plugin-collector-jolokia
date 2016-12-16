#!/bin/bash

set -e

APP_NAME=jolokia

acbuild begin
acbuild set-name ${APP_NAME}
acbuild copy ~/.pyenv/versions/3.5.2/envs/snap-plugins .venv
acbuild copy ${APP_NAME}.py ${APP_NAME}.py
acbuild set-exec ./.venv/bin/python ${APP_NAME}.py
acbuild write snap-plugin-collector-${APP_NAME}-linux-x86_64.aci
acbuild end

