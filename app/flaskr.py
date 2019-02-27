
"""
Simple flask thing
"""

import requests
from subprocess import call
from datetime import datetime, timedelta
from flask import render_template, jsonify, request, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb
from flask_menu import register_menu
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.sql.expression import false, true
from app import app, login_manager, webhook, db
from app.models import Game, User, Player, Relation, Resource, Price
from app.util.job import Job, MarketJob
from app.util import sync


@login_manager.user_loader
def load_user(user_id):
    """Return user"""
    return User.query.get(user_id)


@register_breadcrumb(app, '.login', 'Login')
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle login page and data"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter(User.email == email).first()
        if user is not None:
            if user.check_password(password):
                login_user(user, remember=True)
                flash('You were successfully logged in.', 'success')
                if request.args.get("next") is not None:
                    return redirect(request.args.get("next"))
                return redirect(url_for('index'))
            else:
                flash('Incorrect password.', 'danger')
        else:
            flash('User not found.', 'danger')

        return redirect(url_for('login'))
    else:
        return render_template('user/login.html')


@app.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    if request.method != "POST":
        return redirect(url_for('login'))

    if "name" not in request.form or not request.form['name']:
        flash('Fill in the name.', 'warning')
        return render_template('user/login.html')

    if "email" not in request.form or not request.form['email']:
        flash('Fill in the email.', 'warning')
        return render_template('user/login.html', name=request.form['name'])

    if "password" not in request.form or not request.form['password']:
        flash('Fill in the password.', 'warning')
        return render_template(
            'user/login.html',
            name=request.form['name'],
            email=request.form['email']
        )

    user = User.query.filter(User.name == request.form['name']).first()
    if user is None:
        flash('Name not found.', 'warning')
        return render_template(
            'user/login.html',
            name=request.form['name'],
            email=request.form['email']
        )

    if user.email is not None:
        flash('User already taken.', 'warning')
        return render_template(
            'user/login.html',
            name=request.form['name'],
            email=request.form['email']
        )

    user.email = request.form['email']
    user.password = request.form['password']

    db.session.commit()
    login_user(user, remember=True)
    flash('Succesfully registered account "%s".' % (user.name), 'success')

    if request.args.get("next") is not None:
        return redirect(request.args.get("next"))
    else:
        return redirect(url_for('index'))


@app.route("/logout")
@login_required
def logout():
    """Logout function for users"""
    logout_user()
    flash('succesfully logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/')
@register_menu(app, '.', 'Home')
@register_breadcrumb(app, '.', 'Home')
def index():
    """Show homepage"""

    if current_user.is_authenticated:
        games = current_user.players.filter(
            Player.game.has(Game.end_of_game == false())
        ).order_by(
            Player.game_id.desc()
        ).all()
    else:
        games = None

    return render_template(
        'site/index.html',
        games=games
    )


@app.route('/games')
@register_menu(app, 'games', 'Games')
@register_breadcrumb(app, '.games', 'Games')
def game_index():
    """Return game index"""

    games = Game.query.all()
    return render_template('game/index.html', games=games)


def game_overview_dlc(*args, **kwargs):
    """Generate dynamic_list for games"""
    game_id = request.view_args['game_id']
    game = Game.query.filter(Game.game_id == game_id).first()
    return [{'text': game.game_id, 'url': game.url}]


@app.route('/game/<int:game_id>')
@register_breadcrumb(app, '.games.game_id', '',
                     dynamic_list_constructor=game_overview_dlc)
def game_overview(game_id):
    """Show game overview"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()
    players = game.active_players()
    return render_template('game/overview.html', game=game, players=players)


@app.route('/game/<int:game_id>/players')
@register_breadcrumb(app, '.games.game_id', '',
                     dynamic_list_constructor=game_overview_dlc)
def game_players(game_id):
    """Show game overview"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()
    players = game.all_players()
    return render_template('game/players.html', game=game, players=players)


@app.route('/game/<int:game_id>/relations')
@register_breadcrumb(app, '.games.game_id', '',
                     dynamic_list_constructor=game_overview_dlc)
def game_relations(game_id):
    """Show game relations"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()
    players = game.active_players()
    return render_template('game/relations.html', game=game, players=players)


@app.route('/game/<int:game_id>/market')
@register_breadcrumb(app, '.games.game_id', '',
                     dynamic_list_constructor=game_overview_dlc)
def game_market(game_id):
    """Show game market"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()
    market_job = MarketJob(game)
    return render_template('game/market.html', game=game, market_job=market_job)


@app.route('/game/<int:game_id>/config')
@register_breadcrumb(app, '.games.game_id', '',
                     dynamic_list_constructor=game_overview_dlc)
def game_config(game_id):
    """Show game config"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()
    return render_template('game/config.html', game=game)


@app.route('/api/game/<int:game_id>/config', methods=['POST'])
def api_game_config(game_id):
    """Save game config"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()

    game.track_game = True if request.form.get('track_game') == 'on' else False
    game.track_score = True if request.form.get('track_score') == 'on' else False
    game.track_players = True if request.form.get('track_players') == 'on' else False
    game.track_relations = True if request.form.get('track_relations') == 'on' else False
    game.track_market = True if request.form.get('track_market') == 'on' else False
    game.track_coalitions = True if request.form.get('track_coalitions') == 'on' else False

    MarketJob(game).check()
    Job(game).check()

    db.session.commit()

    return redirect(request.referrer, code=302)


@app.route('/api/game/<int:game_id>/score/<string:score_type>')
def api_game_score(game_id, score_type):
    """Returns list days with players"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()

    day_dict = {}

    for day in game.days:
        if day.day not in day_dict:
            day_dict[day.day] = {}
            day_dict[day.day]["day"] = day.day

        day_dict[day.day][day.player.name] = day.points

    day_list = []

    for day in day_dict:
        day_list.append(day_dict[day])

    player_list = []

    if score_type == "players":
        players = game.players.filter(Player.user_id != None).all()
    elif score_type == "active":
        three_days_ago = datetime.now() - timedelta(days=3)
        players = game.players.filter(Player.last_login >= three_days_ago).all()
    else:
        players = game.players

    for player in players:
        player_list.append({
            "title": player.nation_name,
            "valueField": player.name,
            "lineColor": player.primary_color,
        })

    score = {
        "days": day_list,
        "players": player_list,
    }

    return jsonify(score)


@app.route('/api/game/<int:game_id>/relations/<relation_type>')
def api_game_relations(game_id, relation_type):
    """Returns list of players with relationships"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()

    player_list = []

    for player in game.players:
        native_relations = player.native_relations.filter(Relation.end_day == None).filter(Relation.status == relation_type)
        foreign_relations = player.foreign_relations.filter(Relation.end_day == None).filter(Relation.status == relation_type)
        if native_relations.count() or foreign_relations.count():
            relation_list = []
            for relation in native_relations.all():
                relation_list.append(relation.player_foreign.nation_name)

            player_list.append({
                "name": player.nation_name,
                "imports": relation_list,
            })

    return jsonify(player_list)


@app.route('/api/game/<int:game_id>/force_relations')
def api_game_force_relations(game_id):
    """Returns list of players with relationships"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()

    relation_list = []

    for player in game.players:
        for relation in player.native_relations.filter(Relation.end_day == None):
            relation_list.append({
                "source": relation.player_native.nation_name,
                "target": relation.player_foreign.nation_name,
                "type": relation.status_formatted,
            })

    return jsonify(relation_list)


@app.route('/api/game/<int:game_id>/edge_relations')
def api_game_edge_relations(game_id):
    """Returns list of players with relationships"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()

    player_list = []

    for player in game.players.order_by(Player.nation_name).all():
        war = []
        right_of_way = []
        share_map = []
        share_info = []
        native_relations = player.native_relations.filter(Relation.end_day == None)
        foreign_relations = player.foreign_relations.filter(Relation.end_day == None)
        if native_relations.count() or foreign_relations.count():
            for relation in native_relations.all():
                if relation.status == -2:
                    war.append(relation.player_foreign.nation_name)
                elif relation.status == 3:
                    right_of_way.append(relation.player_foreign.nation_name)
                elif relation.status == 4:
                    share_map.append(relation.player_foreign.nation_name)
                elif relation.status == 6:
                    share_info.append(relation.player_foreign.nation_name)

            player_list.append({
                "name": player.nation_name,
                "wars": war,
                "right_of_ways": right_of_way,
                "share_maps": share_map,
                "share_infos": share_info,
            })

    return jsonify(player_list)


@app.route('/api/game/<int:game_id>/market/<string:resource_type>')
@app.route('/api/game/<int:game_id>/market', defaults={'resource_type': None})
def api_market(game_id, resource_type):
    """Returns list of markets with prices"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()

    market_dict = {}

    resources = {
        "grain": 0,
        "fish": 1,
        "iron": 2,
        "wood": 3,
        "coal": 4,
        "oil": 5,
        "gas": 6
    }

    resource_id = resources.get(resource_type, None)

    for market in game.markets:
        dict_ = {}
        # prices = market.prices
        if resource_id is None:
            prices = market.prices.all()
        else:
            prices = market.prices.filter(Price.resource_id == resource_id).all()
        for price in prices:
            name = price.resource.name
            if price.buy:
                name = "sell_%s" % name
            else:
                name = "buy_%s" % name
            dict_[name] = str(price.value)

        dict_["date"] = market.datetime.strftime('%m-%d %H:%M')
        market_dict[market.datetime] = dict_

    market_list = []

    for market in market_dict:
        market_list.append(market_dict[market])

    resource_list = []

    if resource_id is None:
        resources = Resource.query.all()
    else:
        resources = Resource.query.filter(Resource.id == resource_id).all()

    for resource in resources:
        resource_list.append({
            "title": "buy %s" % resource.name,
            "valueField": "buy_%s" % resource.name,
            "lineColor": resource.color,
            "price_type": "buy",
        })
        resource_list.append({
            "title": "sell %s" % resource.name,
            "valueField": "sell_%s" % resource.name,
            "lineColor": resource.color,
            "price_type": "sell",
        })

    market_prices = {
        "markets": market_list,
        "resources": resource_list,
    }

    return jsonify(market_prices)


@app.route('/api/game/sync', methods=['POST'])
def api_sync_game():
    """Update game in the database"""

    game_id = request.form.get('game_id')
    sync_type = request.form.get('sync_type')

    game = Game.query.filter(Game.game_id == game_id).first()

    try:
        if game is not None:
            if sync_type == 'score':
                sync.update_score(game)
            elif sync_type == 'relations':
                sync.update_relations(game)
            elif sync_type == 'players':
                sync.update_players(game)
            elif sync_type == 'market':
                sync.update_market(game)
            elif sync_type == 'game':
                sync.update_game(game)
        else:
            sync.new_game(game_id)
            sync.update_players(game)
    except sync.GameDoesNotExistError:
        flash('Game %s doesn\'t exist anymore.' % game_id, 'danger')
    except requests.exceptions.ConnectionError:
        flash('Supremacy server connection error.', 'warning')


    if "games" in request.referrer:
        return redirect(url_for("game_overview", game_id=game_id), code=302)
    return redirect(request.referrer, code=302)


@app.route('/users')
@register_menu(app, 'users', 'Users')
@register_breadcrumb(app, '.users', 'Users')
def user_index():
    """Return user index"""

    users = User.query.all()
    return render_template('user/index.html', users=users)


def user_overview_dlc(*args, **kwargs):
    """Generate dynamic_list for user"""
    site_id = request.view_args['site_id']
    user = User.query.filter(User.site_id == site_id).first()
    return [{'text': user.name, 'url': user.url}]


@app.route('/user/<int:site_id>')
@register_breadcrumb(app, '.users.site_id', '',
                     dynamic_list_constructor=user_overview_dlc)
def user_overview(site_id):
    """Show user overview"""
    site_id = int(site_id)
    user = User.query.filter(User.site_id == site_id).first()
    return render_template('user/overview.html', user=user)


@app.route('/user_claim', methods=['POST'])
def user_claim():
    if "name" in request.form:
        return render_template(
            'user/login.html',
            name=request.form['name'],
        )
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('site/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('site/500.html'), 500


@webhook.hook()
@app.route('/deploy/<int:data>')
def on_push(data):
    call(["git", "pull"])
    call(["yarn"])
    call(["touch", "flask.wsgi"])
    call(["yarn", "gulp"])
    return jsonify(True)
