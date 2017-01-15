// addresses_to_process should be set in the html file using this javascript and should be the ids of the country selects

var first_time_address_processing = [];

$(document).ready(function()
{
    var i;

    for (i = 0; i < addresses_to_process.length; i++)
    {
        var country_select = $("#" + addresses_to_process[i]);
        var saved_country_id = country_select.data("saved-country-id");
        var state_select_id = country_select.data("state-select-id");
        var city_select_id = country_select.data("city-select-id");

        first_time_address_processing.push(state_select_id);
        first_time_address_processing.push(city_select_id);

        country_select.on("change", function()
        {
            var state_select_id = $(this).data("state-select-id");
            var state_select = $("#" + state_select_id);
            var city_select_id = $(this).data("city-select-id");
            var city_select = $("#" + city_select_id);
            var state_div_id = $(this).data("state-div-id");
            var state_div = $("#" + state_div_id);
            var city_div_id = $(this).data("city-div-id");
            var city_div = $("#" + city_div_id);

            state_select.val("");
            city_select.val("");

            state_div.hide();
            city_div.hide();

            if ($(this).val() != "")
            {
                get_states($(this));
            }
        });

        country_select.val(saved_country_id).trigger("change");
    }
});

// All functions below will be moved into their own javascript file to be used as utility.
function get_states(country_select)
{
    var country_id = country_select.val();
    var state_select_id = country_select.data("state-select-id");
    var state_select = $("#" + state_select_id);
    var state_div_id = country_select.data("state-div-id");
    var state_div = $("#" + state_div_id);
    var state_type_label_id = country_select.data("state-type-label-id");
    var state_type_label = $("#" + state_type_label_id);
    var url = country_select.data("get-states-url").slice(0, -2) + "/" + country_id;

    $.ajax(
    {
        type: "GET",
        url: url,

        success: function (out_data_json)
        {
            var out_data = JSON.parse(out_data_json);
            var state_info_list = out_data["state_info_list"];
            var state_type = out_data["state_type"];

            state_select.empty();
            state_type_label.text(state_type);

            add_item_to_select(state_select, "", "", true);

            // Add each state to the state select
            for (var i = 0; i < state_info_list.length; i++)
            {
                add_item_to_select(state_select, state_info_list[i][0], state_info_list[i][1], false);
            }

            // Add state-select change-event
            state_select.on("change", function ()
            {
                get_cities(country_select, $(this));
            });

            state_div.show();

            var first_time_address_processing_index = $.inArray(state_select_id, first_time_address_processing);

            if (first_time_address_processing_index >= 0)
            {
                var saved_state_id = country_select.data("saved-state-id");

                first_time_address_processing.splice(first_time_address_processing_index, 1);

                if (saved_state_id != "")
                {
                    state_select.val(saved_state_id).trigger("change");
                }
            }
        },

        error: function (XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
        }
    });
}


function get_cities(country_select, state_select)
{
    var state_id = state_select.val();
    var city_select_id = country_select.data("city-select-id");
    var city_select = $("#" + city_select_id);
    var city_div_id = country_select.data("city-div-id");
    var city_div = $("#" + city_div_id);
    var url = country_select.data("get-cities-url").slice(0, -2) + "/" + state_id;

    $.ajax(
    {
        type: "GET",
        url: url,

        success: function(out_data_json)
        {
            var city_info_list = JSON.parse(out_data_json);

            city_select.empty();

            add_item_to_select(city_select, "", "", true);

            for (var i = 0; i < city_info_list.length; i++)
            {
                add_item_to_select(city_select, city_info_list[i][0], city_info_list[i][1], false);
            }

            city_div.show();

            var first_time_address_processing_index = $.inArray(city_select_id, first_time_address_processing);

            if (first_time_address_processing_index >= 0)
            {
                var saved_city_id = country_select.data("saved-city-id");

                first_time_address_processing.splice(first_time_address_processing_index, 1);

                if (saved_city_id != "")
                {
                    city_select.val(saved_city_id).trigger("change");
                }
            }
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
        }
    });
}

function add_item_to_select(item_select, item_id, name, should_be_selected)
{
    var option = $("<option></option>").prop("value", item_id).text(name);

    if (should_be_selected)
    {
        option.prop("selected", true);
    }

    item_select.append(option);
}