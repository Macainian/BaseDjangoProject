function send_email_notification_for_new_user(url)
{
    $.ajax(
    {
        type: "GET",
        url: url,

        success: function()
        {
            alert("Email successfully sent");
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
        }
    });
}

function create_account_for_staff_member(url)
{
    $.ajax(
    {
        type: "GET",
        url: url,

        success: function()
        {
            alert("Account successfully created");
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
        }
    });
}