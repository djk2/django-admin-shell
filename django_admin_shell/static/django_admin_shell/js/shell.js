// Django admin shell
// author : Grzegorz Tężycki

$(document).ready(function(){

    var $shell = $("#id_code");
    var $form = $("#shell_form");
    var $output_container = $("#output_container");

    // load_step is as index from end of code array
    // when press ctrl + up load_step + 1
    // when press ctrl + down load_step - 1
    var load_step = 0;

    // Scroll output to bottom
    $output_container.scrollTop($output_container.prop("scrollHeight"));

    // Add linenumbers to shell
    $shell.linedtextarea();
    // Set focus on shell textarea
    $shell.focus();

    // Submit form
    var run_code = function(){
        $form.submit();
    };

    // Load last code
    var load_last = function(){
        var code_list = $(".code pre");
        var len = code_list.length;
        if (load_step < len) {
            load_step++;
        }
        var $pre = $(code_list[len - load_step]);
        $shell.val($pre.text());
    };

    // Load next code
    var load_next = function(){
        var code_list = $(".code pre");
        var len = code_list.length;
        if (load_step > 0) {
            load_step--;
        }
        var $pre = $(code_list[len - load_step]);
        $shell.val($pre.text());
    }

    // calculate height for output container
    var set_height = function(){
        var top = $output_container.position().top;
        var shell_height = $shell.height();
        var document_height = $(document).height();
        var margin = 150;
        var height = document_height - top - shell_height - margin;
        $output_container.css("height", height + "px");
    };

    set_height();

    // ----------
    // Keys:
    // Ctrl + Enter = execute code
    // Ctrl + UP = load previous code
    // Ctrl + Down = load next code
    // Tab = replace to spaces
    $shell.keydown(function(e) {
        // Ctrl + Enter
        if (e.ctrlKey && e.keyCode == 13) {
            run_code();
        }

        // Ctrl + Up
        if (e.ctrlKey && e.keyCode == 38) {
            load_last();
        }

        // Ctrl + Down
        if (e.ctrlKey && e.keyCode == 40) {
            load_next();
        }

        // Indent - replace tab to spaces
        if (e.keyCode == 9) {
            var sh = $(this);
            var sh0 = sh.get(0);
            e.preventDefault();
            var start = sh0.selectionStart;
            var end = sh0.selectionEnd;
            sh.val(sh.val().substring(0, start) + "    "  + sh.val().substring(end));
            sh0.selectionStart = sh0.selectionEnd = start + 4;
        }

    });

});
