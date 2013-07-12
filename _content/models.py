from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeOneToOneField
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify

# Create your models here.

class StructureNode(MPTTModel):
    title = models.CharField(max_length=200)
    pubDate = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    #setting up content
    #If both content_type and id are null then it is a container node
    #Otherwise it is a content node.
    #setting up relationships for multiple model types
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    #need to create a smarter object id that would work across object types.
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey()
    isPublished = models.BooleanField()
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=255, unique=True, blank=True)
    position = models.PositiveIntegerField()
    
    #These methods determine the content type of the node.
    def isTypeNone(self):
        return self.content_type == None
    
    def isTypeParagraph(self):
        return self.content_type == ContentType.objects.get_for_model(Paragraph)
    
    def isTypeImage(self):
        return self.content_type == ContentType.objects.get_for_model(Image)
    
    def isTypeTimelike(self):
        return self.content_type == ContentType.objects.get_for_model(Timelike)
    
    def getNearestAbstractParagraph(self):
        if self.isTypeParagraph():
            return self.content_object.text
        else:
            for child in self.get_descendants():
                if child.isTypeParagraph():
                    return child.content_object.text
                    break
            for predecessor in self.get_ancestors():
                if predecessor.isTypeParagraph():
                    return predecessor.content_object.text
                    break
            else:
                return "NO PARAGRAPHS ANYWHERE!"
            
    def getNearestAbstractImage(self):
        if self.isTypeImage():
            return self.content_object
        else:
            for child in self.get_descendants():
                if child.isTypeImage():
                    return child.content_object
                    break
            for predecessor in self.get_ancestors():
                if predecessor.isTypeImage():
                    return predecessor.content_object
                    break
            else:
                return False
                
    def __str__(self):
        return '%i %i %i %s' % (self.pubDate.year, self.pubDate.month, self.pubDate.day, self.title)
    
    #making a slug and creating ratings and views if it is an aritcle
    def save(self):
        if not self.pk:
            super(StructureNode, self).save()
            if (not self.content_type):
                nodeRating = Rating(structureNode_id=self.id, rating = 1)
                nodeViewCount = ViewCount(structureNode_id=self.id, viewCount= 1)
                nodeRating.save()
                nodeViewCount.save()
        super(StructureNode, self).save()
        if self.slug is None or self.slug == "":
            # create a slug that's unique to siblings
            slug = slugify(self.title)
            self.slug = slug
            siblings = self.get_siblings()
            i = 1
            while siblings.filter(slug=self.slug).exists():
                i += 1
                self.slug = slug + '-%d' % i
        if self.parent:
            self.url = '%s/%s' % (self.parent.url, self.slug)
        else:
            self.url = self.slug
        super(StructureNode, self).save()
    
    class Meta:
        unique_together = ('parent', 'position')
        
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['position']

class Rating(models.Model):
    structureNode = TreeOneToOneField(StructureNode)
    rating = models.PositiveIntegerField()
    
    def __str__(self):
        return self.structureNode.title
    
class ViewCount(models.Model):
    structureNode = TreeOneToOneField(StructureNode)
    viewCount = models.PositiveIntegerField()
    
    def __str__(self):
        return self.structureNode.title
    
class Paragraph(models.Model):
    structureNode = generic.GenericRelation(StructureNode)
    text = models.TextField()
    
    def __str__(self):
        if self.structureNode.order_by('pubDate').exists():
            return self.structureNode.order_by('pubDate')[0].title
        
        return "No Node"
    
class Image(models.Model):
    structureNode = generic.GenericRelation(StructureNode)
    linkSource = models.URLField(max_length=200, blank=True, null=True)
    localSource = models.FileField(upload_to='content/image', blank=True, null=True)
    
    def __str__(self):
        if self.structureNode.order_by('pubDate').exists():
            return self.structureNode.order_by('pubDate')[0].title
        
        return "No Node"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        #allow only one source for video/audio
        
        if not (not self.linkSource) ^ (not self.localSource):
            raise ValidationError('Please select exactly one source')
    
    #This is to determine the type of source    
    def isLinkSource(self):
        return not(not self.linkSource)
    
    def isLocalSource(self):
        return not(not self.localSource)
        
    
class Timelike(models.Model):
    structureNode = generic.GenericRelation(StructureNode)
    linkSource = models.URLField(max_length=200, blank=True, null=True)
    localSource = models.FileField(upload_to='content/image', blank=True, null=True)
    
    def __str__(self):
        if self.structureNode.order_by('pubDate').exists():
            return self.structureNode.order_by('pubDate')[0].title
        
        return "No Node"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        #allow only one source for video/audio
        
        if not (not self.linkSource) ^ (not self.localSource):
            raise ValidationError('Please select exactly one source')
    
    
    #This is to determine the type of source
    def isLinkSource(self):
        return not(not self.linkSource)
    
    def isLocalSource(self):
        return not(not self.localSource)

#These are tags to organize nodes by subject type.    
class tag(models.Model):
    name = models.CharField(max_length=200)
    nodes = models.ManyToManyField(StructureNode)
    
    def __str__(self):
        return self.name
    
    