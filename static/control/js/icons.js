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

$("#icon-select").on("change", function(){
  console.log($(this).val());
})
