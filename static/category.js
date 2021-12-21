function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

jQuery(function($){
    $(document).ready(function(){
        let id = document.getElementById("cat_id").value;
        // document.getElementById("id_group").innerHTML = '<option value="" selected="">Empty</option>';
        sendid(id);
        function sendid(id){
            $.ajax({
                url:"/groups/",
                type:"POST",
                data:{category_id: id,},
                success: function(result) {
                    console.log(result);
                    col = $( "tr[class='form-row dynamic-subategory_set']" );
                    colx = $( "tr[class='form-row has_original dynamic-subategory_set']" );
                    for(i = 0; i < colx.length; i++){
                        cols = $(colx[i]);
                        col1 = cols.children('td:nth-child(3)');
                        col2 = col1.children('div:nth-child(1)');
                        col3 = col2.children('select:nth-child(1)');
                        col_id = col3.attr('id');
                        cols = document.getElementById(col_id);
                        cols.options.length = 0;
                        for(var k in result){
                            cols.options.add(new Option(k, result[k]));
                        }
                    }
                    col1 = col.children('td:nth-child(3)');
                    col2 = col1.children('div:nth-child(1)');
                    col3 = col2.children('select:nth-child(1)');
                    col_id = col3.attr('id');
                    cols = document.getElementById(col_id);
                    cols.options.length = 0;
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        }
        $( "a[href='#']" ).click(function(){
            let id = document.getElementById("cat_id").value;
            $.ajax({
                url:"/groups/",
                type:"POST",
                data:{category_id: id,},
                success: function(result) {
                    console.log(result);
                    col = $("tr[class='form-row dynamic-subategory_set']").last();
                    col1 = col.children('td:nth-child(3)');
                    col2 = col1.children('div:nth-child(1)');
                    col3 = col2.children('select:nth-child(1)');
                    col_id = col3.attr('id');
                    cols = document.getElementById(col_id);
                    cols.options.length = 0;
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
    }); 
});