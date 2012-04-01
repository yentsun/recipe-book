<%page args="no, ingredient"/>
<tr class="product_amount removable">
    <td class="product_name">
        <input id="product${no}" type="text" name="product" class="span4"
               data-id="${no}" value="${ingredient.product.title}"
               data-provide="typeahead">
    </td>
    <td class="amount">
        <div class="input-append">
            <input id="amount${no}" type="text" name="amount" style="width:30px"
                   value="${ingredient.amount}">
            <span class="add-on">г</span>
        </div>
    </td>
    <td><a class="close remove">&times;</a></td>
</tr>