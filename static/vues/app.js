// var app = Vue.createApp({
//   delimiters: ['[[', ']]'],
//   data() {
//     return {
//       name: "apppppppp",
//       card: [],
//     };
//   },

//   computed: {
//     totalCost() {
//       let tc = 0;
//       this.card.forEach(element => {
//         tc += parseFloat(element.price);
//       });
//       return tc;
//     },
//   },

//   methods: {
//     AddProduct(id, name, image, price) {
//       var item = document.getElementById('item-text');
//       item.textContent = parseInt(item.textContent) + 1;
//       var cost = document.getElementById('item-cost');
//       cost.textContent = parseFloat(cost.textContent) + parseFloat(price);
//       // $.ajax({
//       //   type: 'POST',
//       //   url: 'http://localhost:8000/ajax/addtocart',
//       //   data: { 
//       //     'id': id, 
//       //     'name': name,
//       //     'image': image,
//       //     'price': price
//       //   },
//       //   success: function(resp){
//       //     alert(resp);
//       //   }
//       // });
//     },
//     // deleteProduct(id){
//     //   $.ajax({
//     //     type: 'POST',
//     //     url: 'http://localhost:8000/ajax/addtocart',
//     //     data: { 
//     //       'id': id
//     //     },
//     //     success: function(resp){
//     //       alert(resp);
//     //     }
//     //   });
//     // },
//   },

//   // watch: {
//   //   couponCode(newValue) {
//   //     if (newValue.length === 10) {
//   //       let searchedCoupons = this.coupons.filter(
//   //         (item) => item.code === newValue
//   //       );
//   //       if (searchedCoupons.length === 1) {
//   //         this.appliedCoupon = searchedCoupons[0];
//   //         this.couponCode = "";
//   //       } else {
//   //         alert("Coupon not valid!");
//   //       }
//   //     }
//   //   },
//   // },
// });

// app.mount('#app');


function AddProduct(id, name, image, price) {
  $.ajax({
    type: 'POST',
    url: 'http://localhost:8000/ajax/addtocart',
    data: { 
      'id': id, 
      'name': name,
      'image': image,
      'price': price
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
          document.getElementById('total-cost').innerHTML = resp.cost;
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
          document.getElementById('total-cost').innerHTML = resp.cost;
        }
      });
    }
  }
}


function addCoupon() {
  alert('Yes');
}