var addWallItem = function()  {
    $('#add_wall_item_save').button('loading');
    Dajaxice.wall.add_wall_item(Dajax.process, {'form' : $('#add_wall_item_form').serialize(true)});
};

var addWallItemCallback = function(data) {
    var type= 'success';
    if (data.ret_code==0){
        $('#add__wall_item').modal('hide');
        location.reload();
    }
    else{
        type = 'error';
        $('#add_wall_item_save').button('reset');
    }
    toast(type, data.ret_msg);
};

var deleteWall = function(id, name) {
    $('#wall_event_name').text(name);
    $('#delete_wall_ok').attr('href', '/wall/' + id + '/delete');
    $('#delete_wall').modal('show');
};

function showNewMessages(datas){
    for (var i=0; i<datas.length; i++){
        if (datas[i][0] == 'text'){
            datas[i][1] = escapeHtml(datas[i][1]);
            var str = '<div class="msgItem" data-id='+datas[i][3]+'><div class="msg-pic"><img src='+'"'+datas[i][4]+'"'+'/></div><div class="msg-meta"><div class="content"><span id="user_name">'+datas[i][2]+'：</span><span id="msg_content">'+emotion(datas[i][1])+'</span><span id="time">'+datas[i][5]+'<span></div><div class ="button"><button style="margin-right:5px;" onclick="passMsg('+datas[i][3]+')"'+'class="btn btn-success">审核</button><button onclick="rejectMsg('+datas[i][3]+')"'+' class="btn">拒绝</button></div></div></div>'
            $('.msgList').append(str);
        }else{
            var str = '<div class="msgItem-pic" data-id='+datas[i][3]+'><div class="msg-pic"><img src='+'"'+datas[i][4]+'"'+'/></div><div class="msg-meta-pic"><div class="content-message"><span id="user_name">'+datas[i][2]+'：分享了一张照片</span><span id="time">'+datas[i][5]+'</span></div><div class="content-pic"><img class="pic" src='+'"'+datas[i][1]+'"'+'/></div><div class ="button"><button style="margin-right:5px;"onclick="passMsg('+datas[i][3]+')"'+' class="btn btn-success">审核</button><button onclick="rejectMsg('+datas[i][3]+')"'+' class="btn">拒绝</button></div></div></div>'
            $('.msgList').append(str);
        }
    }
};

function passMsg(data_id){
    Dajaxice.wall.pass_message(Dajax.process, {'data_id':data_id})  
};

function rejectMsg(data_id){
    Dajaxice.wall.reject_message(Dajax.process, {'data_id':data_id})     
};

function showRejectMessages(data){
    if (data[0] == 'text'){
    data[1] = escapeHtml(data[1]);
    var str = '<div class="msgItem waiting" data-id='+data[3]+'><div class="msg-pic"><img src='+'"'+data[4]+'"'+'/></div><div class="msg-meta"><div class="content"><span id="user_name">'+data[2]+'：</span><span id="msg_content">'+emotion(data[1])+'</span><span id="time">'+data[6]+'<span></div><div class ="button"><button style="margin-right:5px;" onclick="passMsg('+data[3]+')"'+'class="btn btn-success">审核</button></div></div></div>'
    $('.reject-msgList').append(str);
    }else{
    var str = '<div class="msgItem-pic waiting" data-id='+data[3]+'><div class="msg-pic"><img src='+'"'+data[4]+'"'+'/></div><div class="msg-meta-pic"><div class="content-message"><span id="user_name">'+data[2]+'：分享了一张照片</span><span id="time">'+data[6]+'</span></div><div class="content-pic"><img class="pic" src='+'"'+data[1]+'"'+'/></div><div class ="button"><button style="margin-right:5px;"onclick="passMsg('+data[3]+')"'+' class="btn btn-success">审核</button></div></div></div>'
    $('.reject-msgList').append(str);
    }

};

function showPassMessages(data){
    if(data[0] == 'text'){
    data[1] = escapeHtml(data[1]);
    var str = '<div class="msgItem waiting" data-id='+data[3]+'><div class="msg-pic"><img src='+'"'+data[4]+'"'+'/></div><div class="msg-meta"><div class="content"><span id="user_name">'+data[2]+'：</span><span id="msg_content">'+emotion(data[1])+'</span><span id="time">'+data[6]+
'<span></div><div class ="state_wait"><span class="icon-ok icon-time icon-white flag" id="waitforwall"></span>等待上墙</div></div></div>'
    $('.pass-msgList').append(str);
    }else{
    var str = '<div class="msgItem-pic waiting" data-id='+data[3]+'><div class="msg-pic"><img src='+'"'+data[4]+'"'+'/></div><div class="msg-meta-pic"><div class="content-message"><span id="user_name">'+data[2]+'：分享了一张照片</span><span id="time">'+data[6]+'</span></div><div class="content-pic"><img class="pic" src='+'"'+data[1]+'"'+'/></div><div class ="state_wait"><span class="icon-ok icon-time icon-white flag" id="waitforwall"></span>等待上墙</div></div></div>'
     $('.pass-msgList').append(str);
    }
};


function onWall(data){
        var len = $('div[data-id]').length;
        data[1] = escapeHtml(data[1]);
        data[1] = emotion(data[1]);
        if(data[0] == 'text'){
            var data_content=data[2]+"："+data[1];
            var msg_content_css;
            if (data_content.length <= 15){
                msg_content_css = "msg_content_one";
            }else if(data_content.length <=19){
                msg_content_css = "msg_content_two_one";
            }else if(data_content.length <=38){
                msg_content_css = "msg_content_two";
            }else if (data_content.length <= 48){
                msg_content_css = "msg_content_three_two";
            }else{
                msg_content_css = "msg_content_three";
            } 
            str = '<div style="display:none" type="text" class="msgItem-on-wall" '+'data-id='+data[3]+'> <div class="msg-pic-on-wall"><img src="'+data[4]+'"/></div><div class="msg-content"><p id="'+msg_content_css+'">'+'<span id="name">'+data[2]+'</span>'+'：'+data[1]+'</p></div></div>';
            $('.on-wall-msgList').append(str);
            //对不同情况进行判断
            var add_id = 'div[data-id ='+data[3]+']';
            var id = $('div[data-id]').get(0).getAttribute("data-id");
            var delete_id = 'div[data-id ='+id+']';
            if (len == 0||len == 1){
                $(add_id).fadeIn(3000);
            }else if (len == 2){
                var type1 = $('div[data-id]').get(0).getAttribute("type");
                var type2 = $('div[data-id]').get(1).getAttribute("type");
                if (type1 == 'pic' || type2=='pic'){
                    $(delete_id).fadeOut(3000,function(){
                    $(delete_id).remove();
                    $(add_id).fadeIn(3000);
                });
                }else{
                    $(add_id).fadeIn(3000);
                }
            }else if (len == 3){
                $(delete_id).fadeOut(3000,function(){
                    $(delete_id).remove();
                    $(add_id).fadeIn(3000);
                });
            }else{}
        }else{
        var str = '<div style="display:none" type="pic" class="msgItem-on-wall-pic" '+'data-id='+data[3]+'> <div class="msg-pic-on-wall"><img src="'+data[4]+'"/></div><div class="msg-content-on-wall"><span id ="name">'+data[2]+'：</span>分享了一张照片</div>'+' <div id="pic-content-on-wall"><img src="'+data[1]+'"/></div></div>'
        $('.on-wall-msgList').append(str);
        //对不同情况进行判断
        var add_id = 'div[data-id ='+data[3]+']';
        var id = $('div[data-id]').get(0).getAttribute("data-id");
        var delete_id = 'div[data-id ='+id+']';
        if (len == 0){
            $(add_id).fadeIn(3000);
        }else if (len == 1){
            var type = $('div[data-id]').get(0).getAttribute("type");
            if (type == 'pic'){
                $(delete_id).fadeOut(3000,function(){
                    $(delete_id).remove();
                    $(add_id).fadeIn(3000);
                });
             }else{
                $(add_id).fadeIn(3000); 
             }
        }else if (len == 2){
             var type1 = $('div[data-id]').get(0).getAttribute("type");
             var type2 = $('div[data-id]').get(1).getAttribute("type");
             if (type1 == 'pic'){
                 $(delete_id).fadeOut(3000,function(){
                    $(delete_id).remove();
                    $(add_id).fadeIn(3000);
                 });
             }
             else if (type2 == 'pic'){
                 var id_second = $('div[data-id]').get(1).getAttribute("data-id");
                 var delete_id_second = 'div[data-id ='+id_second+']';
                 $(delete_id).fadeOut(1500,function(){
                 $(delete_id).remove();
                 });
                 $(delete_id_second).fadeOut(1500,function(){
                 $(delete_id_second).remove();
                 $(add_id).fadeIn(3000);
                 });
             }
             else{
                 $(delete_id).fadeOut(3000,function(){
                    $(delete_id).remove();
                    $(add_id).fadeIn(3000);
                 });
             }
        }else if (len == 3){
            var id_second = $('div[data-id]').get(1).getAttribute("data-id");
            var delete_id_second = 'div[data-id ='+id_second+']';
            $(delete_id).fadeOut(1500,function(){
                $(delete_id).remove();
            });
            $(delete_id_second).fadeOut(1500,function(){
                $(delete_id_second).remove();
                $(add_id).fadeIn(3000);
            });
        }else{}
        }
};

function itemDeleted(){
    art.dialog({
        title: '删除提示',
        content: '活动已被删除，此页面将在3秒后自动关闭！',
        width: '400px',
        lock:true,
        time: 3000,
    });
    setTimeout(function(){
        window.opener=null;
        window.open("", "_self");
        window.close();
        }, 3000);
}


function scroll(data_id){
    var str = 'div[data-id="'+data_id+'"]';
    var y=$(str).position().top;
    var x=$(str).position().left;
    window.scrollTo(x,y);
};

function refreshPage(){
    window.location.reload();
};
    
function escapeHtml(unsafe){
    unsafe = unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
    return unsafe;
};

function add_len_pass(){
    var count = parseInt($('#counter_pass').text());
    count = count + 1;
    $('#counter_pass').text(count);
}

function add_len_reject(){
    var count = parseInt($('#counter_reject').text());
    count = count + 1;
    $('#counter_reject').text(count);
}

function minus_len_reject(){
    var count = parseInt($('#counter_reject').text());
    if (count>=1){
        count = count - 1;
        $('#counter_reject').text(count);
    }
}

function changeTitle(data){
    document.title=data.event_name+'管理'+'('+data.num+'条新消息)';
}

function wall_item_tip(){
    $('#wall-item-tip').modal(); 
}

function showAddDialog(){
        $('#id_event_name').val('');
        $('#id_keyword').val('');
        $('#id_begin_time_0').val('');
        $('#id_end_time_0').val('');
        $('#id_welcome').val('');
        $('#id_id').val('');
        document.form.flag_check[0].checked=true;
        document.form.anonymity[0].checked=true;
        $('#add_wall_item').modal();
        $('#id_event_name').css({'width':"176px"});
        $('#id_keyword').css({'width':"176px"});
        $('#id_welcome').css({'width':"176px"});
        $('#id_begin_time_0').css({'width':"150px"});
        $('#id_end_time_0').css({'width':"150px"});
        $('label[for="id_flag_check_0"]').css({"display":"inline-block","margin-top":'4px', "margin-right":"10px", "margin-bottom":"0", });
        $('input[id="id_flag_check_0"]').css({"margin-top":'0', 'margin-bottom': '1px'});
        $('label[for="id_flag_check_1"]').css({"display":"inline-block","margin-top":'4px', "margin-right":"10px", "margin-bottom":"0", });
        $('input[id="id_flag_check_1"]').css({"margin-top":'0', 'margin-bottom': '1px'});
        $('label[for="id_anonymity_0"]').css({"display":"inline-block","margin-top":'4px', "margin-right":"10px", "margin-bottom":"0", });
        $('input[id="id_anonymity_0"]').css({"margin-top":'0', 'margin-bottom': '1px'});
        $('label[for="id_anonymity_1"]').css({"display":"inline-block","margin-top":'4px', "margin-right":"10px", "margin-bottom":"0", });
        $('input[id="id_anonymity_1"]').css({"margin-top":'0', 'margin-bottom': '1px'});
        $('#add__wall_item.control-group').removeClass('error');

    }

function showChangeDialog(id, event_name, keyword, begin_time, end_time, welcome, flag_check, anonymity){
        $('#id_event_name').val(event_name);
        $('#id_keyword').val(keyword);
        $('#id_begin_time_0').val(begin_time);
        $('#id_end_time_0').val(end_time);
        $('#id_welcome').val(welcome);
        $('#id_id').val(id);
        if (flag_check == "是"){
          for(var i=0;i<2;i++){
              if('是'==document.form.flag_check[i].value){
                 document.form.flag_check[i].checked=true;
           }
          }
        }
        if (flag_check == "否"){
           for(var i=0;i<2;i++){
              if('否'==document.form.flag_check[i].value){
                 document.form.flag_check[i].checked=true;
           }
          }
        }
        if (anonymity == "是"){
          for(var i=0;i<2;i++){
              if('是'==document.form.anonymity[i].value){
                 document.form.anonymity[i].checked=true;
           }
          }
        }
        if (anonymity == "否"){
           for(var i=0;i<2;i++){
              if('否'==document.form.anonymity[i].value){
                 document.form.anonymity[i].checked=true;
           }
          }
        }
        $('#add_wall_item').modal();
        $('#id_begin_time_0').css({'width':"150px"});
        $('#id_end_time_0').css({'width':"150px"});
        $('#id_event_name').css({'width':"176px"});
        $('#id_keyword').css({'width':"176px"});
        $('#id_welcome').css({'width':"176px"});
        $('label[for="id_flag_check_0"]').css({"display":"inline-block",'margin-top':'5px', "margin-right":"10px"});
        $('input[id="id_flag_check_0"]').css({'margin-top':'0','margin-bottom':'1px' });
        $('label[for="id_flag_check_1"]').css({"display":"inline-block",'margin-top':'5px', "margin-right":"10px"});
        $('input[id="id_flag_check_1"]').css({'margin-top':'0','margin-bottom':'1px' });
        $('label[for="id_anonymity_0"]').css({"display":"inline-block","margin-top":'4px', "margin-right":"10px", "margin-bottom":"0", });
        $('input[id="id_anonymity_0"]').css({"margin-top":'0', 'margin-bottom': '1px'});
        $('label[for="id_anonymity_1"]').css({"display":"inline-block","margin-top":'4px', "margin-right":"10px", "margin-bottom":"0", });
        $('input[id="id_anonymity_1"]').css({"margin-top":'0', 'margin-bottom': '1px'});
        $('#add__wall_item.control-group').removeClass('error');
    } 
