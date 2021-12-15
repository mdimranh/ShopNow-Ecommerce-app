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
      alert(resp.cost);
      document.getElementById("item-text").innerHTML = resp.item;
      document.getElementById("item-cost").innerHTML = resp.cost;
    }
  });
  return
}