
function quantity(type, amount){
  var val = parseInt(document.getElementById('pro-quantity').value);
  if(type === 'inc' && amount > val){
    document.getElementById('pro-quantity').value++;
  }
  else if(type === 'dec' && val > 0){
    document.getElementById('pro-quantity').value--;
  }
}

function AddProduct(id, quantity) {
  document.getElementById("overlay").style.display = "block";
  if (document.getElementById('user').innerText === 'yes'){
    if(quantity === 'no'){
      quantity = 1;
    }
    else{
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
      success: function(resp){
        document.getElementById("cart-total-price").innerHTML = "&#2547;"+resp.cost;
        $("#dropdown-cart-products").empty();
        varjson = JSON.parse(JSON.stringify(resp.cart));
        varjson.forEach(function(data){
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
        // for (var property in product) {
        //     console.log(property,":",product[property]);
        // }
      },
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
    });
  }
  else{
    document.getElementById("overlay").style.display = "none";
    document.getElementById('login-modal-btn').click();
  }
}

function Update(id, quantity){
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    type: 'POST',
    url: 'http://localhost:8000/ajax/addtocart',
    data: {
      'id': id,
      'update-quantity': quantity,
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(resp){
      if (resp.msg_type){
        alert(resp.msg);
      }
      else{
      document.getElementById("cart-total-price").innerHTML = "&#2547;"+resp.cost;
      document.getElementById("total-cost").innerHTML = "&#2547;"+resp.cost;
        $("#dropdown-cart-products").empty();
        varjson = JSON.parse(JSON.stringify(resp.cart));
        varjson.forEach(function(data){
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

$("input[class='form-control amount']").on('change', function(){
  Update($(this).attr("cart-id"), $(this).val());
});

$("#coupon-btn").click(function(){
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
    success: function(resp){
      if(resp.added == 'fail'){
        document.getElementById('coupon-fail').innerHTML = resp.msg;
      }
      else{
        $("#coupon-success").removeClass('d-none');
        document.getElementById('coupon-fail').innerHTML = '';
        document.getElementById("coupon-amount").innerHTML = resp.value;
        document.getElementById("cart-total-price").innerHTML = "&#2547;"+resp.cost;
        document.getElementById("total-cost").innerHTML = "&#2547;"+resp.cost;
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



function CartDelete(id){
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    type: 'POST',
    url: 'http://localhost:8000/ajax/cartdelete',
    data: {
      'id': id,
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(resp){
      $('#cart'+id).remove();
      document.getElementById("cart-total-price").innerHTML = "&#2547;"+resp.cost;
      document.getElementById("total-cost").innerHTML = "&#2547;"+resp.cost;
        $("#dropdown-cart-products").empty();
        varjson = JSON.parse(JSON.stringify(resp.cart));
        varjson.forEach(function(data){
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
  if (document.getElementById('user').innerText === 'yes'){
    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000/ajax/addtowishlist',
      data: { 
        'id': id,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function(resp){
        document.getElementById("overlay").style.display = "none";
        alert(resp.msg);
      },
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
    });
  }
  else{
    document.getElementById("overlay").style.display = "none";
    document.getElementById('login-modal-btn').click();
  }
}




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