$(function() {
    $('.unit_title').attr('autocomplete', 'off').typeahead({source:units});
});

function clone_apu() {
    var container = $('#APUs').find('tbody');
    var original = container.find('.apu:last');
    var duplicate;
    if (original.length) {
        duplicate = original.clone();
        duplicate.find('input').val('').css('background', '#fff');
    } else {
        duplicate = $('<tr class="apu removable"><td>' +
            '<input type="text" name="unit_title" class="span4 unit_title" ' +
            'value="" data-provide="typeahead" autocomplete="off"></td>' +
            '<td class="amount"><div class="input-append"><input type="text" ' +
            'name="amount" class="amount" value="">' +
            '<span class="add-on" style="margin-left:-5px;">г</span></div></td>' +
            '<td><a class="close remove">×</a></td></tr>');
    }
    duplicate.appendTo(container);
    var unit_title_input = duplicate.find('[name=unit_title]');
    unit_title_input.typeahead({source:units});
    unit_title_input.attr('autocomplete', 'off').focus();
}