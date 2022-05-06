// function uuidv4() {
//   return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
//     var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
//     return v.toString(16);
//   });
// }
// unique = uuidv4()
// document.cookie = 'unique=' + Date.now() + unique + ";domain=;path=/"


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

// $("#unique").val(getCookie('unique'))

var Drop = Dropzone.options.DidDropzone = {
  url: '/control/product/imagesave',
  autoProcessQueue: true,
  paramName: "images",
  uploadMultiple: true,
  maxFilesize: 200,
  clickable: true,
  acceptedFiles: '.jpg,.jpeg,.JPEG,.JPG,.png,.PNG',
  parallelUploads: 100,
  maxFiles: 100,
  addRemoveLinks: true,
  headers: {
    "X-CSRFToken": getCookie("csrftoken")
  },
  // previewTemplate: '<div class="dz-preview dz-image-preview">' +
  //   '<div class="dz-image">' +
  //   '<img data-dz-thumbnail />' +
  //   '</div>' +

  //   '<div class="dz-details">' +
  //   '<div class="dz-filename"><span data-dz-name></span></div>' +
  //   '<div class="dz-size" data-dz-size></div>' +
  //   '</div>' +

  //   '<div class="dz-success-mark"><span>✔</span></div>' +
  //   '<div class="dz-error-mark"><span>✘</span></div>' +
  //   '<div class="dz-error-message"><span data-dz-errormessage></span></div>' +
  //   '</div>',
  init: function () {
    myDropzone = this;
    myDropzone.on('sending', function (data, xhr, formData) {
      formData.append('unique', $("#unique").val());
    });
    myDropzone.on('successmultiple', function (file, resp) {
      var elem = $(".dz-remove")
      console.log(elem.length, resp.ids.length)
      for (i = elem.length - resp.ids.length; i < elem.length; i++) {
        $(elem[i]).html(`<i class="fas fa-trash" id="trash" img_id="${resp.ids[i - (elem.length - resp.ids.length)]}"></i>`);
        document.querySelectorAll("#trash").forEach((element) => {
          $(element).click(function () {
            $.ajax({
              url: '/control/product/deleteimage',
              type: 'POST',
              data: { id: $(element).attr('img_id') },
              success: function (resp) {
                $('i[img_id = "' + resp.id + '"]').parent().parent().remove()
              },
              headers: {
                "X-CSRFToken": getCookie("csrftoken")
              },
            })
          })
        })
      }
      // for (i = 0; i < resp.ids.length; i++) {
      //   var prev = `<div class="additional-image-thumbnail" id="image${resp.ids[i]}">
      //     <i class="fas fa-trash" id="trash" img-id="${resp.ids[i]}"></i>
      //     <img class="thumbnail no-border" src="${resp.urls[i]}" style="height: 150px; width: auto;">
      //   </div>`
      //   $("#preview-images").append(prev)
      //   document.querySelectorAll("#trash").forEach((element) => {
      //     $(element).click(function () {
      //       $.ajax({
      //         url: '/control/product/deleteimage',
      //         type: 'POST',
      //         data: { id: $(element).attr('img-id') },
      //         success: function (resp) {
      //           $("#image" + resp.id).remove()
      //         },
      //         headers: {
      //           "X-CSRFToken": getCookie("csrftoken")
      //         },
      //       })
      //     })
      //   })
      // }
    });
  },
  success: function (file, json) {
  },
}


var editDrop = Dropzone.options.editDropzone = {
  url: '/control/product/imagesave',
  autoProcessQueue: true,
  paramName: "images",
  uploadMultiple: true,
  maxFilesize: 200,
  clickable: true,
  acceptedFiles: '.jpg,.jpeg,.JPEG,.JPG,.png,.PNG',
  parallelUploads: 100,
  maxFiles: 100,
  addRemoveLinks: true,
  headers: {
    "X-CSRFToken": getCookie("csrftoken")
  },

  init: function () {
    myDropzone = this;
    myDropzone.on('sending', function (data, xhr, formData) {
      formData.append('unique', $("#edit-unique").val());
    });
    myDropzone.on('successmultiple', function (file, resp) {
      var elem = $(".dz-remove")
      console.log(elem.length, resp.ids.length)
      for (i = elem.length - resp.ids.length; i < elem.length; i++) {
        $(elem[i]).html(`<i class="fas fa-trash" id="trash" img_id="${resp.ids[i - (elem.length - resp.ids.length)]}"></i>`);
        document.querySelectorAll("#trash").forEach((element) => {
          $(element).click(function () {
            $.ajax({
              url: '/control/product/deleteimage',
              type: 'POST',
              data: { id: $(element).attr('img_id') },
              success: function (resp) {
                $('i[img_id = "' + resp.id + '"]').parent().parent().remove()
              },
              headers: {
                "X-CSRFToken": getCookie("csrftoken")
              },
            })
          })
        })
      }
    });
  },
  success: function (file, json) {
  },
}