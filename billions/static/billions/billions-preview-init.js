(function () {
    $('.billions-preview-area').each(function () {
        var area_id = $(this).attr('id');
        var config = JSON.parse($(this).find('textarea').attr('billions-preview-config'));
        editormd.markdownToHTML(area_id, config);
    });
})();