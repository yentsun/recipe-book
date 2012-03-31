<%page args="step"/>
<section class="step removable">
    <a class="close remove">&times;</a>
    <div class="controls pull-left"><div class="input-prepend">
        <span class="step_title add-on">Шаг №</span>
        <input id="step${step.number}" class="step_no" size="3" type="text" name="step_number"
               value="${step.number}">
    </div></div>
    <div class="controls time"><div class="input-prepend input-append">
        <span class="add-on"><i class="icon-time"></i></span>
        <input type="text" name="time_value" class="time_value span1" size="2"
               id="timevalue_${step.number}" value="${step.time_value}">
        <span class="add-on">мин</span>
    </div></div>
    <textarea name="step_text" id="steptext_${step.number}"
              cols="30" rows="10">
        ${step.text}
    </textarea>
</section>