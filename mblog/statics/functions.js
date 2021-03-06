function load(endpoint, callback){
    $.ajax({
        method: "GET",
        url: endpoint,
        success: callback
    });
}

function default_process_fn(resp){
    return resp.data
}

function replace(tag_id, resp, process_fn){
   $('#' + tag_id).html(process_fn(resp))
}

function add_table_attribute(){
   $('table').each(function(){
       $(this).addClass('table')
   })
}

function load_replace(endpoint, tag_id, process_fn=default_process_fn){
    load(endpoint, function cb(resp){
        replace(tag_id, resp, process_fn)
        change_img_to_responsive()
        images_loaded('/statics/loader.gif')
        add_table_attribute()
        })
}

function list_to_link_process_fn(resp){
    html = ""
    lst = $.each(resp.titles, function(index, val){
            html = html + "<a href='/blogs/" + val +"' >" + val + "</a>"
    })
    return html
}

function change_img_to_responsive(){
    imgs = $("img").each(function(){
        $(this).addClass("img-responsive")
    })
}

function images_loaded(loading_gif){
    $('img[src!=""]').each(function(){
        var old_img = this;
        var img = new Image();
        img.onload = function(){$(old_img).attr('src',img.src)};
        img.src = this.src;
        this.src = loading_gif
    })
}

function active_menu(){
    var path = window.location.pathname.substring(1);
    $('.nav>li.active').removeClass('active');
    var elem = $('.nav>li>a[href="/' + path + '"]');
    if (elem.length == 0){
        first_sub_path = path.split('/')[0];
        elem = $('.nav>li>a[href="/' + first_sub_path + '"]');
    }
    if (elem.length == 0) {
        elem = $('.nav>li>a[href="/"]');
    }
    elem.parent().addClass('active');
}

function show_temperature(){
    $.ajax({
        method: "GET",
        url: '/data/temperature',
        success: function cb(resp) {
            var str = String(resp);
            $('#temper').text(' ' + str.substring(0, 2));
            $('#humidity').text(' ' + str.substring(2, 4));
        }
    });
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function login(){
  var usr = getCookie('X-USER-ID');
  if (usr){
    $("#loginli").text(usr);
  }
}

function getCellValue(row, index){ return $(row).children('td').eq(index).text() }
function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index)
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.localeCompare(valB)
    }
}

function register_sort_fun(){
  $('th').click(function(){
      var table = $(this).parents('table').eq(0);
      console.log($(this).index());
      var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()));
      $('tbody').remove();
      this.asc = !this.asc;
      if (!this.asc){rows = rows.reverse();}
      for (var i = 0; i < rows.length; i++){table.append(rows[i]);}
  })
}

function insert_loading_after(after_obj){
  i_tag = $("<i/>");
  i_tag.attr('class', "fa fa-spinner fa-spin fa-3x fa-fw");
  span_tag = $("<span/>");
  span_tag.attr('class', "sr-only");
  span_tag.text("Loading...");
  div_tag = $("<div/>");
  div_tag.attr('class', 'loading-gif');
  div_tag.append(i_tag);
  div_tag.append(span_tag);
  div_tag.insertAfter(after_obj);

}

function control(cls, sid, action){
  var a_tag = $("<a/>");
  a_tag.attr("href", "#");
  a_tag.append('<i class="fa ' + cls + ' fa-lg"></i>');
  a_tag.click(function(){
    action(sid);
  })
  return a_tag;

}
function delete_control(sid, action){
  return control("fa-trash-o", sid, action);
}

function edit_control(sid, action){
  return control("fa-pencil", sid, action);
}

function check_control(sid, action){
  return control("fa-check", sid, action);
}

function remove_control(sid, action){
  return control("fa-remove", sid, action);
}

function remove_loading(){
  $(".loading-gif").remove();
}

function put_data_in_table(ths, tds, cth, buttons){
  var table_tag = $("<table/>");
  var thead = $("<thead/>");
  table_tag.attr("class", "table");
  var head_tr = $("<tr/>");
  for(i = 0; i < ths.length; i++){
    var th_tag = $("<th/>");
    th_tag.text(ths[i]);
    head_tr.append(th_tag);
  }
  var th_tag = $("<th/>");
  th_tag.text(cth);
  head_tr.append(th_tag);

  thead.append(head_tr);
  table_tag.append(thead);
  var tbody = $("<tbody/>");
  for(i = 0; i < tds.length; i++){
    var tr_tag = $("<tr/>");
      for(j = 0; j < tds[i].length; j++){
        var td_tag = $("<td/>");
        td_tag.text(tds[i][j]);
        tr_tag.append(td_tag);
      }
      if (buttons != null){
        var td_tag = $("<td/>");
        for (x = 0; x < buttons[i].length; x++){
          td_tag.append(buttons[i][x]);
          td_tag.append(" | ");
        }
        tr_tag.append(td_tag);
      }

    tbody.append(tr_tag);
  }
  table_tag.append(tbody)
  return table_tag;
}

function cal_percentage(bid_price, stop_loss_price){
        return ((bid_price - stop_loss_price) / bid_price * 100).toFixed(2);
}
function cal_stop_loss_price(bid_price, risk_percent){
        return (bid_price - risk_percent * bid_price / 100).toFixed(2);
}

function cal_total_price(bid_price, hold_position){
        return bid_price * hold_position;
}

function cal_total_lost(bid_price, hold_position, risk_percent){
        return bid_price * hold_position * risk_percent / 100;
}

function register_stop_loss_price_change_event(){
  $("#stop-loss-price").change(function(){
                  percent = cal_percentage($("#bid-price").val(), $("#stop-loss-price").val());
                  $("#risk").val(percent);
                  total_lost = cal_total_lost($("#bid-price").val(), $("#hold-position").val(), percent);
                  $("#total-lost").val(total_lost);
    });
  
  $("#risk").change(function(){
                  price = cal_stop_loss_price($("#bid-price").val(), $("#risk").val());
                  $("#stop-loss-price").val(price);
                  total_lost = cal_total_lost($("#bid-price").val(), $("#hold-position").val(), $("#risk").val());
                  $("#total-lost").val(total_lost);

    });

  $("#hold-position").change(function(){
                  total_p = cal_total_price($("#bid-price").val(), $("#hold-position").val());
                  $("#total-price").val(total_p);
                  percent = cal_percentage($("#bid-price").val(), $("#stop-loss-price").val());
                  total_lost = cal_total_lost($("#bid-price").val(), $("#hold-position").val(), percent);
                  $("#total-lost").val(total_lost);

    });

  $("#bid-price").change(function(){
                  total_p = cal_total_price($("#bid-price").val(), $("#hold-position").val());
                  $("#total-price").val(total_p);
                  percent = cal_percentage($("#bid-price").val(), $("#stop-loss-price").val());
                  total_lost = cal_total_lost($("#bid-price").val(), $("#hold-position").val(), percent);
                  $("#total-lost").val(total_lost);

    })

}

