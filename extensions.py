# extensions.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database import db
from app.models import User
from app.models.transaction import Transaction
from sqlalchemy import extract, func
from datetime import datetime


my_template = "templates"