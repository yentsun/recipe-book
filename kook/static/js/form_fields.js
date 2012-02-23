$(function() {
    create_ckeditor($('#steptext_1, #description'));
});

function create_ckeditor(element) {
    element.ckeditor({
        height: '100px',
        toolbar_Full: [
            {name: 'basicstyles', items: ['Bold','Italic',
                                          'Underline','Strike']},
//            {name: 'clipboard', items: ['Cut','Copy','Paste','PasteText',
//                'PasteFromWord','-','Undo','Redo']},
            {name: 'paragraph', items: ['NumberedList','BulletedList']},
            {name: 'links', items: ['Link', 'Unlink']},
            {name: 'misc', items: ['Source']}]});
}