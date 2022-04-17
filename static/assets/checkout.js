
// convert curreny BDT to USD
// $.get("https://fcsapi.com/api-v2/forex/converter?symbol=BDT/USD&amount=200&access_key=ohHkx8n2tCX9BBoaGvFUwY", function (resp) {
//     $("#usd").text(($("#total-cost").text().slice(1) * resp.response.price_1x_USD).toFixed(2));
//     $("#rate").text(resp.response.price_1x_BDT);
//     $("#rate-input").val(resp.response.price_1x_BDT);
// });


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
        // onClick: function (data, actions) {
        //     alert($("#rate").text())
        // },

        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{ "amount": { "currency_code": "USD", "value": 1 } }]
            });
        },

        onApprove: function (data, actions) {
            return actions.order.capture().then(function (orderData) {

                // Full available details
                console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
                const user_id = JSON.parse(document.getElementById('user_id').textContent)
                data = {
                    'user_id': user_id,
                    'company_name': $("#company_name").val(),
                    'email': $("#email").val(),
                    'notes': $("#notes").val(),
                    'diff_address': $("#checkout-diff-address").val(),
                    'ab_name': $("#ab-name").val(),
                    'phone': $("#phone").val(),
                    'ab_country': $(".ab-country").val(),
                    'ab_region': $(".ab-region").val(),
                    'ab_city': $(".ab-city").val(),
                    'ab_area': $(".ab-area").val(),
                    'ab_address': $("#ab-address").val(),
                    'address_book': $("input[name='address_book']:checked").val(),
                    'payment_mode': 'paypal',
                    'rate': $("#rate").text(),
                    'payment_id': orderData.id,
                    'total': orderData.purchase_units[0].amount.value,
                    'total_bdt': $("#total-cost-bdt").text()
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