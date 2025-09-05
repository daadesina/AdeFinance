# extensions.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from app.models import User

my_template = "templates"