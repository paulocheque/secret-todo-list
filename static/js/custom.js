if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.slice(0, str.length) == str;
    };
}

if (typeof String.prototype.endsWith != 'function') {
    String.prototype.endsWith = function (str){
        return this.slice(-str.length) == str;
    };
}

if (typeof String.prototype.contains != 'function') {
    String.prototype.contains = function (str) {
        return this.indexOf(str) !== -1;
    };
}

function createLink(href, label) {
    var link = $("<a/>").attr("href", href).html(label);
    return link;
}

function createCheckbox(name, value) {
    var input = $("<input/>").attr("type", "checkbox").attr("name", name).attr("id", name);
    if (value == true || value == "true") {
        input.attr("checked", "checked");
    }
    return input;
}
