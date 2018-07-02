import os
import secrets
from PIL import Image
from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from app.models import User, Post, Pickup, Product, CommentsPost, CommentsPickup, CommentsProduct
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, PickupForm, ProductForm, PostCommentForm, ProductCommentForm, PickupCommentForm
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/post_home')
def post_home():
    posts = Post.query.all()
    return render_template('post_home.html', posts=posts)

@app.route('/product_home')
def product_home():
    products = Product.query.all()
    return render_template('product_home.html', products=products)

@app.route('/pickup_home')
def pickup_home():
    pickups = Pickup.query.all()
    return render_template('pickup_home.html', pickups=pickups)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('post_home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')



@app.route('/post/<int:post_id>/',methods=["GET","POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostCommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_post_comment = CommentsPost(comment=comment, post_id=post_id, user_id=current_user.id)
        # new_post_comment.save_post_comments()
        db.session.add(new_post_comment)
        db.session.commit()
    comments = CommentsPost.query.all()
    return render_template('post.html', title=post.title, post=post, post_form=form, comments=comments)


@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('post_home'))



@app.route('/product/new', methods=['GET','POST'])
@login_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(product)
        db.session.commit()
        flash('Your Product Pitch has been created!', 'success')
        return redirect(url_for('product_home'))
    return render_template('create_product.html', title='New Product', form=form, legend='New Product')



@app.route('/product/<int:product_id>/', methods=['GET','POST'])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductCommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_product_comment = CommentsProduct(comment=comment, product_id=product_id, user_id=current_user.id)
        db.session.add(new_product_comment)
        db.session.commit()
    comments = CommentsProduct.query.all()
    return render_template('product.html', title=product.title, product=product, product_form=form, comments=comments)

@app.route('/product/<int:product_id>/update', methods=['GET','POST'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.author != current_user:
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        product.title = form.title.data
        product.content = form.content.data
        db.session.commit()
        flash('Your Product Pitch has been updated!', 'success')
        return redirect(url_for('product', product_id=product.id))
    elif request.method == 'GET':
        form.title.data = product.title
        form.content.data = product.content
    return render_template('create_product.html', title='Update Product Pitch', form=form, legend='Update Product Pitch')

@app.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.author != current_user:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash('Your Product Pitch has been deleted!', 'success')
    return redirect(url_for('product_home'))

@app.route('/pickup/new', methods=['GET','POST'])
@login_required
def new_pickup():
    form = PickupForm()
    if form.validate_on_submit():
        pickup = Pickup(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(pickup)
        db.session.commit()
        flash('Your Pick Up Line has been created!', 'success')
        return redirect(url_for('pickup_home'))
    return render_template('create_pickup.html', title='New Pick Up Line', form=form, legend='New Pick Up Line')



@app.route('/pickup/<int:pickup_id>/', methods=['GET','POST'])
def pickup(pickup_id):
    pickup = Pickup.query.get_or_404(pickup_id)
    form = PickupCommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_pickup_comment = CommentsPickup(comment=comment, pickup_id=pickup_id, user_id=current_user.id)
        db.session.add(new_pickup_comment)
        db.session.commit()
    comments = CommentsPickup.query.all()
    return render_template('pickup.html', title=pickup.title, pickup=pickup, pickup_form=form, comments=comments)


@app.route('/pickup/<int:pickup_id>/update', methods=['GET','POST'])
@login_required
def update_pickup(pickup_id):
    pickup = Pickup.query.get_or_404(pickup_id)
    if pickup.author != current_user:
        abort(403)
    form = PickupForm()
    if form.validate_on_submit():
        pickup.title = form.title.data
        pickup.content = form.content.data
        db.session.commit()
        flash('Your Pick Up Line has been updated!', 'success')
        return redirect(url_for('pickup', pickup_id=pickup.id))
    elif request.method == 'GET':
        form.title.data = pickup.title
        form.content.data = pickup.content
    return render_template('create_pickup.html', title='Update Pick Up Line', form=form, legend='Update Pick Up Line')

@app.route('/pickup/<int:pickup_id>/delete', methods=['POST'])
@login_required
def delete_pickup(pickup_id):
    pickup = Pickup.query.get_or_404(pickup_id)
    if pickup.author != current_user:
        abort(403)
    db.session.delete(pickup)
    db.session.commit()
    flash('Your Pick Up Line has been deleted!', 'success')
    return redirect(url_for('pickup_home'))
