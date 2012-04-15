<%page args="step"/>
<%
if step is None:
    number = 1
    time_value = ''
    text = ''
else:
    number = step.number
    time_value = step.time_value
    text = step.text
%>
<div class="step removable" id="step_${number}">
    <div class="topline">
        <a class="close remove">&times;</a>
        <div class="input-prepend number_set" style="width:90px">
            <label for="step${number}" class="add-on">Шаг №</label>
            <input id="step${number}" class="step_no" type="text"
                   name="step_number" value="${number}">
        </div>
        <div class="input-prepend input-append time_set" style="width:95px">
            <label for="timevalue_${number}" class="add-on">
                <i class="icon-time"></i>
            </label>
            <input type="text" name="time_value" class="time_value"
                   id="timevalue_${number}" value="
% if time_value is not None:
${time_value}
% endif
">
            <div class="add-on" style="margin-bottom:4px">мин</div>
        </div>
    </div>
    <textarea id="initial_step" name="step_text"
              cols="30" rows="5">${text}</textarea>
</div>