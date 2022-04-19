$("#basicTree").on("changed.jstree", function (e, data) {
  var getdata = JSON.parse(data.instance.get_node(data.selected).li_attr.data);
  if (getdata.type === "category") {
    $("#category-form h6").text("Category");
    $("#category-form").removeClass("d-none");
    $("#category-form #delete-btn").removeClass("d-none");
    $("#category-form #delete-btn").attr("href", "/control/category/delete/" + getdata.id + "")
    $("#group-form").removeClass("d-none");
    $("#group-form h6").text("Add Group");
    $("#group-form #save-btn").text("Add");
    $("#group-form #delete-btn").addClass("d-none");
    $("#subcategory-form").addClass("d-none");
    $("#category-form #type").val(getdata.type)
    $("#category-form #id").val(getdata.id)
    $("#group-form #type").val(getdata.type)
    $("#group-form #id").val(getdata.id)
    document.getElementById("icon-select").setValue((getdata.icon).replace(",", ' '));
    $("#category-form #category-name").val(getdata.name)
    if (getdata.search === 'True') {
      $("#category-form #search").attr("checked", "checked")
    }
    if (getdata.enable === 'True') {
      $("#category-form #enable").attr("checked", "checked")
    }
  } else if (getdata.type === "group") {
    $("#category-form").addClass("d-none");
    $("#group-form h6").text("Group");
    $("#group-form #save-btn").text("Save");
    $("#group-form #delete-btn").removeClass("d-none");
    $("#group-form #delete-btn").attr("href", "/control/group/delete/" + getdata.id + "")
    $("#group-form").removeClass("d-none");
    $("#subcategory-form").removeClass("d-none");
    $("#subcategory-form h6").text("Add Subcategory");
    $("#subcategory-form #save-btn").text("Add");
    $("#subcategory-form #delete-btn").addClass("d-none");
    $("#group-form #type").val(getdata.type)
    $("#group-form #id").val(getdata.id)
    $("#subcategory-form #type").val(getdata.type)
    $("#subcategory-form #id").val(getdata.id)
    $("#group-form #group-name").val(getdata.name)
    if (getdata.search === 'True') {
      $("#group-form #search").attr("checked", "checked")
    }
    if (getdata.enable === 'True') {
      $("#group-form #enable").attr("checked", "checked")
    }
  } else if (getdata.type === "subcategory") {
    $("#category-form").addClass("d-none");
    $("#group-form").addClass("d-none");
    $("#subcategory-form").removeClass("d-none");
    $("#subcategory-form h6").text("Subcategory");
    $("#subcategory-form #save-btn").text("Save");
    $("#subcategory-form #delete-btn").attr("href", "/control/subcategory/delete/" + getdata.id + "")
    $("#subcategory-form #delete-btn").removeClass("d-none");
    $("#subcategory-form #type").val(getdata.type)
    $("#subcategory-form #id").val(getdata.id)
    $("#subcategory-form #subcategory-name").val(getdata.name)
    if (getdata.search === 'True') {
      $("#subcategory-form #search").attr("checked", "checked")
    }
    if (getdata.enable === 'True') {
      $("#subcategory-form #enable").attr("checked", "checked")
    }
  }
  $("#add-category-form #name").val(getdata.name);
});


$("#add-root-category-btn").on("click", function () {
  var selected_node = $("#basicTree").jstree("get_selected");
  var getdata = JSON.parse($("#basicTree").jstree("get_node", selected_node).li_attr.data);
  $("#category-form").removeClass("d-none")
  $("#category-form h6").text("Add Root Category");
  $("#category-form #delete-btn").removeClass("d-none");
  $("#category-form #type").val("new-cat")
  $("#category-form #id").val('id')
  $("#category-form #category-name").val("");
  document.getElementById("icon-select").setValue('');
  $("#category-form #search").attr("checked", false);
  $("#category-form #enable").attr("checked", false);
  $("#category-form .search-field").removeClass("d-none");
  $("#category-form #cancel-btn").removeClass("d-none");
  $("#category-form #delete-btn").addClass("d-none");
  $("#group-form").addClass("d-none");
  $("#subcategory-form").addClass("d-none");
});

$(".collapse-all").on("click", function () {
  $("#basicTree").jstree("close_all");
})

$(".expand-all").on("click", function () {
  $("#basicTree").jstree("open_all");
})

//! product menu section
$(".product-menu .menu").not(".disable").on("click", function () {
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

// let ins = tail.select("#category-select", {
//   search: true,
//   placeholder: "Select category",
// });
// let group = tail.select("#group-select", {
//   search: true,
//   placeholder: "Select category",
// });
// tail.select("#subcategory-select", {
//   search: true,
//   placeholder: "Select category",
// });
// tail.select("#discount-type", {
//   placeholder: "Discount type",
// });
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

// var loadthumbnail = function (event) {
//   var output = event.path[1].firstElementChild.firstElementChild
//   // var output = document.getElementById("thumbnail");
//   // console.log(output)
//   output.src = URL.createObjectURL(event.target.files[0]);
//   output.onload = function () {
//     URL.revokeObjectURL(output.src); // free memory
//   };
// };

$("#add-thumbnail-input").change(function (event) {
  var output = $(this).parent().children("label").children("img")[0]
  output.src = URL.createObjectURL(event.target.files[0]);
})

$("#add-thumbnail-input-1").change(function (event) {
  var output = $(this).parent().children("label").children("img")[0]
  output.src = URL.createObjectURL(event.target.files[0]);
})

$("#edit-thumbnail-input").change(function (event) {
  var output = $(this).parent().children("label").children("img")[0]
  output.src = URL.createObjectURL(event.target.files[0]);
})

document.querySelectorAll("#trash").forEach((element) => {
  $(element).click(function () {
    if ($("#remove-images").val().length > 0) {
      var val = $("#remove-images").val() + ',' + $(this).attr("img-id")
    }
    else {
      var val = $("#remove-images").val() + $(this).attr("img-id")
    }
    $("#remove-images").val(val)
    $(this).parent().remove()
  })
})

// add color btn

$("#add-color").on("click", function () {
  var inp = `<input class="mx-1 my-1" id="color-pick" name="color" type="color" />`;
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
      $(this).parent().children(".options-option").last().append(div1);
      var option_increase = parseInt($(this).parent().children(".options-option").children().first().val()) + 1;
      $(this).parent().children(".options-option").children().first().val(option_increase);
      $(".new-option .fa-trash").on("click", function () {
        var option_decrease = parseInt($(this).parent().parent().parent().parent().children().first().val()) - 1;
        $(this).parent().parent().parent().parent().children().first().val(option_decrease);
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
  VirtualSelect.init({
    ele: "select",
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
                            name="option-name"
                            id="option-name"
                            placeholder="Option name"
                          />
                        </div>
                        <div class="col-sm-4">
                          <select id="discount-type" name="option-style">
                            <option value="dropdown">Dropdown</option>
                            <option value="radion">Radio</option>
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
                            <option value="dropdown">Dropdown</option>
                            <option value="radio">Radio</option>
                          </select>
                        </div>
                      </div> -->
                      <div class="options-option">
                        <input type="hidden" id="option-count" name="option-count" value="1">
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
                              name="options-option-name"
                              placeholder="Label"
                            />
                          </div>
                          <div class="col-sm-4 d-flex flex-fill">
                            <input
                              type="number"
                              class="form-control"
                              name="option-price"
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
  $(this).parent().children(".options-option").last().append(div1);
  var option_increase = parseInt($(this).parent().children(".options-option").children().first().val()) + 1;
  $(this).parent().children(".options-option").children().first().val(option_increase);
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
      var option_decrease = parseInt($(this).parent().parent().parent().children().first().val()) - 1;
      $(this).parent().parent().parent().children().first().val(option_decrease);
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
                  name="options-option-name"
                  placeholder="Label"
                />
              </div>
              <div class="col-sm-4 d-flex flex-fill">
                <input
                  type="number"
                  class="form-control"
                  name="option-price"
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
  var option_decrease = parseInt($(this).parent().parent().parent().parent().children().first().val()) - 1;
  $(this).parent().parent().parent().parent().children().first().val(option_decrease);
  $(this).parent().parent().parent().remove();
});

$("#add-options")
  .children(".option-sec")
  .children()
  .last()
  .on("click", function () {
    $(this).parent().remove();
  });

$(".add-product-btn").on("click", function () {
  $(".product-list").addClass("d-none");
  $(".add-product-sec").removeClass("d-none");
  var el = document.querySelectorAll(".submenu");
  el.forEach((element) => {
    let height = element.scrollHeight;
    element.style.setProperty("--height", height + "px");
  });
})

$(".add-coupon-btn").on("click", function () {
  $(".coupon-list").addClass("d-none");
  $(".add-coupon-sec").removeClass("d-none");
  var el = document.querySelectorAll(".submenu");
  el.forEach((element) => {
    let height = element.scrollHeight;
    element.style.setProperty("--height", height + "px");
  });
})

$(".add-user-btn").on("click", function () {
  $(".user-list").addClass("d-none");
  $(".add-user-sec").removeClass("d-none");
  var el = document.querySelectorAll(".submenu");
  el.forEach((element) => {
    let height = element.scrollHeight;
    element.style.setProperty("--height", height + "px");
  });
})

$(".add-slide-btn").on("click", function () {
  $(".slide-list").addClass("d-none");
  $(".add-slide-sec").removeClass("d-none");
  var el = document.querySelectorAll(".submenu");
  el.forEach((element) => {
    let height = element.scrollHeight;
    element.style.setProperty("--height", height + "px");
  });
})

//! sitefront section
// slide page

// const dragArea = document.querySelector(".wrapper");
// new Sortable(dragArea, {
//   animation: 350,
//   handle: '.handle'
// })


// product page



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

VirtualSelect.init({
  ele: ".hideClear.hideSearch",
  search: false,
  hideClearButton: true,
})

VirtualSelect.init({
  ele: ".hideClear",
  search: true,
  hideClearButton: true
})

VirtualSelect.init({
  ele: "select",
  search: true
});

$("#add-category-select").on('change', function () {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    url: "/control/productgroups",
    type: "POST",
    data: { category_id: $(this).val(), },
    success: function (result) {
      opt = []
      result.forEach(function (data) {
        opt.push({ label: data.name, value: data.id })
      })
      VirtualSelect.init({
        ele: "#add-group-select",
        options: opt
      })
      VirtualSelect.init({
        ele: "#subcategory-select",
      })
      document.getElementById("overlay").style.display = "none";
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
});

$("#add-group-select").on('change', function () {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    url: "/control/productgroups",
    type: "POST",
    data: { group_id: $(this).val(), },
    success: function (result) {
      opt = []
      result.forEach(function (data) {
        opt.push({ label: data.name, value: data.id })
      })
      VirtualSelect.init({
        ele: "#add-subcategory-select",
        options: opt
      })
      document.getElementById("overlay").style.display = "none";
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
});


$("#edit-product-category-select").on('click', function () {
  $("#edit-product-category-select").on('change', function () {
    document.getElementById("overlay").style.display = "block";
    $.ajax({
      url: "/control/productgroups",
      type: "POST",
      data: { category_id: $(this).val(), },
      success: function (result) {
        opt = []
        result.forEach(function (data) {
          opt.push({ label: data.name, value: data.id })
        })
        VirtualSelect.init({
          ele: "#edit-product-group-select",
          options: opt
        })
        VirtualSelect.init({
          ele: "#edit-product-subcategory-select",
        })
        document.getElementById("overlay").style.display = "none";
      },
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      error: function (e) {
        console.error(JSON.stringify(e));
      },
    });
  });
});

$("#edit-product-group-select").on('click', function () {
  $("#edit-product-group-select").on('change', function () {
    document.getElementById("overlay").style.display = "block";
    $.ajax({
      url: "/control/productgroups",
      type: "POST",
      data: { group_id: $(this).val(), },
      success: function (result) {
        opt = []
        result.forEach(function (data) {
          opt.push({ label: data.name, value: data.id })
        })
        VirtualSelect.init({
          ele: "#edit-product-subcategory-select",
          options: opt
        })
        document.getElementById("overlay").style.display = "none";
      },
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      error: function (e) {
        console.error(JSON.stringify(e));
      },
    });
  });
});

$(".add-link-btn").click(function () {
  $(this).parent().children("#new-link").append(linkdiv)
  document.querySelectorAll("#removelink").forEach((element) => {
    $(element).click(function () {
      $(this).parent().remove()
    })
  })
})

linkdiv = `<div class="row mb-3">
            <div class="col-sm-4">
              <input
                type="text"
                class="form-control"
                name="title"
                placeholder="Title"
                required
              />
              <div class="invalid-feedback">Please enter title</div>
            </div>
            <div class="col-sm-7">
              <input
                type="text"
                class="form-control"
                name="link"
                placeholder="Link"
                required
              />
              <div class="invalid-feedback">Please enter link</div>
            </div>
            <i id="removelink" class="fas fa-trash col-sm-1 mt-2 d-flex flex-fill justify-content-end"></i>
          </div>`

document.querySelectorAll("#removelink").forEach((element) => {
  $(element).click(function () {
    $(this).parent().remove()
  })
})

// product carousel

$(".add-carousel-btn").click(function () {
  $(".caro-item.selected").removeClass("selected")
  $("#caro-name").val("")
  document.getElementById("caro-category").reset()
  if ($("#caro-group").val().length > 0) {
    document.getElementById("caro-group").reset()
  }
  if ($("#caro-subcategory").val().length > 0) {
    document.getElementById("caro-subcategory").reset()
  }
  $("#caro-enable").attr("checked", true)
  $("#save-btn").text("Add Carousel")
  $(".carousel-title").text("Add New Carousel")
  $("#id").val('')
})
$(".caro-item").click(function () {
  $(".caro-item.selected").removeClass("selected")
  if (!$(this).hasClass("selecded")) {
    $(this).addClass("selected")
  }
  $("#caro-name").val($(this).attr("name"))
  document.getElementById("caro-category").setValue($(this).attr("category").split(","))
  if ($(this).attr("group").length > 0) {
    document.getElementById("caro-group").setValue($(this).attr("group").split(","))
  }
  else {
    document.getElementById("caro-group").reset()
  }
  if ($(this).attr("subcat").length > 0) {
    document.getElementById("caro-subcategory").setValue($(this).attr("subcat").split(","))
  }
  else {
    document.getElementById("caro-subcategory").reset()
  }
  if ($(this).attr("status") == 'True') {
    $("#caro-enable").attr("checked", true)
  }
  else {
    $("#caro-enable").attr("checked", false)
  }
  $("#save-btn").text("Save")
  $(".carousel-title").text($(this).attr("name"))
  $("#id").val($(this).attr("id"))
})

$(".delete-carousel").on("click", function () {
  document.getElementById("overlay").style.display = "block";
  var action = 'delete'
  $.ajax({
    url: "/control/carousel/update",
    type: "POST",
    data: { carousel_id: $(this).parent().children(".caro-item").attr("id"), action: action },
    success: function (result) {
      document.getElementById("overlay").style.display = "none";
      new PNotify({
        title: 'Successfully deleted',
        type: 'success',
        text: `Selected carousel deleted successfully. You can now add carousel.`,
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
      if ($("div[id=" + result.id + "]").parent().children(".caro-item").hasClass("selected")) {
        $("div[id=" + result.id + "]").parent().remove()
        $("#edit-carousel-form").trigger("reset")
      }
      else {
        $("div[id=" + result.id + "]").parent().remove()
      }
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
})

//! User list table


var allowall = document.querySelectorAll("span[ids=allow-all]")
for (i = 0; i < allowall.length; i++) {
  allowall[i].addEventListener("click", function () {
    // $(this).parent().parent().children("li").children().children(".btn-group").children("#allow-btn").click();
    var allow = document.querySelectorAll("input[ids=allow-btn]")
    for (index = 0; index < allow.length; index++) {
      allow[index].click();
    }
  });
}

var denyall = document.querySelectorAll("span[ids=deny-all]")
for (i = 0; i < allowall.length; i++) {
  denyall[i].addEventListener("click", function () {
    // $(this).parent().parent().children("li").children().children(".btn-group").children("#allow-btn").click();
    var deny = document.querySelectorAll("input[ids=deny-btn]")
    for (index = 0; index < deny.length; index++) {
      deny[index].click();
    }
  });
}

// var inheritall = document.querySelectorAll("span[ids=inherit-all]")
// for (i = 0; i < allowall.length; i++) {
//   inheritall[i].addEventListener("click", function () {
//     // $(this).parent().parent().children("li").children().children(".btn-group").children("#allow-btn").click();
//     var inherit = document.querySelectorAll("input[ids=inherit-btn]")
//     for (index = 0; index < inherit.length; index++) {
//       inherit[index].click();
//     }
//   });
// }

var allowallsec = document.querySelectorAll("span[ids=allow]")
for (i = 0; i < allowallsec.length; i++) {
  allowallsec[i].addEventListener("click", function () {
    var allow = this.parentNode.parentNode.parentNode.querySelectorAll("input[ids=allow-btn]");
    for (index = 0; index < allow.length; index++) {
      allow[index].click();
    }
  });
}

var denyallsec = document.querySelectorAll("span[ids=deny]")
for (i = 0; i < denyallsec.length; i++) {
  denyallsec[i].addEventListener("click", function () {
    var deny = this.parentNode.parentNode.parentNode.querySelectorAll("input[ids=deny-btn]");
    for (index = 0; index < deny.length; index++) {
      deny[index].click();
    }
  });
}

// var inheritallsec = document.querySelectorAll("span[ids=inherit]")
// for (i = 0; i < inheritallsec.length; i++) {
//   inheritallsec[i].addEventListener("click", function () {
//     var inherit = this.parentNode.parentNode.parentNode.querySelectorAll("input[ids=inherit-btn]");
//     for (index = 0; index < inherit.length; index++) {
//       inherit[index].click();
//     }
//   });
// }

var $remove = $('#remove')

var $usertable = $('#user-table')
var selections = []

$usertable.on('check.bs.table uncheck.bs.table ' +
  'check-all.bs.table uncheck-all.bs.table',
  function () {
    $remove.prop('disabled', !$usertable.bootstrapTable('getSelections').length)
    selections = getUserIdSelections()
  })

$(".user-remove").click(function () {
  var ids = getUserIdSelections()
  $remove.prop('disabled', true)
})

function getUserIdSelections() {
  return $.map($usertable.bootstrapTable('getSelections'), function (row) {
    return row[1]
  })
}

$(".user-remove").click(function () {
  var ids = getUserIdSelections()
  var users = new Array();
  for (i = 0; i <= ids.length - 1; i++) {
    users.push(ids[i]);
  }
  $("#selected-user").val(users);
  deleteUser();
})


function deleteUser() {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    url: "/user/delete-user",
    type: "POST",
    data: { users: $("#selected-user").val() },
    success: function (result) {
      $remove.prop('disabled', true);
      $('#user-table tr.selected').remove();
      if (parseInt(result.total) === 1) {
        total = '1 user';
      }
      else {
        total = `${result.total} users`;
      }
      document.getElementById("overlay").style.display = "none";
      new PNotify({
        title: 'Successfully deleted',
        type: 'success',
        text: `${total} deleted successfully. You can now add user.`,
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
};


//! user role section

var $grouptable = $('#group-table')
var selections = []

$grouptable.on('check.bs.table uncheck.bs.table ' +
  'check-all.bs.table uncheck-all.bs.table',
  function () {
    $remove.prop('disabled', !$grouptable.bootstrapTable('getSelections').length)
    selections = getGroupIdSelections()
  })

$(".group-remove").click(function () {
  $remove.prop('disabled', true)
})

function getGroupIdSelections() {
  return $.map($grouptable.bootstrapTable('getSelections'), function (row) {
    return row[1]
  })
}

$(".group-remove").click(function () {
  var ids = getGroupIdSelections()
  var roles = new Array();
  for (i = 0; i <= ids.length - 1; i++) {
    roles.push(ids[i]);
  }
  $("#selected-group").val(roles);
  deleteGroup();
})


function deleteGroup() {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    url: "/group/delete-group",
    type: "POST",
    data: { groups: $("#selected-group").val() },
    success: function (result) {
      $remove.prop('disabled', true);
      $('#group-table tr.selected').remove();
      if (parseInt(result.total) === 1) {
        total = '1 group';
      }
      else {
        total = `${result.total} groups`;
      }
      document.getElementById("overlay").style.display = "none";
      new PNotify({
        title: 'Successfully deleted',
        type: 'success',
        text: `${total} deleted successfully. You can now add group.`,
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
};


//! product list table

var $producttable = $('#product-table')

function getProductIdSelections() {
  return $.map($producttable.bootstrapTable('getSelections'), function (row) {
    return row[2]
  })
}

$producttable.on('check.bs.table uncheck.bs.table ' +
  'check-all.bs.table uncheck-all.bs.table',
  function () {
    $remove.prop('disabled', !$producttable.bootstrapTable('getSelections').length)
    selections = getProductIdSelections()
  })

$(".pro-remove").click(function () {
  var ids = getProductIdSelections()
  var products = new Array();
  for (i = 0; i <= ids.length - 1; i++) {
    products.push(ids[i].slice(39, ids[i].length - 6));
  }
  $("#selected-product").val(products);
  deleteProduct();
})


// $producttable.on("click-cell.bs.table", function(field, value, row, $element){
//   var link = $element[2];
//   if(value === 3){
//     var lnk = link.slice(9, link.length-6)
//     location.href = lnk
//   }
// })


// delete product

function deleteProduct(products) {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    url: "/control/product/delete-product",
    type: "POST",
    data: { product: $("#selected-product").val() },
    success: function (result) {
      $remove.prop('disabled', true);
      $('#product-table tr.selected').remove();
      if (parseInt(result.total) === 1) {
        total = '1 product';
      }
      else {
        total = `${result.total} products`;
      }
      document.getElementById("overlay").style.display = "none";
      new PNotify({
        title: 'Successfully deleted',
        type: 'success',
        text: `${total} deleted successfully. You can now add product.`,
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
};


//! add product section

// $("#save-btn").on("click", function(){
//   alert("click");
// })

var savebtn = document.querySelectorAll("div[id=save-btn]");
for (i = 0; i < savebtn.length; i++) {
  savebtn[i].addEventListener('click', function (e) {
    if ($("#add-product-name").val().length === 0 || $("#add-short-desc").val().length === 0 || $("#add-quantity").val().length === 0 || $("#add-short-desc").val().length === 0) {
      $("[for=add-general]").click();
    }
    else if ($("#add-category-select").val().length === 0) {
      $("[for=add-category]").click();
    }
    else if ($("#add-main-price").val().length === 0) {
      $("[for=add-price]").click();
    }
    else if ($("#add-thumbnail-input").val().length === 0) {
      $("[for=add-images]").click();
    }
    else if ($("#add-meta-title").val().length === 0 || $("#add-meta-keywords").val().length === 0 || $("#add-meta-descriptions").val().length === 0) {
      $("[for=add-seo]").click();
    }
    else if ($("#add-description").val().length === 0) {
      $("[for=add-additional]").click();
    }
  })
}

$("#color-pick").on("change", function () {
  console.log($(this).val());
})

// product-name
// short-desc
// quantity
// category-select
// main-proce
// discount
// discount-type
// thumbnail-input
// meta-title
// meta-keywords
// meta-descriptions
// description
// additional-info
// shipping-info


var forms = document.querySelectorAll('.needs-validation')

// Loop over them and prevent submission
Array.prototype.slice.call(forms)
  .forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')

      // select invalid input section
      // if ($("#add-product-name").not("#").val().length === 0 || $("#add-short-desc").val().length === 0 || $("#add-quantity").val().length === 0) {
      //   $("[for=add-general]").click();
      //   if (!($(".basic").hasClass("selected"))) {
      //     $(".basic").addClass("selected");
      //     $(".advance").removeClass("selected");
      //   }
      // }
      // else if ($("#add-category-select").val().length === 0) {
      //   $("[for=add-category]").click();
      //   if (!($(".basic").hasClass("selected"))) {
      //     $(".basic").addClass("selected");
      //     $(".advance").removeClass("selected");
      //   }
      // }
      // else if ($("#add-main-price").val().length === 0) {
      //   $("[for=add-price]").click();
      //   if (!($(".basic").hasClass("selected"))) {
      //     $(".basic").addClass("selected");
      //     $(".advance").removeClass("selected");
      //   }
      // }
      // else if ($("#add-thumbnail-input").val().length === 0) {
      //   $("[for=add-images]").click();
      //   if (!($(".basic").hasClass("selected"))) {
      //     $(".basic").addClass("selected");
      //     $(".advance").removeClass("selected");
      //   }
      // }
      // else if ($("#add-meta-title").val().length === 0 || $("#add-meta-keywords").val().length === 0 || $("#add-meta-descriptions").val().length === 0) {
      //   $("[for=add-seo]").click();
      //   if (!($(".basic").hasClass("selected"))) {
      //     $(".basic").addClass("selected");
      //     $(".advance").removeClass("selected");
      //   }
      // }
      // else if ($("#add-description").val().length === 0) {
      //   $("[for=add-additional]").click();
      //   if (!($(".advance").hasClass("selected"))) {
      //     $(".basic").removeClass("selected");
      //     $(".advance").addClass("selected");
      //   }
      // }
    }, false)
  })


// $("#filer_input1").on("change", function(){
//   var len = $(this)[0].jFiler.files_list.length;
//   // console.log($(this)[0].jFiler);
//   // console.log($(this)[0].jFiler.files_list[0]);
//   for (i = 0; i <= len+1; i++) {
//     console.log($(this)[0].jFiler.files_list[i]);
//   }
// })

$("#filer_input1").on("change", function () {
  console.log($(this)[0].jFiler.current_file)
})


//! related product table

var rel_pro = new Array()
var related_product_input = $("input[name=related-products]");

$('#related-product-table').on('change', function () {
  if ($('#related-product-table').bootstrapTable('getSelections').length === 0) {
    rel_pro = new Array();
    related_product_input.val(rel_pro);
  }
  else {
    rel_pro = new Array();
    $('#related-product-table').bootstrapTable('getSelections').forEach((element) => {
      // console.log(element[2]);
      rel_pro.push(element[2]);
      related_product_input.val(rel_pro);
    });
  }

})



// menu page
$(".add-menu-btn").click(function () {
  $(".menu-item.selected").removeClass("selected")
  $("#menu-name").val("")
  document.getElementById("menu-style").setValue("dropdown")
  document.getElementById("menu-icon-select").reset()
  document.getElementById("menu-category").reset()
  document.getElementById("menu-group").reset()
  document.getElementById("menu-subcategory").reset()
  $("#menu-enable").attr("checked", true)
  $("#save-btn").text("Add Menu")
  $(".form-title").text("Add New Menu")
  $("#id").val('')
})
$(".menu-item").click(function () {
  $(".menu-item.selected").removeClass("selected")
  if (!$(this).hasClass("selecded")) {
    $(this).addClass("selected")
  }
  $("#menu-name").val($(this).attr("name"))
  document.getElementById("menu-style").setValue($(this).attr("style"))
  document.getElementById("menu-icon-select").setValue($(this).attr("icon"))
  document.getElementById("menu-category").setValue($(this).attr("category").split(","))
  if ($(this).attr("group").length > 0) {
    document.getElementById("menu-group").setValue($(this).attr("group").split(","))
  }
  else {
    document.getElementById("menu-group").reset()
  }
  if ($(this).attr("subcat").length > 0) {
    document.getElementById("menu-subcategory").setValue($(this).attr("subcat").split(","))
  }
  else {
    document.getElementById("menu-subcategory").reset()
  }
  if ($(this).attr("status") == 'True') {
    $("#menu-enable").attr("checked", true)
  }
  else {
    $("#menu-enable").attr("checked", false)
  }
  $("#save-btn").text("Save")
  $(".form-title").text($(this).attr("name"))
  $("#id").val($(this).attr("id"))
})

$(".delete-menus").on("click", function () {
  document.getElementById("overlay").style.display = "block";
  var action = 'delete'
  $.ajax({
    url: "/control/menu/update",
    type: "POST",
    data: { menu_id: $(this).parent().children(".menu-item").attr("id"), action: action },
    success: function (result) {
      document.getElementById("overlay").style.display = "none";
      if ($("div[id=" + result.id + "]").parent().children(".menu-item").hasClass("selected")) {
        $("div[id=" + result.id + "]").parent().remove()
        $("#edit-menu-form").trigger("reset")
        document.getElementById("menu-style").setValue("dropdown")
      }
      else {
        $("div[id=" + result.id + "]").parent().remove()
      }
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
})


//! brand section

var $brandtable = $('#brand-table')
var selections = []

$brandtable.on('check.bs.table uncheck.bs.table ' +
  'check-all.bs.table uncheck-all.bs.table',
  function () {
    $remove.prop('disabled', !$brandtable.bootstrapTable('getSelections').length)
    selections = getBrandIdSelections()
  })

$(".brand-remove").click(function () {
  $remove.prop('disabled', true)
})

function getBrandIdSelections() {
  return $.map($brandtable.bootstrapTable('getSelections'), function (row) {
    return row[1]
  })
}

$(".brand-remove").click(function () {
  var ids = getBrandIdSelections()
  var brands = new Array();
  for (i = 0; i <= ids.length - 1; i++) {
    brands.push(ids[i]);
  }
  $("#selected-brand").val(brands);
  deleteBrand();
})


function deleteBrand() {
  console.log($("#selected-brand").val())
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    url: "/control/brand/delete",
    type: "POST",
    data: { brands: $("#selected-brand").val() },
    success: function (result) {
      $remove.prop('disabled', true);
      $('#brand-table tr.selected').remove();
      if (parseInt(result.total) === 1) {
        total = '1 brand';
      }
      else {
        total = `${result.total} brands`;
      }
      document.getElementById("overlay").style.display = "none";
      new PNotify({
        title: 'Successfully deleted',
        type: 'success',
        text: `${total} deleted successfully. You can now add brand.`,
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
};



//! page section

var $pagetable = $('#page-table')
var selections = []

$pagetable.on('check.bs.table uncheck.bs.table ' +
  'check-all.bs.table uncheck-all.bs.table',
  function () {
    $remove.prop('disabled', !$pagetable.bootstrapTable('getSelections').length)
    selections = getPageIdSelections()
  })

$(".page-remove").click(function () {
  $remove.prop('disabled', true)
})

function getPageIdSelections() {
  return $.map($pagetable.bootstrapTable('getSelections'), function (row) {
    return row[1]
  })
}

$(".page-remove").click(function () {
  var ids = getPageIdSelections()
  var pages = new Array();
  for (i = 0; i <= ids.length - 1; i++) {
    pages.push(ids[i]);
  }
  $("#selected-page").val(pages);
  deletePage();
})


function deletePage() {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    url: "/control/page/delete-page",
    type: "POST",
    data: { pages: $("#selected-page").val() },
    success: function (result) {
      $remove.prop('disabled', true);
      $('#page-table tr.selected').remove();
      if (parseInt(result.total) === 1) {
        total = '1 page';
      }
      else {
        total = `${result.total} pages`;
      }
      document.getElementById("overlay").style.display = "none";
      new PNotify({
        title: 'Successfully deleted',
        type: 'success',
        text: `${total} deleted successfully. You can now add page.`,
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
};



//! coupon section

var $coupontable = $('#coupon-table')

$coupontable.on('check.bs.table uncheck.bs.table ' +
  'check-all.bs.table uncheck-all.bs.table',
  function () {
    $remove.prop('disabled', !$coupontable.bootstrapTable('getSelections').length)
    selections = getCouponIdSelections()
  }
)

function getCouponIdSelections() {
  return $.map($coupontable.bootstrapTable('getSelections'), function (row) {
    return row[1]
  })
}

$(".coupon-remove").click(function () {
  var ids = getCouponIdSelections()
  var coupons = new Array();
  for (i = 0; i <= ids.length - 1; i++) {
    coupons.push(ids[i]);
  }
  $("#selected-coupon").val(coupons);
  deleteCoupon();
})


function deleteCoupon() {
  document.getElementById("overlay").style.display = "block";
  $.ajax({
    url: "/control/coupon/delete-coupon",
    type: "POST",
    data: { coupons: $("#selected-coupon").val() },
    success: function (result) {
      $remove.prop('disabled', true);
      $('#coupon-table tr.selected').remove();
      if (parseInt(result.total) === 1) {
        total = '1 coupon';
      }
      else {
        total = `${result.total} coupons`;
      }
      document.getElementById("overlay").style.display = "none";
      new PNotify({
        title: 'Successfully deleted',
        type: 'success',
        text: `${total} deleted successfully. You can now add coupon.`,
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    error: function (e) {
      console.error(JSON.stringify(e));
    },
  });
};


//! setting file

// social login

$("#facebook-enable").on("click", function () {
  if ($(this).is(":checked")) {
    $(".facebook-login-field").removeClass("d-none")
    $("#facebook-app-id").attr("required", true)
    $("#facebook-app-secret").attr("required", true)
  }
  else {
    $(".facebook-login-field").addClass("d-none")
    $("#facebook-app-id").removeAttr("required")
    $("#facebook-app-secret").removeAttr("required")
  }
})

$("#google-enable").on("click", function () {
  if ($(this).is(":checked")) {
    $(".google-login-field").removeClass("d-none")
    $("#google-app-id").attr("required", true)
    $("#google-app-secret").attr("required", true)
  }
  else {
    $(".google-login-field").addClass("d-none")
    $("#google-app-id").removeAttr("required")
    $("#google-app-secret").removeAttr("required")
  }
})

$("#free-shipping-enable").on("click", function () {
  if ($(this).is(":checked")) {
    $(".free-shipping-label-field").removeClass("d-none")
    $(".free-shipping-amount-field").removeClass("d-none")
    $("#free-shipping-label").attr("required", true)
    $("#free-shipping-amount").attr("required", true)
  }
  else {
    $(".free-shipping-label-field").addClass("d-none")
    $(".free-shipping-amount-field").addClass("d-none")
    $("#free-shipping-label").removeAttr("required")
    $("#free-shipping-amount").removeAttr("required")
  }
})

$("#local-shipping-enable").on("click", function () {
  if ($(this).is(":checked")) {
    $(".local-shipping-label-field").removeClass("d-none")
    $(".local-shipping-amount-field").removeClass("d-none")
    $("#local-shipping-label").attr("required", true)
    $("#local-shipping-amount").attr("required", true)
  }
  else {
    $(".local-shipping-label-field").addClass("d-none")
    $(".local-shipping-amount-field").addClass("d-none")
    $("#local-shipping-label").removeAttr("required")
    $("#local-shipping-amount").removeAttr("required")
  }
})

//* ----------------payment method-------------
// paypal field

$("#paypal-enable").on("click", function () {
  if ($(this).is(":checked")) {
    $(".paypal-field").removeClass("d-none")
    $("#paypal-client-id").attr("required", true)
    $("#paypal-secret").attr("required", true)
  }
  else {
    $(".paypal-field").addClass("d-none")
    $("#paypal-client-id").removeAttr("required")
    $("#paypal-secret").removeAttr("required")
  }
})


// all countries

// countrys = [];
// for (const country in countries) {
//   countrys.push({ label: countries[country].name, value: countries[country].name });
// }
// VirtualSelect.init({
//   ele: "#country-select",
//   options: countrys,
//   search: true,
// });

$("#country-select").on("click", function () {
  $("#country-select").on("change", function () {
    select = []
    selected = $("#country-select").val();
    for (var name in selected) {
      select.push({ label: selected[name], value: selected[name] });
    }
    VirtualSelect.init({
      ele: "#default-country-select",
      options: select,
      search: true,
    });
  })
})



$("#add-staff").click(function () {
  if ($(this).is(":checked")) {
    $("#add-role").removeClass("d-none")
  }
  else {
    $("#add-role").addClass("d-none")
  }
})

$("#edit-staff").click(function () {
  if ($(this).is(":checked")) {
    $("#edit-role").removeClass("d-none")
  }
  else {
    $("#edit-role").addClass("d-none")
  }
})


// location tree customize

$("#basicTree").on("changed.jstree", function (e, data) {
  var getdata = JSON.parse(data.instance.get_node(data.selected).li_attr.data);
  if (getdata.type === "add-country") {
    $("#location-form .form-title").text("Add Country")
    $("#location-form #type").val("add-country")
    $(".location-delete").addClass("disabled")
  }
  else if (getdata.type === "add-region") {
    $("#location-form .form-title").text("Add Region")
    $("#location-form #type").val("add-region")
    $("#location-form #id").val(getdata.country_id)
    $(".location-delete").addClass("disabled")
  }
  else if (getdata.type === "add-city") {
    $("#location-form .form-title").text("Add City")
    $("#location-form #type").val("add-city")
    $("#location-form #id").val(getdata.region_id)
    $(".location-delete").addClass("disabled")
  }
  else if (getdata.type === "add-area") {
    $("#location-form .form-title").text("Add Area")
    $("#location-form #type").val("add-area")
    $("#location-form #id").val(getdata.city_id)
    $(".location-delete").addClass("disabled")
  }
  else if (getdata.type === "country") {
    $("#location-form .form-title").text(getdata.name)
    $("#location-form #name").val(getdata.name)
    $("#location-form #id").val(getdata.id)
    $("#location-form #type").val("edit-country")
    $(".location-delete").removeClass("disabled")
    if (getdata.enable == 'True') {
      $("#enable").attr("checked", true)
    }
    else {
      $("#enable").attr("checked", false)
    }
  }
  else if (getdata.type === "region") {
    $("#location-form .form-title").text(getdata.name)
    $("#location-form #name").val(getdata.name)
    $("#location-form #id").val(getdata.id)
    $("#location-form #type").val("edit-region")
    $(".location-delete").removeClass("disabled")
    if (getdata.enable == 'True') {
      $("#enable").attr("checked", true)
    }
    else {
      $("#enable").attr("checked", false)
    }
  }
  else if (getdata.type === "city") {
    $("#location-form .form-title").text(getdata.name)
    $("#location-form #name").val(getdata.name)
    $("#location-form #id").val(getdata.id)
    $("#location-form #type").val("edit-city")
    $(".location-delete").removeClass("disabled")
    if (getdata.enable == 'True') {
      $("#enable").attr("checked", true)
    }
    else {
      $("#enable").attr("checked", false)
    }
  }
  else if (getdata.type === "area") {
    $("#location-form .form-title").text(getdata.name)
    $("#location-form #name").val(getdata.name)
    $("#location-form #id").val(getdata.id)
    $("#location-form #type").val("edit-area")
    $(".location-delete").removeClass("disabled")
    if (getdata.enable == 'True') {
      $("#enable").attr("checked", true)
    }
    else {
      $("#enable").attr("checked", false)
    }
  }
})

$(".location-delete").click(function () {
  document.getElementById("overlay").style.display = "block";
  var selected_node = $("#basicTree").jstree("get_selected");
  var arr = []
  selected_node.forEach(element => {
    var getdata = JSON.parse($("#basicTree").jstree("get_node", element).li_attr.data);
    var info = [getdata.type, getdata.id]
    arr.push(info)
  });
  console.log(arr)
  $.ajax({
    url: '/control/area/delete',
    type: 'POST',
    dataType: "json",
    data: {
      info: JSON.stringify({ data: arr })
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    success: function (resp) {
      document.getElementById("overlay").style.display = "none";
      selected_node.forEach(element => {
        $("#basicTree #" + element).remove()
      });
      new PNotify({
        title: 'Successfully deleted',
        type: 'success',
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
    },
    error: function (resp) {
      console.log(resp)
      document.getElementById("overlay").style.display = "none";
      selected_node.forEach(element => {
        $("#basicTree #" + element).remove()
      });
    }
  })
})