$(function() {
    var $modal = $("#reorder-pages-modal");
    var highLightTask = -1;
    var DURATION = 1000;

    function ensureBtns() {
        $(".move-up, .move-down", $modal).removeClass("disabled");
        $(".move-up", $modal).first().addClass("disabled");
        $(".move-down", $modal).last().addClass("disabled");
    }

    function swap(r1, r2) {
        if(highLightTask != -1) {
            $("tr.highlight", $modal).removeClass("highlight");
            clearTimeout(highLightTask);
            highLightTask = -1;
        }

        r1.detach();
        r1.addClass("highlight");
        r1.insertAfter(r2);
        highLightTask = setTimeout(function() {
            r1.removeClass("highlight");
            highLightTask = -1;
        }, DURATION);
    }

    function moveUp() {
        var $this = $(this);
        if($this.hasClass("disabled")) {
            return;
        }

        var $curRow = $this.parent().parent();
        var $prevRow = $curRow.prev();
        swap($prevRow, $curRow);
        ensureBtns();
    }

    function moveDown() {
        var $this = $(this);
        if($this.hasClass("disabled")) {
            return;
        }

        var $curRow = $this.parent().parent();
        var $nextRow = $curRow.next()
        swap($curRow, $nextRow);
        ensureBtns();
    }

    $(".move-up", $modal).click(moveUp);
    $(".move-down", $modal).click(moveDown);

    function getPages() {
        var pages = []
        $("td.page", $modal).each(function(index) {
            var $this = $(this);
            pages.push($this.data("pageid"));
        });
        return pages;
    }

    function on_error(msg) {
        $this.button("reset");
        toast('error', msg || '操作失败，请稍后再试。');
    }

    $("#reorder-pages").click(function() {
        var $this = $(this);
        $this.button("loading");

        Dajaxice.microsite.reorder_pages(function(data) {
            $this.button("reset");
            if(data.ret_code !== 0) {
                toast('error', data.ret_msg);
                return;
            }

            toast('success', data.ret_msg);
            $modal.modal('hide');
            setTimeout(function() {
                window.location.reload();
            }, 500);
        }, {'page_list': getPages().join(',')}, {'error_callback': on_error});
    });
});
