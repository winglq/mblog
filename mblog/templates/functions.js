<script>
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
    $('.nav>li>a[href="/' + path + '"]').parent().addClass('active');
}
</script>
