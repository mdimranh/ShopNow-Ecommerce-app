$(document).ready(function () {
  // jsonObject.forEach(element => {
  //     console.log(element);
  // });
  // console.log(typeof(jsonObject));
  opt = [];
  for (const icon in jsonObjects.icons) {
    var st = `<i class="${jsonObjects.icons[icon]} mx-3 fa-lg"></i> ${jsonObjects.icons[icon]}`;
    opt.push({ label: st, value: jsonObjects.icons[icon] });
  }
  VirtualSelect.init({
    ele: "#icon-select",
    options: opt,
    search: true,
  });
});
// $(".get-data").on("click", function(){
//   var val = $("#icon-select").val();
//   if(val === ""){
//     alert("Null");
//   }
//   else{
//     alert(val);
//   }
// })

// $(".get-data").on("click", function(){
//   console.log("yes");
//   var position = "inside";
//   var parent = $("#basicTree").jstree("get_selected");
//   console.log(parent);
// })

// $(".get-data").on("click", function(){
//   var selected_node = $("#basicTree").jstree("get_selected");
//   var getdata = JSON.parse($("#basicTree").jstree("get_node", selected_node).li_attr.data);
//   console.log(getdata.id);
// })

// $("#basicTree").on("changed.jstree", function (e, data) {
//   var selected_node = $("#basicTree").jstree("get_selected");
//   var getdata = JSON.parse($("#basicTree").jstree("get_node", selected_node).li_attr.data);
//   $("#id").val(getdata.id)
//   $("#type").val(getdata.type)
// })