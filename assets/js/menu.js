var on_error = function() {
    $('#add_edit_menu_save').button('reset');
    $('#add_edit_menu_cancel').button('reset');
    $("#add_edit_menu").modal('unlock');
    toast('error', '添加/编辑菜单项失败！');
}

var addEditMenu = function() {
    var form = $("#add_edit_menu_form")[0];
    var data = {
        id: form.id.value != '' ? form.id.value : null,
        name: form.name.value,
        pages: form.pages.value
    };

    $('#add_edit_menu_save').button('loading');
    $('#add_edit_menu_cancel').button('loading');
    $("#add_edit_menu").modal('lock');
    Dajaxice.microsite.add_edit_menu(function(data) {
        // setTimeout(function() {
        $('#add_edit_menu_save').button('reset');
        $('#add_edit_menu_cancel').button('reset');
        $("#add_edit_menu").modal('unlock');

        if(!data || data.ret_code != 0) {
            toast('error', data.ret_msg);
            return;
        }

        toast('success', '添加/编辑菜单项成功！');

        setTimeout(function() {
            $('#add_edit_menu').modal('hide');
            location.reload();
        }, 2000);
        // }, 10000);
    }, data, {'error_callback': on_error});
};

var editMenu = function(id, name, pages) {
    $('#id_id').val(id);
    $('#name input').val(name);
    $('#add_edit_menu').modal('show');
    $('#pages').val(pages.split(',')).trigger('change');
};

var deleteMenu = function(id, name) {
    $('#menu_name').text(name);
    $('#delete_menu_ok').attr('href', '/menu/' + id + '/delete');
    $('#delete_menu').modal('show');
};

var generateMenu = function() {
    if (!$('#generate_menu').hasClass('disabled')) {
        $('#generate_menu').button('loading');
        Dajaxice.microsite.generate_menu(Dajax.process, {});
    }
};

var generateMenuCallback = function(data) {
    if (data) {
        if (data.ret_code == 0) {
            toast('success', '生成菜单成功，请重新关注微信公众号查看效果！');
        } else {
            toast('error', data.ret_msg);
        }
    }

    $('#generate_menu').button('reset');
}

$(function() {

$('#nav-menu').addClass('active');
$('#add_edit_menu_save').click(addEditMenu);

var tags = [];
$(".pages button").each(function() {
    var $this = $(this);
    tags.push({id: $this.data("pageid"), text: $this.text()});
});

var $pageSelector = $("#pages");
$pageSelector.select2({ 
    initSelection: function(element, callback) {
        var $el = $(element);
        var pages = $el.val().split(",");
        var data = []
        $(tags).each(function() {
            var index = pages.indexOf(this.id.toString());
            if(index != -1) {
                data[index] = this;
            }
        });
        callback(data);
    },
    query: function(options) {
        var bingo = [];
        $(tags).each(function() {
            if(options.term != '' && this.text.indexOf(options.term) != -1) {
                bingo.push(this);
            }
        });
        options.callback({results: bingo, more: false, context: options.context});
    },
    formatNoMatches: function() {
        return '';
    },
    tags: tags,
    createSearchChoice: function(term) { return null; }
});

$pageSelector.select2("container").find("ul.select2-choices").sortable({
    containment: 'parent',
    start: function() { $pageSelector.select2("onSortStart"); },
    update: function() { $pageSelector.select2('onSortEnd'); }
});

$('#add_edit_menu').on('hidden', function() {
    $('#name input').val('');
    $('#page input').val('');
    $('#id_id').val('');
    $('#add_edit_menu .control-group').removeClass('error');
    $pageSelector.select2('val', null, true);
});

$pageSelector.change(function() {
    $(".pages > button").removeClass("selected");
    var selectedPages = $pageSelector.select2('val') || [];
    for(var i = 0; i < selectedPages.length; i++) {
        var $page = $("#page_" + selectedPages[i]).addClass("selected");
    }
});

$(".pages > button").click(function(e) {
    e.preventDefault();
    var $this = $(this);
    var selectedPages = $pageSelector.select2('val') || [];
    var pageid = $this.data("pageid");
    var index = selectedPages.indexOf(pageid.toString());
    if(index != -1) {
        selectedPages.splice(index, 1);
    } else {
        selectedPages.push(pageid);
    }
    $pageSelector.select2('val', selectedPages, true);
});

});
