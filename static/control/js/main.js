
$("#basicTree").on("changed.jstree", function (e, data) {
  var getdata = JSON.parse(data.instance.get_node(data.selected).li_attr.data);
  if (getdata.type === "category") {
    $("#add-category-form h6").text("Category");
    $("#add-category-form .search-field").removeClass("d-none");
    $("#add-category-form #cancel-btn").addClass("d-none");
    $("#add-category-form #delete-btn").removeClass("d-none");
    $("#add-subcategory-form").addClass("d-none");
    $("#add-group-form").removeClass("d-none");
  } else if (getdata.type === "group") {
    $("#add-category-form h6").text("Group");
    $("#add-category-form .search-field").addClass("d-none");
    $("#add-category-form #cancel-btn").addClass("d-none");
    $("#add-category-form #delete-btn").removeClass("d-none");
    $("#add-subcategory-form").removeClass("d-none");
    $("#add-group-form").addClass("d-none");
  } else {
    $("#add-category-form h6").text("Subcategory");
    $("#add-category-form .search-field").removeClass("d-none");
    $("#add-category-form #cancel-btn").addClass("d-none");
    $("#add-category-form #delete-btn").removeClass("d-none");
    $("#add-group-form").addClass("d-none");
    $("#add-subcategory-form").addClass("d-none");
  }
  $("#add-category-form #name").val(getdata.name);
  if (getdata.search) {
    $("#add-category-form #search").attr("checked", true);
  } else {
    $("#add-category-form #search").attr("checked", false);
  }
  if (getdata.enable) {
    $("#add-category-form #enable").attr("checked", true);
  } else {
    $("#add-category-form #enable").attr("checked", false);
  }
});

$("#add-root-category-btn").on("click", function () {
  $("#add-category-form h6").text("Add Root Category");
  $("#add-category-form #name").val("");
  $("#add-category-form #search").attr("checked", false);
  $("#add-category-form #enable").attr("checked", false);
  $("#add-category-form .search-field").removeClass("d-none");
  $("#add-category-form #cancel-btn").removeClass("d-none");
  $("#add-category-form #delete-btn").addClass("d-none");
  $("#add-group-form").addClass("d-none");
  $("#add-subcategory-form").addClass("d-none");
});

//! product menu section
$(".product-menu .menu").on("click", function () {
  if ($(this).hasClass("selected")) {
    $(this).removeClass("selected");
  } else {
    $(this).addClass("selected");
    $(".product-menu .menu.selected").not($(this)).removeClass("selected");
  }
});

$(".product-menu .submenu li").on("click", function () {
  if ($(this).hasClass("selected") === false) {
    $(this).addClass("selected");
    $(".product-menu .submenu li.selected")
      .not($(this))
      .removeClass("selected");
  }
});

// //! Select 2 customize

let ins = tail.select("#category-select", {
  search: true,
  placeholder: "Select category",
});
let group = tail.select("#group-select", {
  search: true,
  placeholder: "Select category",
});
tail.select("#subcategory-select", {
  search: true,
  placeholder: "Select category",
});
tail.select("#discount-type", {
  placeholder: "Discount type",
});
console.log(ins);
// ins.options.items = {};
// ins.options.add("New option", "Yes", false, false, false, '', true);

//! product sidenav section


$(".product-menu .menu-sec .submenu li").on("click", function () {
  var select = $(this).attr("for");
  $("#" + select).removeClass("d-none");
  $(".product-form")
    .not("#" + select)
    .addClass("d-none");
});

// Load thumbnail

var loadthumbnail = function (event) {
  var output = document.getElementById("thumbnail");
  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function () {
    URL.revokeObjectURL(output.src); // free memory
  };
};

// add color btn

$("#add-color").on("click", function () {
  var inp = `<input class="mx-1 my-1" id="color-pick" type="color" />`;
  $("#color-picker").append(inp);
  document.querySelectorAll("[id=color-pick]").forEach((element) => {
    console.log(element.value);
  });
});

document.querySelectorAll("[id=option-name]").forEach((element) => {
  $(element).on("keyup", function () {
    $(this)
      .parent()
      .parent()
      .parent()
      .children(".option-head")
      .children(".option-name")
      .text($(this).val());
  });
});

$(".add-new-option").on("click", function () {
  $(".new-option").append(div);
  tail.select("#discount-type", {
    placeholder: "Discount type",
  });
  document.querySelectorAll("[id=option-name]").forEach((element) => {
    $(element).on("keyup", function () {
      $(this)
        .parent()
        .parent()
        .parent()
        .children(".option-head")
        .children(".option-name")
        .text($(this).val());
    });
  });
  $(".new-option .add-options-option")
    .last()
    .on("click", function () {
      $(this).parent().children(".options-option").append(div1);
      $(".new-option .fa-trash").on("click", function () {
        $(this).parent().parent().parent().remove();
      });
    });
  $(".new-option .option .option-head")
    .last()
    .on("click", function () {
      if ($(this).parent().hasClass("selected")) {
        $(this).parent().removeClass("selected");
      } else {
        $(this).parent().addClass("selected");
        $(".option-head").not($(this)).parent().removeClass("selected");
      }
    });
  $(".new-option")
    .children(".option-sec")
    .children()
    .last()
    .on("click", function () {
      $(this).parent().remove();
    });
});

var div = `<div class="d-flex flex-fill align-items-center option-sec">
                    <div class="option w-100">
                      <div
                        class="
                          option-head
                          d-flex
                          flex-fill
                          justify-content-between
                          mb-3
                        "
                      >
                        <h6 class="option-name">Option Name</h6>
                        <span class="arrow"
                          ><i class="fa fa-angle-right"></i
                        ></span>
                      </div>
                      <div class="row mb-3 mx-2">
                        <label
                          for="inputEmail3"
                          class="col-sm-2 col-form-label d-none d-xl-block"
                          >Name</label
                        >
                        <div class="col-sm-6">
                          <input
                            type="text"
                            class="form-control"
                            id="option-name"
                            placeholder="Option name"
                          />
                        </div>
                        <div class="col-sm-4">
                          <select id="discount-type">
                            <option value="2">Dropdown</option>
                            <option value="1">Radio</option>
                          </select>
                        </div>
                      </div>
                      <!-- <div class="row mb-3 mx-2">
                        <label
                          for="inputEmail3"
                          class="col-sm-2 col-form-label d-none d-xl-block"
                          >Type</label
                        >
                        <div class="col-sm-10">
                          <select id="discount-type">
                            <option value="2">Dropdown</option>
                            <option value="1">Radio</option>
                          </select>
                        </div>
                      </div> -->
                      <div class="options-option">
                        <div class="row mb-3 mx-2">
                          <label
                            for="inputEmail3"
                            class="col-sm-2 col-form-label d-none d-xl-block"
                            >Option</label
                          >
                          <div class="col-sm-5 d-flex">
                            <input
                              type="text"
                              class="form-control"
                              id="option-name"
                              placeholder="Label"
                            />
                          </div>
                          <div class="col-sm-4 d-flex flex-fill">
                            <input
                              type="number"
                              class="form-control"
                              placeholder="Price"
                            />
                            <div class="btn col-sm-1">
                              <i class="fa fa-trash"></i>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="btn add-options-option">Add option</div>
                    </div>
                    <i class="fa fa-trash fa-lg ms-3"></i>
                  </div>`;

$(".add-options-option").on("click", function () {
  $(this).parent().children(".options-option").append(div1);
  $(this)
    .parent()
    .children(".options-option")
    .children()
    .last()
    .children()
    .last()
    .children()
    .last()
    .on("click", function () {
      $(this).parent().parent().remove();
    });
});

var div1 = `<div class="row mb-3 mx-2">
              <label
                for="inputEmail3"
                class="col-sm-2 col-form-label d-none d-xl-block"
                >Option</label
              >
              <div class="col-sm-5 d-flex">
                <input
                  type="text"
                  class="form-control"
                  id="option-name"
                  placeholder="Label"
                />
              </div>
              <div class="col-sm-4 d-flex flex-fill">
                <input
                  type="number"
                  class="form-control"
                  placeholder="Price"
                />
                <div class="btn col-sm-1">
                  <i class="fa fa-trash"></i>
                </div>
              </div>
            </div>`;

// $(".option-head").on("click", function () {
//   if ($(this).parent().hasClass("selected") !== true) {
//     $(this).parent().removeClass("selected");
//   } else {
//     $(this).parent().addClass("selected");
//   }
// });

$(".option-head").on("click", function () {
  if ($(this).parent().hasClass("selected")) {
    $(this).parent().removeClass("selected");
  } else {
    $(this).parent().addClass("selected");
    $(".option-head").not($(this)).parent().removeClass("selected");
  }
});

$(".options-option .fa-trash").on("click", function () {
  $(this).parent().parent().parent().remove();
});

$("#options")
  .children(".option-sec")
  .children()
  .last()
  .on("click", function () {
    $(this).parent().remove();
  });

$(".add-product-btn").on("click", function(){
  $(".product-list").addClass("d-none");
  $(".add-product-sec").removeClass("d-none");
  var el = document.querySelectorAll(".submenu");
  el.forEach((element) => {
    let height = element.scrollHeight;
    element.style.setProperty("--height", height + "px");
  });
})

$(".add-coupon-btn").on("click", function(){
  $(".coupon-list").addClass("d-none");
  $(".add-coupon-sec").removeClass("d-none");
  var el = document.querySelectorAll(".submenu");
  el.forEach((element) => {
    let height = element.scrollHeight;
    element.style.setProperty("--height", height + "px");
  });
})


// product page
$(".check-column-header").on("click", function(){
  const check = $(this).parent().parent().parent().children("tbody").children().children(".check-column").children().children().children(".check");
  // check.forEach((element) => { 
  //   console.log(element);
  // })
  const elem = $(this).children().children().children();

  if (elem.checked == true){
    for (const ch of check){
      ch.checked = false;
    }
    elem.checked = false;
  }
  else{
    for (const ch of check){
      ch.checked = true;
    }
    elem.checked = true;
  }
})


// category page
// $("#category-select").on("change", function(){
//   alert($(this).val());
// })


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$("#category-select").change(function(){
    $.ajax({
        url:"/productgroups/",
        type:"POST",
        data:{category_id: $(this).val(),},
        success: function(result) {
          result.forEach(function(data){
            var id = (data.id).tostring()
            group.options.add(id, data.name, false, false, false, '', true);
          })
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        error: function(e){
            console.error(JSON.stringify(e));
        },
    });
});