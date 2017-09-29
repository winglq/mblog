<script>
function load(endpoint, callback){
    $.ajax({
        method: "GET",
        url: endpoint,
        success: callback
    });
}

function default_process_fn(resp){
    console.log(resp.data)
    return resp.data
}

function replace(tag_id, resp, process_fn){
   $('#' + tag_id).html(process_fn(resp))
}

function load_replace(endpoint, tag_id, process_fn=default_process_fn){
    load(endpoint, function cb(resp){
        replace(tag_id, resp, process_fn)
        })
}

function list_to_link_process_fn(resp){
    html = "<img src='arch.png'>image</img>"
    lst = $.each(resp.titles, function(index, val){
            html = html + "<a href='/blogs/" + val +"' >" + val + "</a>"
    })
    console.log(html)
    return html
}

</script>
