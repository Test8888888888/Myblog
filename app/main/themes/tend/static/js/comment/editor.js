$(function () {
    var simplemde = new SimpleMDE({
        element: document.getElementById("comment-form"),
        autoDownloadFontAwesome: false,
        insertTexts: {
            horizontalRule: ["", "\n\n-----\n\n"],
            image: ["![图片Alt](http://", ")"],
            link: ["[链接描述](http://", ")"],
            table: ["", "\n\n| Column 1 | Column 2 | Column 3 |\n| -------- | -------- | -------- |\n| Text     | Text      | Text     |\n\n"],
        },
        toolbar: [{
            name: "bold",
            action: SimpleMDE.toggleBold,
            className: "fa fa-bold",
            title: "粗体",
            "default": !0
        }, {
            name: "italic",
            action: SimpleMDE.toggleItalic,
            className: "fa fa-italic",
            title: "斜体",
            "default": !0
        }, {
            name: "quote",
            action: SimpleMDE.toggleBlockquote,
            className: "fa fa-quote-left",
            title: "引用",
            "default": !0
        }, {
            name: "code",
            action: SimpleMDE.toggleCodeBlock,
            className: "fa fa-code",
            title: "代码"
        }, {
            name: "link",
            action: SimpleMDE.drawLink,
            className: "fa fa-link",
            title: "插入链接",
            "default": !0
        }, {
            name: "image",
            action: SimpleMDE.drawImage,
            className: "fa fa-picture-o",
            title: "插入图片",
            "default": !0
        }, {
            name: "table",
            action: SimpleMDE.drawTable,
            className: "fa fa-table",
            title: "插入表格"
        }, {
            name: "preview",
            action: SimpleMDE.togglePreview,
            className: "fa fa-eye no-disable",
            title: "预览",
            "default": !0
        }],
    });
    $(".editor-statusbar").append("<span class='float-left text-info ml-0 hidden' id='rep-to'></span>");
    $("#editor-footer").append("<button type='button' class='btn btn-danger btn-sm float-right mr-4 f-16 hidden' id='no-rep'>取消回复</button>");

    var emoji_tag = $("#emoji-list img");
    emoji_tag.click(function () {
        var e = $(this).data('emoji');
        simplemde.value(simplemde.value() + e);
    });

//    粘贴图片
    /*图片粘贴功能实现*/

    $('#write-editor').on("paste", function (e) {

        //判断图片类型的正则
        var isImage = (/.jpg$|.jpeg$|.png$|.gif$/i);
        var e = e || event;
        var contentE = $('#content');
        var img = null;
        //IE支持window.clipboardData,chrome支持e.originalEvent.clipboardData
        var clipboardData = e.originalEvent.clipboardData || window.clipboardData;
        if (!(clipboardData && clipboardData.items)) {
            return;
        }

        for (var i = 0, length = clipboardData.items.length; i < length; i++) {
            var item = clipboardData.items[i];
            if (item.kind === 'file' && isImage.test(item.type)) {
                img = item.getAsFile();
                var url = '/common/upload';
                var formData = new FormData();
                formData.append('file', img);

                //上传图片
                var xhr = new XMLHttpRequest();
                //上传结束
                xhr.onload = function () {
                    var data = JSON.parse(xhr.responseText);
                    //console.log(data)
                    if (data.code === 200) {
                        if (contentE.val().length === 0) {
                            contentE.insertAtCousor("![image](" + data.detail + ")\r\n");
                        } else {
                            contentE.insertAtCousor("\r\n![image](" + data.detail + ")");
                        }
                        var currentPosition = contentE.getSelectionEnd();
                        contentE.setSelection(currentPosition);
                    }
                }

                xhr.open('POST', url, true);
                xhr.send(formData);
                //当剪贴板里是图片时，禁止默认的粘贴
                return false;
            }
        }

    });
    /*smc 2018.12.26 end*/
//    点击回复
    $(".rep-btn").click(function () {
        simplemde.value('')
        var u = $(this).data('repuser')
        var i = $(this).data('repid')
        sessionStorage.setItem('rep_id', i);
        $("#rep-to").text("回复 @" + u).removeClass('hidden');
        $("#no-rep").removeClass('hidden');
        $(".rep-btn").css("color", "#868e96");
        $(this).css("color", "red");
        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top - 55
        }, 500);
    });

//    点击取消回复
    $("#no-rep").click(function () {
        simplemde.value('')
        sessionStorage.removeItem('rep_id');
        $("#rep-to").text('').addClass('hidden');
        $("#no-rep").addClass('hidden');
        $(".rep-btn").css("color", "#868e96");
    });

//    点击提交评论
    $("#push-com").click(function () {
        var content = simplemde.value();
        if (content.length == 0) {
            alert("评论内容不能为空！");
            return;
        }
        if (content.length > 1048) {
            alert("评论字数(含空格)为：" + content.length + "，超过1048，请精简后再提交！");
            return;
        }
        var base_t = sessionStorage.getItem('base_t');
        base_t = 0;
        var now_t = Date.parse(new Date());
        if (base_t) {
            var tt = now_t - base_t;
            if (tt < 40000) {
                alert('两次评论时间间隔必须大于40秒，还需等待' + (40 - parseInt(tt / 1000)) + '秒');
                return;
            } else {
                sessionStorage.setItem('base_t', now_t);
            }
        } else {
            sessionStorage.setItem('base_t', now_t)
        }
        ;
        var article_id = $(this).data('article-id');
        var URL = $(this).data('ajax-url');
        var rep_id = sessionStorage.getItem('rep_id');
        if (!rep_id) {
            rep_id = 0;
        }
        $.ajax({
            type: 'post',
            url: URL,
            data: {
                'reply_id': rep_id,
                'content': content,
                'article_id': article_id
            },
            dataType: 'json',
            success: function (ret) {
                console.log(ret)
                if (ret.code === 1) {
                    simplemde.value('')
                    sessionStorage.removeItem('rep_id');
                    sessionStorage.setItem('new_point', ret.id);
                    window.location.reload();
                }
            },
            error: function (ret) {
                alert(ret.msg);
            }
        });
    });

//    提交评论后定位到新评论处
    if (sessionStorage.getItem('new_point')) {
        var top = $(sessionStorage.getItem('new_point')).offset().top - 100;
        $('body,html').animate({scrollTop: top}, 200);
        window.location.hash = sessionStorage.getItem('new_point');
        sessionStorage.removeItem('new_point');
    }
    ;
    sessionStorage.removeItem('rep_id');

    $(".comment-body a").attr("target", "_blank");
})


var sw = window.screen.width;
if (sw > 1200) {
    POWERMODE.colorful = true;
    POWERMODE.shake = false;
    document.body.addEventListener('input', POWERMODE)
}
;