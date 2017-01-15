$(document).ready(function()
{
    create_ckeditor_item("html-code-textarea");

    empty_email_batch_template_info();

    $("#email-batch-template-select").change(function()
    {
        if ($(this).val() == "")
        {
            empty_email_batch_template_info();
        }
        else
        {
            load_email_batch_template();
        }
    });

    // Defaults all ckeditor links to _blank.
    // Refer to http://ckeditor.com/forums/CKEditor/How-to-set-default-as-targetblank-while-disabling-the-target-tab-in-CK-editor
    CKEDITOR.on("dialogDefinition", function (event)
    {
        if(event.data.name == "link")
        {
            event.data.definition.getContents("target").get("linkTargetType")["default"] = "_blank";
        }
    });
});

function get_ckeditor_html(id)
{
    return CKEDITOR.instances[id].getData();
}

function set_ckeditor_html(id, html)
{
    setTimeout(function()  // Strange bug. Refer to: http://stackoverflow.com/questions/11934243/ckeditor-inserttext-not-working-after-setdata
    {
        CKEDITOR.instances[id].setData(html);
    }, 0);
}

function create_ckeditor_item(id)
{
    CKEDITOR.replace(
        id,
        {
            height: ["650px"]
        }
    );
}

function remove_ckeditor_item(id)
{
    CKEDITOR.instances[id].destroy(true);
}

function go_to_preview(url)
{
    get_email_preview(url);
    $("#email-batch-template-edit-div").hide();
    $("#email-batch-template-preview-div").show();
}

function go_to_edit()
{
    $("#email-batch-template-preview-div").hide();
    $("#email-batch-template-edit-div").show();
}

function load_email_batch_template()
{
    var email_batch_template_id = $("#email-batch-template-select").val();
    var url = get_email_batch_template_url.slice(0, -2) + email_batch_template_id + "/";

    $.ajax(
    {
        type: "GET",
        url: url,

        success: function(out_data)
        {
            var out_data_json = JSON.parse(out_data);

            $("#email-batch-template-name-text").val(out_data_json["email_batch_template_name"]);
            $("#from-code-text").val(out_data_json["from_code"]);
            $("#subject-code-text").val(out_data_json["subject_code"]);
            $("#basic-message-textarea").val(out_data_json["basic_message"]);
            set_ckeditor_html("html-code-textarea", out_data_json["html_code"]);
            $("#copy-email-batch-template-warning-message-p").hide();
            $("#copy-email-batch-template-button").prop("disabled", false);

            remove_spinner();
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
            remove_spinner();
        }
    });
}

function get_email_preview(url)
{
    var html_code = get_ckeditor_html("html-code-textarea");
    var data = {};

    data["html_code"] = html_code;

    add_spinner();

    $.ajax(
    {
        data: data,
        type: "POST",
        url: url,

        success: function(html_code)
        {
            $("#email-preview-div").html(html_code);
            remove_spinner();
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
            remove_spinner();
        }
    });
}

function copy_email_batch_template(base_copy_email_url)
{
    var new_email_batch_template_name = $("#new-email-batch-template-name-text").val();
    var original_email_batch_template_id = $("#email-batch-template-select").val();
    var url = base_copy_email_url.slice(0, -2) + original_email_batch_template_id + "/";
    var data = {};

    add_spinner();

    data["new_email_batch_template_name"] = new_email_batch_template_name;

    $.ajax(
    {
        data: data,
        type: "POST",
        url: url,

        success: function()
        {
            // $("success-notification")
            location.reload(true);
            $("#copy-email-batch-template-warning-message-p").hide();
            remove_spinner();
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
            remove_spinner();
        }
    });
}

function save_email_batch_template(base_save_email_url)
{
    var email_batch_template_id = $("#email-batch-template-select").val();
    var email_batch_template_name = $("#email-batch-template-name-text").val();
    var from_code = $("#from-code-text").val();
    var subject_code = $("#subject-code-text").val();
    var basic_message = $("#basic-message-textarea").val();
    var html_code = get_ckeditor_html("html-code-textarea");
    var url;
    var data = {};

    if (email_batch_template_id == "")
    {
        url = base_save_email_url.slice(0, -2) + "new/";
    }
    else
    {
        url = base_save_email_url.slice(0, -2) + email_batch_template_id + "/";
    }

    data["email_batch_template_name"] = email_batch_template_name;
    data["from_code"] = from_code;
    data["subject_code"] = subject_code;
    data["basic_message"] = basic_message;
    data["html_code"] = html_code;

    add_spinner();

    $.ajax(
    {
        data: data,
        type: "POST",
        url: url,

        success: function()
        {
            // $("success-notification")
            location.reload(true);
            $("#copy-email-batch-template-warning-message-p").hide();
            remove_spinner();
        },

        error: function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(XMLHttpRequest.responseText);
            remove_spinner();
        }
    });
}

function empty_email_batch_template_info()
{
    $("#email-batch-template-name-text").val("");
    $("#from-code-text").val("");
    $("#subject-code-text").val("");
    $("#basic-message-textarea").val("");
    set_ckeditor_html("html-code-textarea", "");
    $("#copy-email-batch-template-warning-message-p").hide();
    $("#copy-email-batch-template-button").prop("disabled", true);
}

function show_copy_email_batch_template_warning_message()
{
    $("#copy-email-batch-template-warning-message-p").show();
}