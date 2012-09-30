<%page args="apu"/>
<%!
    from kook.mako_filters import failsafe_get as get
%>
<tr class="apu removable">
    <td>
        <input type="text" name="unit_title" class="span4 unit_title"
               value="${get(apu, 'unit_title') or\
               apu.unit.title}"
               data-provide="typeahead">
    </td>
    <td class="amount">
        <div class="input-append">
            <input type="text" name="amount" class="amount"
                   value="${get(apu, 'amount')}">
            <span class="add-on" style="margin-left:-5px;">г</span>
        </div>
    </td>
    <td><a class="close remove">&times;</a></td>
</tr>