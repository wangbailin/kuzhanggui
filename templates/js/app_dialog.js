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

