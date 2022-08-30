from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


@admin.register(Tag)
class ScopeAdmin(admin.ModelAdmin):
    pass


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                count += 1

        if count > 1:
            raise ValidationError('Только одна категория может быть основной')

        if count == 0:
            raise ValidationError('Укажите основную категорию')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
