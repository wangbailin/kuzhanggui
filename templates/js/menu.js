var addEditMenu = function() {
    $('#add_edit_menu_save').button('loading');
    Dajaxice.microsite.add_edit_menu(Dajax.process, {'form' : $('#add_edit_menu_form').serialize(true)});
};

var addEditMenuCallback = function(data) {
    if (data && data.ret_code == 0) {
        $('#add_edit_menu').modal('hide');
        toast('success', '添加/编辑菜单项成功！')

        location.reload();
    }

    $('#add_edit_menu_save').button('reset');
};

var editMenu = function(id, name, page) {
    $('#id_id').val(id);
    $('#name input').val(name);
    $('#page select').val(page);
    $('#add_edit_menu').modal('show');
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