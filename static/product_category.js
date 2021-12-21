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
        $("#id_category").change(function(){
            $.ajax({
                url:"/productgroups/",
                type:"POST",
                data:{category_id: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_group");
                    cols.options.length = 0;
                    cols.options.add(new Option("Group", "Group"));
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
        $("#id_group").change(function(){
            $.ajax({
                url:"/productgroups/",
                type:"POST",
                data:{group_id: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_subcategory");
                    cols.options.length = 0;
                    cols.options.add(new Option("Subategory", "Subategory"));

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