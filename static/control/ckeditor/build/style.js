
// ClassicEditor.create(document.querySelector("#short-desc"));
ClassicEditor.create(document.querySelector("#description"), {
    removePlugins: ['Title']
});
ClassicEditor.create(document.querySelector("#additional-info"), {
    removePlugins: ['Title']
});
ClassicEditor.create(document.querySelector("#shipping-info"), {
    removePlugins: ['Title']
});
// ClassicEditor.create(document.querySelector("#add-short-desc"));
ClassicEditor.create(document.querySelector("#add-description"), {
    removePlugins: ['Title']
});
ClassicEditor.create(document.querySelector("#add-additional-info"), {
    removePlugins: ['Title']
});
ClassicEditor.create(document.querySelector("#add-shipping-info"), {
    removePlugins: ['Title']
});

ClassicEditor.create(document.querySelector("#body"), {
    removePlugins: ['Title']
});
