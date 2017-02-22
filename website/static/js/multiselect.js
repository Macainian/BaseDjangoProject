$(document).ready(function()
{
    // Fixes selection bugs when you click on the slider or empty space.
    $("select.multi-select").mousedown(function(event)
    {
        return false;
    });

    var options = $("select.multi-select option");

    options.unbind("click").click(option_click_event);

    // This is necessary to fix "click and drag scrolling on the options" bug in Chrome
    options.mousemove(option_mousemove_event);
});

function option_click_event(event)
{
    $(this).prop("selected", !$(this).prop("selected"));

    return false;
}

// This is necessary to fix "click and drag scrolling on the options" bug in Chrome
function option_mousemove_event(event)
{
    return false;
}