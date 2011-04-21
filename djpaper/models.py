from django.db import models

# Create your models here.

class People(models.Model):
	name = models.CharField(max_length=30)
	depBig = models.ForeignKey('Department')
	depSmall = models.ForeignKey('DepartmentChild',blank=True,null=True)
	headshot = models.ImageField(upload_to='/tmp')
	pswd = models.CharField(max_length=32)
	
	def __unicode__(self):
		return self.name
#class Department(models.Model):
#	name = models.CharField(max_length=30)
#	childs = models.ForeignKey('self',blank=True,null=True,related_name='deptmnt')
#	isLocal = models.BooleanField()
#
#class DpHierarchy(models.Model):
#	parent = models.ForeignKey('self',blank=True,null=True)
#	class Meta:
#		abstract = True
class Department(models.Model):
	name = models.CharField(max_length=30)
	isLocal = models.BooleanField()
	
	def __unicode__(self):
		return self.name

class DepartmentChild(models.Model):
	parents = models.ForeignKey(Department)
	name = models.CharField(max_length=30)
	def __unicode__(self):
		return self.name

class Paper(models.Model):
	title = models.CharField(max_length=100)
	author = models.ForeignKey(People)
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

	
