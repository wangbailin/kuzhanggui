var addCaseClass = function()  {
    $('#add_case_class_save').button('loading');
    Dajaxice.framework.add_case_class(Dajax.process, {'form' : $('#add_case_class_form').serialize(true)});
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
    Dajaxice.framework.add_product_class(Dajax.process, {'form' : $('#add_product_class_form').serialize(true)});
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

