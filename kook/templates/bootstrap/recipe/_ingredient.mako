# -*- coding: utf-8 -*-
<%page args="ingredient"/>
<%! from kook.mako_filters import failsafe_get as get %>
<tr class="product_amount removable">
    <td class="product_title">
        <input type="text" name="product_title" class="span4"
               value="${get(ingredient, 'product_title')}"
               data-provide="typeahead">
    </td>
    <td class="amount">
        <div class="input-append">
            <input type="text" name="measured_amount" style="width:30px"
                   value="${get(ingredient, 'measured') or \
                            get(ingredient, 'amount')}"
                   onkeyup="set_amount(this)"
                   data-multiplier="${get(ingredient, 'apu') or 1}">
            <input type="hidden" name="amount"
                   value="${get(ingredient, 'amount') or 0}">
            <input type="hidden" name="unit_title"
                   value="${get(ingredient, 'unit_title') or ''}">
            <span class="dropdown">
                <a href="#" class="btn dropdown-toggle add-on"
                   data-toggle="dropdown">
                    <span class="chosen_unit_abbr">
                        ${get(ingredient, 'unit.abbr') or u'г'}
                    </span><b class="caret"></b></a>
                <ul class="dropdown-menu">
                    <li><a onclick="set_measure(this, '', 'г', 1)"
                           data-estimated_amount="${get(ingredient, 'amount')}">
                        грамм</a>
                    </li>
                    <span class="alt_measures">
                    <% APUs = get(ingredient, 'product.APUs') or [] %>
                    % if len(APUs) > 0:
                    <li class="divider"></li>
                    % for apu in APUs:
                    <li><a onclick="set_measure(this, '${apu.unit.title}',
                                                '${apu.unit.abbr}',
                                                ${apu.amount})"
                           data-estimated_amount="${apu.measure(
                                ingredient.amount)}">
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