<%page args="step"/>
<%! from kook.mako_filters import failsafe_get as get %>
<div class="step removable" id="step_${get(step, 'number')}">
    <div class="topline">
        <a class="close remove">&times;</a>
        <div class="input-prepend number_set" style="width:90px">
            <label for="step${get(step, 'number')}" class="add-on">Шаг №</label>
            <input id="step${get(step, 'number')}" class="step_no" type="text"
                   name="step_number" value="${get(step, 'number') or 1}">
        </div>
        <div class="input-prepend input-append time_set" style="width:95px">
            <label for="timevalue_${get(step, 'number')}" class="add-on">
                <i class="icon-time"></i>
            </label>
            <input type="text" name="time_value" class="time_value"
                   id="timevalue_${get(step, 'number')}"
                   value="${get(step, 'time_value')}">
            <div class="add-on" style="margin-bottom:4px">мин</div>
        </div>
    </div>
    <textarea id="initial_step" name="step_text"
              cols="30" rows="5">${get(step, 'text')}</textarea>
</div>