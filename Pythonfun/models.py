from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Tag(models.Model):
    """文章标签模型"""
    name = models.CharField(_("标签名称"), max_length=50, unique=True)
    slug = models.SlugField(_("URL别名"), max_length=50, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = _("标签")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class MainCategory(models.Model):
    """主分类模型"""
    name = models.CharField(_("主分类名称"), max_length=100, unique=True)
    slug = models.SlugField(_("URL别名"), max_length=100, unique=True, allow_unicode=True)
    order = models.PositiveIntegerField(_("排序权重"), default=0, help_text=_("数字越大，排序越靠后"))
    is_enabled = models.BooleanField(_("是否启用"), default=True)
    icon = models.CharField(_("图标类名"), max_length=50, blank=True, null=True, help_text=_("例如：fas fa-book"))
    description = models.TextField(_("描述"), blank=True, null=True)

    class Meta:
        verbose_name = _("主分类")
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    """子分类模型"""
    parent = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories', verbose_name=_("所属主分类"))
    name = models.CharField(_("子分类名称"), max_length=100)
    slug = models.SlugField(_("URL别名"), max_length=100, allow_unicode=True)
    is_enabled = models.BooleanField(_("是否启用"), default=True)
    icon = models.CharField(_("图标类名"), max_length=50, blank=True, null=True)
    description = models.TextField(_("描述"), blank=True, null=True)

    class Meta:
        verbose_name = _("子分类")
        verbose_name_plural = verbose_name
        unique_together = ('parent', 'name') # 同一主分类下，子分类名称不能重复
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.name} -> {self.name}"

class Article(models.Model):
    """文章模型"""
    class ContentType(models.TextChoices):
        TUTORIAL = 'TU', _('教程')
        STRUCTURE = 'ST', _('结构')
        STORY = 'SO', _('故事')

    title = models.CharField(_("文章标题"), max_length=200)
    subtitle = models.CharField(_("副标题"), max_length=200, blank=True, null=True)
    summary = models.TextField(_("摘要"))
    content_type = models.CharField(_("内容类型"), max_length=2, choices=ContentType.choices, default=ContentType.TUTORIAL)
    read_time_minutes = models.PositiveIntegerField(_("预计阅读时间"), default=5)
    
    content_html = models.TextField(_("富文本内容"), help_text=_("用于存储TinyMCE编辑器的HTML内容"))
    content_code = models.TextField(_("代码内容"), blank=True, null=True, help_text=_("用于存储Monaco编辑器的代码"))
    code_language = models.CharField(_("代码语言"), max_length=50, default='python')

    category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("所属分类"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("标签"))

    is_published = models.BooleanField(_("是否发布"), default=False)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("文章")
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def clean(self):
        """模型验证"""
        if self.is_published:
            if not self.title or self.title.strip() == '':
                raise ValidationError(_('发布时文章标题不能为空'))
            if not self.category:
                raise ValidationError(_('发布时必须选择文章分类'))
            if not self.summary or self.summary.strip() == '':
                raise ValidationError(_('发布时文章摘要不能为空'))
            if not self.content_html or self.content_html.strip() == '':
                raise ValidationError(_('发布时文章内容不能为空'))
            
    def save(self, *args, **kwargs):
        """保存前的验证"""
        if self.is_published:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title