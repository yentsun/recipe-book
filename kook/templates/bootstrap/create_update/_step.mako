<%page args="step"/>
<div class="step removable" id="step_${step.number}">
    <div class="topline">    <a class="close remove">&times;</a>
    <div class="input-prepend number_set" style="width:90px">
            <label for="step${step.number}" class="add-on">Шаг №</label>
            <input id="step${step.number}" class="step_no" type="text" name="step_number"
                   value="${step.number}">
        </div>
    <div class="input-prepend input-append time_set" style="width:95px">
            <label for="timevalue_${step.number}" class="add-on"><i class="icon-time"></i></label>
            <input type="text" name="time_value" class="time_value"
                   id="timevalue_${step.number}" value="${step.time_value}">
            <div class="add-on" style="margin-bottom:4px">мин</div>
    </div>
    </div>


                <textarea name="step_text" id="steptext_${step.number}"
                          cols="30" rows="10">
                    ${step.text}
                </textarea>
</div>