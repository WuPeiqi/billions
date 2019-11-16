#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.template import Library
from django.conf import settings

register = Library()


@register.inclusion_tag('billions/preview/css.html')
def preview_css():
    return {
        'links': [
            'billions/editormd/css/editormd.preview.css',
            'billions/billions-preview-init.css',
        ]
    }


@register.inclusion_tag('billions/preview/content.html')
def preview_content(text, config_name='default', area_id='billions_preview_area'):
    config = settings.PREVIEW_CONFIGS.get(config_name)['config']
    return {
        'area_id': area_id,
        'text': text,
        'billions_preview_config': json.dumps(config)

    }


@register.inclusion_tag('billions/preview/js.html')
def preview_js(config_name='default'):
    plugins = settings.PREVIEW_CONFIGS.get(config_name)['plugins']
    return {
        'scripts': plugins
    }
