
function quantity(type, amount){
  var val = parseInt(document.getElementById('pro-quantity').value);
  if(type === 'inc' && amount > val){
    document.getElementById('pro-quantity').value++;
  }
  else if(type === 'dec' && val > 0){
    document.getElementById('pro-quantity').value--;
  }
}

function AddProduct(id, name, image, price, quantity) {
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
        'name': name,
        'image': image,
        'price': price,
        'quantity': quantity,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function(resp){
        // document.getElementById("myAlert-message").innerHTML = resp.msg;
        // showAlert();
        // document.getElementById("item-text").innerHTML = resp.item;
        // document.getElementById("item-cost").innerHTML = resp.cost;
        // var product = JSON.parse(resp.product);
        // document.getElementById('product-title').innerHTML = product.title;
        // document.getElementById('product-category-title').innerHTML = product.category;
        // document.getElementById('product-amount').innerHTML = quantity;
        // document.getElementById('product-image').src = product.image;
        // document.getElementById('product-price').innerHTML = "&#2547;"+(parseFloat(product.price)*quantity);
        // document.getElementById('product-main-price').innerHTML = "&#2547;"+product.main_price;
        // document.getElementById('product-discount').innerHTML = "("+product.discount+"% off)";
        // $("#add-product-modal").iziModal('open');
        // document.getElementById("overlay").style.display = "none";
        // varstr = JSON.stringify(resp.cart);
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
                      <a href="#" class="btn-remove" title="Remove Product"><i class="icon-close"></i></a>
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
  // else{
  //   window.location = 'http://127.0.0.1:8000/auth';
  //   document.getElementById("overlay").style.display = "none";
  // }
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
      console.log(resp.msg);
      document.getElementById("overlay").style.display = "none";
    },
    headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
  });
}

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
        document.getElementById('total-cost').innerHTML = "&#2547;"+resp.cost;
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

// $('#cart-quantity').on('change', function(){
//   console.log($(this).val());
//   console.log($(this).attr("product-id"));
// });

$("input[class='form-control amount']").on('change', function(){
  Update($(this).attr("cart-id"), $(this).val());
});


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