$(".edit-btn").on('click', function () {
    $(".address-edit").removeClass('d-none');
    $(".address-view").addClass('d-none');
});

$(".male-btn").on('click', function () {
    $(this).addClass("active");
    $(".female-btn").removeClass("active");
})

$(".female-btn").on('click', function () {
    $(this).addClass("active");
    $(".male-btn").removeClass("active");
})

$(".address-edit-btn").on("click", function () {
    $("#address-edit-form").removeClass("d-none");
    $(".address").addClass("d-none");
})

$(".address-cancel-btn").on("click", function () {
    $("#address-edit-form").addClass("d-none");
    $(".address").removeClass("d-none");
    $("#add-address-form").addClass("d-none");
})

$(".add-address-btn").on("click", function () {
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

$("#add-country").on("change", function () {
    if ($(this).val() != 'null') {
        document.getElementById("overlay").style.display = "block";
        $.ajax({
            url: "/get-region",
            type: "POST",
            data: { id: $(this).val(), },
            success: function (result) {
                document.getElementById("add-region").options.length = 0;
                $("#add-region").attr("disabled", false)
                $("#add-region").append(new Option('', 'null'))
                for (i = 0; i < result.length; i++) {
                    $("#add-region").append(new Option(result[i][0], result[i][1]))
                }
                document.getElementById("overlay").style.display = "none";
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            error: function (e) {
                console.error(JSON.stringify(e));
            },
        });
    }
    else {
        document.getElementById("add-region").options.length = 0;
        $("#add-region").attr("disabled", true)
        $("#add-city").attr("disabled", true)
        $("#add-area").attr("disabled", true)
    }
})

$("#add-region").on("change", function () {
    if ($(this).val() != 'null') {
        document.getElementById("overlay").style.display = "block";
        $.ajax({
            url: "/get-city",
            type: "POST",
            data: { id: $(this).val(), },
            success: function (result) {
                document.getElementById("add-city").options.length = 0;
                $("#add-city").attr("disabled", false)
                $("#add-city").append(new Option('', 'null'))
                for (i = 0; i < result.length; i++) {
                    $("#add-city").append(new Option(result[i][0], result[i][1]))
                }
                document.getElementById("overlay").style.display = "none";
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            error: function (e) {
                console.error(JSON.stringify(e));
            },
        });
    }
    else {
        document.getElementById("add-city").options.length = 0;
        $("#add-city").attr("disabled", true)
        $("#add-area").attr("disabled", true)
    }
})

$("#add-city").on("change", function () {
    if ($(this).val() != 'null') {
        document.getElementById("overlay").style.display = "block";
        $.ajax({
            url: "/get-area",
            type: "POST",
            data: { id: $(this).val(), },
            success: function (result) {
                document.getElementById("add-area").options.length = 0;
                $("#add-area").attr("disabled", false)
                $("#add-area").append(new Option('', 'null'))
                for (i = 0; i < result.length; i++) {
                    $("#add-area").append(new Option(result[i][0], result[i][1]))
                }
                document.getElementById("overlay").style.display = "none";
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            error: function (e) {
                console.error(JSON.stringify(e));
            },
        });
    }
    else {
        document.getElementById("add-area").options.length = 0;
        $("#add-area").attr("disabled", true)
    }
})