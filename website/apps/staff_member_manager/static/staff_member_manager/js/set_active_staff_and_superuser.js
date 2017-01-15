function set_is_active(set_is_active_url, other_username, user_id)
{
    var is_active_checkbox = $("#" + user_id + "-is-active-checkbox");
    var is_checked = is_active_checkbox.is(":checked");
    var data = {};

    data["other_staff_member_username"] = other_username;
    data["is_checked"] = is_checked;

    $.ajax(
    {
        data: data,
        type: "POST",
        url: set_is_active_url,

        success: function()
        {
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
        }
    });
}

function set_is_staff(set_is_staff_url, other_username, user_id)
{
    var is_staff_checkbox = $("#" + user_id + "-is-staff-checkbox");
    var is_checked = is_staff_checkbox.is(":checked");
    var data = {};

    data["other_staff_member_username"] = other_username;
    data["is_checked"] = is_checked;

    $.ajax(
    {
        data: data,
        type: "POST",
        url: set_is_staff_url,

        success: function()
        {
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
        }
    });
}

function set_is_superuser(set_is_superuser_url, other_username, user_id)
{
    var is_superuser_checkbox = $("#" + user_id + "-is-superuser-checkbox");
    var is_checked = is_superuser_checkbox.is(":checked");
    var data = {};

    data["other_staff_member_username"] = other_username;
    data["is_checked"] = is_checked;

    $.ajax(
    {
        data: data,
        type: "POST",
        url: set_is_superuser_url,

        success: function()
        {
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
        }
    });
}