
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
        document.getElementById("myAlert-message").innerHTML = resp.msg;
        showAlert();
        document.getElementById("item-text").innerHTML = resp.item;
        document.getElementById("item-cost").innerHTML = resp.cost;
        var product = JSON.parse(resp.product);
        document.getElementById('product-title').innerHTML = product.title;
        document.getElementById('product-category-title').innerHTML = product.category;
        document.getElementById('product-amount').innerHTML = quantity;
        document.getElementById('product-image').src = product.image;
        document.getElementById('product-price').innerHTML = "&#2547;"+(parseFloat(product.price)*quantity);
        document.getElementById('product-main-price').innerHTML = "&#2547;"+product.main_price;
        document.getElementById('product-discount').innerHTML = "("+product.discount+"% off)";
        $("#add-product-modal").iziModal('open');
        document.getElementById("overlay").style.display = "none";
      }
    });
  }
  else{
    window.location = 'http://127.0.0.1:8000/auth';
    document.getElementById("overlay").style.display = "none";
  }
}

function desc(b, c, a, d, e){
  document.getElementById("overlay").style.display = "block";
  id = "inp"+d;
  val = parseInt(document.getElementById(id).value);
  if(b === 'inc'){
    value = val+1;
    if(value <= c){
      document.getElementById(id).value = value;
      $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/ajax/addtocart',
        data: {
          'id': e,
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(resp){
          total = a*value;
          document.getElementById('product-total'+d).innerHTML = parseFloat(total)+".00";
          document.getElementById("myAlert-message").innerHTML = resp.msg;
          showAlert();
          document.getElementById("item-text").innerHTML = resp.item;
          document.getElementById("item-cost").innerHTML = resp.cost;
          document.getElementById('total-cost').innerHTML = "&#2547;"+resp.cost;
          document.getElementById("overlay").style.display = "none";
        }
      });
    }
  }
  else{
    value = val-1;
    if(value >= 0){
      document.getElementById(id).value = value;
      $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/ajax/addtocart',
        data: {
          'id': e,
          'desc': true,
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(resp){
          total = a*value;
          document.getElementById('product-total'+d).innerHTML = parseFloat(total)+".00";
          document.getElementById("myAlert-message").innerHTML = resp.msg;
          showAlert();
          document.getElementById("item-text").innerHTML = resp.item;
          document.getElementById("item-cost").innerHTML = resp.cost;
          document.getElementById('total-cost').innerHTML = "&#2547;"+resp.cost;
          document.getElementById("overlay").style.display = "none";
        }
      });
    }
  }
}


function addCoupon() {
  document.getElementById("overlay").style.display = "none";
  var code = document.getElementById("coupon_code").value;
  $.ajax({
    type: 'POST',
    url: 'http://localhost:8000/ajax/addtocart',
    data: {
      'coupon_code': code,
      'id': 1
    },
    success: function(resp){
      if(resp.added == 'fail'){
        document.getElementById('coupon-fail').innerHTML = resp.msg;
      }
      else{
        document.getElementById("myAlert-message").innerHTML = resp.msg;
        showAlert();
        document.getElementById("item-text").innerHTML = resp.item;
        document.getElementById("item-cost").innerHTML = resp.cost;
        document.getElementById('total-cost').innerHTML = "&#2547;"+resp.cost;
        var div = document.getElementById('coupon-all');
        div.remove();
        var couponadd = document.getElementById("coupon-added");
        couponadd.classList.toggle("d-none");
        couponadd.classList.toggle("d-flex");
        document.getElementById('coupon-fail').innerHTML = '';
        document.getElementById("overlay").style.display = "none";
      }
    }
  });
}