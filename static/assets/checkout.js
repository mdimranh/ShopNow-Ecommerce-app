
var total = $("#total-amount").val()
const shopcartid = $("#cartid").val()

var mycurrency = getCookie('mycurrency')
if (mycurrency !== 'USD') {
    $.get(`https://fcsapi.com/api-v2/forex/converter?symbol=${mycurrency}/USD&amount=${total}&access_key=ohHkx8n2tCX9BBoaGvFUwY`, function (resp) {
        $("#total-amount-usd").val(parseFloat(resp.response.total).toFixed(2));
    });
}

else {
    $("#total-amount-usd").val($("#total-amount").val())
}

// create checkout using paypal

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

function initPayPalButton() {
    paypal.Buttons({
        style: {
            shape: 'rect',
            color: 'gold',
            layout: 'vertical',
            label: 'paypal',

        },
        onClick: function (data, actions) {
            if ($("#checkout-diff-address").is(":checked")) {
                if ($("#first_name").val().length > 0 &&
                    $("#last_name").val().length > 0 &&
                    $("#email").val().length > 0 &&
                    $("#phone").val().length > 0 &&
                    $("#add-country").val().length > 0 &&
                    $("#add-region").val().length > 0 &&
                    $("#add-city").val().length > 0 &&
                    $("#add-area").val().length > 0 &&
                    $("#address").val().length > 0) {
                    return true
                }
                else {
                    $("#submit-btn").click()
                    return false
                }
            }
            else {
                if (
                    $("#first_name").val().length > 0 &&
                    $("#last_name").val().length > 0 &&
                    $("#email").val().length > 0 &&
                    $("#phone").val().length > 0
                ) {
                    return true
                }
                else {
                    $("#submit-btn").click()
                    return false
                }
            }
        },

        createOrder: function (data, actions) {
            return actions.order.create({
                application_context: {
                    'shipping_preference': 'NO_SHIPPING'
                },
                purchase_units: [{
                    "amount": {
                        "currency_code": "USD",
                        "value": $("#total-amount-usd").val()
                    }
                }]
            });
        },

        onApprove: function (data, actions) {
            return actions.order.capture().then(function (orderData) {

                // Full available details
                console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));

                if ($("#checkout-diff-address").val() == 'on') {
                    data = {
                        'cartid': shopcartid,
                        'first_name': $("#first_name").val(),
                        'last_name': $("#last_name").val(),
                        'company_name': $("#company_name").val(),
                        'email': $("#email").val(),
                        'phone': $("#phone").val(),
                        'notes': $("#notes").val(),
                        'diff-address': 'on',
                        'country': $("#add-country").val(),
                        'region': $("#add-region").val(),
                        'city': $("#add-city").val(),
                        'area': $("#add-area").val(),
                        'address': $("#address").val(),
                        'payment_mode': 'paypal',
                        'payment_id': orderData.id,
                        'total': orderData.purchase_units[0].amount.value,
                    }
                }
                else {
                    data = {
                        'cartid': shopcartid,
                        'first_name': $("#first_name").val(),
                        'last_name': $("#last_name").val(),
                        'company_name': $("#company_name").val(),
                        'diff-address': 'off',
                        'email': $("#email").val(),
                        'notes': $("#notes").val(),
                        'phone': $("#phone").val(),
                        'address_book': $("input[name='address_book']:checked").val(),
                        'payment_mode': 'paypal',
                        'payment_id': orderData.id,
                        'total': orderData.purchase_units[0].amount.value,
                    }
                }

                $.ajax({
                    url: "/place-order",
                    type: "POST",
                    data: data,

                    success: function (response) {
                        Swal.fire({
                            title: 'Congratulation',
                            text: "Order confirmed successfully",
                            icon: 'success',
                            showCancelButton: false,
                            showConfirmButton: false,
                            timer: 1000
                        }).then((result) => {
                            window.location.href = "/profile"
                        });
                    },
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                });
            });
        },

        onError: function (err) {
            console.log(err);
        }
    }).render('#paypal-button-container');
}

initPayPalButton();



// $("#btn").click(function () {
//     data = {
//         'user_id': $("#user_id").text(),
//         'company_name': $("#company_name").val(),
//         'email': $("#email").val(),
//         'notes': $("#notes").val(),
//         'payment_mode': 'paypal',
//         'payment_id': 12,
//         'diff_address': $("#checkout-diff-address").val(),
//         'ab_name': $("#ab-name").val(),
//         'ab_phone': $("#ab-phone").val(),
//         'ab_country': $(".ab-country").val(),
//         'ab_region': $(".ab-region").val(),
//         'ab_city': $(".ab-city").val(),
//         'ab_area': $(".ab-area").val(),
//         'ab_address': $("#ab-address").val(),
//         'total': $("#usd").text(),
//         'address_book': $("input[name='address_book']:checked").val()
//     }
//     $.ajax({
//         url: "/place-order",
//         type: "POST",
//         data: data,
//         success: function (response) {
//             Swal.fire({
//                 title: 'Congratulation',
//                 text: "Order confirmed successfully",
//                 icon: 'success',
//                 showCancelButton: false,
//                 showConfirmButton: false,
//                 timer: 1000
//             })
//         },
//         headers: {
//             "X-CSRFToken": getCookie("csrftoken")
//         },
//     });
// })