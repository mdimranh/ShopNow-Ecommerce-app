/**
 * Theme: Uplon Admin Template
 * Author: Coderthemes
 * Tree view
 */

$(document).ready(function () {
    // Basic
    $('#basicTree').jstree({
        'core': {
            'themes': {
                'responsive': false,
                'animation': 300
            }
        },
        'types': {
            'default': {
                'icon': ''
            },
            'file': {
                'icon': 'icofont icofont-file-alt'
            }
        },
        'plugins': ['types', "search"]
    });
    var to = false
    $("#treeSearch").keyup(function () {
        if (to) { clearTimeout(to); }
        to = setTimeout(function () {
            var v = $("#treeSearch").val();
            $("#basicTree").jstree(true).search(v);
        }, 250)
    })

    // Checkbox
    $('#checkTree').jstree({
        'core': {
            'themes': {
                'responsive': false
            }
        },
        'types': {
            'default': {
                'icon': 'icofont icofont-folder'
            },
            'file': {
                'icon': 'icofont icofont-file-alt'
            }
        },
        'plugins': ['types', 'checkbox']
    });

    // Drag & Drop
    $('#dragTree').jstree({
        'core': {
            'check_callback': true,
            'themes': {
                'responsive': false
            }
        },
        'types': {
            'default': {
                'icon': 'icofont icofont-folder'
            },
            'file': {
                'icon': 'icofont icofont-file-alt'
            }
        },
        'plugins': ['types', 'dnd']
    });

    // Ajax
    $('#ajaxTree').jstree({
        'core': {
            'check_callback': true,
            'themes': {
                'responsive': false
            },
            'data': {
                'url': function (node) {
                    return node.id === '#' ? 'assets/plugins/jstree/ajax_roots.json' : 'assets/plugins/jstree/ajax_children.json';
                },
                'data': function (node) {
                    return { 'id': node.id };
                }
            }
        },
        "types": {
            'default': {
                'icon': 'icofont icofont-folder'
            },
            'file': {
                'icon': 'icofont icofont-file-alt'
            }
        },
        "plugins": ["contextmenu", "dnd", "search", "state", "types", "wholerow"]
    });
});