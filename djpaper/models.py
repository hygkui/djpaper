from django.db import models

# Create your models here.

class People(models.Model):
	name = models.CharField(max_length=30)
	departTree = models.ForeignKey('Department')
	headshot = models.ImageField(upload_to='/tmp/')
			
	def __unicode__(self):
		return self.name

class Account(models.Model):
	name = models.CharField(max_length=32)
	pswd = models.CharField(max_length=32)
	department = models.ForeignKey('Department')
	mode = models.ManyToManyField('ModeAuth')

	def __unicode__(self):
		return self.name

class ModeAuth(models.Model):
	name = models.CharField(max_length=32)
	value = models.IntegerField()

	def __unicode__(self):
		return self.name
	
class Department(models.Model):
	parent = models.ForeignKey('self',blank=True,null=True)
	name = models.CharField(max_length=30)
	level = models.IntegerField() 

	def __unicode__(self):
		return self.name

class Paper(models.Model):
	title = models.CharField(max_length=100)
	author = models.ManyToManyField(People)
	pic = models.ManyToManyField('Pic')
	publication = models.ForeignKey('Publication')
	pub_date = models.DateField()
	tag = models.ManyToManyField('Tag')
	abstract = models.CharField(max_length=1000)

	def __unicode__(self):
		return self.title

class Pic(models.Model):
	upload_date = models.DateField()
	author = models.ForeignKey(People)
	image = models.ImageField(upload_to='/tmp')

class Tag(models.Model):
	title = models.CharField(max_length=30)
	times = models.IntegerField(default=1)

	def __unicode__(self):
		return self.title

class Publication(models.Model):
	name = models.CharField(max_length=100)
	reg = models.CharField(max_length=100)
	classType = models.ForeignKey('Type')
	publisher = models.ForeignKey('Publisher')

	def __unicode__(self):
		return self.name

class Publisher(models.Model):
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return self.name

class Type(models.Model):
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return self.name

class ShortMessage(models.Model):
	source  = models.ForeignKey(People,related_name='p_source')
	dest = models.ForeignKey(People,related_name='p_dest')
	title = models.CharField(max_length=100)
	msg = models.CharField(max_length=1000)
	msg_date = models.DateField()
	isRead = models.BooleanField()
	child = models.CharField(max_length=20,default='--to be')

	def __unicode__(self):
		return self.title

	
