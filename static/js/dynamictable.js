(function($) {
    $.fn.asyncForm = function(success, error) {
        error = error || function(data, status) {
            $.pnotify({
                type: 'notice',
                delay: 3000,
                title: 'Invalid action',
                text: 'Please, fix your data and try again'
            });
        };
        return $(this).on('submit', function (e) {
            $.ajax({
                url: $(this).attr('action') || $(this).attr('target'),
                method: $(this).attr('method') || 'POST',
                data: $(this).serialize()
            }).done($.proxy(success, this)).fail($.proxy(error, this));

            e.preventDefault();
        });
    };
})(jQuery);

(function($) {
    $.fn.populateTable = function(success, error) {
        error = error || function(data, status) {
            $.pnotify({
                type: 'notice',
                delay: 3000,
                title: 'Invalid action',
                text: 'Could not retrieve server data right now'
            });
        };
        var initial = $(this).attr('initial') || 0;
        var amount = $(this).attr('amount') || 50;
        $.ajax({
            url: $(this).attr('action') || $(this).attr('target'),
            method: $(this).attr('method') || 'GET',
            data: "initial=" + initial + "&amount=" + amount
        }).done($.proxy(success, this)).fail($.proxy(error, this));
    };

    $.fn.tableData = {};

    $.fn.getData = function() {
        return $.fn.tableData[$(this).attr("id")];
    };

    $.fn.createTableLine = function(data, lineId, target, cols) {
        $.fn.tableData[lineId] = data;
        var newRow = $('<tr id="' + lineId + '" target="' + target + '">');
        for (var i in cols) {
            var text = cols[i];
            var col = $("<td>");
            col.append(text);
            newRow.append(col);
        }
        $(this).find("tbody:last").append(newRow);
        var table = $(this);
        table.trigger("update");
    };

    $.fn.refreshTableLine = function(success, error) {
        error = error || function() {
            $.pnotify({
                type: 'notice',
                delay: 3000,
                title: 'Invalid action',
                text: 'Could not refresh the data right now'
            });
        };
        $.ajax({
            url: $(this).attr('target') || $(this).attr('action'),
            method: $(this).attr('method') || 'GET'
        }).done($.proxy(success, this)).fail($.proxy(error, this));
    }

    $.fn.updateTableLine = function(data, cols) {
        $.fn.tableData[data._id] = data;
        for (var i in cols) {
            var text = cols[i];
            var col = $(this).find("td").eq(i);
            col.html(text);
        }
        var table = $(this).closest("table");
        table.trigger("update");
    };

    $.fn.deleteTableLine = function(lineId) {
        delete $.fn.tableData[lineId];
        $(this).remove();
        var table = $(this).closest("table");
        table.trigger("update");
        table.trigger("updateAll");
    }

    $.fn.removeModal = function() {
        $(this).modal('hide');
        $(this).remove();
        $('.modal-backdrop').remove();
    }
})(jQuery);

function htmlEscape(text) {
    return text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function createUpdateForm(url) {
    var form = $("<form>").attr("action", url).attr("method", "put").attr("class", "form-update");
    form.append('<button type="submit" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-edit"></span></button>');
    form.asyncForm(function(data, status) {
    }, function(data, status) {
        $.pnotify({
            type: 'notice',
            delay: 3000,
            title: 'Invalid action',
            text: 'Please, fix your data and try again'
        });
    });
    return form;
}

function createUpdateButtonModal(onclick) {
    var button = $("<button/>").attr("type", "button").attr("class", "btn btn-default btn-xs").html('<span class="glyphicon glyphicon-edit"></span>');
    button.click(onclick);
    return button;
}

function createDeleteForm(url) {
    var form = $("<form>").attr("action", url).attr("method", "delete").attr("class", "form-delete");
    form.append('<button type="submit" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-trash"></span></button>');
    form.asyncForm(function(data, status) {
        $(this).closest("tr").deleteTableLine();
    }, function(data, status) {
        $.pnotify({
            type: 'notice',
            delay: 3000,
            title: 'Invalid action',
            text: 'Could not delete this item'
        });
    });
    return form;
}

function createDeleteForm2() {
    var form = $("<form>").attr("method", "delete").attr("class", "form-delete");
    form.append('<button type="submit" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-trash"></span></button>');
    return form;
}

function createEditableField(name, value) {
    var fixed = $("span").html(value);
    var editable = $("input").attr("type", "text").attr("class", "").attr("name", name).attr("value", value);
    return $("div").append(fixed).append(editable);
}

function createModal(content) {
    var modal = $("<div/>").attr("class", "modal fade");
    var divDialog = $("<div/>").attr("class", "modal-dialog");
    var divContent = $("<div/>").attr("class", "modal-content");
    var divHeader = $("<div/>").attr("class", "modal-header");
    var divBody = $("<div/>").attr("class", "modal-body");
    var divFooter = $("<div/>").attr("class", "modal-footer");
    divHeader.append($("<button/>").attr("type", "button").attr("class", "close").attr("aria-hidden", "true").attr("data-dismiss", "modal").html("&times;"));
    divHeader.append($("<h4/>").attr("class", "modal-title").html("Editing"));
    divBody.append(content);
    divFooter.append($("<button/>").attr("type", "button").attr("class", "btn btn-default").attr("data-dismiss", "modal").html("Close"));
    divFooter.append($("<button/>").attr("type", "submit").attr("class", "btn btn-primary").html("Save"));
    divContent.append(divHeader);
    divContent.append(divBody);
    divContent.append(divFooter);
    divDialog.append(divContent);
    modal.append(divDialog);
    modal.attr('tabindex', -1); // fix bootstrap keyboard ESC issue
    return modal;
}

function createModalWithForm(id, url, formContent, callbackSuccess, callbackError) {
    var modal = $("<div/>").attr("id", id).attr("class", "modal fade");
    var divDialog = $("<div/>").attr("class", "modal-dialog");
    var divContent = $("<div/>").attr("class", "modal-content");
    var form = $("<form>").attr("action", url).attr("method", "put").attr("class", "form-update");
    var divHeader = $("<div/>").attr("class", "modal-header");
    var divBody = $("<div/>").attr("class", "modal-body");
    var divFooter = $("<div/>").attr("class", "modal-footer");
    divHeader.append($("<button/>").attr("type", "button").attr("class", "close").attr("aria-hidden", "true").attr("data-dismiss", "modal").html("&times;"));
    divHeader.append($("<h4/>").attr("class", "modal-title").html("Editing"));
    divBody.append(formContent);
    divFooter.append($("<button/>").attr("type", "button").attr("class", "btn btn-default").attr("data-dismiss", "modal").html("Close"));
    divFooter.append($("<button/>").attr("type", "submit").attr("class", "btn btn-primary").html("Save"));

    form.append(formContent);
    form.asyncForm(callbackSuccess, callbackError);
    form.append(divBody);
    form.append(divFooter);
    divContent.append(divHeader);
    divContent.append(form);
    divDialog.append(divContent);
    modal.append(divDialog);
    modal.attr('tabindex', -1); // fix bootstrap keyboard ESC issue
    modal.on('hidden.bs.modal', function () {
        $(this).data('bs.modal', null);
        modal.remove();
    });
    modal.on('shown.bs.modal', function() {
        modal.find('input:text')[0].focus();
    });
    return modal;
}

function createModalWithForm2(id, formContent) {
    var modal = $("<div/>").attr("id", id).attr("class", "modal fade");
    var divDialog = $("<div/>").attr("class", "modal-dialog");
    var divContent = $("<div/>").attr("class", "modal-content");
    var form = $("<form>").attr("class", "form-update");
    var divHeader = $("<div/>").attr("class", "modal-header");
    var divBody = $("<div/>").attr("class", "modal-body");
    var divFooter = $("<div/>").attr("class", "modal-footer");
    divHeader.append($("<button/>").attr("type", "button").attr("class", "close").attr("aria-hidden", "true").attr("data-dismiss", "modal").html("&times;"));
    divHeader.append($("<h4/>").attr("class", "modal-title").html("Editing"));
    divBody.append(formContent);
    divFooter.append($("<button/>").attr("type", "button").attr("class", "btn btn-default").attr("data-dismiss", "modal").html("Close"));
    divFooter.append($("<button/>").attr("type", "submit").attr("class", "btn btn-primary").html("Save"));

    form.append(formContent);
    form.append(divBody);
    form.append(divFooter);
    divContent.append(divHeader);
    divContent.append(form);
    divDialog.append(divContent);
    modal.append(divDialog);
    modal.attr('tabindex', -1); // fix bootstrap keyboard ESC issue
    modal.on('hidden.bs.modal', function () {
        $(this).data('bs.modal', null);
        modal.remove();
    });
    modal.on('shown.bs.modal', function() {
        modal.find('input:text')[0].focus();
    });
    return [modal, form];
}

function createInput(name, label, value, type, properties) {
    properties = properties || {placeholder:"", autocomplete:"off", autofocus:""};
    var div = $("<div/>").attr("class", "form-group");
    var labelComponent = $("<label/>").attr("for", name).html(label);
    var inputComponent = $("<input/>").attr("type", type || "text").attr("name", name).attr("id", name).attr("value", value || "");
    inputComponent = inputComponent.attr("class", "form-control " + (properties["style"] || "input-medium"));
    for (var key in properties) {
        inputComponent = inputComponent.attr(key, properties[key]);
    }
    div.append(labelComponent);
    div.append(inputComponent);
    return div;
}

function createSelect(name, label, options, value, style, required) {
    var div = $("<div/>").attr("class", "form-group");
    var labelComponent = $("<label/>").attr("for", name).html(label);
    var selectComponent = $("<select/>").attr("name", name).attr("id", name).attr("required", required || "true").attr("class", "form-control" + (style || "input-medium"));
    for (var i in options) {
        var l = options[i].label;
        var v = options[i].value;
        var selected = options[i].selected || false;
        var option = $("<option/>").attr("value", v).html(l);
        if (v == value || selected == true) {
            option.attr("selected", "selected");
        }
        selectComponent.append(option);
    }
    div.append(labelComponent);
    div.append(selectComponent);
    return div;
}

function createCheckbox(name, value) {
    var input = $("<input/>").attr("type", "checkbox").attr("name", name).attr("id", name);
    if (value == true || value == "true") {
        input.attr("checked", "checked");
    }
    return input;
}

function createFormCheckbox(name, label, value) {
    var div = $("<div/>").attr("class", "form-group");
    var labelComponent = $("<label/>").attr("class", "checkbox");
    var inputComponent = createCheckbox(name, value)
    labelComponent.append(inputComponent);
    labelComponent.append(" " + label);
    div.append(labelComponent);
    return div;
}

function createLink(href, label) {
    var link = $("<a/>").attr("href", href).html(label);
    return link;
}
