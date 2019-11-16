(function () {

    $('.billions-area').find('textarea').each(function () {
        var config = JSON.parse($(this).attr('billions-config'));
        editormd(config);
    });
})();