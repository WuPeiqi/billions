## 插件说明
> billions组件是基于前端插件 editor.md 和 django 整合起来一个组件，基于它可以在项目中快速实现markdown编辑器的功能（参考django-ckeditor源码的实现方式）。

## 组件的应用

在使用此组件时，一定需要先将咱们的组件 billions 注册到 django 的 app 中。
```
INSTALLED_APPS = [
    ...
    'billions.apps.BillionsConfig',
]

# 错误提示中文
LANGUAGE_CODE = 'zh-hans'
```


### 1.编辑&可视化

#### 1.1 Model中定义相关字段。

```
from billions.fields import BillionsMarkdownTextField

class Index(models.Model):
    
    title = models.CharField(verbose_name='标题', max_length=64, db_index=True)
    text = BillionsMarkdownTextField(verbose_name='内容',config_name='default')  # config_name参数指在配置文件中为改插件定义的属性。
```
#### 1.2 定义ModelForm 或 Form
```
from django import forms

# 定义ModelForm
class IndexModelForm(forms.ModelForm):
    class Meta:
        model = models.Index
        fields = "__all__"


# 定义Form字段
from django import forms
from billions.fields import BillionsMarkdownTextFormField
class IndexModelForm1(forms.ModelForm):
    title = forms.CharField()
    text = BillionsMarkdownTextFormField(config_name='default')


# 自定义Form插件
from django import forms
from billions.widgets import BillionsMarkdownEditorWidget
class IndexModelForm2(forms.ModelForm):
    title = forms.CharField()
    text = forms.CharField(widget=BillionsMarkdownEditorWidget(config_name='default'))

```

#### 1.3 配置路由
```

from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from billions.views import billions_upload_image

urlpatterns = [
    # 固定写法，用于上传图片。
    url(r'^billions/upload/image/$', billions_upload_image, name='billions_upload_image'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    
    # 视图函数，编辑markdown页面
    url(r'^edit/$', edit), 
]

```

#### 1.4 视图函数中使用Form或ModelForm

```
def edit(request):
    form = IndexModelForm()
    return render(request,'edit.html',{'form':form})
```


#### 1.5 HTML模板中应用

```
{% load staticfiles %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>pythonav资源分享</title>
    {{ form.media.css }}
</head>
<body>
     
    {% for field in form %}
        {{field}}
    {% endfor %}
     
    <script src='jquery'></script>
    {{ form.media.js }}
</body>
</html>
```

#### 1.6 定制markdown功能:settings.py
```

# 定义media（用于文件上传）
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# 文件上传到 /media/updoads目录下
BILLIONS_UPLOAD_PATH = "uploads/"

# 配置文件（完全按照editor.md插件的配置，详见：http://editor.md.ipandao.com/ ）
BILLIONS_CONFIGS = {
    'default': {
        # 文件上传的URL
        'imageUploadURL': "/billions/upload/image/",
    }
}

```


### 2.markdown格式数据展示

此处某些配置和上一步中【编辑&可视化】中的某些配置可能重复(url.py和settings.py)，如果两个功能都想用，只需要配置一遍即可。

#### 2.1 配置路由

```

from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from billions.views import billions_upload_image

urlpatterns = [
    # 固定写法，用于显示图片。
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    
    # 视图函数，编辑markdown页面
    url(r'^index/$', index), 
]

```

#### 2.2 视图函数

```
def index(request):
    content = """###科学公式 TeX(KaTeX)          
    $$E=mc^2$$
    ![](/media/uploads/2019/05/15/1111_AUhxSxW.png?20)
    """
    return render(request,'index.html',{'content':content})
    
```

#### 2.3 模板

```
{% load billions %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    {% preview_css %}
</head>
<body>


<div class="luffy-container">
    {% preview_content content 'default' %}

</div>


<script src='https://cdn.bootcss.com/jquery/3.4.1/jquery.js'></script>
{% preview_js %}

</body>
</html>
```

#### 2.4 配置文件

```

# 定义media（用于文件上传）
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# 文件上传到 /media/updoads目录下
BILLIONS_UPLOAD_PATH = "uploads/"

# 用于展示markdown
BILLIONS_PREVIEW_CONFIGS = {
    'default': {
        'config': {
            "htmlDecode": True,
            "taskList": True,
        },
        'plugins': [
            'billions/editormd/lib/marked.min.js',
            'billions/editormd/lib/prettify.min.js',
            'billions/editormd/editormd.js',
            'billions/mdeditor-preview-init.js'
        ]
    },
    'article':{
        'config': {
            "htmlDecode": True,
            "emoji": True,
            "taskList": True,
            "tex: true"
            "flowChart": True,
            "sequenceDiagram": True,
            "tocContainer": "#custom-toc-container",
            "tocDropdown": False,
        },
        'plugins': [
            'billions/editormd/lib/marked.min.js',
            'billions/editormd/lib/prettify.min.js',
            'billions/editormd/editormd.js',
            'billions/editormd/lib/raphael.min.js',
            'billions/editormd/lib/underscore.min.js',
            'billions/editormd/lib/sequence-diagram.min.js',
            'billions/editormd/lib/flowchart.min.js',
            'billions/editormd/lib/jquery.flowchart.min.js',
            'billions/billions-preview-init.js'
        ]
    },
}

```


## 写在最后

值得注意的是，此组件中对前端插件 editor.md 中的 markend.min.js 进行了修改，以支持图片显示的缩放。
- 原内容
    ```javascript
    Renderer.prototype.image = function(href, title, text) {
      href = cleanUrl(this.options.sanitize, this.options.baseUrl, href);
      if (href === null) {
        return text;
      }
      var out = '<img src="' + href + '" alt="' + text + '"';
      if (title) {
        out += ' title="' + title + '"';
      }
      out += this.options.xhtml ? '/>' : '>';
      return out;
    };
    
    ```

- 修改为
    ```javascript
    Renderer.prototype.image = function(href, title, text) {
      href = cleanUrl(this.options.sanitize, this.options.baseUrl, href);
      if (href === null) {
        return text;
      }
    
      var out = '<img src="' + href + '" alt="' + text + '"';
      if (title) {
        out += ' title="' + title + '"';
      }
    
      var array = href.split('?');
      if(array.length > 1){
        var param = array[array.length-1];
        var width_height = param.split('*');
        var style = "";
        if(width_height.length == 1){
          style += 'width:' + width_height[0] + '%;';
        }else if(width_height.length == 2){
          style += 'width:' + width_height[0] + 'px;height:' + width_height[1] + 'px;';
        }
        out += ' style="' + style + '"';
      }
    
      //var array = href.split('?');if(array.length > 1){var param = array[array.length-1];var width_height = param.split('*');var style = "";if(width_height.length == 1){style += 'width:' + width_height[0] + '%;';}else if(width_height.length == 2){style += 'width:' + width_height[0] + 'px;height:' + width_height[1] + 'px;';}out += " style='" + style + "'";}
    
      out += this.options.xhtml ? '/>' : '>';
      return out;
    };
    
    ```

所以，以后如果想要更新前端插件 editor.md，记得在 marked.js 中修改上述的内容。

那么，以后再编写文档时候，只需要按照如下格式，就是控制图片的大小：

```

# 按照：50%缩放
![](/media/uploads/2019/05/15/1111_AUhxSxW.png?50) 

# 按照：宽度50px;高度200px
![](/media/uploads/2019/05/15/1111_AUhxSxW.png?50*200)

```












