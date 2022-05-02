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

var Drop = Dropzone.options.DidDropzone = {
  url: '/control/product/imagesave',
  autoProcessQueue: false,
  paramName: "images",
  uploadMultiple: false,
  maxFilesize: 20,
  clickable: true,
  acceptedFiles: '.jpg,.jpeg,.JPEG,.JPG,.png,.PNG',
  parallelUploads: 100,
  maxFiles: 100,
  addRemoveLinks: true,
  timeout: 15000,
  headers: {
    "X-CSRFToken": getCookie("csrftoken")
  },
  previewTemplate: '<div class="dz-preview dz-image-preview">' +
    '<div class="dz-image">' +
    '<img data-dz-thumbnail />' +
    '</div>' +

    '<div class="dz-details">' +
    '<div class="dz-filename"><span data-dz-name></span></div>' +
    '<div class="dz-size" data-dz-size></div>' +
    '</div>' +

    '<div class="dz-success-mark"><span>✔</span></div>' +
    '<div class="dz-error-mark"><span>✘</span></div>' +
    '<div class="dz-error-message"><span data-dz-errormessage></span></div>' +
    '</div>',
  init: function () {
    myDropzone = this;
    unq = $("#unique").val();
    $("#add-category-form").on("submit", function () {
      if (document.getElementById("add-category-form").checkValidity()) {
        myDropzone.processQueue();
      }
    });
    myDropzone.on('sending', function (data, xhr, formData) {
      formData.append('unique', $("#edit-unique").val());
    })
    myDropzone.on("complete", function (file) {
      myDropzone.removeFile(file);
    });
  },
  success: function (file, json) {
  },
}