from flask import Flask
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "foodu-udem-2024"

