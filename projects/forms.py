from django import forms

from .models import Donation, Image, Project,Comment, Review


class ProjectForm(forms.ModelForm):
    class Meta:
        fields=['Title','Description','target','start','end','tags','category',]
        model = Project
      

class EditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields=['Title','Description','target','start','end','tags','category',]


        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.Textarea(attrs={'class': 'form-control'}),
        }
class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Image
        fields = ("image",)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
class DonationForm(forms.ModelForm):
    # quantity = forms.IntegerField()

    class Meta:
        model = Donation
        fields=('quantity',)

        # widgets = {
        #     'quantity': forms.IntegerField(),
        # }



# class ProjectForm(ProjectPartForm):
#     images = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={"multiple": True})
#     )

#     class Meta(ProjectPartForm.Meta):
#         fields = ProjectPartForm.Meta.fields + [
#             "images",
#         ]

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ("rating",)
        


























# from .models import Image, Project,Comment, Review


# class ProjectForm(forms.ModelForm):
#     class Meta:
#         fields='__all__'
#         model = Project
      


# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(
#         label="Image",
#         widget=forms.ClearableFileInput(attrs={"multiple": True}),
#     )

#     class Meta:
#         model = Image
#         fields = ("image",)


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('name', 'body')

#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control'}),
#         }
# # class ProjectForm(ProjectPartForm):
# #     images = forms.FileField(
# #         widget=forms.ClearableFileInput(attrs={"multiple": True})
# #     )

# #     class Meta(ProjectPartForm.Meta):
# #         fields = ProjectPartForm.Meta.fields + [
# #             "images",
# #         ]

# class ReviewForm(forms.ModelForm):
# 	class Meta:
# 		model = Review
# 		fields = ("comment","rating")