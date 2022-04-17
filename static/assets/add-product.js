
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
    let options = new Array()
    options.push('color', $(".color-select:checked").val())
    options.push('size', $("#size").val())
    document.querySelectorAll("#option").forEach((element) => {
      options.push($(element).attr('op-name'), $(element)[0].options[$(element)[0].options.selectedIndex].attributes.name.value)
    })
    console.log(options)
    $.ajax({
      type: 'POST',
      url: '/ajax/addtocart',
      data: {
        'id': id,
        'quantity': quantity,
        'options': options
      },
      success: function (resp) {
        document.getElementById("cart-total-price").innerHTML = "&#2547;" + resp.subtotal;
        $("#cart-total-price").parent().removeClass("d-none")
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

// function Update(id, quantity) {
//   document.getElementById("overlay").style.display = "block";
//   $.ajax({
//     type: 'POST',
//     url: '/ajax/addtocart',
//     data: {
//       'id': id,
//       'update-quantity': quantity,
//     },
//     success: function (resp) {
//       if (resp.msg_type) {
//         alert(resp.msg);
//       }
//       else {
//         document.getElementById("cart-total-price").innerHTML = "&#2547;" + resp.subtotal;
//         $(".total-col" + id).text("৳" + (parseFloat($(".price-col" + id).attr("price")) * quantity).toFixed(2))
//         $(".total-cost").text("৳" + resp.cost)
//         $("#subtotal").text("৳" + resp.subtotal)
//         $("#dropdown-cart-products").empty();
//         varjson = JSON.parse(JSON.stringify(resp.cart));
//         varjson.forEach(function (data) {
//           var div = `<div class="product">
//                       <div class="product-cart-details">
//                           <h4 class="product-title">
//                               <a href="product.html">${data.title}</a>
//                           </h4>
//                           <span class="cart-product-info">
//                               <span class="cart-product-qty">${data.amount}</span>
//                               X${data.price}
//                           </span>
//                       </div><!-- End .product-cart-details -->
//                       <figure class="product-image-container">
//                           <a href="product.html" class="product-image">
//                               <img src="${data.image}" alt="product">
//                           </a>
//                       </figure>
//                       <a href="#" class="btn-remove" title="Remove Product" id="cart-remove" cart-id="${resp.id}"><i class="icon-close"></i></a>
//                   </div>`
//           $('#dropdown-cart-products').append(div);
//         });
//       }
//       document.getElementById("overlay").style.display = "none";
//     },
//     headers: {
//       "X-CSRFToken": getCookie("csrftoken")
//     },
//   });
// }

$("input[class='form-control amount']").on('change', function () {
  var val = parseInt($(this).val())
  var max = parseInt($(this).attr('max'))
  if (val <= max && val > 0) {
    $(this).parent().submit()
  }
  else {
    $(".message-sec").append('<p class="message error"><i class="fas fa-info-circle"></i>Invalid quantity</p>')
  }
});

$("#coupon-btn").click(function () {
  addCoupon();
});
function addCoupon() {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    type: 'POST',
    url: '/ajax/addtocart',
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
        document.getElementById("cart-total-price").innerHTML = "&#2547;" + resp.subtotal;
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
    url: '/ajax/cartdelete',
    data: {
      'id': id
    },
    success: function (resp) {
      $('#cart' + id).remove();
      document.getElementById("cart-total-price").innerHTML = "&#2547;" + resp.subtotal;
      $("#subtotal").text("৳" + resp.subtotal)
      $(".total-cost").text("৳" + resp.cost)
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
      url: '/ajax/addtowishlist',
      data: {
        'id': id
      },
      success: function (resp) {
        document.getElementById("overlay").style.display = "none";
        if (resp.type == 'success') {
          $(".wishlist-count").text(parseInt($(".wishlist-count").text()) + 1)
          title = 'Successfully Added'
          document.querySelectorAll("#btn-wishlist" + id).forEach((element) => {
            $(element).addClass("select")
          })
        }
        else {
          $(".wishlist-count").text(parseInt($(".wishlist-count").text()) - 1)
          title = 'Successfully removed'
          document.querySelectorAll("#btn-wishlist" + id).forEach((element) => {
            $(element).removeClass("select")
          })
        }
        new PNotify({
          title: title,
          type: resp.type,
          text: resp.msg,
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


// $("#option").change(function () {
//   console.log(($(this)[0].options[$(this)[0].options.selectedIndex]).innerText)
// })

document.querySelectorAll("#option").forEach((element) => {
  $(element).change(function () {
    console.log($(this)[0].options[$(this)[0].options.selectedIndex].attributes.name.value)
    var pr = parseFloat($("#pro-price").attr('price'))
    document.querySelectorAll("#option").forEach((elem) => {
      pr = pr + parseFloat($(elem).val())
    })
    pr = pr * parseInt($("#pro-quantity").val())
    $("#pro-price").text($("#pro-price").attr('currency') + pr.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ','))
  })
})

$("#pro-quantity").change(function () {
  var pr = parseFloat($("#pro-price").attr('price'))
  document.querySelectorAll("#option").forEach((elem) => {
    pr = pr + parseFloat($(elem).val())
  })
  $("#pro-price").text($("#pro-price").attr('currency') + (pr * parseInt($(this).val())).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ','))
})