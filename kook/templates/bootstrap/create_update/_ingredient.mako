<%page args="no, ingredient"/>
<tr class="product_amount removable">
    <td class="product_title">
        <input id="product${no}" type="text" name="product_title" class="span4"
               data-id="${no}" value="${ingredient.product.title}"
               data-provide="typeahead">
    </td>
    <td class="amount">
        <div class="input-append">
            <input id="measured_amount${no}" type="text" name="measured_amount" style="width:30px"
                   value="${ingredient.measured}" onkeyup="set_amount(this)"
                   data-multiplier="${ingredient.apu}">
            <input id="amount${no}" type="hidden" name="amount" value="${ingredient.amount}">
            <input id="unit_title${no}" type="hidden" name="unit_title"
                   value="${ingredient.string_unit_title()}">
            <span class="dropdown">
                <a href="#" class="btn dropdown-toggle add-on" data-toggle="dropdown">
                    <span class="chosen_unit_abbr">
                        % if ingredient.unit is not None:
                        ${ingredient.unit.abbr}
                        %else:
                        г
                        % endif
                    </span><b class="caret"></b></a>
                <ul class="dropdown-menu">
                    <li><a onclick="set_measure(this, '', 'г', 1)"
                           data-estimated_amount="${ingredient.amount}">
                        грамм</a></li>
                    <span class="alt_measures">
                    % if len(ingredient.product.APUs) > 0:
                    <li class="divider"></li>
                    % for apu in ingredient.product.APUs:
                    <li><a onclick="set_measure(this, '${apu.unit.title}',
                                                '${apu.unit.abbr}', ${apu.amount})"
                           data-estimated_amount="${apu.measure(ingredient.amount)}">
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