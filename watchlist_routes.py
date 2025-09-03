from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from models import WatchlistItem, WatchedItem
from forms import AddItemForm, UpdateWatchedForm

watchlist = Blueprint("watchlist", __name__)


#Watchlist
@watchlist.route("/watchlist")
@login_required
def show_watchlist():
    items =  WatchlistItem.query.filter_by(user_id=current_user.id).all()
    return render_template("watchlist.html", items=items)


#Watched
@watchlist.route("/watched")
@login_required
def show_watched():
    items = WatchedItem.query.filter_by(user_id=current_user.id).all()
    return render_template("watched.html", items=items)


#Add new item in watchlist
@watchlist.route("/add_item", methods=["GET", "POST"])
@login_required
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        new_item = WatchlistItem(
            title=form.title.data,
            genre=form.genre.data,
            rating=form.rating.data,
            comment=form.comment.data,
            user_id=current_user.id,
        )
        db.session.add(new_item)
        db.session.commit()
        flash("Item added to watchlist")
        return redirect(url_for("watchlist.show_watchlist"))
    return render_template("add_item.html", form=form)


#Move item to watched
@watchlist.route("/move_to_watched/<int:item_id>")
@login_required
def move_to_watched(item_id):
    item = WatchlistItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("You are not allowed to modify this item!")
        return redirect(url_for("watchlist.show_watchlist"))

    watched = WatchedItem(
        title=item.title,
        genre=item.genre,
        rating=item.rating,
        comment=item.comment,
        user_id=current_user.id,
    )

    db.session.add(watched)
    db.session.delete(item)
    db.session.commit()
    flash("Item moved to watched")
    
    return redirect(url_for("watchlist.show_watched"))


#Update watched item
@watchlist.route("/update_watched/<int:item_id>", methods=["GET", "POST"])
@login_required
def update_watched(item_id):
    item = WatchedItem.query.get_or_404(item_id)
    if item.user != current_user.id:
        flash("You are not allowed to edit this item!")
        return redirect(url_for("watchlist.show_watched"))
    
    form = UpdateWatchedForm(obj=item)
    if form.validate_on_submit():
        item.comment = form.comment.data
        item.my_rating = form.my_rating.data
        db.session.commit()
        flash("Watched item updated")
        return redirect(url_for("watchlist.show_watched"))
    
    return render_template("update_watched.html", form=form, item=item)