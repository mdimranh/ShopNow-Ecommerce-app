
var mdl = $("#add-product-modal").iziModal({
  radius: 0,
  padding: 20,
  closeButton: true,
  title: 'Product add successfully.',
  headerColor: '#8160B7',
  width: 850,
  fullscreen: true,
  zindex: 2000,
});


function quantity(type, amount) {
  var val = parseInt(document.getElementById('pro-quantity').value);
  if (type === 'inc' && amount > val) {
    document.getElementById('pro-quantity').value++;
  }
  else if (type === 'dec' && val > 0) {
    document.getElementById('pro-quantity').value--;
  }
}

function AddProduct(id, quantity) {
  document.getElementById("overlay").style.display = "block";
  if (document.getElementById('user').innerText === 'yes') {
    if (quantity === 'no') {
      quantity = 1;
    }
    else {
      quantity = document.getElementById('pro-quantity').value;
    }
    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000/ajax/addtocart',
      data: {
        'id': id,
        'quantity': quantity,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (resp) {
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
        if ($("#wishitem" + id).length > 0) {
          document.getElementById("wishitem" + id).remove();
        }
        $(".cart-count").text(resp.item);
        var product = JSON.parse(resp.product);
        var div = `<tr>
                    <td class="product-col">
                        <div class="product">
                            <figure class="product-media">
                                <a href="/products/${product.id}">
                                    <img src="${product.image}" alt="Product image">
                                </a>
                            </figure>
                            <h3 class="product-title">
                                <a href="/products/${product.id}">${product.title}</a>
                            </h3><!-- End .product-title -->
                        </div><!-- End .product -->
                    </td>
                    <td class="product-price">
                      <div class="d-flex flex-column">
                        <span class="new-price">${product.price}</span><clear>
                        <span class="old-price"><span>${product.main_price}</span> (${product.discount}%)</span>
                      </div>
                    </td>
                    <td class="quantity-col">
                        <div class="cart-product-quantity">
                            <span>${quantity}</span>
                        </div><!-- End .cart-product-quantity -->
                    </td>
                </tr>`;
        document.getElementById("overlay").style.display = "none";
        $('#modal-table-body').empty();
        $('#modal-table-body').append(div);
        $('#add-product-modal').iziModal('open');
      },
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
    });
  }
  else {
    document.getElementById("overlay").style.display = "none";
    document.getElementById('login-modal-btn').click();
  }
}

function Update(id, quantity) {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    type: 'POST',
    url: 'http://localhost:8000/ajax/addtocart',
    data: {
      'id': id,
      'update-quantity': quantity,
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function (resp) {
      if (resp.msg_type) {
        alert(resp.msg);
      }
      else {
        document.getElementById("cart-total-price").innerHTML = "&#2547;" + resp.cost;
        document.getElementById("total-cost").innerHTML = "&#2547;" + resp.cost;
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
      document.getElementById("overlay").style.display = "none";
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
  });
}

$("input[class='form-control amount']").on('change', function () {
  Update($(this).attr("cart-id"), $(this).val());
});

$("#coupon-btn").click(function () {
  addCoupon();
});
function addCoupon() {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    type: 'POST',
    url: 'http://localhost:8000/ajax/addtocart',
    data: {
      'coupon_code': $("#coupon-code").val(),
      'id': 1
    },
    success: function (resp) {
      if (resp.added == 'fail') {
        document.getElementById('coupon-fail').innerHTML = resp.msg;
      }
      else {
        $("#coupon-success").removeClass('d-none');
        document.getElementById('coupon-fail').innerHTML = '';
        document.getElementById("coupon-amount").innerHTML = resp.value;
        document.getElementById("cart-total-price").innerHTML = "&#2547;" + resp.cost;
        document.getElementById("total-cost").innerHTML = "&#2547;" + resp.cost;
        var div = document.getElementById('coupon-section');
        div.remove();
      }
      document.getElementById("overlay").style.display = "none";
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
  });
}



function CartDelete(id) {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    type: 'POST',
    url: 'http://localhost:8000/ajax/cartdelete',
    data: {
      'id': id,
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function (resp) {
      $('#cart' + id).remove();
      document.getElementById("cart-total-price").innerHTML = "&#2547;" + resp.cost;
      document.getElementById("total-cost").innerHTML = "&#2547;" + resp.cost;
      $(".cart-count").text(resp.item);
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
        document.getElementById("overlay").style.display = "none";
      });
      document.getElementById("overlay").style.display = "none";
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
  });
}


function AddWishlist(id) {
  document.getElementById("overlay").style.display = "block";
  if (document.getElementById('user').innerText === 'yes') {
    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000/ajax/addtowishlist',
      data: {
        'id': id,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (resp) {
        document.getElementById("overlay").style.display = "none";
        $(".wishlist-count").text(parseInt($(".wishlist-count").text()) + 1)
        new PNotify({
          title: 'Successfully Added',
          type: 'success',
          text: `Product successfully added to wishlist`,
          addclass: 'stack-bottom-right',
          icon: true,
          delay: 2500
        });
      },
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
    });
  }
  else {
    document.getElementById("overlay").style.display = "none";
    document.getElementById('login-modal-btn').click();
  }
}

function WishItemDelete(id) {
  document.getElementById("overlay").style.display = "block";
  if (document.getElementById('user').innerText === 'yes') {
    $.ajax({
      type: 'POST',
      url: '/ajax/deletewishlist',
      data: {
        'id': id,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (resp) {
        $('#item' + id).remove();
        $(".wishlist-count").text(parseInt($(".wishlist-count").text()) - 1)
        if (parseInt($(".wishlist-count").text()) == 0) {
          $(".wishlist-table").addClass("d-none")
          $(".empty-wishlist").removeClass("d-none")
        }
        else {
          $(".empty-wishlist").addClass("d-none")
        }
        document.getElementById("overlay").style.display = "none";
        new PNotify({
          title: 'Successfully deleted',
          type: 'success',
          text: `Product successfully deleted from wishlist`,
          addclass: 'stack-bottom-right',
          icon: true,
          delay: 2500
        });
      },
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
    });
  }
  else {
    document.getElementById("overlay").style.display = "none";
    document.getElementById('login-modal-btn').click();
  }
}