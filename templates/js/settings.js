$(function() {
    var $modal = $("#reorder-pages-modal");
    $('#page-list', $modal).sortable({
        containment: $("#page-list-wrapper"),
        placeholder: "placeholder",
        update: function() {
            $('#page-list li').each(function(index) {
                $(this).removeClass("even");
                $(this).removeClass("odd");
                $(this).addClass(index % 2 == 0 ? 'even' : 'odd');
            });
        }
    });
    $('#page-list', $modal).disableSelection();

    function getPages() {
        var pages = []
        $("#page-list li", $modal).each(function(index) {
            var $this = $(this);
            pages.push($this.data("pageid"));
        });
        return pages;
    }

    function on_error(msg) {
        $this.button("reset");
        $("cancel-reorder-pages").button('reset');
        $modal.modal('unlock');
        toast('error', msg || '操作失败，请稍后再试。');
    }

    $("#reorder-pages").click(function() {
        var $this = $(this);
        $this.button("loading");
        $("#cancel-reorder-pages").button('loading');
        $modal.modal('lock');

        Dajaxice.microsite.reorder_pages(function(data) {
            // setTimeout(function() {
            $this.button("reset");
            $("#cancel-reorder-pages").button('reset');
            $modal.modal('unlock');

            if(data.ret_code !== 0) {
                toast('error', data.ret_msg);
                return;
            }

            toast('success', data.ret_msg);
            setTimeout(function() {
                $modal.modal('hide');
                window.location.reload();
            }, 2000);
            // }, 10000);
        }, {'page_list': getPages().join(',')}, {'error_callback': on_error});
    });
});
