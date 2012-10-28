# -*- coding: utf-8 -*-
<%page args="product_title, amount, measured_amount=None, unit_title='',
             unit_abbr=u'г', apu=1, APUs=[]"/>
<tr class="product_amount removable">
    <td class="product_title">
        <input type="text" name="product_title" class="span4"
               value="${product_title}" data-provide="typeahead">
    </td>
    <td class="amount">
        <div class="input-append">
            <input type="text" name="measured_amount" style="width:30px"
                   value="${measured_amount or amount}"
                   onkeyup="set_amount(this)"
                   data-multiplier="${apu}">
            <input type="hidden" name="amount" value="${amount}">
            <input type="hidden" name="unit_title" value="${unit_title}">
            <span class="dropdown">
                <a href="#" class="btn dropdown-toggle add-on"
                   data-toggle="dropdown">
                    <span class="chosen_unit_abbr">
                        ${unit_abbr}
                    </span><b class="caret"></b></a>
                <ul class="dropdown-menu">
                    <li><a onclick="set_measure(this, '', 'г', 1)"
                           data-estimated_amount="${amount}">
                        грамм</a>
                    </li>
                    <span class="alt_measures">
                    % if len(APUs) > 0:
                    <li class="divider"></li>
                    % for apu in APUs:
                    <li><a onclick="set_measure(this, '${apu.unit.title}',
                                                      '${apu.unit.abbr}',
                                                       ${apu.amount})"
                           data-estimated_amount="${apu.measure(amount)}">
                        ${apu.unit.title}
                    </a></li>
                    % endfor
                    % endif
                    </span>
                    <li class="divider"></li>
                    <li><a onclick="alert('!!!')">
                        добавить меру
                    </a></li>
                </ul>
            </span>
        </div>
    </td>
    <td><a class="close remove">&times;</a></td>
</tr>