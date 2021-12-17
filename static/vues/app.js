
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
      'quantity': quantity
    },
    success: function(resp){
      document.getElementById("myAlert-message").innerHTML = resp.msg;
      showAlert();
      document.getElementById("item-text").innerHTML = resp.item;
      document.getElementById("item-cost").innerHTML = resp.cost;
    }
  });
  return
}

function desc(b, c, a, d, e){
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
          'id': e
        },
        success: function(resp){
          total = a*value;
          document.getElementById('product-total'+d).innerHTML = parseFloat(total)+".00";
          document.getElementById("myAlert-message").innerHTML = resp.msg;
          showAlert();
          document.getElementById("item-text").innerHTML = resp.item;
          document.getElementById("item-cost").innerHTML = resp.cost;
          document.getElementById('total-cost').innerHTML = "&#2547;"+resp.cost;
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
          'desc': true
        },
        success: function(resp){
          total = a*value;
          document.getElementById('product-total'+d).innerHTML = parseFloat(total)+".00";
          document.getElementById("myAlert-message").innerHTML = resp.msg;
          showAlert();
          document.getElementById("item-text").innerHTML = resp.item;
          document.getElementById("item-cost").innerHTML = resp.cost;
          document.getElementById('total-cost').innerHTML = "&#2547;"+resp.cost;
        }
      });
    }
  }
}


function addCoupon() {
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
      }
    }
  });
}