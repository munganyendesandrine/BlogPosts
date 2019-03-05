from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required
from flask_login import current_user



class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')   

class PostsForm(FlaskForm):
   
    description = TextAreaField('Add Your Post Here!',validators=[Required()])
   
    submit = SubmitField('Post')       

class CommentForm(FlaskForm):
   
    comment = TextAreaField('Please Leave your comment!',validators=[Required()])
    submit = SubmitField('Submit')                  

# class CategoryForm(FlaskForm):
   
#     name = StringField('Category',validators=[Required()])
#     submit = SubmitField('Post')       