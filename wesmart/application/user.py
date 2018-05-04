# -*- coding: utf-8 -*-

################################################################################
#
#
# Copyright(c) 2017, WeSmart Artificial Intelligent Co.Ltd, All rights reserved.
# 
#
# Description: 
# Desc
# Author: Fu adon
# Versions: 
#     Created by Fu adon on 2018/1/1 下午10:07 for version 1.0
#     Modified by Fu adon on 2018/1/1 下午10:07 form version 1.0
#
################################################################################

from flask import Blueprint


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
def index():
    return "User's Index page"
