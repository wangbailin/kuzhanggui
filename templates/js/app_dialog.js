var addEditJoinItem = function()  {
    $('#add_edit_join_item_save').button('loading');
    Dajaxice.microsite.add_edit_join_item(Dajax.process, {'form' : $('#add_edit_join_item_form').serialize(true)});
}

var addEditJoinItemCallback = function(data) {
    var type= 'success';
    if (data.ret_code==0){
        $('#add_edit_join_item').modal('hide');
    }
    else{
        type = 'error';
        $('#add_edit_join_item').button('reset');
    }
    toast(type, data.ret_msg);
};

var addCaseClass = function()  {
    $('#add_case_class_save').button('loading');
    Dajaxice.microsite.add_case_class(Dajax.process, {'form' : $('#add_case_class_form').serialize(true)});
};

var addCaseClassCallback = function(data) {
    var type= 'success';
    if (data.ret_code==0){
        $('#add_case_class').modal('hide');
    }
    else{
        type = 'error';
        $('#add_case_class_save').button('reset');
    }
    toast(type, data.ret_msg);
};

var addProductClass = function()  {
    $('#add_product_class_save').button('loading');
    Dajaxice.microsite.add_product_class(Dajax.process, {'form' : $('#add_product_class_form').serialize(true)});
};

var addProductClassCallback = function(data) {
    var type= 'success';
    if (data.ret_code==0){
        $('#add_product_class').modal('hide');
    }
    else{
        type = 'error';
        $('#add_product_class_save').button('reset');
    }
    toast(type, data.ret_msg);
};

var changeCaseClass = function()  {
    $('#change_case_class_save').button('loading');
    Dajaxice.microsite.change_case_class(Dajax.process, {'form' : $('#change_case_class_form').serialize(true)});
};

var changeCaseClassCallback = function(data) {
    var type= 'success';
    if (data.ret_code==0){
        $('#change_case_class').modal('hide');
    }
    else{
        type = 'error';
        $('#change_case_class_save').button('reset');
    }
    toast(type, data.ret_msg);
};


var changeProductClass = function()  {
    $('#change_product_class_save').button('loading');
    Dajaxice.microsite.change_product_class(Dajax.process, {'form' : $('#change_product_class_form').serialize(true)});
};

var changeProductClassCallback = function(data) {
    var type= 'success';
    if (data.ret_code==0){
        $('#change_product_class').modal('hide');
    }
    else{
        type = 'error';
        $('#change_product_class_save').button('reset');
    }
    toast(type, data.ret_msg);
};

var addEditContactPeople = function()  {
    $('#add_edit_contact_people_save').button('loading');
    Dajaxice.microsite.add_edit_contact_people(Dajax.process, {'form' : $('#add_edit_contact_people_form').serialize(true)});
};

var addEditContactPeopleCallback = function(data) {
    var type= 'success';
    if (data.ret_code==0){
        $('#add_edit_contact_people').modal('hide');
    }
    else{
        type = 'error';
        $('#add_edit_contact_people').button('reset');
    }
    toast(type, data.ret_msg);
};

var deleteJoinItem = function(id, name) {
    $('#join_item_name').text(name);
    $('#delete_join_item_ok').attr('href', '/join/' + id + '/delete');
    $('#delete_join_item').modal('show');
}

var deleteTrend = function(id, name) {
    $('#trend_name').text(name);
    $('#delete_trend_ok').attr('href', '/trend/' + id + '/delete');
    $('#delete_trend').modal('show');
};

var deleteTeam = function(id, name) {
    $('#team_name').text(name);
    $('#delete_team_ok').attr('href', '/team/' + id + '/delete');
    $('#delete_team').modal('show');
};


var deleteContact = function(id, name) {
    $('#contact_name').text(name);
    $('#delete_contact_ok').attr('href', '/contact/' + id + '/delete');
    $('#delete_contact').modal('show');
};

var deleteContactPeople = function(id, name) {
    $('#contact_people_name').text(name);
    $('#delete_contact_people_ok').attr('href', '/contact_people/' + id + '/delete');
    $('#delete_contact_people').modal('show');
};

var deleteCase = function(id, name) {
    $('#case_name').text(name);
    $('#delete_case_ok').attr('href', '/case/' + id + '/delete');
    $('#delete_case').modal('show');
};

var deleteCaseClass = function(id, name) {
    $('#case_class_name').text(name);
    $('#delete_case_class_ok').attr('href', '/case_class/' + id + '/delete');
    $('#delete_case_class').modal('show');
};

var deleteProduct = function(id, name) {
    $('#product_name').text(name);
    $('#delete_product_ok').attr('href', '/product/' + id + '/delete');
    $('#delete_product').modal('show');
};

var deleteProductClass = function(id, name) {
    $('#case_product_name').text(name);
    $('#delete_product_class_ok').attr('href', '/product_class/' + id + '/delete');
    $('#delete_product_class').modal('show');
};

