from django.db import models

# Create your models here.

class People(models.Model):
	name = models.CharField(max_length=30)
	departTree = models.ForeignKey('Department')
	headshot = models.ImageField(upload_to='images/people/%Y%m%d')
			
	def __unicode__(self):
		return self.name
	def get_ab_url(self):
		return "/people/%s/" % self.id

class Account(models.Model):
	name = models.CharField(max_length=32)
	pswd = models.CharField(max_length=32)
	department = models.ForeignKey('Department')
	
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
	publication = models.ForeignKey('Publication')
	pub_date = models.DateField()
	tag = models.ManyToManyField('Tag')
	abstract = models.TextField()

	def __unicode__(self):
		return self.title
	
	def get_ab_url(self):
		return "/paper/%i/" % self.id
	def all_the_authors(self):
		_author = ""
		for au in self.author.all():
			_author += au.name+"; "	
		return "%s " % _author   
	def all_the_tags(self):
		_tag=""
		for t in self.tag.all():
			_tag += t.title + "; "
		return "%s" % _tag 
class Pic(models.Model):
	upload_date = models.DateField()
	paper = models.ForeignKey(Paper)
	image = models.ImageField(upload_to='images/%Y/%m/%d')

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

	
