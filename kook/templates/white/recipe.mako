<%inherit file="layout.mako"/>
<%def name="title()">
    ${recipe.dish.title} ${recipe.description} - от
    ${recipe.author.display_name}
</%def>
<%def name="js()"></%def>
<section id="recipe">
    <h1>${recipe.dish.title} <br><span>${recipe.description}</span></h1>
    <div class="row">
        <div id="photo" class="span6">
            <div>
                <img width="100%" src="${recipe.dish.image.url}" alt="">
            </div>
            <div id="photo_credit">
                Фото: ${recipe.dish.image.credit or recipe.dish.image.get_credit()}
            </div>
        </div>
        <div id="ingredients">

        </div>
    </div>
</section>