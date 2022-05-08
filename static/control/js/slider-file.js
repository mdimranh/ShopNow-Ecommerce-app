var wrapper_len = $(".wrapper").children().length
$("#wrapper_len").val(wrapper_len)

var wrap_len = $(".wrapper").children().length
for (i = 1; i <= wrap_len; i++) {
  $("#add-thumbnail-input-" + i).change(function (event) {
    var id = "#" + $(this).attr("for")
    $(id).attr("src", URL.createObjectURL(event.target.files[0]));
  })
}

$(".add-new-slide-btn").click(function () {
  wrapper_len = parseInt($("#wrapper_len").val()) + 1
  $("#wrapper_len").val(wrapper_len)
  $(".wrapper").append(slide(wrapper_len))
  $(".fa-times").click(function () {
    $(this).parent().parent().remove()
  })
  $("#new-add-thumbnail-input-" + wrapper_len).change(function (event) {
    var id = "#" + $(this).attr("for")
    $(id).attr("src", URL.createObjectURL(event.target.files[0]));
  })
})

function slide(num) {
  var slide = `<div class="d-flex flex-column mb-4">
    <div class="d-flex flex-fill mt-2 mb-4 justify-content-between"><h6><i class="fas fa-th-list me-3 drag-icon handle"></i>Image Slide</h6><i class="fas fa-times fa-lg"></i></div>
        <div class="d-flex flex-column flex-xl-row align-items-center align-items-xl-start">
            <div class="me-4">
                <label class="slide-thumbnail d-flex flex-fill justify-content-center" for="new-add-thumbnail-input-${num}">
                    <img
                    class="thumbnail border-1"
                    id="new-add-thumbnail-${num}"
                    src="/static/control/css/image.png"
                    />
                </label>
                <input
                    class="d-none"
                    type="file"
                    accept="image/*"
                    id="new-add-thumbnail-input-${num}"
                    for = "new-add-thumbnail-${num}"
                    name="thumbnail"
                    required
                />
            </div>
            <input type="hidden" name="id" value="new">
            <div class="w-100">
                <nav>
                    <div class="nav nav-pills" id="nav-tab" role="tablist">
                        <button class="nav-link active" id="nav-${num}-home-tab" data-bs-toggle="tab" data-bs-target="#nav-${num}-home" type="button" role="tab" aria-controls="nav-${num}-home" aria-selected="true">General</button>
                        <button class="nav-link" id="nav-${num}-profile-tab" data-bs-toggle="tab" data-bs-target="#nav-${num}-profile" type="button" role="tab" aria-controls="nav-${num}-profile" aria-selected="false">Options</button>
                    </div>
                </nav>
                <div class="tab-content mt-3" id="nav-tabContent">
                    <div class="tab-pane fade show active" id="nav-${num}-home" role="tabpanel" aria-labelledby="nav-${num}-home-tab">
                      <div class="container-fluid px-0">
                        <div class="row">
                          <div class="col-xxl-4 col-xl-6 col-12 mb-2">
                            <label class="my-1" for="caption1">Caption 1</label>
                            <input class="form-control" type="text" id="caption1" name="caption1">
                          </div>
                          <div class="col-xxl-4 col-xl-6 col-12 mb-2">
                            <label class="my-1" for="caption1">Caption 2</label>
                            <input class="form-control" type="text" id="caption2" name="caption2">
                          </div>
                          <div class="col-xxl-4 col-xl-6 col-12 mb-2">
                            <label class="my-1" for="caption1">Caption 3</label>
                            <input class="form-control" type="text" id="caption3" name="caption3">
                          </div>
                          <div class="col-xxl-4 col-xl-6 col-12 mb-2">
                            <label class="my-1" for="caltotext">Call To Action Text</label>
                            <input class="form-control" type="text" id="caltotext" name="calltotext">
                          </div>
                          <div class="col-xxl-4 col-xl-6 col-12 mb-2">
                            <label class="my-1" for="caltourl">Call To Action URL</label>
                            <input class="form-control" type="text" id="caltourl" name="calltourl">
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="tab-pane fade" id="nav-${num}-profile" role="tabpanel" aria-labelledby="nav-${num}-profile-tab">
                      <div class="container-fluid px-0">
                        <div class="row">
                          <div class="col-12 mb-2 mt-3">
                            <div class="checkbox-fade fade-in-primary">
                              <label>
                                <input id="enable" type="checkbox" name="open"/>
                                <span class="cr">
                                  <i
                                    class="
                                      cr-icon
                                      icofont icofont-ui-check
                                      txt-primary
                                    "
                                  ></i>
                                </span>
                                <span>Open in New Window</span>
                              </label>
                            </div>
                          </div>
                          <div class="col-12 mb-2">
                            <div class="checkbox-fade fade-in-primary">
                              <label>
                                <input id="enable" type="checkbox" name="enable" checked  />
                                <span class="cr">
                                  <i
                                    class="
                                      cr-icon
                                      icofont icofont-ui-check
                                      txt-primary
                                    "
                                  ></i>
                                </span>
                                <span>Enable this slide</span>
                              </label>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`
  return slide
}

$(".fa-times").click(function () {
  $(this).parent().parent().remove()
})


var form = document.getElementById("edit-slide-form")
form.addEventListener('submit', function (event) {
  var inp = $("input[type=file]")
  event.preventDefault()
  event.stopPropagation()
  var ar = []
  for (i = 0; i < inp.length; i++) {
    if (inp[i].files.length != 0) {
      ar.push(i)
    }
  }
  $("#pos").val(ar)
  form.submit()
})