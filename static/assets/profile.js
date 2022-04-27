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
    $.ajax({
        url: "api/addressbook/" + $(this).attr('add-id'),
        type: "GET",
        success: function (resp) {
            $("#edit-address-id").val(resp.address.id)
            $("#edit-country option[value='" + resp.address.country + "']").prop('selected', true)
            $("#edit-address-name").val(resp.address.name)
            $("#edit-address-phone").val(resp.address.phone)
            $("#edit-address-address").val(resp.address.address)
            console.log(resp.regions)
            document.getElementById("edit-region").options.length = 0;
            $("#edit-region").attr("disabled", false)
            $("#edit-region").append(new Option('', 'null'))
            for (i = 0; i < resp.regions.length; i++) {
                $("#edit-region").append(new Option(resp.regions[i].name, resp.regions[i].id))
            }
            document.getElementById("edit-city").options.length = 0;
            $("#edit-city").attr("disabled", false)
            $("#edit-city").append(new Option('', 'null'))
            for (i = 0; i < resp.cities.length; i++) {
                $("#edit-city").append(new Option(resp.cities[i].name, resp.cities[i].id))
            }
            document.getElementById("edit-area").options.length = 0;
            $("#edit-area").attr("disabled", false)
            $("#edit-area").append(new Option('', 'null'))
            for (i = 0; i < resp.areas.length; i++) {
                $("#edit-area").append(new Option(resp.areas[i].name, resp.areas[i].id))
            }
            $("#edit-region option[value='" + resp.address.region + "']").prop('selected', true)
            $("#edit-city option[value='" + resp.address.city + "']").prop('selected', true)
            $("#edit-area option[value='" + resp.address.area + "']").prop('selected', true)
        }
    })
    $("#address-name").val()
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
                // $("#add-area").append(new Option('', 'null'))
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





$("#edit-country").on("change", function () {
    if ($(this).val() != 'null') {
        document.getElementById("overlay").style.display = "block";
        $.ajax({
            url: "/get-region",
            type: "POST",
            data: { id: $(this).val(), },
            success: function (result) {
                document.getElementById("edit-region").options.length = 0;
                $("#edit-region").attr("disabled", false)
                $("#edit-region").append(new Option('', 'null'))
                for (i = 0; i < result.length; i++) {
                    $("#edit-region").append(new Option(result[i][0], result[i][1]))
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
        document.getElementById("edit-region").options.length = 0;
        $("#edit-region").attr("disabled", true)
        $("#edit-city").attr("disabled", true)
        $("#edit-area").attr("disabled", true)
    }
})

$("#edit-region").on("change", function () {
    if ($(this).val() != 'null') {
        document.getElementById("overlay").style.display = "block";
        $.ajax({
            url: "/get-city",
            type: "POST",
            data: { id: $(this).val(), },
            success: function (result) {
                document.getElementById("edit-city").options.length = 0;
                $("#edit-city").attr("disabled", false)
                $("#edit-city").append(new Option('', 'null'))
                for (i = 0; i < result.length; i++) {
                    $("#edit-city").append(new Option(result[i][0], result[i][1]))
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
        document.getElementById("edit-city").options.length = 0;
        $("#edit-city").attr("disabled", true)
        $("#edit-area").attr("disabled", true)
    }
})

$("#edit-city").on("change", function () {
    if ($(this).val() != 'null') {
        document.getElementById("overlay").style.display = "block";
        $.ajax({
            url: "/get-area",
            type: "POST",
            data: { id: $(this).val(), },
            success: function (result) {
                document.getElementById("edit-area").options.length = 0;
                $("#edit-area").attr("disabled", false)
                // $("#edit-area").append(new Option('', 'null'))
                for (i = 0; i < result.length; i++) {
                    $("#edit-area").append(new Option(result[i][0], result[i][1]))
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
        document.getElementById("edit-area").options.length = 0;
        $("#edit-area").attr("disabled", true)
    }
})