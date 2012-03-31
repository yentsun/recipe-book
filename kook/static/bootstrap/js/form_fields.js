$(function() {
    create_ckeditor($('.step textarea, #description'));
});

function create_ckeditor(element) {
    element.ckeditor({
        disableNativeSpellChecker: false,
        height: '100px',
        removePlugins: 'elementspath',
        resize_enabled: false,
        toolbar_Full: [
            {name: 'basicstyles', items: ['Bold','Italic',
                                          'Underline','Strike']},
//            {name: 'clipboard', items: ['Cut','Copy','Paste','PasteText',
//                'PasteFromWord','-','Undo','Redo']},
            {name: 'paragraph', items: ['NumberedList','BulletedList']},
            {name: 'links', items: ['Link', 'Unlink']},
            {name: 'misc', items: ['Source']}]});
}