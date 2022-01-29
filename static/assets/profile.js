$(".edit-btn").on('click', function(){
    $(".address-edit").removeClass('d-none');
    $(".address-view").addClass('d-none');
});

$(".male-btn").on('click', function(){
    $(this).addClass("active");
    $(".female-btn").removeClass("active");
})

$(".female-btn").on('click', function(){
    $(this).addClass("active");
    $(".male-btn").removeClass("active");
})

$(".address-edit-btn").on("click", function(){
    $("#address-edit-form").removeClass("d-none");
    $(".address").addClass("d-none");
})

$(".address-cancel-btn").on("click", function(){
    $("#address-edit-form").addClass("d-none");
    $(".address").removeClass("d-none");
    $("#add-address-form").addClass("d-none");
})

$(".add-address-btn").on("click", function(){
    $("#add-address-form").removeClass("d-none");
    $(".address").addClass("d-none");
    $("#address-edit-form").addClass("d-none");
})









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

$("#region").on("change", function(){
    $.ajax({
        url:"/city/",
        type:"POST",
        data:{id: $(this).val(),},
        success: function(result) {
            console.log(result);
            cols = document.getElementById("city");
            cols.options.length = 0;
            for(var k in result){
                cols.options.add(new Option(result[k][0], result[k][1]));
            }
            $("#city").removeAttr("disabled");
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        error: function(e){
            console.error(JSON.stringify(e));
        },
    });
})


$("#city").on("change", function(){
    $.ajax({
        url:"/area/",
        type:"POST",
        data:{id: $(this).val(),},
        success: function(result) {
            console.log(result);
            cols = document.getElementById("area");
            cols.options.length = 0;
            for(var k in result){
                cols.options.add(new Option(result[k][0], result[k][1]));
            }
            $("#area").removeAttr("disabled");
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        error: function(e){
            console.error(JSON.stringify(e));
        },
    });
})