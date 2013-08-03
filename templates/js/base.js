var toast = function(type, text) {
    $.pnotify({
        text: text,
        type: type,
        delay: 3000,
        history: false,
        stack: false,
        closer: false,
        sticker: false,
        before_open: function(pnotify) {
            pnotify.css({
                "top": ($(window).height() / 2) - (pnotify.height() / 2),
                "left": ($(window).width() / 2) - (pnotify.width() / 2)
            });
        }
    });
};