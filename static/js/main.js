(function() {
  $(function() {
    var editor, ws;
    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
      lineNumbers: true,
      mode: "text/x-vb",
      matchBrackets: true
    });
    ws = new WebSocket("ws://nado.oknctict.tk:8000/echo");
    return $("#btn-upload").click(function() {
      return console.log(editor.getValue());
    });
  });

}).call(this);
