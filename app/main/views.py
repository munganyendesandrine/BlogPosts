from flask import render_template,request,redirect,url_for,abort
from . import main

from .forms import UpdateProfile

from .forms import PostsForm,CommentForm
from ..models import User,BlogPost,Comment
from flask_login import login_required,current_user
from .. import db, photos



@main.route('/')
def index():
    user = User.query.filter_by().first() #username = uname
    
    form = PostsForm()
    blogs = BlogPost.fetch_blogs()

    # if form.validate_on_submit():
    #     description=BlogPost(blog=form.description.data,user_id=current_user.id)#,pitch_id=pitch_id
    #     db.session.add(description)
    #     db.session.commit()
    #     description.save_blog()
       
    form = CommentForm()
    comment = Comment.fetch_comment() 
    # if form.validate_on_submit():
    #     comment=Comment(comment=form.comment.data,user_id=current_user.id)#,pitch_id=pitch_id
    #     db.session.add(comment)
    #     db.session.commit()
    #     comment.save_comment()
        # return redirect(url_for('.index'))

    if user is None:
        abort(404)

    title = 'Home - Welcome to The best Movie Review Website Online'
    return render_template('index.html', title = title,blogs=blogs,comment=comment)#,opinion=form,blogs=blogs


@main.route('/user/<uname>',methods = ["GET","POST"])
def profile(uname):
    user = User.query.filter_by(username = uname).first()


    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)#+,comment=form)   #,opinion=form,blogs=blogs,comment=form


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
    

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    


#Posts routing
@main.route('/posts',methods = ["GET","POST"])
@login_required
def posts():
    form = PostsForm()
   
    if form.validate_on_submit():
        # blog=form.blog.data
        posted=BlogPost(blog=form.description.data,user_id=current_user.id)
        db.session.add(posted)
        db.session.commit()
        posted.save_blog()
        return redirect(url_for('.index'))
        print(posted)
    return render_template('posts.html',posts_form = form,comment=form)


#Comments routing
@main.route('/comments/new/<int:id>',methods = ["GET","POST"])#/<int:id>
@login_required
def comments(id):    
    form = CommentForm()
    blog = BlogPost.query.filter_by(id=id).first()
    # comment = Comment.fetch_comment() 
    if form.validate_on_submit():
        comment=Comment(comment=form.comment.data,user_id=current_user.id, blog_id=id)#, blog_id=id
        db.session.add(comment)
        db.session.commit()
        comment.save_comment()
        comment.delete_comment()
        # print(comment)
        return redirect(url_for('.index'))
    return render_template('comments.html',comments_form=form,comment=form,blog=blog)

    
