from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
def index():
    """Display home page.

    GET: Renders home page from template 'home.html'.
    """
    return render_template('home.html', title='Cocktail World')
