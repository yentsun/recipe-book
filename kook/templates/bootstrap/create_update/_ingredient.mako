<%page args="ingredient"/>
<%
if ingredient is None:
    product_title = ''
    measured = ''
    apu = 1
    amount = ''
    unit_title = ''
    unit_abbr = None
    APUs = []
else:
    product_title = ingredient.product.title
    measured = ingredient.measured
    apu = ingredient.apu
    amount = ingredient.amount
    unit_title = ingredient.string_unit_title()
    if ingredient.unit is None:
        unit_abbr = None
    else:
        unit_abbr = ingredient.unit.abbr
    APUs = ingredient.product.APUs

%>
<tr class="product_amount removable">
    <td class="product_title">
        <input type="text" name="product_title" class="span4"
               value="${product_title}"
               data-provide="typeahead">
    </td>
    <td class="amount">
        <div class="input-append">
            <input type="text" name="measured_amount" style="width:30px"
                   value="${measured}" onkeyup="set_amount(this)"
                   data-multiplier="${apu}">
            <input type="hidden" name="amount" value="${amount}">
            <input type="hidden" name="unit_title"
                   value="${unit_title}">
            <span class="dropdown">
                <a href="#" class="btn dropdown-toggle add-on"
                   data-toggle="dropdown">
                    <span class="chosen_unit_abbr">
                        % if unit_abbr is not None:
                        ${unit_abbr}
                        %else:
                        г
                        % endif
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