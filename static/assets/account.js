$("#pass-alert").css("display", "none");
$('#signup-password').keyup(function () {
    if ($("#singnup-password").val() === $("#signup-confirm-password").val() && $("#signup-password").val().length > 0) {
        $("#registration-btn").removeAttr("disabled");
        $("#pass-alert").css('display', 'none');
    }
    else {
        $("#registration-btn").attr("disabled", "true");
        $("#pass-alert").css('display', 'block');
    }
});
$('#signup-confirm-password').keyup(function () {
    if ($("#signup-password").val() === $("#signup-confirm-password").val() && $("#signup-password").val().length > 0) {
        $("#registration-btn").removeAttr("disabled");
        $("#pass-alert").css('display', 'none');
    }
    else {
        $("#registration-btn").attr("disabled", "true");
        $("#pass-alert").css('display', 'block');
    }
});


function AddPro(resp) {
    document.getElementById("cart-total-price").innerHTML = "&#2547;" + resp.cost;
    $("#dropdown-cart-products").empty();
    varjson = JSON.parse(JSON.stringify(resp.cart));
    varjson.forEach(function (data) {
        var div = `<div class="product">
              <div class="product-cart-details">
                  <h4 class="product-title">
                      <a href="product.html">${data.title}</a>
                  </h4>
                  <span class="cart-product-info">
                      <span class="cart-product-qty">${data.amount}</span>
                      X${data.price}
                  </span>
              </div><!-- End .product-cart-details -->
              <figure class="product-image-container">
                  <a href="product.html" class="product-image">
                      <img src="${data.image}" alt="product">
                  </a>
              </figure>
              <a href="#" class="btn-remove" title="Remove Product" id="cart-remove" cart-id="${resp.id}"><i class="icon-close"></i></a>
          </div>`
        $('#dropdown-cart-products').append(div);
    });
}

function setcart(resp) {
    var cart = `<div class="header-dropdown-link">
                                        <div class="dropdown compare-dropdown">
                                            <a href="#" class="dropdown-toggle" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-display="static" title="Compare Products" aria-label="Compare Products">
                                                <i class="icon-random"></i>
                                                <span class="compare-txt">Compare</span>
                                            </a>

                                            <div class="dropdown-menu dropdown-menu-right">
                                                <ul class="compare-products">
                                                    <li class="compare-product">
                                                        <a href="#" class="btn-remove" title="Remove Product"><i class="icon-close"></i></a>
                                                        <h4 class="compare-product-title"><a href="product.html">Blue Night Dress</a></h4>
                                                    </li>
                                                    <li class="compare-product">
                                                        <a href="#" class="btn-remove" title="Remove Product"><i class="icon-close"></i></a>
                                                        <h4 class="compare-product-title"><a href="product.html">White Long Skirt</a></h4>
                                                    </li>
                                                </ul>

                                                <div class="compare-actions">
                                                    <a href="#" class="action-link">Clear All</a>
                                                    <a href="#" class="btn btn-outline-primary-2"><span>Compare</span><i class="icon-long-arrow-right"></i></a>
                                                </div>
                                            </div><!-- End .dropdown-menu -->
                                        </div><!-- End .compare-dropdown -->

                                        <a href="/wishlist" class="wishlist-link">
                                            <i class="icon-heart-o"></i>
                                            <span class="wishlist-count">3</span>
                                            <span class="wishlist-txt">Wishlist</span>
                                        </a>

                                        <div class="dropdown cart-dropdown">
                                            <a href="#" class="dropdown-toggle" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-display="static">
                                                <i class="icon-shopping-cart"></i>
                                                <span class="cart-count">${resp.item}</span>
                                                <span class="cart-txt">Cart</span>
                                            </a>

                                                <div class="dropdown-menu dropdown-menu-right">
                                                    <div class="dropdown-cart-products" id="dropdown-cart-products">
                                                        {% for item in shopcart %}
                                                        <div class="product">
                                                            <div class="product-cart-details">
                                                                <h4 class="product-title">
                                                                    <a href="product.html">{{item.product.title}}</a>
                                                                </h4>

                                                                <span class="cart-product-info">
                                                                    <span class="cart-product-qty">{{item.quantity}}</span>
                                                                     X &#2547;{{item.product.price}}
                                                                </span>
                                                            </div><!-- End .product-cart-details -->

                                                            <figure class="product-image-container">
                                                                <a href="product.html" class="product-image">
                                                                    <img src="{{item.product.image.url}}" alt="product">
                                                                </a>
                                                            </figure>
                                                            <a href="#" class="btn-remove" title="Remove Product"><i class="icon-close"></i></a>
                                                        </div><!-- End .product -->
                                                        {% endfor %}

                                                    </div><!-- End .cart-product -->

                                                    <div class="dropdown-cart-total">
                                                        <span>Total</span>
                                                        <span class="cart-total-price" id="cart-total-price">&#2547;{{cost}}</span>
                                                    </div><!-- End .dropdown-cart-total -->

                                                    <div class="dropdown-cart-action">
                                                        <a href="/cart" class="btn btn-primary">View Cart</a>
                                                        <a href="checkout.html" class="btn btn-outline-primary-2"><span>Checkout</span><i class="icon-long-arrow-right"></i></a>
                                                    </div><!-- End .dropdown-cart-total -->
                                                </div><!-- End .dropdown-menu -->
                                        </div><!-- End .cart-dropdown -->
                                    </div>`
    var user_option = `<div class="header-dropdown">
        <a href="#">${resp.name}</a>
        <div class="header-menu">
            <ul>
                <li><a id="my-account" href="/profile">My Account</a></li>
                <li><a href="/auth/logout">Logout</a></li>
            </ul>
        </div><!-- End .header-menu -->
    </div><!-- End .header-dropdown -->`
    $("#login").css('display', 'none');
    $("#signin-modal-close-btn").click();
    $("#user-option").empty();
    $("#user-option").append(user_option);
    $("#cart-section").empty();
    $("#cart-section").append(cart);
    AddPro(resp);
}


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


function Registration(event) {
    event.preventDefault();

    $.ajax({
        url: "/auth/",
        type: "POST",
        data: {
            first_name: $("#signup-first-name").val(),
            last_name: $("#signup-last-name").val(),
            email: $("#signup-email").val(),
            password: $("#signup-password").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (result) {
            if (result.success === 'yes') {
                document.getElementById('signin-tab').click();
                $("#registration-form")[0].reset();
            }
            alert(result.msg);
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        error: function (e) {
            console.error(JSON.stringify(e));
        },
    });
}

function Login(event) {
    event.preventDefault();

    $.ajax({
        url: "/auth/",
        type: "POST",
        data: {
            email: $("#signin-email").val(),
            password: $("#signin-password").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (result) {
            document.getElementById('user').innerText = 'yes';
            setcart(result);
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        error: function (e) {
            console.error(JSON.stringify(e));
        },
    });
}